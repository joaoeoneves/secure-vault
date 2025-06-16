from checker.base import Checker, HealthCheckResult

# Checker que verifica se a password está a ser reutilizada noutras entradas.
class PasswordReuseChecker(Checker):
    def check(self, payload):
        entry_list = payload.get("all_entries", [])
        entry      = payload.get("entry", payload)

        if entry.get("type") != "password":
            return HealthCheckResult()

        pw = entry.get("password") or entry.get("data", {}).get("password") or ""
        if not pw:
            return HealthCheckResult("yellow", "Password vazia")

        count = sum(
            1 for e in entry_list
            if (e.get("password") or e.get("data", {}).get("password") or "") == pw
        )
        if count > 1:
            return HealthCheckResult("yellow", "Password reutilizada")
        return HealthCheckResult()
