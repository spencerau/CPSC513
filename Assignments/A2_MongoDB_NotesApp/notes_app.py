from pymongo import MongoClient
from datetime import datetime


client = MongoClient('mongodb://localhost:27017/')

db = client['NotesApp']

folders_collection = db['folders']
notes_collection = db['notes']
tags_collection = db['tags']

# all_notes = notes_collection.find()
# for note in all_notes:
#     print(note)

# folder = {
#     'folderId': 4,
#     'folderName': "Fitness",
#     'createdAt': datetime(2023, 10, 1)
# }
# folders_collection.insert_one(folder)

# for folder in folders_collection.find():
#     print(folder)

# folders_collection.update_one(
#     { 'folderId': 4 }, # filter
#     { '$set': { 'folderName': 'Health & Fitness' } } # update name to health and fitness
# )

#folders_collection.delete_one({ 'folderId': 4 })

# client.close()
# print("Connection closed")


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
    


def main():
    print("Welcome to Your Notes App!")

    while True:
        choice = int(input('''
    Options:
    1. See all notes
    2. Search Notes
    3. Create a new note
                   
    Choice: '''))
        match choice:
            case 1:
                printAllNotes()
            case 2:
                searchNotes()
            case 3:
                createNewNote()
            case _:
                break


if __name__ == "__main__":
    main() 