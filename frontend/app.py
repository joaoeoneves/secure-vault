from flask import Flask
from flask_bootstrap import Bootstrap
from routes import blueprint

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'superSecretKey'
app.config['WTF_CSRF_SECRET_KEY'] = 'superSecretKey'

app.register_blueprint(blueprint)
Bootstrap(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
