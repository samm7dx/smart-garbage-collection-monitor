import datetime
from types import SimpleNamespace

from app import models
from app.status_utils import compute_collection_status


def test_compute_collection_status_marks_on_time_when_actual_within_grace():
    record = SimpleNamespace(
        scheduled_date=datetime.datetime(2026, 1, 1, 9, 0),
        scheduled_time="09:00",
        actual_collection_date=datetime.datetime(2026, 1, 1, 9, 20),
        actual_collection_time="09:20",
    )

    status, delay_minutes = compute_collection_status(record)

    assert status == models.CollectionStatus.ON_TIME
    assert delay_minutes == 20


def test_compute_collection_status_marks_delayed_when_actual_over_grace():
    record = SimpleNamespace(
        scheduled_date=datetime.datetime(2026, 1, 1, 9, 0),
        scheduled_time="09:00",
        actual_collection_date=datetime.datetime(2026, 1, 1, 10, 5),
        actual_collection_time="10:05",
    )

    status, delay_minutes = compute_collection_status(record)

    assert status == models.CollectionStatus.DELAYED
    assert delay_minutes == 65


def test_compute_collection_status_marks_missed_when_not_collected_and_past_grace():
    record = SimpleNamespace(
        scheduled_date=datetime.datetime(2026, 1, 1, 9, 0),
        scheduled_time="09:00",
        actual_collection_date=None,
        actual_collection_time=None,
    )

    status, delay_minutes = compute_collection_status(record, now=datetime.datetime(2026, 1, 1, 10, 0))

    assert status == models.CollectionStatus.MISSED
    assert delay_minutes == 0
