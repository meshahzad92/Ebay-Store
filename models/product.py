from flask import Flask
import sqlite3


class products:
    def db_connection():
        conn=sqlite3.connect('store.db')
        return conn
    
    def create_table():
        conn = products.db_connection()
        conn.execute('CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, description TEXT, price REAL, qty INTEGER)')
        conn.close()


    def add_product(name, description, price, qty):
        conn = products.db_connection()
        conn.execute('INSERT INTO products (name, description, price, qty) VALUES (?, ?, ?, ?)', (name, description, price, qty))
        conn.commit()
        conn.close()


    def get_all_products():
        conn = products.db_connection()
        products = conn.execute('SELECT * FROM products').fetchall()
        conn.close()
        return products
    


    def get_product(id):
        conn = products.db_connection()
        product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()
        conn.close()
        return product
    
    def delete_product(id):
        conn = products.db_connection()
        conn.execute('DELETE FROM products WHERE id = ?', (id,))
        conn.commit()
        conn.close()
    


    def update_product(id, name, description, price, qty):
        conn = products.db_connection()
        conn.execute('UPDATE products SET name = ?, description = ?, price = ?, qty = ? WHERE id = ?', (name, description, price, qty, id))
        conn.commit()
        conn.close()    



    