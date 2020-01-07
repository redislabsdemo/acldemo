#!/usr/bin/python

import redis, bcrypt

r = redis.Redis(host='52.41.87.175', port=6379, db=0)

def check_existing_password(username = None , password = None):
    utf8password = password.encode('utf8')
    stored_password = r.get("secret:" + username + ":password")
    compare_password = bcrypt.hashpw(utf8password, stored_password)
    try:
        if bcrypt.checkpw(utf8password, stored_password) == True:
            print("You are allowed in! Lucky password Guess ;)")
        else:
            print("The username and password combo you entered do not exist")
    except:   #Ignore obvious pep8 issues
        print("An error occured, please try again.")

def add_new_user(username = None , password = None):
    usersalt = bcrypt.gensalt(12)
    utf8password = password.encode('utf8')
    hashed_password = bcrypt.hashpw(utf8password, usersalt)
    try:
        r.set("secret:" + username + ":password", hashed_password)
        print('The user ' + username + " has been added")
    except:  #Ignore obvious pep8 issues
        print("An error occured, please try again.")