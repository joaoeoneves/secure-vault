from flask import Blueprint, request, jsonify
from checker.password_weak import PasswordWeaknessChecker
from checker.password_reuse import PasswordReuseChecker
from checker.card_expiry import CardExpiryChecker

health_bp = Blueprint("health_api", __name__, url_prefix="/api/health")

# Configura a cadeia: weak → reuse → card
weak  = PasswordWeaknessChecker()
reuse = PasswordReuseChecker()
card  = CardExpiryChecker()

weak.set_next(reuse).set_next(card)

@health_bp.route("/check", methods=["POST"])
def check_health():
    payload = request.get_json()  # pode ser flat ou com {"entry", "all_entries"}
    result = weak.handle(payload)
    return jsonify(result)
