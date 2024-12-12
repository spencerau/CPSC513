import pydantic
import mysql.connector
import os
from pydantic import BaseModel
import dotenv


dotenv.load_dotenv()

class database_connection():
    class Book(BaseModel):
        isbn: str
        title: str
        author: str
        publish_date: str
        publisher: int


    def __init__(self):
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": os.getenv("PASSWORD"),
            "database": "chapmanlibrary"
        }
        self.connection = mysql.connector.connect(**db_config)
        # dictionary = True returns the results as a dictionary
        self.cursor = self.connection.cursor(dictionary=True)

    
    def select_books(self):
        self.cursor.execute("SELECT * FROM books")
        result = self.cursor.fetchall()
        return result
    

    def select_book(self, isbn):
        self.cursor.execute("SELECT * FROM books WHERE isbn = %s", (isbn,))
        result = self.cursor.fetchall()
        return result[0]
    

    def create_book(self, book: Book):
        query = '''
        INSERT INTO books
        VALUES(%s, %s, %s, %s, %s)
        '''
        params = (book.isbn, book.title, book.author, book.publish_date, book.publisher)
        self.cursor.execute(query, params)
        self.connection.commit()
        return (f"ISBN: {book.isbn}")


    def destructor(self):
        self.cursor.close()
        self.connection.close()


db = database_connection()
#print(db.select_books())