TIME_TO_SLEEP = 100  # 100 frame (10 s) to sleep

WAKEUP_TIMESTAMP = -1 - TIME_TO_SLEEP
WAKEUP_STATUS = False


def check_wakeup_status(current_time: int) -> bool:
    global WAKEUP_STATUS

    if current_time - WAKEUP_TIMESTAMP > TIME_TO_SLEEP:
        WAKEUP_STATUS = False

    return WAKEUP_STATUS


def wakeup(current_time: int):
    global WAKEUP_STATUS, WAKEUP_TIMESTAMP
    WAKEUP_STATUS = True
    WAKEUP_TIMESTAMP = current_time
