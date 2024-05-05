from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
import sqlite3
import os
import databasee
from werkzeug.utils import secure_filename
from datetime import datetime
# Inside your code


from flask import url_for,flash
from flask import session

app = Flask(__name__)
app.secret_key = '03025202775Abc$'  # replace 'your secret key' with your actual secret key

admin_username = 'site_admin'
admin_password = 'admin_123'

@app.route('/login_pg.html')
def index():
    return render_template('login_pg.html')

@app.route('/check_admin', methods=['POST'])
def check_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if admin_username==username and admin_password==password:
            return redirect('admin_pg.html')
        return redirect('/login_pg.html')

@app.route('/admin_pg.html')
def index2():
     users,address,category,product,order,data = Total_Values()
     return render_template('admin_pg.html',users=users,address=address,category=category,product=product,order=order,data=data)


def Total_Values():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM USERS")
    users=cursor.fetchone()[0]
    address = cursor.execute("SELECT COUNT(*) FROM PRODUCT")
    address=cursor.fetchone()[0]
    category = cursor.execute("SELECT COUNT(*) FROM ORDERS")
    category=cursor.fetchone()[0]
    product = cursor.execute("SELECT COUNT(*) FROM CATEGORY")
    product=cursor.fetchone()[0]
    order = cursor.execute("SELECT COUNT(*) FROM ADDRESSES")
    order=cursor.fetchone()[0]
    cursor.execute("SELECT ORDERID,STATUS FROM ORDERSSTATUS")
    data = cursor.fetchall()
    conn.close()
    return users,address,category,product,order,data

@app.route('/Customer.html')
def index3():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT USERID,USERPASSWORD,USEREMAIL,USERNAME,USERCONTACT FROM USERS WHERE USERID <>35 ORDER BY USERID")
    data = cursor.fetchall()
    conn.close()
    return render_template('Customer.html',data=data)

@app.route('/MyNotes.html')
def index4():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT NOTE_ID,NOTE_TEXT FROM ADMIN_NOTES ORDER BY NOTE_ID")
    data = cursor.fetchall()
    conn.close()
    return render_template('MyNotes.html',data=data)

@app.route('/Products.html')
def index5():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT PRODUCTID,PRODUCTNAME,PRODUCTCONDITION,PRODUCTDESCRIPTION,PRODUCTPRICE,USEREMAIL,CATEGORY FROM PRODUCT ORDER BY PRODUCTID")
    data = cursor.fetchall()
    conn.close()
    return render_template('Products.html',data=data)

@app.route('/orders.html')
def index6():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ORDERID,ORDERDATE FROM ORDERS ORDER BY ORDERID")
    data = cursor.fetchall()
    conn.close()
    return render_template('orders.html',data=data)

@app.route('/add_note', methods=['POST'])
def add_note():
    if request.method == 'POST':
        note_text = request.form['note_text']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO admin_notes (note_text) VALUES (?)', (note_text,))
        conn.commit()
        conn.close()
    return redirect('/MyNotes.html')

@app.route('/edit_user', methods=['POST'])
def edit_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_password = request.form['user_password']
        user_email = request.form['user_email']
        user_name = request.form['user_name']
        user_contact = request.form['user_contact']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        update_query = "UPDATE users SET "
        params = []
        if user_password:
            update_query += "userpassword=?, "
            params.append(user_password)

        if user_email:
            update_query += "useremail=?, "
            params.append(user_email)

        if user_name:
            update_query += "username=?, "
            params.append(user_name)

        if user_contact:
            update_query += "usercontact=?, "
            params.append(user_contact)

        update_query = update_query.rstrip(', ')

        update_query += " WHERE userid=?"
        params.append(user_id)

        cursor.execute(update_query, tuple(params))
        connection.commit()
        connection.close()
        
    return redirect('/Customer.html')

@app.route('/edit_product', methods=['POST'])
def edit_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        product_condition = request.form['Product_Condition']
        product_description = request.form['Product_Description']
        product_price = request.form['Product_Price']
        user_email = request.form['User_Email']
        product_category = request.form['Product_Category']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        update_query = "UPDATE PRODUCT SET "
        params = []
        if product_name:
            update_query += "PRODUCTNAME=?, "
            params.append(product_name)

        if product_condition:
            update_query += "PRODUCTCONDITION=?, "
            params.append(product_condition)

        if product_description:
            update_query += "PRODUCTDESCRIPTION=?, "
            params.append(product_description)

        if product_price:
            update_query += "PRODUCTPRICE=?, "
            params.append(product_price)
        
        if user_email:
            update_query += "USEREMAIL=?, "
            params.append(user_email)

        update_query = update_query.rstrip(', ')

        update_query += " WHERE PRODUCTID=?"
        params.append(product_id)

        cursor.execute(update_query, tuple(params))
        connection.commit()
        connection.close()
        
    return redirect('/Products.html')


@app.route('/edit_order', methods=['POST'])
def edit_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        order_date = request.form['order_date']
        shipping_cost = request.form['shipping_cost']
        shipping_address_id = request.form['shipping_address_id']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        update_query = "UPDATE ORDERS SET "
        params = []
        if order_date:
            update_query += "ORDERDATE=?, "
            params.append(order_date)

        if shipping_cost:
            update_query += "SHIPPINGCOST=?, "
            params.append(shipping_cost)

        if shipping_address_id:
            update_query += "SHIPPINGADDRESSID=?, "
            params.append(shipping_address_id)

        update_query = update_query.rstrip(', ')

        update_query += " WHERE ORDERID=?"
        params.append(order_id)
        cursor.execute(update_query, tuple(params))
        connection.commit()
        connection.close()
        
    return redirect('/orders.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_password = request.form['user_password']
        user_email = request.form['user_email']
        user_name = request.form['user_name']
        user_contact = request.form['user_contact']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                       (user_id, user_password, user_email, user_name, user_contact))
        connection.commit()
        connection.close()
    return redirect('/Customer.html')

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        product_name = request.form['product_name']
        product_condition = request.form['product_condition']
        product_description = request.form['product_description']
        product_price = request.form['product_price']
        user_email = request.form['user_email']
        product_category = request.form['product_category']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO PRODUCT VALUES (?, ?, ?, ?, ?,?,?)",
                       (product_id, product_name, product_condition,product_description, product_price, user_email, product_category))
        connection.commit()
        connection.close()
    return redirect('/Products.html')

