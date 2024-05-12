import sqlite3
from functools import wraps

def handle_database_operations(func):
    @wraps(func)
    def wrapper(self, *args,  **kwargs):

        connection,cursor = Note.connect()
        try:
            result = func(self,cursor,*args)
            connection.commit()
            return result
        
        except Exception as Error:
            print("Error:", Error)
            connection.rollback()

        finally:
            connection.close()

    return wrapper    

class Note:
    def __init__(self,title,content):
        self.id = 0
        self.title = title
        self.content = content
        self.done = False

    @classmethod
    @handle_database_operations
    def get_notes(cls,cursor):
        cursor.execute("SELECT * FROM notes")
        rows = cursor.fetchall()
        return rows

    @classmethod
    def connect(cls):
        connection = sqlite3.connect("Database/database.db")
        cursor = connection.cursor()
        return(connection,cursor)
    
    @handle_database_operations
    def add_note(self, cursor):
        cursor.execute("INSERT INTO notes (title, content, done) VALUES (?, ?, ?)",(self.title, self.content, self.done))

    @classmethod
    @handle_database_operations
    def delete(cls,cursor,id):
        cursor.execute("DELETE FROM notes WHERE id = ?",(id,))

    @classmethod
    @handle_database_operations
    def set_done(cls,cursor,id):
        cursor.execute("SELECT done FROM notes WHERE id = ?" ,(id,))
        done = cursor.fetchone()[0]
        print(done)

        new_done = change_values(done)

        print(new_done)
        cursor.execute("UPDATE notes SET done = ? WHERE id = ?" ,(new_done,id))

def change_values(number):
    if (number == '0'):
        return '1'
    
    if(number == '1'):
        return '0'