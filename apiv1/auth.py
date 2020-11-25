from flask import jsonify
from flask_restplus import Resource, Namespace, fields
from common.models import auth_parser
from models import User
from run import app, redis_store
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, get_jwt_identity,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies, jwt_refresh_token_required,
    get_jti, get_raw_jwt)

from utils.decorator import token_required

jwt = JWTManager()

authapi = Namespace('auth', description='Authorization API Compensar')

creds = authapi.model('Credentials', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

user = User()


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    if not User.objects(username__exact=identity):
        return None

    return User.objects(username__exact=identity).get()


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return jsonify(ret), 404


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'user': user}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


# @authapi.route('/registration')
# @api.doc(False)
class UserRegistration(Resource):
    @authapi.expect(creds)
    def post(self):
        data = authapi.payload

        try:
            user.username = data['username']
            user.password = user.generate_hash(data['password'])
            user.save()

            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)

            resp = jsonify({
                'message': 'User {} was created'.format(data['username'])
            })

            return resp
        except Exception as e:
            if "E11000 duplicate key error collection" in e.args[0]:
                return {'message': 'User {} already exists'.format(data['username'])}
            else:
                return {'message': 'Oops'}


@authapi.route('/login')
class UserLogin(Resource):
    @authapi.expect(creds)
    def post(self):
        data = authapi.payload
        try:
            current_user = User.objects(username__exact=data['username'])

        except Exception as err:
            print(err.args[0])
            return {'message': '{}'.format(err.args[0])}

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if user.verify_hash(data['password'], current_user.get().password):
            access_token = create_access_token(identity=current_user)
            refresh_token = create_refresh_token(identity=current_user)
            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)
            redis_store.set(access_jti, 'false',
                            app.config['JWT_ACCESS_TOKEN_EXPIRES'])
            redis_store.set(refresh_jti, 'false',
                            app.config['JWT_REFRESH_TOKEN_EXPIRES'])

            resp = jsonify({
                'message': 'Logged in as {}'.format(current_user.get().username),
                'access_token': access_token,
                'refresh_token': refresh_token
            })

            return resp

        else:
            return {'message': 'Wrong credentials'}


@authapi.route('/logout')
class UserLogout(Resource):
    def post(self):
        try:
            if not get_raw_jwt():
                response_object = {
                    'status': 'fail',
                    'message': 'Not logged in'
                }
                return response_object, 401
            else:
                resp = jsonify({'logout': True})
                jti = get_raw_jwt()['jti']
                ttl = redis_store.ttl(jti)
                redis_store.set(jti, 'true', ttl)

                return resp

            return {'message': "Successfully logged out"}, 200
        except:
            return jsonify({'error': 'Something went wrong deleting token'})


@authapi.expect(auth_parser)
@authapi.route('/token/refresh')
class TokenRefresh(Resource):
    @token_required
    @jwt_refresh_token_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user)
            refresh_token = create_refresh_token(identity=current_user)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        except:
            return jsonify({'error': 'Something went wrong refreshing token'})
