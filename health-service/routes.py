from flask import Blueprint, request, jsonify
from checker.password_weak import PasswordWeaknessChecker
from checker.password_reuse import PasswordReuseChecker
from checker.card_expiry import CardExpiryChecker

# Blueprint para agrupar as rotas da API de health-check.
health_bp = Blueprint("health_api", __name__, url_prefix="/api/health")

# Instancia os checkers e encadeia-os (Chain of Responsibility).
weak  = PasswordWeaknessChecker()
reuse = PasswordReuseChecker()
card  = CardExpiryChecker()
weak.set_next(reuse).set_next(card)

# Endpoint principal: recebe um payload e executa a cadeia de checkers.
@health_bp.route("/check", methods=["POST"])
def check_health():
    payload = request.get_json()
    result = weak.handle(payload)
    return jsonify(result)