@app.route('/add_order', methods=['POST'])
def add_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        order_date = request.form['order_date']
        shipping_cost = request.form['shipping_cost']
        shipping_address_id = request.form['shipping_address_id']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ORDERS VALUES (?, ?, ?, ?)",
                       (order_id,order_date,shipping_cost,shipping_address_id))
        connection.commit()
        connection.close()
    return redirect('/orders.html')


@app.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        user_id = request.form['user_id']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE userid=?", (user_id,))
        connection.commit()
        connection.close()
    return redirect('/Customer.html')

@app.route('/delete_product', methods=['POST'])
def delete_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM PRODUCT WHERE PRODUCTID=?", (product_id,))
        connection.commit()
        connection.close()
    return redirect('/Products.html')

@app.route('/delete_order', methods=['POST'])
def delete_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM ORDERS WHERE ORDERID=?", (order_id,))
        connection.commit()
        connection.close()
    return redirect('/orders.html')

@app.route('/delete_notes', methods=['POST'])
def delete_notes():
    if request.method == 'POST':
        note_id = request.form['note_id']
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM ADMIN_NOTES WHERE NOTE_ID=?", (note_id,))
        connection.commit()
        connection.close()
    return redirect('/MyNotes.html')

'''
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute(''INSERT INTO ORDERSSTATUS VALUES(4,'Delivered')'')
conn.commit()
conn.close()
'''






@app.route("/temp2")
def temp2():
    return render_template("malefashion-master/temp2.html")

@app.route("/")
def home():
    if request.method=="GET":
       
        image_url = url_for('static', filename='images/gg.jpg')   
        electronics=databasee.execute_query("select * from product where category='Electronics'",()) 
        fashion=databasee.execute_query("select * from product where category='Fashion'",())
        sports=databasee.execute_query("select * from product where category='Sporting Goods'",())
        motors=databasee.execute_query("select * from product where category='Motors'",())
        home_and_garden=databasee.execute_query("select * from product where category='Home & Garden'",())  
        books=databasee.execute_query("select * from product where category='Books'",())
        latest_products=databasee.execute_query("select * from product   ORDER BY productId DESC LIMIT 50")
        on_sale=databasee.execute_query("select * from product  where category='Motors'  ORDER BY productId  ASC LIMIT 50")
        best_seller=databasee.execute_query("select * from product  where category='Fashion'  ORDER BY productId  ASC LIMIT 50")
        top_viewed=databasee.execute_query("select * from product  where category='Home & Garden'  ORDER BY productId  ASC LIMIT 50")

        electronics_imagePaths=[]
        fashion_imagePaths=[]
        sports_imagePaths=[]
        motors_imagePaths=[]
        home_and_garden_imagePaths=[]
        books_imagePaths=[]
        latest_products_image_paths=[]
        on_sale_imagePaths=[]
        best_seller_imagePaths=[]
        top_viewed_imagePaths=[]

        for on_sale_product in on_sale:
            on_sale_imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (on_sale_product[0],)))
        for best_seller_product in best_seller:
            best_seller_imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (best_seller_product[0],)))
        for top_viewed_product in top_viewed:
            top_viewed_imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (top_viewed_product[0],)))

        for product in latest_products:
            latest_products_image_paths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (product[0],)))

        for product in electronics:
            electronics_imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (product[0],)))
        for product in fashion:
            fashion_imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (product[0],))
        )
        for product in sports:
            sports_imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (product[0],))
        )   
        for product in motors:
            motors_imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (product[0],))
        )
        for product in home_and_garden:
            home_and_garden_imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (product[0],))
        )
        for product in books:
            books_imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (product[0],))
        )   

        return render_template("malefashion-master/home.html",image_url=image_url,
                           electronics=electronics,fashion=fashion,sports=sports,
                           motors=motors,home_and_garden=home_and_garden,books=books,
                           electronics_imagePaths=electronics_imagePaths,
                           fashion_imagePaths=fashion_imagePaths,
                           sports_imagePaths=sports_imagePaths
                           ,motors_imagePaths=motors_imagePaths,
                           home_and_garden_imagePaths=home_and_garden_imagePaths
                           ,books_imagePaths=books_imagePaths,latest_products=latest_products,
                           latest_products_image_paths=latest_products_image_paths,
                           top_viewed=top_viewed,on_sale=on_sale
                           ,best_seller=best_seller,
                           top_viewed_imagePaths=top_viewed_imagePaths,
                           on_sale_imagePaths=on_sale_imagePaths
                           ,best_seller_imagePaths=best_seller_imagePaths)



@app.route("/userProfile",methods=["GET","POST"])
def userProfile():
    if request.method=="GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for("login"))

        return render_template("malefashion-master/userProfile.html")
    return render_template("malefashion-master/userProfile.html")

@app.route("/search",methods=["GET","POST"])
def search():
    if request.method=="POST":
         search_query = request.form['search']
         session["search"]=search_query
         print("i am here in the ",search_query)

         return redirect(url_for("shop_list"))





