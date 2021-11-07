import hashlib

from utils.database import db

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.String(), primary_key=True)

    url = db.Column(db.String())

    heading = db.Column(db.String())
    paragraph = db.Column(db.String())

    def __init__(self, url, heading, paragraph):
        self.id = hashlib.sha256(url.encode()).hexdigest()

        self.url = url

        self.heading = heading
        self.paragraph = paragraph

    def sync(self):
        record = News.query.filter_by(id = self.id).first()

        if record: return

        db.session.add(self)
        db.session.commit()
        
        pass