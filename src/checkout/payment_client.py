import time


class PaymentGatewayTimeout(Exception):
    pass


TIMEOUT_MS = 5000


def charge(order_id, amount, gateway):
    start = time.monotonic()
    response = gateway.send(order_id, amount, timeout=TIMEOUT_MS / 1000)
    if response is None:
        raise PaymentGatewayTimeout(
            "payment provider did not respond within 5000ms"
        )
    return response
