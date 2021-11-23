import jwt
from flask import request, current_app

from models.user import User

def token_required(func):
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        
        if not token:
            return '<h1>No token was provided</h1>'
        
        try:
            data = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
            current_user = User.query.filter_by(id = data['id']).first()
        except:
            return '<h1>Wrong credentials</h1>'
        
        return func(current_user, *args, **kwargs)
  
    return decorated