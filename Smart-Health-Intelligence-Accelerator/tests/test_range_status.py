from src.health_intelligence.range_status import calculate_status


def test_within_range_inclusive():
    assert calculate_status(4.0, 4.0, 5.6) == "WITHIN RANGE"
    assert calculate_status(5.6, 4.0, 5.6) == "WITHIN RANGE"


def test_high():
    assert calculate_status(6.2, 4.0, 5.6) == "HIGH"


def test_low():
    assert calculate_status(11.4, 12.0, 16.0) == "LOW"


def test_missing_and_no_range():
    assert calculate_status(None, 4.0, 5.6) == "MISSING"
    assert calculate_status(5.0, None, 5.6) == "NO REFERENCE RANGE"
