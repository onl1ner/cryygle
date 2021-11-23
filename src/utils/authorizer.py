import jwt

from hashlib import sha256
from datetime import datetime, timedelta

from flask import current_app

from models.user import User

class Authorizer:
    def __generate_token(self, user_id):
        payload = {
            'id':  user_id,
            'exp': datetime.utcnow() + timedelta(minutes = 30)
        }

        secret_key = current_app.config['SECRET_KEY']
        
        return jwt.encode(
            payload   = payload, 
            key       = secret_key,
            algorithm = 'HS256'
        )

    def __register(self, login, password):
        user = User(
            login    = login,
            password = sha256(password.encode()).hexdigest()
        )
        
        user.sync()

        return {
            'user':  user,
            'token': self.__generate_token(user.id)
        }

    def __login(self, user, password):
        pass_hash = sha256(password.encode()).hexdigest()

        if user.password == pass_hash:
            return {
                'user':  user,
                'token': self.__generate_token(user.id)
            }

        return None

    def auth(self, login, password):
        user = User.query.filter_by(login = login).first()

        if user:
            return self.__login(user, password)
        
        return self.__register(login, password)

    pass