@app.route("/addAddress",methods=["GET","POST"])
def addAddress():

    if request.method=="POST":

        databasee.addressess.insertAddress(request.form["userContact"],request.form["userCountry"],request.form["userCity"],request.form["userStreet"],request.form["userZipCode"],session["userEmail"])
        
        return redirect(url_for("home"))
    elif request.method=="GET":
        if databasee.is_user_logged_in(session)==False:
            session['referrer'] = request.referrer
            return redirect(url_for("login"))
        return render_template("malefashion-master/addAddress.html")



    return render_template("malefashion-master/addAddress.html")



@app.route("/sell", methods=["GET", "POST"])
def sell():
    if request.method == "GET":
        if not databasee.is_user_logged_in(session):
            return redirect(url_for("login"))

        categories = databasee.execute_query("SELECT categoryName FROM category")
  
        return render_template("malefashion-master/sell.html", categories=categories)
    
    elif request.method == "POST":
        print("I am in POST")
    
    # Check if the request contains files
        if 'images[]' in request.files:
            print("Files found")
            productName = request.form.get("productName", "")
            productCondition = request.form.get("productCondition", "")
            productDescription = request.form.get("productDescription", "")
            productPrice = request.form.get("productPrice", "")

        # Insert product details into the database
            databasee.execute_query("INSERT INTO product (productName, productCondition, productDescription, productPrice, userEmail, category) VALUES (?, ?, ?, ?, ?, ?)", 
                        (productName, productCondition, productDescription, productPrice, session["userEmail"], request.form.get("selectCategory", "")))

        
        # Get the ID of the latest inserted product
            latestProductId = databasee.execute_query("SELECT MAX(productId) FROM product")[0][0]
        
# Process each image
            images = request.files.getlist('images[]')
            for i, image in enumerate(images):
    # Save the image to a directory
                if image.filename != '':
                    filename = secure_filename(image.filename) # type: ignore
                    path = os.path.join('static/productImages/', f"{latestProductId}_{i+1}_{filename}")
                    image.save(path)

    
    # Insert the image path into the database
                databasee.execute_query("INSERT INTO productImages (productId, imagePath) VALUES (?, ?)", (latestProductId, path))

    
    return redirect(url_for("home"))


@app.route("/myListings",methods=["GET","POST"])
def myListings():
    if request.method=="GET":
        if  databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        products=databasee.execute_query("select * from product where userEmail=?",(session["userEmail"],))
        imagePaths=[]
        for product in products:
            imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (product[0],)))
        for index in range(len(imagePaths)):
            print(imagePaths[index])
        return render_template("malefashion-master/myListings.html",products=products,imagePaths=imagePaths)   
    if request.method=="POST":
        userEmail=request.form.get("userEmail")


@app.route("/viewSellerListings",methods=["GET","POST"])
def viewSellerListings():
    if request.method=="GET":
        print("i am in get of viewSellerListings")
        if  databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        seller_email=session["sellerEmail"]
        products=databasee.execute_query("select * from product where userEmail=?",(seller_email,))
        imagePaths=[]
        for product in products:
            imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? ORDER BY productId ASC LIMIT 1", (product[0],)))
        for index in range(len(imagePaths)):
            print(imagePaths[index])
        return render_template("malefashion-master/sellerListings.html",products=products,imagePaths=imagePaths)   


@app.route("/removeFromWishList",methods=["GET","POST"])
def removeFromWishList():
    if  request.method=="GET":
        return redirect(url_for("home"))
    
    if request.method=="POST":
        product_id = request.form.get('productId')
        print(product_id)
        databasee.execute_query("delete from wishlist where productId=? and userEmail=?", (product_id, session["userEmail"]))
        return redirect(url_for("viewWishList"))


@app.route("/updateAddress", methods=["GET", "POST"])
def updateAddress():
    if request.method == "GET":
        addresses = databasee.execute_query("SELECT * FROM addresses WHERE userEmail=?", (session["userEmail"],))
        return render_template("malefashion-master/updateAddress.html", addresses=addresses)
    
    elif request.method == "POST":
        # Retrieve the address ID from the form data
        address_id = request.form.get("addressId")
        
        # Use the address ID to fetch the address details from the database
        result = databasee.execute_query("SELECT * FROM addresses WHERE userAddressId=?", (address_id,))
        print(result)
        if result:
            # Instantiate the address object
            addressObject = databasee.addressess()
            
            # Assign values to addressObject attributes
            addressObject.userContact = result[0][1]
            addressObject.userCountry = result[0][2]
            addressObject.userCity = result[0][3]
            addressObject.userStreet = result[0][4]
            addressObject.userZipCode = result[0][5]
            addressObject.userEmail = result[0][6]
            addressObject.userAddressId = result[0][0]
            return render_template("malefashion-master/addressess.html", userObject=addressObject)
        else:
            return "Address not found"

@app.route("/deleteAddress", methods=["GET", "POST"])
def deleteAddress():
    if request.method == "GET":
        addresses=databasee.execute_query("select * from addresses where userEmail=?",(session["userEmail"],))
        return render_template("malefashion-master/deleteAddress.html",addresses=addresses)
    elif request.method == "POST":
        # Retrieve the address ID from the form data
        address_id = request.form.get("addressId")
        
        # Use the address ID to fetch the address details from the database
        databasee.execute_query("delete  FROM addresses WHERE userAddressId=?", (address_id,))
        return redirect(url_for("home"))


@app.route("/addPaymentMethod")
def addPaymentMethod():
    return render_template("malefashion-master/addPaymentMethod.html")
@app.route("/updatePaymentMethod")
def updatePaymentMethod():
    return render_template("malefashion-master/updatePaymentMethod.html")
@app.route("/deletePaymentMethod")  
def deletePaymentMethod():
    return render_template("malefashion-master/deletePaymentMethod.html")


@app.route("/addressManagement")
def addressManagement():
    return render_template("malefashion-master/addressManagement.html")

