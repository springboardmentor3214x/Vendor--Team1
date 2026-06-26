from datetime import datetime


def days_between(start, end):
    if not start or not end:
        return 0
    return (end - start).days


def is_late(expected, actual):
    if not expected or not actual:
        return False
    return actual > expected


def safe_filename(name):
    keep = [c for c in name if c.isalnum() or c in "._- "]
    return "".join(keep).strip().replace(" ", "_")


def percentage(part, whole):
    if not whole:
        return 0.0
    return round((part / whole) * 100, 2)
