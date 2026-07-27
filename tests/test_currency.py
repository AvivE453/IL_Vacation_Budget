import pytest

from etl.common.currency import from_usd, to_usd


class FakeCursor:
    def __init__(self, rate_row):
        self._rate_row = rate_row
        self.last_query = None

    def execute(self, query, params):
        self.last_query = (query, params)

    def fetchone(self):
        return self._rate_row


def test_to_usd_passthrough_for_usd():
    cur = FakeCursor(rate_row=None)
    assert to_usd(cur, 100, "USD") == 100.0


def test_to_usd_converts_using_rate():
    cur = FakeCursor(rate_row={"usd_per_unit": 1.1})
    assert to_usd(cur, 100, "EUR") == 110.0


def test_to_usd_raises_when_rate_missing():
    cur = FakeCursor(rate_row=None)
    with pytest.raises(ValueError):
        to_usd(cur, 100, "GEL")


def test_from_usd_passthrough_for_usd():
    cur = FakeCursor(rate_row=None)
    assert from_usd(cur, 100, "USD") == 100.0


def test_from_usd_converts_using_rate():
    cur = FakeCursor(rate_row={"usd_per_unit": 0.27})
    assert from_usd(cur, 100, "ILS") == pytest.approx(370.37, abs=0.01)


def test_from_usd_raises_when_rate_missing():
    cur = FakeCursor(rate_row=None)
    with pytest.raises(ValueError):
        from_usd(cur, 100, "GEL")
