import sqlite3
    
class Table():
    def __init__(self,name,columns,placeholders):
        self.name = name
        self.columns = columns
        self.placeholders = placeholders

    def Connect(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        return(connection,cursor)
    
    def Add(self,Data):
        connection,cursor = self.Connect()
        try:
            cursor.execute(f"INSERT INTO {self.name}{self.columns} VALUES{self.placeholders};",Data)
            connection.commit()

        except Exception as Error:
            print("Error:", Error)
            connection.rollback()

        finally:
            connection.close()

    def Delete(self,Id):
        connection,cursor = self.Connect()
        try:
            cursor.execute(f"DELETE FROM {self.name} WHERE {self.columns[0]} = ?",(Id,))
            connection.commit()

        except Exception as Error:
            print("Error:", Error)
            connection.rollback()

        finally:
            connection.close()

    def GetLastId(self):
        connection,cursor = self.Connect()
        cursor.execute(f"SELECT {self.columns[0]} FROM {self.name} ORDER BY {self.columns[0]} DESC LIMIT 1;")
        return cursor.fetchone()[0]

class Users(Table):
    def Validate(self, Username, Password):
        connection,cursor = self.Connect()
        try:
            cursor.execute("SELECT UserName FROM users WHERE UserName = ? AND UserPassword = ?", (Username, Password))
            User = cursor.fetchone()

            if User:
                return True
            else:
                return False

        except Exception as Error:
            print("Error:", Error)
            return False
        
        finally:
            connection.close()

    def GetId(self,Username):
        connection,cursor = self.Connect()
        try:
            cursor.execute("SELECT Id FROM users WHERE UserName = ?",(Username,))
            return cursor.fetchone()[0]
            

        except Exception as Error:
            print("Error:", Error)
            connection.rollback()

        finally:
            connection.close()

class Notes(Table):
    def GetNotes(self,UserId):
        connection,cursor = self.Connect()
        try:
            cursor.execute("SELECT * FROM notes WHERE UserId = ? ORDER BY date DESC",(UserId,))
            return cursor.fetchall()
            

        except Exception as Error:
            print("Error:", Error)
            connection.rollback()

        finally:
            connection.close()


UsersParameters = {"columns":('Id','UserName','UserPassword'),
                   "placeholders":'(?,?,?)'}

NotesParameters = {"columns":('UserId','Title','Content'),
                   "placeholders":'(?,?,?)'}

TableUsers = Users("users",UsersParameters['columns'],UsersParameters['placeholders'])
TableNotes = Notes("notes",NotesParameters["columns"],NotesParameters["placeholders"])