@app.route("/paymentManagement")
def paymentManagement():
    return render_template("malefashion-master/paymentManagement.html")
@app.route("/updatePersonalInfo")
def updatePersonalInfo():
    return render_template("malefashion-master/updatePersonalInfo.html")
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['referrer'] = request.referrer
        
        userEmail = request.form['userEmail']
        userPassword = request.form['userPassword']
        print(userEmail,userPassword)
        # Query to retrieve user based on email
        query = "SELECT * FROM users WHERE userEmail = ?"
       
        # Retrieve user(s) from the database based on email
        users = databasee.Users.getUsers(query, (userEmail,))

        # Check if any user matches the provided email
        if users:
            print("users is not empty here")
            print(userPassword)
            # Check if the password matches
            if users and len(users) > 0 and users[0][1] == userPassword:
                print("inside storing in session")
                # Storing user information in session
                session["userName"] = users[0][3]
                session["userEmail"] = users[0][2]
                print("successfully logged in   ")
                # if 'referrer' in session:
                #     referrer = session.pop('referrer')  # Get and remove the referrer URL from session
                #     return redirect(referrer)
                return redirect(url_for("home"))  # Redirect to the dashboard route
            else:
                print("password dont matched")
                # Password is incorrect, show login page with an error message
                return render_template('malefashion-master/login.html', error="Invalid email or password")
        else:
         print("user dont exist ")
            # User doesn't exist, show login page with an error message
         return   redirect(url_for('signUp', error="Invalid email or password"))

    elif request.method == 'GET':
        # If it's a GET request, render the login page
       return render_template("malefashion-master/login.html")

@app.route("/signUp", methods=['POST', 'GET'])
def signUp():
    print("hello i am here before post")

    if request.method== 'POST':
               
        print("hello")
        userPassword = request.form['userPassword']
        userEmail = request.form['userEmail']
        firstname=request.form["userFirstName"]
        lastname=request.form["userLastName"]
        userName =firstname+lastname
        userContact = request.form['userContact']
        print(request.form["confirmPassword"])
        print(userPassword,userEmail,userName,userContact)
        if request.form["confirmPassword"]!=userPassword:
            print("i ma in first if")
            return  redirect(url_for("signUp"))
        users=databasee.Users.getUsers("select * from users WHERE userEmail = ?", (userEmail,))
        if users:
            print("i am in second if")
            return redirect(url_for('login', error="User already exists"))
        else:
            print("i am in else")
            print("successfully inserted")
            databasee.execute_query("insert into addresses (userContact,userCountry,userCity,userStreet,userZipCode,userEmail) values(?,?,?,?,?,?)",(userContact,"","","","",userEmail))
            databasee.execute_query("INSERT INTO users (userPassword, userEmail, userName, userContact) VALUES (?, ?, ?, ?)", (userPassword, userEmail, userName, userContact)) 
            return redirect(url_for('login'))
    else:
        return render_template('malefashion-master/signUp.html')

@app.route("/personalInfo", methods=["GET", "POST"])
def personalInfo():
    currentEmail=""
    
    if request.method == "GET":
        # Fetch user's information from the database based on their email
        if 'userEmail' not in session:
            return redirect(url_for('login'))
        user_email = session["userEmail"] 
        
        currentEmail=user_email
        user = databasee.Users.getUsers("SELECT * FROM users WHERE userEmail=?", (user_email,))
        # Check if user exists
        if user:
            userObject = databasee.Users()
            userObject.userName = user[0][3]
            userObject.userEmail = user[0][2]
            userObject.userPassword = user[0][1]
            userObject.userContact = user[0][4]
            return render_template('malefashion-master/personelInfo.html', userObject=userObject)
        else:
            return "User not found"
    elif request.method == "POST":
        # Retrieve edited information from the form
        new_name = request.form["userName"]
        new_password = request.form["userPassword"]
        new_contact = request.form["userContact"]
        new_email = request.form["userEmail"]
        # Update the database with the edited information
        user_email = session["userEmail"]  
        databasee.execute_query("UPDATE users SET userPassword = ?, userEmail = ?, userName = ?, userContact = ? WHERE userEmail = ?",(
                new_password, new_email, new_name, new_contact, user_email


        ))
        # databasee.Users.updateUser(user_email, new_name, new_password, new_contact,session["userEmail"])
        # # Check if there's a referrer URL stored in the session
        if 'referrer' in session:
            referrer = session.pop('referrer')  # Get and remove the referrer URL from session
            return redirect(referrer)  # Redirect the user back to the referrer URL
        else:
            return redirect(url_for("login"))  # Redirect to login if no referrer URL is found

@app.route("/userAddressess", methods=["GET", "POST"]  )
def addressess():
    print("hey i am in addressess")
    if request.method == "GET":
        
        if  databasee.is_user_logged_in(session)==False:
             return  redirect(url_for('login'))
        user_email = session["userEmail"]
        user = databasee.execute_query("SELECT * FROM addresses WHERE userEmail=?", (session["userEmail"],))
        userAddress=databasee.addressess()
        print(user)
        if user:
            userAddress.addressess(user[0][1],user[0][2],user[0][3],user[0][4],user[0][5],user[0][6])
            print(userAddress.userContact,userAddress.userCountry,userAddress.userCity,userAddress.userStreet,userAddress.userZipCode,userAddress.userEmail)
            return render_template('malefashion-master/addressess.html', userObject=userAddress)
        userAddress.userEmail=session["userEmail"]
        return render_template('malefashion-master/addressess.html', userObject=userAddress)
    elif request.method == "POST":
            print("i am in post")
    # # Retrieve edited information from the form
        
            
            new_contact = request.form["userContact"]
            new_country = request.form["userCountry"]
            new_city = request.form["userCity"]
            new_street = request.form["userStreet"]
            new_zip_code = request.form["userZipCode"]
            new_address_id = request.form["userAddressId"]
            databasee.addressess.updateAddress( new_contact, new_country, new_city, new_street, new_zip_code,session["userEmail"],new_address_id)
            
    # # Check if there's a referrer URL stored in the session
            return redirect(url_for("shop_list"))
      
    

