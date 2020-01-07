#!/usr/bin/python

import sys
from authn import add_new_user


def add_user():
    try:
        new_username = input("Please enter the username for your new user: ")
        new_password = input("Please enter the password for " + new_username + " that you would like to set: ")
        add_new_user(username=new_username, password=new_password)
        print(new_username + " has been successfully added with the password " + new_password)
    except:
        print("there was an issue!")

if __name__ == "__main__":
    add_user()