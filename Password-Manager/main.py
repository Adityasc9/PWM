from flask import Flask, render_template, redirect, request, url_for, flash, session, abort
import sqlite3
import hashlib
import os
import random
app = Flask(__name__)
app.secret_key = os.urandom(24)
con = sqlite3.connect("data.db", check_same_thread=False)
cur = con.cursor()

def salter():
    text = ''
    for x in range(16):
        char = str(chr(random.randint(37, 129)))
        text += char
    return text

def ExistingUser(userEmail):
    usersOnDB = cur.execute("SELECT email FROM users").fetchall()
    exists = False
    for tup in usersOnDB:
        if userEmail == tup[0]:
            exists = True
    return exists

def checkLogin(userEmail, password): 
    if ExistingUser(userEmail):
        print(cur.execute(f"SELECT hashPass, salt FROM users WHERE email ='{userEmail}'").fetchone())
        hashPass, salt = cur.execute(f"SELECT hashPass, salt FROM users WHERE email ='{userEmail}'").fetchone()
        SaltyUserPass = password + salt
        if hashlib.sha256(SaltyUserPass.encode('utf-8')).hexdigest() == hashPass:
            return True
    
    return False

@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    if "user" in session:
        session.pop("user")
    if request.method == "POST":
        if ExistingUser(request.form["loginEmail"].strip()):
            if checkLogin(request.form["loginEmail"].strip(), request.form["loginPass"].strip()):
                session["user"] = request.form["loginEmail"].strip()
                return redirect(url_for("home"))
            else:
                flash("Incorrect credentials.")
                return redirect(url_for("login"))
        else:
            flash("User does not exist.")
            return redirect(url_for("login"))
    else:
        return render_template('login.html', title="Login")


@app.route("/home", methods=["POST", "GET"]) 
def home():
    if  "user" in session:
        userAccounts = {"site": [], "username": [], "password": []}
        data = cur.execute(f"SELECT site,userOnSite,EncryptedPassword FROM accounts WHERE email='{session['user']}'").fetchall()
        for accountTup in data:
            userAccounts["site"].append(accountTup[0])
            userAccounts["username"].append(accountTup[1])
            userAccounts["password"].append(accountTup[2])
        print(userAccounts)
        return render_template('home.html', title="Passwords", username = session["user"], userAccounts = userAccounts)
    else:
        flash("Not logged in.")
        return redirect(url_for("login"))



@app.route("/addPassword", methods=["POST", "GET"])
def addPassword():
    if request.method == "POST":
        storedData = cur.execute(f"SELECT site, userOnSite, EncryptedPassword FROM accounts WHERE email = '{session['user']}'").fetchall()
        for tup in storedData:
            if [request.form["newWebsite"].strip(), request.form["newUsername"].strip()] == [tup[0], tup[1]]:
                flash("Account already exists.")
                return redirect(url_for("home"))
        cur.execute("INSERT INTO accounts VALUES(?,?,?,?)", (session["user"],request.form["newWebsite"].strip(), request.form["newUsername"].strip(), request.form["newPass"].strip()))
        con.commit()
        return redirect(url_for("home"))
    else:
        if "user" in session:
            return render_template('addPassword.html', title="Add New Password")
        else:
            flash("Not logged in.")
            return redirect(url_for("login"))



@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        ListOfTuples = cur.execute("SELECT email FROM users").fetchall()
        emailsStored = []
        for tup in ListOfTuples:
            emailsStored.append(tup[0])

        if request.form["userEmail"] not in emailsStored:
            salt = salter()
            SaltyPassword = request.form["userPassword"] + salt
            print(SaltyPassword)
            cur.execute("INSERT INTO users('email', 'hashPass', 'salt') VALUES(?,?,?)", (request.form["userEmail"], hashlib.sha256(SaltyPassword.encode('utf-8')).hexdigest(), salt))
            con.commit()
            flash("Account created successfully")
            return redirect(url_for("login"))
        else:
            flash(f"{request.form['userEmail']} already exists")
            return redirect(url_for("login"))
                
    else:
        return render_template("register.html", title="Register")



if __name__ == "__main__":
    app.run(debug=True, port=8000)