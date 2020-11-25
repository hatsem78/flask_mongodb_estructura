from db_init import db
import os
import logging
from flask import Flask
from flask_jwt_extended import (
    JWTManager
)
from flask_restplus import Api
from pymongo import MongoClient
from flask_cors.core import LOG
from redis import StrictRedis

import config
from flask_script import Manager


app = Flask(__name__)
api = Api(app)
manager = Manager(app)

app.config.from_object(
    config.config_by_name[os.getenv('FLASK_ENVIRONMENT', 'dev')]())
app.logger.info("Config: %s" % 'development')


# Create MongoDB connection object using Mongo URI and instantiate DB (todo_inventory)
mongo_conn = MongoClient(app.config['MONGO_URI'])
mongo_db = mongo_conn[app.config['DB_NAME']]

# Create Logger object
FORMAT = '%(asctime)s %(module)s %(funcName)s %(message)s'
logging.basicConfig(filename="app.log",
                    format=FORMAT,
                    filemode='w')
logger = logging.getLogger()

jwt = JWTManager(app)
blacklist = set()
# Redis DB object
redis_store = StrictRedis(host=app.config['REDIS_HOST'],
                          port=app.config['REDIS_PORT'],
                          db=app.config['REDIS_DB'],
                          decode_responses=True)
# MongoEngine

app.db = db
app.db.init_app(app)

app.config['PROPAGATE_EXCEPTIONS'] = True


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@api.errorhandler(Exception)
def handle_error(e):
    code = e.code
    message = e.__str__
    return {"status": code, "message": message}, code
