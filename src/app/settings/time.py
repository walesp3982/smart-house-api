from datetime import datetime, timezone


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def normalize(dt: datetime) -> datetime:
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt
