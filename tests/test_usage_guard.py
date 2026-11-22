import json

from cimcime.usage_guard import check


def _w(d, name, obj):
    (d / name).write_text(json.dumps(obj))


def test_stale_is_unknown(tmp_path):
    _w(tmp_path, "usage.json", {"checked_at": 1000, "percent": {"five_hour": 94, "seven_day": 73}})
    r = check(tmp_path, now=1000 + 3600)
    assert r["verdict"] == "unknown" and "NOT current" in r["reason"]


def test_fresh_defer(tmp_path):
    _w(tmp_path, "usage.json", {"checked_at": 1000, "percent": {"five_hour": 94, "seven_day": 73}})
    assert check(tmp_path, now=1100)["verdict"] == "defer"


def test_statusline_fresher_wins(tmp_path):
    _w(tmp_path, "usage.json", {"checked_at": 1000, "percent": {"five_hour": 94, "seven_day": 73}})
    _w(tmp_path, "statusline.json", {"captured_at": 5000, "data": {"rate_limits": {
        "five_hour": {"used_percentage": 1, "resets_at": 9}, "seven_day": {"used_percentage": 0, "resets_at": 9}}}})
    assert check(tmp_path, now=5100)["verdict"] == "normal"


def test_no_data(tmp_path):
    assert check(tmp_path, now=1)["verdict"] == "unknown"


def test_weekly_90_stops_dev(tmp_path):
    _w(tmp_path, "usage.json", {"checked_at": 1000, "percent": {"five_hour": 5, "seven_day": 91}})
    assert check(tmp_path, now=1100)["verdict"] == "stop_dev"
