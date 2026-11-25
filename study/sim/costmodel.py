"""Cost models for graphs without measured times (the RH archive), calibrated on Mathlib.

cost[m] = fixed + rate[m] * lines[m]

* `fixed`: per-file start + import loading (RH files import all of Mathlib; measured separately).
* `rate`: seconds per source line. "mean" uses one rate for all files; "heavy" draws each file's
  rate from Mathlib's empirical distribution (heavy-tailed: a few files cost far more per line),
  which is what makes single heavy files show up on critical paths.
* The variable part can be rescaled so that the total work matches a target (core-hours).
"""
from __future__ import annotations

import numpy as np

from .trace import Trace


def mathlib_rates(ml: Trace, fixed_ml: float, min_lines: int = 30) -> np.ndarray:
    """Seconds per line of Mathlib files with at least `min_lines` lines, after removing the
    per-file fixed part."""
    sel = ml.lines >= min_lines
    return np.maximum(ml.cost[sel] - fixed_ml, 0.0) / ml.lines[sel]


def model_costs(t: Trace, rates: np.ndarray, fixed: float, mode: str = "heavy", rng_key: int = 0,
                target_core_h: float | None = None) -> tuple[np.ndarray, dict]:
    lines = np.asarray(t.lines, dtype=np.float64)
    if mode == "mean":
        r = np.full(t.n, float(np.mean(rates)))
    elif mode == "median":
        r = np.full(t.n, float(np.median(rates)))
    elif mode == "heavy":
        gen = np.random.default_rng(rng_key)
        r = gen.choice(rates, size=t.n, replace=True)
    else:
        raise ValueError(mode)
    var = r * lines
    info = {"mode": mode, "fixed_s": fixed, "rate_mean": float(np.mean(r)),
            "work_unscaled_core_h": float((fixed * t.n + var.sum()) / 3600)}
    if target_core_h is not None:
        s = (target_core_h * 3600 - fixed * t.n) / var.sum()
        if s <= 0:
            raise ValueError("target below the fixed part")
        var = var * s
        info["scale"] = float(s)
    cost = fixed + var
    info["work_core_h"] = float(cost.sum() / 3600)
    return cost, info
