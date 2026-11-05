"""Deterministic range-status calculation.

The function uses only the reference range supplied with the record. It does
not introduce universal medical thresholds and does not perform diagnosis.
"""
from __future__ import annotations

from typing import Optional


def calculate_status(
    measured_value: Optional[float],
    reference_low: Optional[float],
    reference_high: Optional[float],
) -> str:
    if measured_value is None:
        return "MISSING"
    if reference_low is None or reference_high is None:
        return "NO REFERENCE RANGE"
    if measured_value < reference_low:
        return "LOW"
    if measured_value > reference_high:
        return "HIGH"
    return "WITHIN RANGE"
