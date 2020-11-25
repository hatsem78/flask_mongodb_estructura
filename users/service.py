from flask import abort
from bson import ObjectId
from passlib.hash import sha256_crypt
from utils.db_utils import Base
from utils.helper import custom_marshal
from models import User
import re

base_obj = Base()


class UserService(object):
    """
    Service Class for User View
    """

    def signup(self, payload):
        """
        signup function
        :return:
        """
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
        try:
            if not EMAIL_REGEX.match(payload.get('email')):
                return {'msg': "Could not create user: Invalid E-Mail addresss", 'code': 0}

            if payload.get('password') != payload.get('confirm_password'):
                return {'msg': "Password does not match", 'code': 0}
            records = User.objects(
                username__exact=payload.get('username'))

            #_id = base_obj.insert(COLLECTIONS['USERS'], payload)
            print(records)
            if records.count() > 0:
                return {'msg': 'Email ID Already Exists', 'code': 0}

            user = User(
                username=payload.get('username'),
                email=payload.get('email'),
                password=User().generate_hash(payload.get('password')),
                active=False,
                firstname=payload.get('firstname'),
                lastname=payload.get('lastname'),
                is_admin=False
            )

            _id = User.objects.insert(user).pk

            return {'msg': str(_id), 'code': 0}
        except Exception as err:
            print(err)
            return err

    def activate(self, id):
        """
            Activate the user
            :param id:
            :return:
        """
        try:
            #user = User.objects(_id=id).get()
            user = User.objects(
                _id__exact=id).get

            user.update(
                is_active=True,
            )

            return {'msg': "User updated!", 'code': 1}

        except Exception as err:
            return {'msg': err, 'code': 0}
