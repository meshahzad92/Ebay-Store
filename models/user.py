from flask import Flask
import sqlite3



class users:

    def connect_db(self):
        conn = sqlite3.connect('database.db')
        return conn

    def create_user_table(self):
        conn = self.connect_db()
        conn.execute()
        conn.close() 
        conn.commit()



    