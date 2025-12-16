"""Utility for single instance application lock."""

import sys
from core.single_instance import SingleInstance


def acquire_single_instance():
    instance_lock = SingleInstance()
    if not instance_lock.acquire():
        sys.exit(0)
    return instance_lock


def release_single_instance(instance_lock):
    if instance_lock:
        instance_lock.release()
