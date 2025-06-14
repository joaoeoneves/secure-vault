from checker.base import Checker, HealthCheckResult
from datetime import datetime
from calendar import monthrange

class CardExpiryChecker(Checker):
    def check(self, payload):
        entry = payload.get("entry", payload)
        if entry.get("type") != "credit_card":
            return HealthCheckResult()

        data = entry.get("data") or {}
        expiry = (
            data.get("expiry_date")
            or data.get("validade")
            or entry.get("expiry_date")
        )
        if not expiry:
            return HealthCheckResult("red", "Validade não fornecida")

        try:
            m, y = expiry.split("/")
            month = int(m)
            year  = int(y) + (2000 if len(y) == 2 else 0)
            last_day = monthrange(year, month)[1]
            exp_date = datetime(year, month, last_day)
        except Exception:
            return HealthCheckResult("yellow", "Formato de validade inválido (MM/AA)")

        if exp_date < datetime.now():
            return HealthCheckResult("red", "Cartão expirado")
        return HealthCheckResult()
