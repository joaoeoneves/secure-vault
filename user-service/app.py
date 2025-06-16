import os
from flask import Flask, g, request
from flask_migrate import Migrate
from flask_login import login_user
from flask_login import LoginManager
from flask.sessions import SecureCookieSessionInterface
from models import db, Utilizador
from routes import utilizador_bp

# Função de fábrica para criar a aplicação Flask.
# Centraliza a configuração, inicialização da base de dados e autenticação.
def create_app():
    app = Flask(__name__)
    # Configuração da app e base de dados
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'superSecretKey')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'database', 'utilizador.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    # Configuração do Flask-Login para gestão de sessões de utilizador
    login_manager = LoginManager(app)
    login_manager.login_view = 'utilizador_api.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Utilizador.query.get(int(user_id))

    # Permite autenticação via header (API key)
    class CustomSessionInterface(SecureCookieSessionInterface):
        def save_session(self, *args, **kwargs):
            if g.get('login_via_header'):
                return
            return super().save_session(*args, **kwargs)

    app.session_interface = CustomSessionInterface()

    @app.before_request
    def before_request():
        # Permite autenticação automática via API key no header
        api_key = request.headers.get('Authorization')
        if api_key:
            user = Utilizador.query.filter_by(api_key=api_key).first()
            if user:
                g.login_via_header = True
                login_user(user)

    # Regista o blueprint das rotas de utilizador
    app.register_blueprint(utilizador_bp)
    return app

# Ponto de entrada da aplicação
if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5001)
