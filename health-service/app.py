from flask import Flask
from routes import health_bp

# Criação da aplicação Flask e registo do blueprint das rotas de health-check.
def create_app():
    app = Flask(__name__)
    app.register_blueprint(health_bp)
    return app

# Ponto de entrada da aplicação.
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5003)
