
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

    new_is_pinned = bool(input("\nPin NOte? (1/0): "))

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

#TODO
# Task 2:
# Create a new option to display each folder and the notes that are within them. Display no
# ids for folders or notes on the output.
def printAllFolders():
    pass

#TODO
# Task 3:
# Create a feature that always shows the titles of pinned notes when you open the
# application
def showPinnedNotes():
    pass

#TODO
# Task 4:
# Create two new options, to edit and delete notes. When editing a note, ensure that you
# are updating the ‘updatedAt’ attribute to be the current user datetime.
def editNote():
    pass

#TODO
def deleteNote():
    pass

#TODO
# Extra Credit (10 points):
# Create the ability to add, update, and delete folders + tags.
def folderStuff():
    pass


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
    8. Folder Stuff (Extra Credit)
                   
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
                folderStuff()
            case _:
                break


if __name__ == "__main__":
    main() 