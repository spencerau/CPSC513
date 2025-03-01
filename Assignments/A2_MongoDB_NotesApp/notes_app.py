
from pymongo import MongoClient
from datetime import datetime


client = MongoClient('mongodb://localhost:27017/')

db = client['NotesApp']

folders_collection = db['folders']
notes_collection = db['notes']
tags_collection = db['tags']


def printAllNotes():
    all_notes = notes_collection.find()
    index = 1
    for note in all_notes:
        print(index, ":", note.get('title'), "-", note.get('content'))
        index += 1
        

def searchNotes():
    search_term = input("Enter your search term: ")

    search_notes = notes_collection.find({'$text': {'$search': search_term}}).sort({'score': {'$meta': 'textScore'}})

    index = 1
    for note in search_notes:
        print(index, ":", note.get('title'), "-", note.get('content'))
        index += 1


def createNewNote():
    aggregate_result = db.notes.aggregate(
        [
            {
                '$group': {
                    '_id': 'allNotes',
                    'maxId': { '$max': '$noteId' }
                }
            }
        ]
    )
    highest_id = aggregate_result.next()
    new_id = int(highest_id['maxId']) + 1

    new_title = input("Note Title: ")
    new_content = input("\nNote Body: ")

    new_created_at = datetime.now()
    new_updated_at = new_created_at

    print("\nSelect Tags: \n")
    all_tags = tags_collection.find()
    for tag in all_tags:
        print(tag['tagId'], tag['tagName'])
    selected_tags = input("\nEnter all tags in comma separated format with no spaces: ").split(',')
    new_tags = [int(x) for x in selected_tags]

    print("\nSelect Folder: \n")
    all_folders = folders_collection.find()
    for folder in all_folders:
        print(folder['folderId'], folder['folderName'])
    new_folder = int(input("\nEnter a single folder number: "))

    new_is_pinned = bool(input("\nPin Note? (1/0): "))

    new_note = {
        'noteId': new_id,
        'title': new_title,
        'content': new_content,
        'createdAt': new_created_at,
        'updatedAt': new_updated_at,
        'folderId': new_folder,
        'tags': new_tags,
        'isPinned': new_is_pinned
    }
    notes_collection.insert_one(new_note)


# Task 1:
# Create a new option to print out all details for some given note. Print out all notes by ID
# and allow a user to select which note they would like to see all details for.
def printAllDetails():
    print()
    all_notes = notes_collection.find()
    for note in all_notes:
        print(f"{note.get("noteId")} : {note.get('title')}")

    print("\n Select the ID of the note you wish to see all details for: \n")

    note_id = int(input("Enter the note ID: "))

    selected_note = notes_collection.find_one({'noteId': note_id})

    print()

    for key, value in selected_note.items():
        print(f"{key}: {value}")


# Task 2:
# Create a new option to display each folder and the notes that are within them. Display no
# ids for folders or notes on the output.
# CHATGPT to debug this function
def printAllFolders():
    all_folders = folders_collection.find()
    #all_notes = notes_collection.find()
    for folder in all_folders:
        print(f"\n{folder.get('folderName')}:")
        # need to refetch the collection to reset the iterator
        all_notes = notes_collection.find()
        for note in all_notes:
            if note.get('folderId') == folder.get('folderId'):
                print(f"{note.get('title')} - {note.get('content')}")


# Task 3:
# Create a feature that always shows the titles of pinned notes when you open the
# application
def showPinnedNotes():
    pinned_notes = notes_collection.find({'isPinned': True})
    for note in pinned_notes:
        print(note.get('title'), " - ", note.get('content'))


# Task 4:
# Create two new options, to edit and delete notes. When editing a note, ensure that you
# are updating the ‘updatedAt’ attribute to be the current user datetime.
def editNote():
    print()
    printAllNotes()
    print("\n Choose the note you want to edit: \n")
    note_id = int(input("Enter the note ID: "))

    fields = {
        1: "title",
        2: "content",
        3: "folderId",
        4: "tags",
        5: "isPinned"
    }
    choice = int(input('''
        1: Title
        2: Content
        3: FolderId
        4: Tags
        5: IsPinned 
                       
    Enter the field number to update: '''))
    field = fields.get(choice)

    new_value = input(f"Enter the new value for {field}: ")
    notes_collection.update_one(
        {'noteId': note_id},
        {'$set': {field: new_value}}
    )

    notes_collection.update_one(
        {'noteId': note_id},
        {'$set': {'updatedAt': datetime.now()}}
    )


def deleteNote():
    print()
    printAllNotes()
    print("\n Choose the note you want to delete: \n")
    note_id = int(input("Enter the note ID: "))

    delete_result = notes_collection.delete_one({'noteId': note_id})
    if delete_result.deleted_count > 0:
        print("Note deleted successfully")
    else:
        print("No note found with that noteId to delete.")


# Extra Credit (10 points):
# Create the ability to add, update, and delete folders + tags.
def folder_tag_stuff():
    print("\nDo you wish to manipulate folders or tags (f/t)? \n")
    choice = input("Enter your choice (f/t): ")
    if (choice == "f"):
        print("\n1. Create a new folder")
        print("2. Update a folder")
        print("3. Delete a folder")
        print("4. View all folders\n")
        folder_choice = int(input("Enter your choice: "))
        if (folder_choice == 1):
            createNewFolder()
        elif (folder_choice == 2):
            updateFolder()
        elif (folder_choice == 3):
            deleteFolder()
        elif (folder_choice == 4):
            viewAllFolders()
        else:
            print("Invalid choice")
    
    elif (choice == "t"):
        print("\n1. Create a new tag")
        print("2. Update a tag")
        print("3. Delete a tag")
        print("4. View all tags\n")
        tag_choice = int(input("Enter your choice: "))
        print()
        if (tag_choice == 1):
            createNewTag()
        elif (tag_choice == 2):
            updateTag()
        elif (tag_choice == 3):
            deleteTag()
        elif (tag_choice == 4):
            viewAllTags()
        else:
            print("Invalid choice")


