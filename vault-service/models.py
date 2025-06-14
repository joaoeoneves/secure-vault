from database import db
from crypto import decrypt

class BaseEntry(db.Model):
    __tablename__ = 'entries'
    id       = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer, nullable=False)
    type     = db.Column(db.String(50), nullable=False)
    title    = db.Column(db.String(100), nullable=False)
    data     = db.Column(db.JSON, nullable=False)

    def to_dict(self):
        out = {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
        }
        out.update(decrypt(self.data))
        return out
