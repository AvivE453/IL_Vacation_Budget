# Sanity checks that the app's queries execute and return the expected shape
# against the migrated + seeded dev database. These skip automatically if the
# database isn't reachable (see conftest.py) -- they are not a substitute for
# having real collected data, just a guard against broken SQL/schema drift.

from app.queries import (
    count_active_destinations,
    get_collection_volume,
    get_data_quality_report,
    list_origin_airports,
)


def test_list_origin_airports_includes_tlv(cur):
    rows = list_origin_airports(cur)
    codes = [r["iata_code"] for r in rows]
    assert "TLV" in codes


def test_count_active_destinations_nonzero(cur):
    assert count_active_destinations(cur) > 0


def test_data_quality_report_shape(cur):
    rows = get_data_quality_report(cur)
    assert len(rows) > 0
    row = rows[0]
    assert "flight_obs_count" in row
    assert "hotel_sample_size" in row


def test_collection_volume_runs_without_error(cur):
    rows = get_collection_volume(cur)
    assert isinstance(rows, list)
