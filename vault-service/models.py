from database import Database
from sqlalchemy.dialects.sqlite import JSON

db = Database.get_db()

class BaseEntry(db.Model):
    __tablename__ = 'entries'
    id       = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, nullable=False)
    type     = db.Column(db.String(50), nullable=False)
    title    = db.Column(db.String(100), nullable=False)
    data     = db.Column(JSON, nullable=False)

    def to_dict(self):
        out = {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
        }
        out.update(self.data)
        return out
