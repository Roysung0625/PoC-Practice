"""Maintain the dedicated GardenWorld registration index and its durable queue."""
import argparse
import json
import logging
import threading

from poc.config import environment


def drain(store, intelligence, limit=10):
    jobs = store.pending(limit=limit)
    indexed = 0
    for job in jobs:
        product_id = job["product_id"]
        lease = job["lease_token"]
        try:
            rows = store.eligible([product_id])
            if not rows:
                raise ValueError("PRODUCT_INELIGIBLE")
            intelligence.index_product(rows[0])
        except Exception:
            # No raw SDK/network exception can reach the audit table or browser.
            store.mark_index_failed(product_id, "INDEX_DEFERRED", lease)
        else:
            if store.mark_indexed(product_id, lease):
                indexed += 1
    return {"claimed": len(jobs), "indexed": indexed}


class IndexWorker:
    def __init__(self, store, provider):
        self.store = store
        self.provider = provider
        self.wake = threading.Event()
        self.stop = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True, name="registration-index")

    def _run(self):
        while not self.stop.is_set():
            self.wake.wait(30)
            self.wake.clear()
            if self.stop.is_set():
                return
            try:
                drain(self.store, self.provider(), limit=5)
            except Exception:
                logging.getLogger(__name__).warning("Registration index queue unavailable")

    def close(self):
        self.stop.set()
        self.wake.set()
        self.thread.join(timeout=3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("sync", "retry"))
    args = parser.parse_args()
    environment()
    from .intelligence import RegistrationIntelligence
    from .store import RegistrationStore
    intelligence, store = RegistrationIntelligence(), RegistrationStore()
    if args.action == "sync":
        intelligence.ensure_index()
        report = intelligence.sync_index(store)
    else:
        report = drain(store, intelligence, limit=100)
    print(json.dumps(report, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
