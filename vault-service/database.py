from flask_sqlalchemy import SQLAlchemy

class Database:
    _db = None

    @classmethod
    def get_db(cls):
        if cls._db is None:
            cls._db = SQLAlchemy()
        return cls._db

    @classmethod
    def init_app(cls, app):
        cls.get_db().init_app(app)
