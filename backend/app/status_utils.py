import datetime
from . import models

STATUS_GRACE_MINUTES = 30


def utcnow_naive() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


def compute_collection_status(record: models.CollectionRecord, now: datetime.datetime | None = None) -> tuple[str, int]:
    if now is None:
        now = utcnow_naive()

    scheduled_time = datetime.datetime.strptime(record.scheduled_time, "%H:%M").time()
    scheduled_datetime = datetime.datetime.combine(record.scheduled_date.date(), scheduled_time)

    if record.actual_collection_date and record.actual_collection_time:
        actual_time = datetime.datetime.strptime(record.actual_collection_time, "%H:%M").time()
        actual_datetime = datetime.datetime.combine(record.actual_collection_date.date(), actual_time)
        delay_minutes = max(0, int((actual_datetime - scheduled_datetime).total_seconds() / 60))
        status = models.CollectionStatus.ON_TIME if delay_minutes <= STATUS_GRACE_MINUTES else models.CollectionStatus.DELAYED
        return status, delay_minutes

    if now > scheduled_datetime + datetime.timedelta(minutes=STATUS_GRACE_MINUTES):
        return models.CollectionStatus.MISSED, 0
    return models.CollectionStatus.ON_TIME, 0


def refresh_collection_record(record: models.CollectionRecord, now: datetime.datetime | None = None) -> bool:
    status, delay_minutes = compute_collection_status(record, now=now)
    updated = False

    if record.status != status:
        record.status = status
        updated = True
    if record.delay_minutes != delay_minutes:
        record.delay_minutes = delay_minutes
        updated = True

    return updated


def get_bin_status_from_latest_collection(
    db_bin: models.GarbageBin, latest_collection: models.CollectionRecord | None
) -> str:
    if latest_collection:
        if latest_collection.status == models.CollectionStatus.MISSED:
            return models.BinStatus.MISSED
        if latest_collection.status == models.CollectionStatus.DELAYED:
            return models.BinStatus.DELAYED

    if db_bin.current_fill_percentage > 80:
        return models.BinStatus.OVERFLOW_RISK
    return models.BinStatus.NORMAL