@app.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('home'))
@app.route("/shop", methods=["GET", "POST"])
def shop():
    if request.method == "GET":
        return render_template('malefashion-master/shop.html')

@app.route("/product", methods=["GET", "POST"])
def product():
    if request.method == "GET":
        print("I am in GET")
        return render_template('malefashion-master/product.html', products=None, imagePaths=None)
    
    if request.method == "POST":
        print("I am in POST")
        product_id = request.form.get('productId')
        # Fetch product information and image paths using a JOIN query
        query = """
            SELECT product.*, productImages.imagePath
            FROM product
            INNER JOIN productImages ON product.productId = productImages.productId
            WHERE product.productId = ?
        """
        products_with_images = databasee.execute_query(query, (product_id,))
        
        # Extract product information and image paths from the query result
        products = []
        imagePaths = []
        for row in products_with_images:
            # product_info = row[:6]  # Assuming first 6 columns contain product information
            image_path = row[8]     # Assuming the 7th column contains the image path
            # products.append(product_info)
            imagePaths.append(image_path)
        products=databasee.execute_query("select * from product where productId=?",(product_id,))   
        
        # Print the retrieved data for debugging
        print("Product Information:")
        print(products)
        print("Image Paths:")
        print(imagePaths)

        return render_template('malefashion-master/product.html', products=products, imagePaths=imagePaths)

@app.route("/shop-list", methods=["GET", "POST"] )
def shop_list():
    if request.method == "GET":
        if not databasee.is_user_logged_in(session):
            return redirect(url_for('login'))
        
        if "search" in session:
            print("search applied")
            search_query = session["search"]
            products = databasee.execute_query("SELECT * FROM product WHERE productName LIKE ? OR productDescription LIKE ?", ('%'+search_query+'%', '%'+search_query+'%'))
            session.pop("search")
        elif "category" in session:
            print("category applied")
            category = session["category"]
            products = databasee.execute_query("SELECT * FROM product WHERE category=?", (category,))
            session.pop("category")
        else:
            print("no categyr or filer applied")
            products = databasee.execute_query("SELECT * FROM product")
            
        imagePaths = []
        for product in products:
            imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? AND imagePath IS NOT NULL LIMIT 1", (product[0],)))
        print("i am in cataogue page")
        print(products)
        return render_template("malefashion-master/shop-grid.html", products=products, imagePaths=imagePaths)

@app.route('/electronics', methods=['GET', 'POST'])
def electronics():
    if request.method == "GET":
        session["category"] = "Electronics"
        return redirect(url_for("shop_list"))

@app.route('/fashion', methods=['GET', 'POST'])
def fashion():
    if request.method == "GET":
        session["category"] = "Fashion"
        return redirect(url_for("shop_list"))

@app.route('/home_and_garden', methods=['GET', 'POST'])
def home_and_garden():
    if request.method == "GET":
        session["category"] = "Home & Garden"
        return redirect(url_for("shop_list"))

@app.route('/art', methods=['GET', 'POST'])
def collectibles_art():
    if request.method == "GET":
        session["category"] = "Collectibles & Art"
        return redirect(url_for("shop_list"))

@app.route('/motors', methods=['GET', 'POST'])
def motors():
    if request.method == "GET":
        session["category"] = "Motors"
        return redirect(url_for("shop_list"))

@app.route('/toys', methods=['GET', 'POST'])
def toys_hobbies():
    if request.method == "GET":
        session["category"] = "Toys & Hobbies"
        return redirect(url_for("shop_list"))

@app.route('/sports', methods=['GET', 'POST'])
def sporting_goods():
    if request.method == "GET":
        session["category"] = "Sporting Goods"
        return redirect(url_for("shop_list"))

@app.route('/health', methods=['GET', 'POST'])
def health_beauty():
    if request.method == "GET":
        session["category"] = "Health & Beauty"
        return redirect(url_for("shop_list"))


@app.route("/videoGames", methods=["GET", "POST"])
def videoGames():
    if request.method == "GET":
        session["category"] = "Video Games & Consoles"
        return redirect(url_for("shop_list"))
@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    if request.method == 'POST':
        # Process the product ID and add it to the wishlist
        product_id = request.form.get('productId')
        
        # Check if the product is already in the wishlist
        existing_product = databasee.execute_query("SELECT * FROM wishlist WHERE productId = ? AND userEmail = ?", (product_id, session["userEmail"]))
        
        if existing_product:
            # Product already exists in the wishlist, you can handle this case as per your requirement
            flash("Product already exists in your wishlist.")
        else:
            # Product doesn't exist in the wishlist, insert it
            databasee.execute_query("INSERT INTO wishlist (productId, userEmail) VALUES (?, ?)", (product_id, session["userEmail"]))
            flash("Product added to wishlist successfully.")
        
        return redirect(url_for('home'))  # Redirect to home page after adding to wishlist

    # Handle GET request to view wishlist
    # You can render a wishlist template here
    return 'View Wishlist'  # Example response for viewing wishlist

@app.route('/viewWishList', methods=['GET', 'POST'])
def viewWishList():
    if request.method == 'GET':
        if  databasee.is_user_logged_in(session) ==False:
            return redirect(url_for('login'))
        print("i am in wishlist get")
        products = databasee.execute_query("SELECT product.productId, product.productName, product.productCondition, product.productDescription, product.productPrice, product.category FROM wishlist JOIN product ON wishlist.productId = product.productId WHERE wishlist.userEmail = ?", (session["userEmail"],))
        print(products)
        if products:
            imagePaths = []
            for product in products:
                imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId = ? ORDER BY productId ASC LIMIT 1", (product[0],)))
            print(products,imagePaths)
            return render_template('malefashion-master/viewWishList.html', products=products, imagePaths=imagePaths)
        else:
            return redirect(url_for("home"))   