# helper function to debug; ONLY views folders and not notes
def viewAllFolders():
    print("All Folders:")
    all_folders = folders_collection.find()
    for folder in all_folders:
        print(f"{folder['folderId']} - {folder['folderName']}")


def createNewFolder():
    aggregate_result = db.folders.aggregate(
        [
            {
                '$group': {
                    '_id': 'allFolders',
                    'maxId': { '$max': '$folderId' }
                }
            }
        ]
    )
    highest_id = aggregate_result.next()
    new_id = int(highest_id['maxId']) + 1
    folder_name = input("Enter the folder name: ")
    new_created_at = datetime.now()

    new_folder = {
        'folderId': new_id,
        'folderName': folder_name,
        'createdAt': new_created_at
    }
    folders_collection.insert_one(new_folder)
    print()
    viewAllFolders()


def updateFolder():
    print()
    viewAllFolders()
    print("\nSelect the Folder you want to update: \n")

    folder_id = int(input("Enter the ID of the folder you wish to edit: "))

    print("\nYou can only update the folder name\n")

    new_folder_name = input("Enter the new folder name: ")
    print()

    folders_collection.update_one(
        {'folderId': folder_id},
        {'$set': {'folderName': new_folder_name}}
    )


def deleteFolder():
    print()
    viewAllFolders()
    print("\nSelect the folder you want to delete: \n")

    folder_id = int(input("Enter the ID of the folder you wish to delete: "))
    print()

    # need to go and deference any folders in notes
    # set folderId to null?
    # for note in notes_collection.find():
    #     if folder_id == note['folderId']:
    #         notes_collection.update_one(
    #             {'noteId': note['noteId']},
    #             {'$set': {'folderId': None}}
    #         )
    # can just use this:
    # update_many finds all notes that match the folderId and sets them to None in a single operation, 
    # which is more efficient than individually updating each document. - CHATGPT to debug
    notes_collection.update_many(
        {'folderId': folder_id},
        {'$set': {'folderId': -1}}
    )

    delete_result = folders_collection.delete_one({'folderId': folder_id})
    if delete_result.deleted_count > 0:
        print("Folder deleted successfully")
    else:
        print("No folder found with that folderId to delete.")


def viewAllTags():
    print("All Tags:")
    all_tags = tags_collection.find()
    for tag in all_tags:
        print(f"{tag['tagId']} - {tag['tagName']}")


def createNewTag():
    aggregate_result = db.tags.aggregate(
        [
            {
                '$group': {
                    '_id': 'allTags',
                    'maxId': { '$max': '$tagId' }
                }
            }
        ]
    )
    highest_id = aggregate_result.next()
    new_id = int(highest_id['maxId']) + 1
    tag_name = input("Enter the tag name: ")

    new_tag = {
        'tagId': new_id,
        'tagName': tag_name
    }
    tags_collection.insert_one(new_tag)


def updateTag():
    print()
    viewAllTags()
    print("\nSelect the tag you want to update: \n")

    tag_id = int(input("Enter the ID of the tag you wish to edit: "))

    print("\nYou can only update the tag name\n")

    new_tag_name = input("Enter the new tag name: ")
    print()

    tags_collection.update_one(
        {'tagId': tag_id},
        {'$set': {'tagName': new_tag_name}}
    )


def deleteTag():
    print()
    viewAllTags()
    print("\nSelect the tag you want to delete: \n")

    tag_id = int(input("Enter the ID of the tag you wish to delete: "))
    print()

    delete_result = tags_collection.delete_one({'tagId': tag_id})
    if delete_result.deleted_count > 0:
        print("Tag deleted successfully")
    else:
        print("No tag found with that tagId to delete.")

    # need to go and deference any tags in notes
    for note in notes_collection.find():
        if tag_id in note['tags']:
            note['tags'].remove(tag_id)
            # prob would have been smarter to make editNote() modular and do CLI stuff in main()
            notes_collection.update_one(
                {'noteId': note['noteId']},
                {'$set': {'tags': note['tags']}}
            )


def main():
    print("Welcome to Your Notes App!")

    print("\nYour Pinned Notes: \n")
    showPinnedNotes()

    while True:
        choice = int(input('''
    Options:
    1. See all notes
    2. Search Notes
    3. Create a new note
    4. Print all details for a given note
    5. Display all folders and notes within them
    6. Edit Note
    7. Delete Note
    8. Folder and Tag Stuff (Extra Credit)
    9. Exit
                   
    Choice: '''))
        match choice:
            case 1:
                printAllNotes()
            case 2:
                searchNotes()
            case 3:
                createNewNote()
            case 4:
                printAllDetails()
            case 5: 
                printAllFolders()
            case 6:
                editNote()
            case 7:
                deleteNote()
            case 8:
                folder_tag_stuff()
            case 9:
                print("\nGoodbye!")
                break
            case _:
                break


if __name__ == "__main__":
    main() 