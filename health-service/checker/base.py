class HealthCheckResult:
    def __init__(self, status="green", reason="Tudo ok"):
        self.status = status
        self.reason = reason

    def to_dict(self):
        return {"status": self.status, "reason": self.reason}


class Checker:
    def __init__(self):
        self.next_checker = None

    def set_next(self, checker):
        self.next_checker = checker
        return checker

    def handle(self, payload):
        result = self.check(payload)
        if result.status != "green":
            return result.to_dict()
        if self.next_checker:
            return self.next_checker.handle(payload)
        return HealthCheckResult().to_dict()

    def check(self, payload):
        raise NotImplementedError
