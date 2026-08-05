from datetime import datetime


def delay_hours(expected: datetime, actual: datetime) -> float:
    delta = actual - expected
    return round(delta.total_seconds() / 3600, 2)


def delivery_status_from_times(expected: datetime, actual: datetime) -> tuple[str, float, int]:
    hours = delay_hours(expected, actual)
    delay_days = max(int(hours // 24), 0)

    if hours < 0:
        status = "Delivered Early"
    elif hours <= 1:
        status = "Delivered On Time"
    elif hours <= 3:
        status = "Delayed 1-3 Hours"
    elif hours <= 5:
        status = "Delayed 3-5 Hours"
    elif hours <= 10:
        status = "Delayed 5-10 Hours"
    elif hours <= 24:
        status = "Delayed 10-24 Hours"
    else:
        status = "Delayed Over 1 Day"

    return status, hours, delay_days
