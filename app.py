from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import redis, bcrypt

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello I think you are already logged in!"


@app.route('/login', methods=['POST'])
def check_existing_password(username=None, password=None):
    """
    This function checks the passwords entered with the password in the Redis Database.
    :param username: The username that comes from the form field of your choice.
    :param password: The passwords that comes from the form field of your choice.
    :return: Returns if the passwords match or not
    """
password = request.form['password'].encode("utf-8")
username = request.form['username']
stored_password = r.hget("user:" + username, "password")
compare_password = bcrypt.hashpw(password, stored_password)
try:
    if bcrypt.checkpw(password, stored_password) == True:
        flash("Passwords Match! We will let you in")
        session['logged_in'] = True
    else:
        flash("The username and password combo you entered do not exist")
except:
    flash("This developer was lazy and didn't try to define errors. This was only a demo.")

@app.route('/newuser', methods=['POST'])
def enter_new_password(username=None, password=None):
    """
    This function imports a new password into the Redis Database in a hashed and salted format according to OWASP best practices.
    This calls for bcrypt to have 12 rounds when used for salting.
    """
    password = request.form['newpassword']
    username = request.form['newusername']
    #create a salt with OWASP password storage cheat sheet best practices.
    usersalt = bcrypt.gensalt(12)
    #generate hashed password with salt
    hashed_password = bcrypt.hashpw(password, usersalt)
    r.hset("user:" + username, "password", hashed_password)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
