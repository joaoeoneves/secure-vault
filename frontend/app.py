from flask import Flask
from flask_bootstrap import Bootstrap
from routes import blueprint

# Criação da aplicação Flask principal do frontend.
# Usa Bootstrap para facilitar o design dos formulários e páginas.
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'superSecretKey'
app.config['WTF_CSRF_SECRET_KEY'] = 'superSecretKey'

# Regista o blueprint com todas as rotas da interface web.
app.register_blueprint(blueprint)
Bootstrap(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
