import os
from flask import Flask, g, request
from flask_migrate import Migrate
from flask_login import login_user
from flask_login import LoginManager
from flask.sessions import SecureCookieSessionInterface
from models import db, Utilizador
from routes import utilizador_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'muda_isto_para_prod')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'database', 'utilizador.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa DB e migrações
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    # Configura LoginManager
    login_manager = LoginManager(app)
    login_manager.login_view = 'utilizador_api.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Utilizador.query.get(int(user_id))

    # Evita guardar sessão cookie quando se autentica via API-Key
    class CustomSessionInterface(SecureCookieSessionInterface):
        def save_session(self, *args, **kwargs):
            if g.get('login_via_header'):
                return
            return super().save_session(*args, **kwargs)

    app.session_interface = CustomSessionInterface()

    # Autentica antes de cada request via header Authorization
    @app.before_request
    def before_request():
        api_key = request.headers.get('Authorization')
        if api_key:
            user = Utilizador.query.filter_by(api_key=api_key).first()
            if user:
                # indica que não queremos guardar sessão cookie
                g.login_via_header = True
                # faz o login com a função pública
                login_user(user)

    app.register_blueprint(utilizador_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5001)
