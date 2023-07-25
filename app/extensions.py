from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
import redis

_api = Api()
db = SQLAlchemy()
red = redis.Redis(host='localhost', port=6379)