from flask import request
from flask_restplus import Namespace, Resource, marshal
from users.models import user_request, user, user_base
from users.service import UserService
from run import api
from common.models import auth_parser
from utils.decorator import token_required, admin_token_required

from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jwt_identity,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies, jwt_refresh_token_required,
    get_jti, get_raw_jwt, jwt_required)

from utils.decorator import token_required

jwt = JWTManager()

users_ns = Namespace('users', description='User Management')
user_service = UserService()


@users_ns.expect(auth_parser)
@users_ns.route('')
class Users(Resource):
    '''
        Add Users
    '''
    @token_required
    @jwt_required
    @admin_token_required
    @users_ns.expect(user_request)
    def post(self):
        """
        Create User use api
        :return:
        """
        try:
            payload = marshal(api.payload, user_request)

            record = user_service.signup(payload)
            if record['code'] == 0:
                return {'status': 0, 'description': record['msg'], 'status_code': 400}
            else:
                return {'status': 1, 'description': "User create Successfully", 'id': record, 'status_code': 200}
        except Exception as err:
            print(err)
            return err


@users_ns.expect(auth_parser)
@users_ns.route('/activate/<string:id>')
class UserActivate(Resource):
    """
    Activate User
    """

    @token_required
    @jwt_required
    @admin_token_required
    def post(self, id):
        """
        Activate the User
        :param id:
        :return:
        """
        record = user_service.activate(id)
        if record['code'] == 0:
            return {'status': 0, 'description': record['msg'], 'status_code': 400}
        else:
            return {'status': 1, 'description': "User Activated Successfully", 'status_code': 200}
