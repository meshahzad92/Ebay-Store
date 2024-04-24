import sqlite3




import sqlite3

class Users:
    
    def insertUser(userPassword, userEmail, userName, userContact):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (userPassword, userEmail, userName, userContact) VALUES (?, ?, ?, ?)", (userPassword, userEmail, userName, userContact))
            conn.commit()
            return 'Data inserted successfully'
        except sqlite3.Error as e:
            return 'Error occurred: {}'.format(e)
        finally:
            conn.close()


    def getUsers(query, params=None):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            return 'Error occurred: {}'.format(e)
        finally:
            conn.close()

            
