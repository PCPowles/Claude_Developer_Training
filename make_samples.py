# make_samples.py - creates sample logs and source code for supervisor.py
from pathlib import Path

FILES = {
    # ---------- LOGS ----------
    "logs/checkout-service.log": """\
2026-10-12T01:45:02Z INFO  checkout-service started version=4.2.0
2026-10-12T01:52:10Z INFO  checkout-service order=A1001 status=completed amount=59.99
2026-10-12T01:58:30Z INFO  deploy-agent applied config change config/payment.yaml (db_pool_size 20 -> 5)
2026-10-12T02:01:15Z INFO  checkout-service order=A1002 status=completed amount=12.50
2026-10-12T02:07:14Z ERROR checkout-service order=A1003 PaymentGatewayTimeout: payment provider did not respond within 5000ms
2026-10-12T02:09:41Z ERROR checkout-service order=A1004 PaymentGatewayTimeout: payment provider did not respond within 5000ms
2026-10-12T02:11:03Z WARN  checkout-service order=A1005 retrying payment attempt=2
2026-10-12T02:11:08Z ERROR checkout-service order=A1005 PaymentGatewayTimeout: payment provider did not respond within 5000ms
2026-10-12T02:15:22Z ERROR checkout-service order=A1006 InventoryLockError: could not acquire inventory lock for SKU
2026-10-12T02:18:47Z ERROR checkout-service order=A1007 PaymentGatewayTimeout: payment provider did not respond within 5000ms
2026-10-12T02:24:09Z INFO  checkout-service order=A1008 status=completed amount=33.00
2026-10-12T02:26:55Z ERROR checkout-service order=A1009 PaymentGatewayTimeout: payment provider did not respond within 5000ms
2026-10-12T02:31:30Z ERROR checkout-service order=A1010 InventoryLockError: could not acquire inventory lock for SKU
2026-10-12T02:35:12Z ERROR checkout-service order=A1011 PaymentGatewayTimeout: payment provider did not respond within 5000ms
2026-10-12T02:41:58Z ERROR checkout-service order=A1012 PaymentGatewayTimeout: payment provider did not respond within 5000ms
2026-10-12T02:44:20Z INFO  deploy-agent rolled back config/payment.yaml (db_pool_size 5 -> 20)
2026-10-12T02:47:03Z INFO  checkout-service order=A1013 status=completed amount=74.25
2026-10-12T02:55:40Z INFO  checkout-service order=A1014 status=completed amount=8.99
2026-10-12T03:12:16Z ERROR checkout-service order=A1015 AddressValidationError: postal code format not recognised
""",
    "logs/payment-service.log": """\
2026-10-12T01:45:00Z INFO  payment-service started pool_size=20
2026-10-12T01:58:35Z INFO  payment-service reloaded config pool_size=5
2026-10-12T02:05:51Z ERROR payment-service ConnectionPoolExhausted: no database connections available in pool
2026-10-12T02:09:30Z ERROR payment-service ConnectionPoolExhausted: no database connections available in pool
2026-10-12T02:18:40Z ERROR payment-service ConnectionPoolExhausted: no database connections available in pool
2026-10-12T02:26:49Z ERROR payment-service ConnectionPoolExhausted: no database connections available in pool
2026-10-12T02:41:50Z ERROR payment-service ConnectionPoolExhausted: no database connections available in pool
2026-10-12T02:44:25Z INFO  payment-service reloaded config pool_size=20
""",
    # ---------- SOURCE CODE ----------
    "src/checkout/payment_client.py": """\
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
""",
    "src/checkout/inventory.py": """\
class InventoryLockError(Exception):
    pass


def reserve(sku, qty, lock_service):
    if not lock_service.acquire(sku, wait_seconds=2):
        raise InventoryLockError("could not acquire inventory lock for SKU")
    return lock_service.decrement(sku, qty)
""",
    "src/payment/db_pool.py": """\
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
""",
    "src/checkout/address.py": """\
import re


class AddressValidationError(Exception):
    pass


def validate_postal_code(code):
    if not re.fullmatch(r"\\d{5}(-\\d{4})?", code):
        raise AddressValidationError("postal code format not recognised")
    return code
""",
    # ---------- CONFIG ----------
    "config/payment.yaml": """\
# Payment service settings
db_pool_size: 20
gateway_timeout_ms: 5000
""",
}

for path, content in FILES.items():
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"created {p}")

print("Done. Sample files are ready.")