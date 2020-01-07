#!/usr/bin/python

import sys
from authn import check_existing_password


def check_user():
    try:
        new_username = input("Please enter the username for your new user: ")
        new_password = input("Please enter the password for " + new_username + " that you would like to set: ")
        check_existing_password(username=new_username, password=new_password)
    except:
        print("The username and password combination you have entered does not exist or an error occured")

if __name__ == "__main__":
    check_user()