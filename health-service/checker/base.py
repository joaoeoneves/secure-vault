# Define o resultado de um health-check e a interface base para todos os checkers.

class HealthCheckResult:
    def __init__(self, status="green", reason="Tudo ok"):
        self.status = status
        self.reason = reason

    def to_dict(self):
        return {"status": self.status, "reason": self.reason}

# Classe base para todos os checkers (Chain of Responsibility).
class Checker:
    def __init__(self):
        self.next_checker = None

    # Permite encadear checkers.
    def set_next(self, checker):
        self.next_checker = checker
        return checker

    # Executa o check atual e, se passar, chama o próximo checker.
    def handle(self, payload):
        result = self.check(payload)
        if result.status != "green":
            return result.to_dict()
        if self.next_checker:
            return self.next_checker.handle(payload)
        return HealthCheckResult().to_dict()

    # Método a ser implementado por cada checker concreto.
    def check(self, payload):
        raise NotImplementedError