@app.route("/editListing", methods=["GET", "POST"])
def editListing():
    if request.method == "GET":
        product_id = request.form.get('productId')
        
    if request.method == "POST":
        
        product_id = request.form.get('productId')
        product=databasee.execute_query("select * from product where productId=?",(product_id,))

        
        return render_template('malefashion-master/editListing.html', product=product)


@app.route("/updateListing", methods=["GET", "POST"])
def updateListing():
    if request.method == "POST":
        product_id = request.form.get('productId')
        productName = request.form.get("productName", "")
        productCondition = request.form.get("productCondition", "")
        productDescription = request.form.get("productDescription", "")
        productPrice = request.form.get("productPrice", "")
        productCategory = request.form.get("productCategory", "")
        print(productName, productCondition, productDescription, productPrice)
        databasee.execute_query("UPDATE product SET productName = ?, productCondition = ?, productDescription = ?, productPrice = ? , category=? WHERE productId = ?", 
            (productName, productCondition, productDescription, productPrice, productCategory,product_id))

        images = request.files.getlist('images[]')
        for i, image in enumerate(images):
            if image.filename != '':
                filename = secure_filename(image.filename)
                path = os.path.join('static/productImages/', f"{product_id}_{i+1}_{filename}")
                image.save(path)

                # Insert the image path into the database
                databasee.execute_query("INSERT INTO productImages (productId, imagePath) VALUES (?, ?)", (product_id, path))

        return redirect(url_for("myListings"))

@app.route("/cart", methods=["GET", "POST"])
def cart():

    if request.method == "POST":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login')   )
        # Process the product ID and add it to the cart
        # You can perform any
        product_id = request.form.get('productId')
        print(product_id)
        if databasee.execute_query("SELECT * FROM cart WHERE productId = ? AND userEmail = ?", (product_id, session["userEmail"])):
            flash("Product already exists in your cart.")
            return redirect(url_for('home'))
        databasee.execute_query("INSERT INTO cart (userEmail, productId) VALUES (?, ?)", (session["userEmail"], product_id))
        databasee.execute_query("DELETE FROM wishlist WHERE productId = ? AND userEmail = ?", (product_id, session["userEmail"]))
        return redirect(url_for('home'))
    
@app.route("/viewCart", methods=["GET", "POST"])
def viewCart():
    if request.method == "GET":
        if  databasee.is_user_logged_in(session)==False:
            return redirect(url_for("login"))
        
        products = databasee.execute_query("SELECT product.productId, product.productName, product.productCondition, product.productDescription, product.productPrice, product.category FROM cart JOIN product ON cart.productId = product.productId WHERE cart.userEmail = ?", (session["userEmail"],))
        if products:
            imagePaths = []
            for product in products:
                imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId = ? ORDER BY productId ASC LIMIT 1", (product[0],)))
        
            print(products)
            print(imagePaths)

            return render_template("malefashion-master/cart.html", products=products, imagePaths=imagePaths)
        else:
            return redirect(url_for("home"))

      
    else:
            return redirect(url_for("home"))
    
@app.route("/removeFromCart", methods=["GET", "POST"])  
def removeFromCart():
    if request.method == "GET":
        return redirect(url_for("home"))
    if request.method == "POST":
        product_id = request.form.get('productId')
        databasee.execute_query("DELETE FROM cart WHERE productId = ? AND userEmail = ?", (product_id, session["userEmail"]))
        return redirect(url_for("viewCart"))
    

@app.route("/deleteListing", methods=["GET", "POST"])  
def deleteListing():
    if request.method == "GET":
        return redirect(url_for("home"))
    if request.method == "POST":
        product_id = request.form.get('productId')
        databasee.execute_query("DELETE FROM product WHERE productId = ? AND userEmail = ?", (product_id, session["userEmail"]))
        databasee.execute_query("DELETE FROM productImages WHERE productId = ?", (product_id,))
        return redirect(url_for("myListings"))
    






@app.route("/sellerProfile", methods=["GET", "POST"])
def sellerProfile():
    
    if request.method == "POST":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        
        print("this is seller",request.form.get('productId'))
        product_id = request.form.get('productId')
        sellerEmail=databasee.execute_query("select userEmail from product where productId=? limit 1", (product_id,))
        sellerEmail=sellerEmail[0][0]
        session["sellerEmail"]=sellerEmail
        print(sellerEmail)
        user = databasee.execute_query("""
    SELECT users.userEmail, users.username, users.userContact,
           addresses.userCountry, addresses.userCity, addresses.userStreet, addresses.userZipCode
    FROM users
    JOIN addresses ON users.userEmail = addresses.userEmail
    WHERE users.userEmail = ?
""",  (sellerEmail,))
        print(user)

        reviews=databasee.execute_query("select * from reviews where userEmail=?",(sellerEmail,))
        print(reviews)
        return render_template('malefashion-master/sellerProfile.html',user=user,reviews=reviews)

    elif request.method == "GET":
         print("i am in get request of the review button")
         sellerEmail = request.args.get('sellerEmail')
         session["sellerEmail"]=sellerEmail
         user = databasee.execute_query("""
    SELECT users.userEmail, users.username, users.userContact,
           addresses.userCountry, addresses.userCity, addresses.userStreet, addresses.userZipCode
    FROM users
    JOIN addresses ON users.userEmail = addresses.userEmail
    WHERE users.userEmail = ?
""",  (sellerEmail,))
    print(user)

    reviews=databasee.execute_query("select * from reviews where userEmail=?",(sellerEmail,))
    print(reviews)
    return render_template('malefashion-master/sellerProfile.html',user=user,reviews=reviews)
        


