from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
import sqlite3
import databasee
from flask import url_for
from flask import session

app = Flask(__name__)
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        userEmail = request.form['userEmail']
        userPassword = request.form['userPassword']
        
        # Query to retrieve user based on email
        query = "SELECT * FROM users WHERE userEmail = ?"
       
        # Retrieve user(s) from the database based on email
        users = databasee.Users.getUsers(query, (userEmail,))
        
        # Check if any user matches the provided email
        if users:
            # Check if the password matches
            if users["userPassword"] == userPassword:
                # Storing user information in session
                session["userName"] = users["userName"]
                session["userEmail"] = users["userEmail"]
                
                return render_template("malefashion-master/shop.html")  # Redirect to the dashboard route
            else:
                # Password is incorrect, show login page with an error message
                return render_template('malefashion-master/login.html', error="Invalid email or password")
        else:
            # User doesn't exist, show login page with an error message
         return   redirect(url_for('signUp', error="Invalid email or password"))

    else:
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
        users=databasee.Users.getUsers("insert into * FROM users WHERE userEmail = ?", (userEmail,))
        if users:
            print("i am in second if")
            return   redirect(url_for('login', error="User already exists"))
        else:
            print("i am in else")
            databasee.Users.insertUser(userPassword, userEmail, userName, userContact)
            return redirect(url_for('login'))
    else:
        return render_template('malefashion-master/signUp.html')


@app.route("/personelInfo")
def personelInfo():
    
    userName.text=session["userName"]
    userEmail.text=session["userEmail"]
    userEmail=session["userEmail"]
    user=databasee.Users.getUsers("select * from users where userEmail=?",userEmail)
    userName.text=user["userName"]
    userEmail.text=user["userEmail"]
    userPassword.text=user["userPassword"]
    userCOntact.text=user["userPassword"]

    return render_template("malefashion-master\personelInfo.html")

@app.route("/userAddressess")
def addressess():
     userEmail=session["userEmail"]
    user=databasee.Users.getUsers("select * from users where userEmail=?",userEmail)
    userCOntact.text=user["userCOntact"]
usercountry.text=user["userCountry"]

userCity=user["userCity"]
userStreet=user["userStreet"]
    
if __name__ == '__main__':
    app.run()