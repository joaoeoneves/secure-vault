import os
from flask import Flask
from flask_migrate import Migrate
from database import db
from routes import vault_bp

# Função de fábrica para criar a aplicação Flask.
# Centraliza configuração, inicialização da base de dados e registo das rotas.
def create_app():
    app = Flask(__name__)
    app.config.update({
        'SECRET_KEY': os.getenv('SECRET_KEY', 'superSecretKey'),
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + os.path.join(os.getcwd(), 'database', 'vault.db'),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    db.init_app(app)
    Migrate(app, db)

    # Garante que a pasta da base de dados existe
    os.makedirs('database', exist_ok=True)
    with app.app_context():
        db.create_all()

    # Regista o blueprint das rotas da API do vault
    app.register_blueprint(vault_bp)
    return app

# Ponto de entrada da aplicação
if __name__ == "__main__":
    create_app().run(host='0.0.0.0', port=5002)