@app.route("/submitReview", methods=["GET", "POST"])
def submitReview():
    if request.method == "POST":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        senderEmail = session["userEmail"]
        review = request.form.get('reviewText')
        
        sellerEmail = request.form.get('userEmail')
        databasee.execute_query("INSERT INTO reviews (text, userEmail, senderEmail) VALUES (?, ?,  ?)", (review,sellerEmail,senderEmail ))
        return redirect(url_for('sellerProfile', sellerEmail=sellerEmail))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if request.method=="GET":
        if databasee.is_user_logged_in(session)==False:
            return render_template('malefashion-master/checkout.html')
        else:
            return render_template('malefashion-master/checkout.html')
    if request.method == "POST":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        product_id=databasee.execute_query("select productId from cart where userEmail=?",(session["userEmail"],))
        products=[]
        print(product_id)
        products = []

        for product_tuple in product_id:
            product_id = product_tuple[0]  # Extracting the product ID from the tuple
            product = databasee.execute_query("SELECT * FROM product WHERE productId=?", (product_id,))
            products.append(product)
            total=databasee.execute_query("select sum(productPrice) from product where productId in (select productId from cart where userEmail=?)",(session["userEmail"],))
        user = databasee.execute_query(
    """
    SELECT u.username, u.userEmail, a.userContact, a.userCountry, a.userCity, a.userStreet, a.userZipCode 
    FROM users AS u 
    JOIN addresses AS a ON u.userEmail = a.userEmail
    WHERE u.userEmail = ? 
    ORDER BY a.userAddressId ASC 
    LIMIT 1;
    """,
    (session["userEmail"],)
    )
        print("I am just before render")
        print(user)
        print(product_id)
        if user:

            print(user)
            return render_template("malefashion-master/checkout.html",products=products,total=total,user=user)
        else:
            print("I am in else")
            user = [None]*10
            return render_template("malefashion-master/checkout.html",products=products,total=total,user=user)


        

    return redirect(url_for("home"))


@app.route("/placeorder", methods=["GET", "POST"])
def placeorder():
    if request.method=="GET":
        return redirect(url_for("home"))
    if request.method=="POST":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        products_id=databasee.execute_query("select productId from cart where userEmail=?",(session["userEmail"],))
        print("i am in checkout post") 
        print(products_id)
        databasee.execute_query("delete from cart where userEmail=?",(session["userEmail"],))
        country = request.form.get('country')
        street = request.form.get('street')
        suite = request.form.get('suite')
        city = request.form.get('city')
        state = request.form.get('state')
        zipCode = request.form.get('zipCode')
        phone = request.form.get('phone')

        # Printing the form data (for debugging)
        print(country, street, suite, city, state, zipCode, phone)
        address=country+street+suite+city+state+zipCode+phone
        address = str(street or "") + "," + str(suite or "") + "," + str(city or "") + "," + str(state or "") + "," + str(zipCode or "") + "," + str(country or "") + "," + str(phone or "")
        databasee.execute_query("insert into orders (orderDate,address ,status) values(?,?,?)",(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),address,"Pending"))
        latest_order_id=databasee.execute_query("select max(orderId) from orders",())
        print("---------------",products_id)
        for product_id in products_id:
            print("i am in for loop")
            print(product_id[0])
        for product_id in products_id:
            seller_email = databasee.execute_query("select userEmail from product where productId=?", (product_id[0],))
            print(seller_email)
            seller_email_str = seller_email[0][0] if seller_email else None
            print(seller_email_str)
            databasee.execute_query("insert into orderHasProducts (orderId,productId,sellerId,buyerId,status,sellerStatus) values(?,?,?,?,?,?)", (latest_order_id[0][0], product_id[0], seller_email_str, session["userEmail"],"not","Pending"))
            databasee.execute_query("update product set sold='True' where productId=?",(product_id[0],))
            databasee.execute_query("delete from product where productId=?",(product_id[0],))
            
        
        return redirect(url_for("home"))






























@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        print("I am in GET of orders")
        return render_template("malefashion-master/orders.html")



@app.route("/myPendingOrders", methods=["GET", "POST"])
def myPendingOrders():
    if request.method == "POST" or request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        query='''
    select 
        orders.orderId, orders.orderDate, orders.address, orderHasProducts.status,
        orderHasProducts.productId, orderHasProducts.sellerId, orderHasProducts.buyerId,
        product.productName, product.productCondition, product.productPrice,
        product.category, product.sold
    from orders 
    join orderHasProducts on orders.orderId = orderHasProducts.orderId 
    join product on product.productId = orderHasProducts.productId where buyerId=? and orderHasProducts.status="not" or orderHasProducts.status="Pending"
'''
        return redirect(url_for('ordersTemplate2', query=query,buttonStatus="visible"))

@app.route("/myRecievedOrders",methods=["GET","POST"])
def myRecievedOrders():
    if request.method == "POST" or request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        query='''
    select 
        orders.orderId, orders.orderDate, orders.address, orderHasProducts.status,
        orderHasProducts.productId, orderHasProducts.sellerId, orderHasProducts.buyerId,
        product.productName, product.productCondition, product.productPrice,
        product.category, product.sold
    from orders 
    join orderHasProducts on orders.orderId = orderHasProducts.orderId 
    join product on product.productId = orderHasProducts.productId where buyerId=? and orderHasProducts.status="Delivered"
'''
        return redirect(url_for('ordersTemplate2', query=query,buttonStatus="hidden"))

