import random

from datetime import datetime, timedelta


def to_chrome_timestamp(dt):
    """Chuyển đổi đối tượng datetime sang WebKit/Chrome timestamp."""
    # Kỷ nguyên của Chrome là 1601-01-01
    epoch_start = datetime(1601, 1, 1)
    # Tính toán sự chênh lệch
    delta = dt - epoch_start
    # Chuyển đổi sang micro giây
    return int(delta.total_seconds() * 1_000_000)


def generate_time():
    timestamp = datetime.now() - timedelta(
        days=random.randint(0, 10),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    return to_chrome_timestamp(timestamp)

