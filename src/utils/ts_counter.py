"""This module provides a global timestamp counter"""

GLOBAL_TIMESTAMP = 0


def increment():
    global GLOBAL_TIMESTAMP
    GLOBAL_TIMESTAMP += 1


def get():
    return get_timestamp()


def get_timestamp():
    return GLOBAL_TIMESTAMP