@app.route("/myCancelledOrders",methods=["GET","POST"])
def myCancelledOrders():
    if request.method == "POST" or request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        query='''
    select 
        orders.orderId, orders.orderDate, orders.address, orderHasProducts.status,
        orderHasProducts.productId, orderHasProducts.sellerId, orderHasProducts.buyerId,
        product.productName, product.productCondition, product.productPrice,
        product.category, product.sold
    from orders 
    join orderHasProducts on orders.orderId = orderHasProducts.orderId 
    join product on product.productId = orderHasProducts.productId where buyerId=? and orderHasProducts.status="Cancelled"
'''
        return redirect(url_for('ordersTemplate2', query=query,buttonStatus="hidden"))

@app.route("/deliverToBuyer", methods=["GET", "POST"])
def deliverToBuyer():
    if request.method == "POST" or request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        query='''
    select 
        orders.orderId, orders.orderDate, orders.address, orderHasProducts.status,
        orderHasProducts.productId, orderHasProducts.sellerId, orderHasProducts.buyerId,
        product.productName, product.productCondition, product.productPrice,
        product.category, product.sold
    from orders 
    join orderHasProducts on orders.orderId = orderHasProducts.orderId 
    join product on product.productId = orderHasProducts.productId where sellerId    =? and orderHasProducts.sellerStatus="Pending"
'''
        return redirect(url_for('ordersTemplate', query=query,buttonStatus="visible"))

@app.route("/deliveredToBuyer", methods=["GET", "POST"])
def deliveredToBuyer():
    if request.method == "POST" or request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        query='''
    select 
        orders.orderId, orders.orderDate, orders.address, orderHasProducts.status,
        orderHasProducts.productId, orderHasProducts.sellerId, orderHasProducts.buyerId,
        product.productName, product.productCondition, product.productPrice,
        product.category, product.sold
    from orders 
    join orderHasProducts on orders.orderId = orderHasProducts.orderId 
    join product on product.productId = orderHasProducts.productId where sellerId=? and orderHasProducts.sellerStatus="Delivered"
'''
        return redirect(url_for('ordersTemplate', query=query,buttonStatus="hidden"))

@app.route("/cancelledToBuyer", methods=["GET", "POST"])
def cancelledToBuyer():
    if request.method == "POST" or request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        query='''
    select 
        orders.orderId, orders.orderDate, orders.address, orderHasProducts.status,
        orderHasProducts.productId, orderHasProducts.sellerId, orderHasProducts.buyerId,
        product.productName, product.productCondition, product.productPrice,
        product.category, product.sold
    from orders 
    join orderHasProducts on orders.orderId = orderHasProducts.orderId 
    join product on product.productId = orderHasProducts.productId where sellerId=? and orderHasProducts.sellerStatus="Cancelled"
'''
    return redirect(url_for('ordersTemplate', query=query,buttonStatus="hidden"))




@app.route("/ordersTemplate", methods=["GET", "POST"])
def ordersTemplate():
    if request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        
        query=request.args.get('query')
        buttonStatus=request.args.get('buttonStatus')
        print(query)
        orders = databasee.execute_query(query, (session["userEmail"],))

        image_paths = [
        ]
        print("from here order to deliver1")
        print(orders)
        if not orders:
            return redirect(url_for("home"))
        for order in orders:
             image_paths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId = ? ORDER BY productId ASC LIMIT 1", (order[4],)))
        print(image_paths)
        # for order in orders:
        #     print(order)                    
        return render_template("malefashion-master/viewOrdersToDeliver.html",products=orders,imagePaths=image_paths,buttonStatus=buttonStatus)   




@app.route("/ordersTemplate2", methods=["GET", "POST"])
def ordersTemplate2():
    if request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        
        query=request.args.get('query')
        buttonStatus=request.args.get('buttonStatus')
        print(query)
        orders = databasee.execute_query(query, (session["userEmail"],))

        image_paths = [
        ]
        print("from here order to deliver2")
        print(orders)
        if not orders:
            return redirect(url_for("home"))
        for order in orders:
             image_paths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId = ? ORDER BY productId ASC LIMIT 1", (order[4],)))
        print(image_paths)
        # for order in orders:
        #     print(order)                    
        return render_template("malefashion-master/viewOrdersToDeliver2.html",products=orders,imagePaths=image_paths,buttonStatus=buttonStatus)   


@app.route("/cancel", methods=["GET", "POST"])
def cancel():
    if request.method == "GET":
        return redirect(url_for("home"))
    if request.method == "POST":
        productId=request.form.get("productId")
        databasee.execute_query("update orderHasProducts set status='Cancelled',sellerStatus='Cancelled' where productId=?",(productId,))
        return redirect(url_for("orders"))    




@app.route('/deliver', methods=['GET', 'POST'])
def deliver():
    if request.method == "GET":
        return redirect(url_for("home"))
    if request.method == "POST":
        print("i am in deliver 1")
        productId=request.form.get("productId")
        databasee.execute_query("update orderHasProducts set status='Pending',sellerStatus='Delivered' where productId=?",(productId,))
        return redirect(url_for("orders"))










@app.route("/cancel2", methods=["GET", "POST"])
def cancel2():
    if request.method == "GET":
        return redirect(url_for("home"))
    if request.method == "POST":
        productId=request.form.get("productId")
        databasee.execute_query("update orderHasProducts set status='Cancelled',sellerStatus='Cancelled' where productId=?",(productId,))
        return redirect(url_for("orders"))    




@app.route('/deliver2', methods=['GET', 'POST'])
def deliver2():
    if request.method == "GET":
        return redirect(url_for("home"))
    if request.method == "POST":
        print("I AM IN DELIVER 2")
        productId=request.form.get("productId")
        print("i am in deliver 2")
        databasee.execute_query("update orderHasProducts set status='Delivered',sellerStatus='Delivered' where productId=?",(productId,))
        return redirect(url_for("orders"))
if __name__ == '__main__':
    app.run()