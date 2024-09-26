from threading import Lock
import redis
from connections.db import redis_client
from contextlib import contextmanager

class SynchronizationService:
    def __init__(self):
        self.locks = {}

    def lock(self, key:str):
        if key not in self.locks:
            self.locks[key] = Lock()
        return self.locks[key]
    

class DistributedLockManager:
    def __init__(self, redis_url: str):
        self.redis = redis_client()

    @contextmanager
    def lock(self, key: str, timeout: int = 10):
        lock = self.redis.lock(f"lock:{key}", timeout=timeout)
        try:
            lock.acquire()
            yield
        finally:
            lock.release()

    def is_locked(self, key: str) -> bool:
        return self.redis.exists(f"lock:{key}")