import getpass
import csv
import requests
from requests import Session
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import sys

def get_CUC_version(CUC, session):
    # Using CUC version query to simply test user authentication. We don't really need the version info for anything.
    request_data = session.get('https://' + CUC +'/vmrest/version/', timeout=2, stream=True)
    return(request_data.status_code)

def insert_contact(CUC, template, row, session, rowNum):
    if rowNum == 0:
        # Basic check to see if CSV columns are likely accurate
        if (row[0],row[1],row[2],row[3],row[4],row[5]) != ('Alias', 'DisplayName', 'FirstName', 'LastName', 'TransferEnabled', 'TransferExtension'):
            print('There may be a problem with your column order:')
            print('Correct names and order: [\'Alias\', \'DisplayName\', \'FirstName\', \'LastName\', \'TransferEnabled\', \'TransferExtension\']')
            print('Your names and order:   ', row)
            sys.exit(0)
        else:
            print ('CSV required columns look accurate.')
            print ('')
    else:
        print('Inserting CSV file row number:',rowNum + 1)
        xml = make_XML(row)
        headers = {'Content-Type':'application/xml'}
        try:
            request_data = session.post('https://' + CUC +'/vmrest/contacts?templateAlias=' + template + '', headers=headers, data=xml, timeout=2)
            print ('Insert response:',request_data)
            print ('')
        except requests.exceptions.RequestException as e:
            print('Something bad happened inserting:')
            print(e)
            return

def delete_contact(CUC, template, alias, session,rowNum):
    headers = {'Content-Type':'application/xml'}
    try:
        print('Getting CUC ObjectId using CSV Alias ' + alias + ' in row number:',rowNum + 1)
        request_data = session.get('https://' + CUC +'/vmrest/contacts?query=(alias%20is%20' + alias + ')', headers=headers, timeout=2, stream=True)
        tree = ET.fromstring(request_data.text)
        count = tree.findall('Contact')
        if len(count) > 0:
            print ('Found ' + str(len(count)) + ' contact with that alias.')
            for contact in tree.findall('Contact'):
                aliastext = contact.find('Alias').text
                objectidtext = contact.find('ObjectId').text
                print('Deleting CUC contact ' + aliastext + ' with ObjectId ' + objectidtext)
                objectid = contact.find('ObjectId').text
                request_data = session.delete('https://' + CUC +'/vmrest/contacts/' + objectid + '', headers=headers, timeout=2, stream=True)
                print ('Delete response:',request_data)
                print ('')
        else:
            print ('Found ' + str(len(count)) + ' contacts with that alias. Skipping...')
            print('')
    except requests.exceptions.RequestException as e:
        print('Something bad happened deleting')
        print(e)
        return

def make_XML(row):
    print('Creating XML from:',row)
    xml = '<Contact>'
    xml = xml + '<Alias>' + row[0] + '</Alias>'
    xml = xml + '<DisplayName>' + row[1] + '</DisplayName>'
    xml = xml + '<FirstName>' + row[2] + '</FirstName>'
    xml = xml + '<LastName>' + row[3] + '</LastName>'
    xml = xml + '<TransferEnabled>' + row[4] + '</TransferEnabled>'
    xml = xml + '<TransferExtension>' + row[5] + '</TransferExtension>'
    xml = xml + '</Contact>'
    return(xml)

def main():

    csvFile = 'YOUR BAT FILENAME HERE'
    CUC = 'YOUR UNITY CONNECTION SERVER FQDN / IP ADDRESS HERE'
    template = 'YOUR CONTACT BAT TEMPLATE ALIAS HERE'

    username = input('UCxN username: ')
    password = getpass.getpass('UCxN password:')
    adddelete = input('[A]dd / [D]elete: ')
    print ('')

    session = Session()
    session.verify = False
    session.auth = HTTPBasicAuth(username, password)

    if get_CUC_version(CUC,session) != 200:
        print ('Authentication Failed.')
        sys.exit(0)

    if adddelete == 'A':
        csvData = csv.reader(open(csvFile))
        rowNum = 0
        for row in csvData:
            insert_contact(CUC, template, row, session, rowNum)
            rowNum +=1
    elif adddelete == 'D':
        csvData = csv.reader(open(csvFile))
        rowNum = 0
        for row in csvData:
            if rowNum == 0:
                print('Skipping column header row 1.')
                print('')
            else:
                delete_contact(CUC, template, row[0], session, rowNum)
            rowNum +=1
    else:
        print('Invalid Entry')
        print('')
        sys.exit(0)


if __name__ == '__main__':
    main()
