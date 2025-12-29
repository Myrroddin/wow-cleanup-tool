"""Utility for single instance application lock."""

import sys
from core.single_instance import SingleInstance


# Reuse a single lock object per process to avoid duplicate acquisitions
_GLOBAL_INSTANCE_LOCK = None


def acquire_single_instance():
    global _GLOBAL_INSTANCE_LOCK
    # If already acquired in this process, reuse the existing lock
    if _GLOBAL_INSTANCE_LOCK and getattr(_GLOBAL_INSTANCE_LOCK, "locked", False):
        return _GLOBAL_INSTANCE_LOCK

    instance_lock = SingleInstance()
    if not instance_lock.acquire():
        sys.exit(0)
    _GLOBAL_INSTANCE_LOCK = instance_lock
    return instance_lock


def release_single_instance(instance_lock):
    global _GLOBAL_INSTANCE_LOCK
    if instance_lock:
        instance_lock.release()
        if _GLOBAL_INSTANCE_LOCK is instance_lock:
            _GLOBAL_INSTANCE_LOCK = None
