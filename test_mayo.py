import datetime as dt
from importlib.machinery import SourceFileLoader
from pathlib import Path

mayo = SourceFileLoader("mayo", str(Path(__file__).with_name("mayo"))).load_module()

TZ = dt.timezone(dt.timedelta(hours=8))
RULE = {"WorkOnTime": "2026-10-14T02:00:00+00:00", "WorkOffTime": "2026-10-14T11:00:00+00:00",
        "AdvanceWorkStatus": False, "AdvanceWorkMinute": 30,
        "PostponeWorkStatus": True, "PostponeWorkMinute": 30}


def at(hm):
    h, m = map(int, hm.split(":"))
    return dt.datetime(2026, 10, 14, h, m, tzinfo=TZ)


def test_needs_reason():
    assert mayo.needs_reason(2, RULE, at("19:30")) is None          # inside the 30-min grace
    assert mayo.needs_reason(2, RULE, at("19:31")) == "PostponeWork"
    assert mayo.needs_reason(1, RULE, at("08:00")) is None          # AdvanceWorkStatus off
    assert mayo.needs_reason(1, {**RULE, "AdvanceWorkStatus": True}, at("09:29")) == "AdvanceWork"
    assert mayo.needs_reason(5, RULE, at("23:00")) is None          # breaks never need a reason


def test_next_actions():
    assert mayo.next_actions({"WorkType": 1, "RestType": 1}) == [1, 5]
    assert mayo.next_actions({"WorkType": 2, "RestType": 2}) == [2, 6]
    assert mayo.next_actions({"WorkType": 3, "RestType": 1}) == []


if __name__ == "__main__":
    test_needs_reason(); test_next_actions(); print("ok")
