import sqlite3




import sqlite3

class Users:
    def __init__(self):
        self.userName = ""
        self.userEmail = ""
        self.userPassword = ""
        self.userContact = ""

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
    def updateUser(user_email, new_name, new_password, new_contact,currentEmail):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET userPassword = ?, userEmail = ?, userName = ?, userContact = ? WHERE userEmail = ?",
               (new_password, user_email, new_name, new_contact, currentEmail))
            conn.commit()
            return 'Data updated successfully'
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

            


class addressess():
    def __init__(self):
        self.userAddressID = 0
        self.userContact = ""
        self.userCountry = ""
        self.userCity = ""
        self.userStreet = ""
        self.userZipCode = ""
        self.userEmail = ""
    def addressess(self, userContact="", userCountry="", userCity="", userStreet="", userZipCode="", userEmail=""):
        
        self.userContact = userContact
        self.userCountry = userCountry
        self.userCity = userCity
        self.userStreet = userStreet
        self.userZipCode = userZipCode
        self.userEmail = userEmail
    def updateAddress(userContact, userCountry, userCity, userStreet, userZipCode, userEmail,new_address_id):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            print("I'm in updateAddress")  # Ensure function is being called
            cursor.execute("UPDATE addresses SET userContact = ?, userCountry = ?, userCity = ?, userStreet = ?, userZipCode = ? WHERE userEmail = ? and userAddressID = ?", (userContact, userCountry, userCity, userStreet, userZipCode, userEmail, new_address_id))
            conn.commit()
            return 'Data updated successfully'
        except sqlite3.Error as e:
            return 'Error occurred: {}'.format(e)
        finally:
            conn.close()

    def insertAddress(userContact, userCountry, userCity, userStreet, userZipCode, userEmail):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO addresses (userContact, userCountry, userCity, userStreet, userZipCode, userEmail) VALUES (?, ?, ?, ?, ?, ?)",
                       (userContact, userCountry, userCity, userStreet, userZipCode, userEmail))
            conn.commit()
            return 'Data inserted successfully'
        except sqlite3.Error as e:
            return 'Error occurred: {}'.format(e)
        finally:
            conn.close()



def user_exist(userEmail,query,params=None):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(query,params)
    user = cursor.fetchall()
    conn.close()
    if user:
        return True
    return False


def is_user_logged_in(session):
    if 'userEmail' in session:
        return True
    return False

def execute_query(query, params=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    rows = cursor.fetchall()  # Fetch result rows
    conn.close()
    return rows

