from utils.database import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)

    login    = db.Column(db.String())
    password = db.Column(db.String())

    def sync(self):
        record = User.query.filter_by(login = self.login).first()

        if record: return

        db.session.add(self)
        db.session.commit()
    
        pass
    