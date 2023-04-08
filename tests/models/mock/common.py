import random
from datetime import datetime, timedelta


def mock_date():
    return datetime(
        year=random.randint(2015, datetime.now().year - 1),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
        hour=random.randint(1, 23),
        minute=random.randint(1, 59),
        second=random.randint(1, 59),
    )


def mock_timestamp():
    return int(mock_date().timestamp())


def mock_date_later_than(dt: datetime):
    return dt + timedelta(milliseconds=random.randint(1000, 5000))


def mock_timestamp_later_than(timestamp: int):
    return timestamp + random.randint(1000, 5000)
