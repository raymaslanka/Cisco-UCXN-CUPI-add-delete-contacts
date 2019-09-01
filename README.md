This is a sample of how to add and / or delete contacts in the Unity Connection database using the CUPI interface.  Unity Connection provides the ability to add contacts manually and via the Bulk Administration tool GUI but there are some limitations.

When adding Unity Connection contacts manually, only the Alias (unique) and the DisplayName is required.
When adding Unity Connection contacts via Bulk Administration, an Alias (unique) and Extension (unique) is required.
A problem arises when you only want to leverage Unity Connection contacts as additional directory entries,
and where you might have multiple names or spellings for the same transfer destination.

Manually, you can add as many contacts as you require with variations of DisplayNames, all using the same TransferNumber, as the TransferNumber does not need to be unique.
If you are managing thousands of DisplayName variations though (full names vs. acronyms vs. friendly names, etc.), manual entry is likely not acceptable.

Since BAT requires a unique Extension, if you enter it accurately you are required to still enter a TransferNumber,
but now need to leverage multiple AlternateNames per contact to deal with name variations.
This is undesireable as contact AlternateNames are not easily searchable via the GUI,
and additionally User and Contact names can't be managed seperately if the extensions are the same.

For example, you may want need to manage directory entries for the President of the United Sates.
Several years ago, the user BObama may have had extension 1111.
This year, user DTrump may have the extension 1111.
You might have historically had a directory entry (contact) with DisplayName POTUS with extension 1111.
You might want a second directory entry (contact) with DisplayName P O T U S with extension 1111.
You cannot add either contact with BAT, as a user already has that extension number.
You can use AlternateNames in the User but when you delete and add a new user every four years, you need to remember to re-add all the asociated alternate names, which aren't searchable.
If you choose to manage those more permanant AlternateNames in a contact and via BAT, you now need to create a bogus unique Extension for the contact and again manage unsearchable AlternateNames.
If you want to be able to search for the AlternateNames, you need to BAT multiple contacts with multiple bogus Extesnsions and use the DisplayName in each instead.

None of this is perfect.
The CUC CUPI interface allows for bulk contact additions and deletions where Extension is not required.

Reads CSV file
converts each row to XML
posts each row XML to Unity Connection CUPI API

Notes:
CSV columns should be Alias,DisplayName,FirstName,LastName,TransferEnabled,TransferExtension
CSV should be saved in UTF-8 format
