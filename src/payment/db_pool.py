class ConnectionPoolExhausted(Exception):
    pass


class Pool:
    def __init__(self, size):
        self.size = size
        self.in_use = 0

    def get(self):
        if self.in_use >= self.size:
            raise ConnectionPoolExhausted(
                "no database connections available in pool"
            )
        self.in_use += 1
        return object()
