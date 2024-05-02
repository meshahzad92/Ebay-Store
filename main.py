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
@app.route("/temp2")
def temp2():
    return render_template("malefashion-master/temp2.html")

@app.route("/")
def home():
    if request.method=="GET":
        print("I am in GET of homw") 
        image_url = url_for('static', filename='images/bmw.jpg')   
        electronics=databasee.execute_query("select * from product where category='Electronics'",()) 
        fashion=databasee.execute_query("select * from product where category='Fashion'",())
        sports=databasee.execute_query("select * from product where category='Sporting Goods'",())
        motors=databasee.execute_query("select * from product where category='Motors'",())
        home_and_garden=databasee.execute_query("select * from product where category='Home & Garden'",())  
        books=databasee.execute_query("select * from product where category='Books'",())
        latest_products=databasee.execute_query("select * from product   ORDER BY productId DESC LIMIT 50")
        electronics_imagePaths=[]
        fashion_imagePaths=[]
        sports_imagePaths=[]
        motors_imagePaths=[]
        home_and_garden_imagePaths=[]
        books_imagePaths=[]
        latest_products_image_paths=[]

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
        print(latest_products,latest_products_image_paths)
        return render_template("malefashion-master/home.html",image_url=image_url,
                           electronics=electronics,fashion=fashion,sports=sports,
                           motors=motors,home_and_garden=home_and_garden,books=books,
                           electronics_imagePaths=electronics_imagePaths,
                           fashion_imagePaths=fashion_imagePaths,
                           sports_imagePaths=sports_imagePaths
                           ,motors_imagePaths=motors_imagePaths,
                           home_and_garden_imagePaths=home_and_garden_imagePaths
                           ,books_imagePaths=books_imagePaths,latest_products=latest_products,latest_products_image_paths=latest_products_image_paths)



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
        session["category"]=""
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
            return redirect(url_for("shop"))
      
    

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
            search_query = session["search"]
            products = databasee.execute_query("SELECT * FROM product WHERE productName LIKE ? OR productDescription LIKE ?", ('%'+search_query+'%', '%'+search_query+'%'))
            session.pop("search")
        elif "category" in session:
            category = session["category"]
            products = databasee.execute_query("SELECT * FROM product WHERE category=?", (category,))
            session.pop("category")
        else:
            products = databasee.execute_query("SELECT * FROM product")
            
        imagePaths = []
        for product in products:
            imagePaths.append(databasee.execute_query("SELECT imagePath FROM productImages WHERE productId=? AND imagePath IS NOT NULL LIMIT 1", (product[0],)))
            
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
            redirect(url_for('home'))
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
    





@app.route("/sellerProfile", methods=["GET", "POST"])
def sellerProfile():
    
    if request.method == "POST":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        
        print("this is seller",request.form.get('productId'))
        product_id = request.form.get('productId')
        sellerEmail=databasee.execute_query("select userEmail from product where productId=? limit 1", (product_id,))
        sellerEmail=sellerEmail[0][0]
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
        for product_id in products_id:
            seller_email = databasee.execute_query("select userEmail from product where productId=?", (product_id[0],))
            seller_email_str = seller_email[0][0] if seller_email else None
            print(seller_email_str)
            databasee.execute_query("insert into orderHasProducts (orderId,productId,sellerId,buyerId) values(?,?,?,?)", (latest_order_id[0][0], product_id[0], seller_email_str, session["userEmail"]))
            databasee.execute_query("update product set sold='True' where productId=?",(product_id[0],))
            return redirect(url_for("home"))
        
        return redirect(url_for("home"))

@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        print("I am in GET of orders")
        return render_template("malefashion-master/orders.html")

@app.route("/viewMyOrders", methods=["GET", "POST"])
def viewMyOrders():
    if request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        return render_template("malefashion-master/viewMyOrders.html")
    if request.method=="POST":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        
        return render_template("malefashion-master/viewMyOrders.html",orders=orders)

@app.route("/viewOrdersToDeliver", methods=["GET", "POST"])
def viewOrdersToDeliver():
    if request.method == "GET":
        if databasee.is_user_logged_in(session)==False:
            return redirect(url_for('login'))
        return render_template("malefashion-master/viewOrdersToDeliver.html")   

if __name__ == '__main__':
    app.run()