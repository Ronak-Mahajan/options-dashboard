"""Closed-form Black-Scholes checks for model.py.

Run with:  python -m pytest tests/
"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model import BlackScholes  # noqa: E402


@pytest.mark.parametrize("S,K,T,r,sigma", [
    (100.0, 100.0, 1.0, 0.05, 0.2),
    (90.0, 100.0, 0.5, 0.03, 0.35),
    (120.0, 100.0, 2.0, 0.01, 0.1),
])
def test_put_call_parity(S, K, T, r, sigma):
    bs = BlackScholes(S, K, T, r, sigma)
    lhs = bs.call_price() - bs.put_price()
    rhs = S - K * math.exp(-r * T)
    assert lhs == pytest.approx(rhs, abs=1e-10)


def test_reference_price():
    # Hull, Options, Futures and Other Derivatives: S=42, K=40, r=10%, sigma=20%, T=0.5
    bs = BlackScholes(42.0, 40.0, 0.5, 0.10, 0.20)
    assert bs.call_price() == pytest.approx(4.76, abs=0.01)
    assert bs.put_price() == pytest.approx(0.81, abs=0.01)


@pytest.mark.parametrize("S", [96.0, 100.0, 104.0, 100.0 * math.exp(-0.05)])
def test_zero_vol_is_deterministic_limit(S):
    K, T, r = 100.0, 1.0, 0.05
    bs = BlackScholes(S, K, T, r, 0.0)
    fwd_strike = K * math.exp(-r * T)
    assert bs.call_price() == pytest.approx(max(S - fwd_strike, 0.0), abs=1e-12)
    assert bs.put_price() == pytest.approx(max(fwd_strike - S, 0.0), abs=1e-12)
    assert bs.put_price() >= 0.0
    assert bs.call_price() >= 0.0


@pytest.mark.parametrize("S", [96.0, 100.0, 104.0, 100.0 * math.exp(-0.05)])
def test_zero_vol_greeks_are_finite(S):
    with np.errstate(all="raise"):
        bs = BlackScholes(S, 100.0, 1.0, 0.05, 0.0)
        for g in (bs.call_greeks(), bs.put_greeks()):
            for name in ("delta", "gamma", "theta", "vega", "rho"):
                assert math.isfinite(getattr(g, name)), name
            assert g.gamma == 0.0


def test_greeks_match_finite_differences():
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2
    bs = BlackScholes(S, K, T, r, sigma)
    h = 1e-3

    def call(s=S, t=T, rr=r, sg=sigma):
        return BlackScholes(s, K, t, rr, sg).call_price()

    def put(s=S):
        return BlackScholes(s, K, T, r, sigma).put_price()

    cg, pg = bs.call_greeks(), bs.put_greeks()
    assert cg.delta == pytest.approx((call(S + h) - call(S - h)) / (2 * h), abs=1e-5)
    assert pg.delta == pytest.approx((put(S + h) - put(S - h)) / (2 * h), abs=1e-5)
    assert cg.gamma == pytest.approx((call(S + h) - 2 * call() + call(S - h)) / h**2, abs=1e-4)
    assert cg.gamma == pg.gamma
    # vega and rho are quoted per 1% move; theta per calendar day
    assert cg.vega == pytest.approx((call(sg=sigma + h) - call(sg=sigma - h)) / (2 * h) / 100, abs=1e-6)
    assert cg.rho == pytest.approx((call(rr=r + h) - call(rr=r - h)) / (2 * h) / 100, abs=1e-6)
    assert cg.theta == pytest.approx(-(call(t=T + h) - call(t=T - h)) / (2 * h) / 365, abs=1e-6)
