from checker.base import Checker, HealthCheckResult
import string

class PasswordWeaknessChecker(Checker):
    def check(self, payload):
        entry = payload.get("entry", payload)
        if entry.get("type") != "password":
            return HealthCheckResult()

        data = entry.get("data") or {}
        pw = data.get("password") or entry.get("password", "")

        if len(pw) < 8:
            return HealthCheckResult("red", "Password muito curta")

        categorias = [
            any(c.islower()     for c in pw),
            any(c.isupper()     for c in pw),
            any(c.isdigit()     for c in pw),
            any(c in string.punctuation for c in pw)
        ]
        if sum(categorias) < 3:
            return HealthCheckResult("yellow", "Password fraca (falta variedade)")

        return HealthCheckResult()
