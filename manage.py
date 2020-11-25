import json

from flask import logging

from db_init import FlaskDocument
from models import User
from run import manager, api
import getpass
import re
import sys


@manager.command
def hello():
    print("hello")


@manager.command
def createusers():
    CreateUser().run()


@manager.command
def createsuperuser():
    CreateSuperUser().run()


@manager.command
def postmanCollection():
    Postman().run()


class ResetDB:
    """Drops all tables and recreates them"""

    def run(self):
        self.drop_collections()

    def drop_collections(self):
        for klass in FlaskDocument.all_subclasses():
            klass.drop_collection()


class CreateSuperUser:
    """Fills in predefined data to DB"""

    def run(self):
        try:
            self.create_users()
        except Exception as e:
            print(e)

    @staticmethod
    def create_users():
        users = []
        users = []
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

        print('Create user: ')
        email = input('User E-Mail: ')
        email_confirm = input('Confirm E-Mail: ')

        if not email == email_confirm:
            sys.exit('\nCould not create user: E-Mail did not match')

        if not EMAIL_REGEX.match(email):
            sys.exit('\nCould not create user: Invalid E-Mail addresss')

        password = getpass.getpass('User password: ')
        password_confirm = getpass.getpass('Confirmed password: ')

        if not password == password_confirm:
            sys.exit('\nCould not create user: Passwords did not match')

        user_name = input('User Name: ')
        user_last_name = input('User LastName: ')
        user = User(
            username=user_name,
            email=email,
            password=User().generate_hash(password),
            active=True,
            firstname=user_name,
            lastname=user_last_name,
            is_admin=True
        )
        users.append(user)

        User.objects.insert(users)
        print('User Admin added.')


class CreateUser:
    """Fills in predefined data to DB"""

    def run(self):
        try:
            self.creates()
        except Exception as e:
            print(e)

    @staticmethod
    def creates():
        users = []
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

        print('Create user: ')
        email = input('User E-Mail: ')
        email_confirm = input('Confirm E-Mail: ')

        if not email == email_confirm:
            sys.exit('\nCould not create user: E-Mail did not match')

        if not EMAIL_REGEX.match(email):
            sys.exit('\nCould not create user: Invalid E-Mail addresss')

        password = getpass.getpass('User password: ')
        password_confirm = getpass.getpass('Confirmed password: ')

        if not password == password_confirm:
            sys.exit('\nCould not create user: Passwords did not match')

        user_name = input('User Name: ')
        user_last_name = input('User LastName: ')

        user = User(
            username=user_name,
            email=email,
            password=User().generate_hash(password),
            active=True,
            firstname=user_name,
            lastname=user_last_name,
            is_admin=False
        )

        User.objects.insert(user)

        print('User added.')


class Postman:
    def run(self):
        self.getPostmanCollection()

    def getPostmanCollection(self):
        data = api.as_postman(urlvars=False, swagger=True)
        print(json.dumps(data))


if __name__ == "__main__":
    manager.run()
