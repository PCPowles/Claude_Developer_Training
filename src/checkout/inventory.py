class InventoryLockError(Exception):
    pass


def reserve(sku, qty, lock_service):
    if not lock_service.acquire(sku, wait_seconds=2):
        raise InventoryLockError("could not acquire inventory lock for SKU")
    return lock_service.decrement(sku, qty)
