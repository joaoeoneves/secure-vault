import os
from flask import Flask
from flask_migrate import Migrate
from database import Database
from routes import vault_bp

def create_app():
    app = Flask(__name__)
    app.config.update({
      'SECRET_KEY': os.getenv('SECRET_KEY', 'muda_isto'),
      'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + os.path.join(os.getcwd(),'database','vault.db'),
      'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    Database.init_app(app)
    db = Database.get_db()
    Migrate(app, db)

    os.makedirs('database', exist_ok=True)
    with app.app_context():
        db.create_all()

    app.register_blueprint(vault_bp)
    return app

if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port=5002)
