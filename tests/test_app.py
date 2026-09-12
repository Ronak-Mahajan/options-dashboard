"""Headless end-to-end checks of app.py via streamlit.testing.v1.AppTest.

These run the real Streamlit script (no browser) and read back the metric
cards and the heatmap figure, so they cover the UI-reachable paths that the
closed-form tests in test_model.py cannot: the sigma = 0 input that used to
render negative put prices and nan/inf Greeks, and the heatmap volatility axis
that used to run backwards for sigma < 3.33%.

Run with:  python -m pytest tests/
"""

import base64
import json
import math
from pathlib import Path

import numpy as np
import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def _run(**inputs):
    """Run the app with default widgets, then re-run with `inputs` (by label)."""
    at = AppTest.from_file(str(APP), default_timeout=60)
    at.run()
    assert not at.exception, [e.value for e in at.exception]
    if inputs:
        by_label = {ni.label: ni for ni in at.number_input}
        for label, value in inputs.items():
            by_label[label].set_value(value)
        at.run()
        assert not at.exception, [e.value for e in at.exception]
    return at


def _cards(at):
    """Metric card values: six for the call (Price, Delta, Gamma, Theta, Vega, Rho), six for the put."""
    values = [m.value for m in at.metric]
    assert len(values) == 12
    return values[:6], values[6:]


def _money(text):
    return float(text.replace("$", "").replace(",", ""))


def _vol_axis_pct(at):
    """Volatility axis (in %) of the first heatmap, read from the Plotly figure spec."""
    charts = at.get("plotly_chart")
    assert len(charts) == 2
    spec = json.loads(charts[0].proto.spec)
    y = spec["data"][0]["y"]
    if isinstance(y, dict):  # plotly >= 6 serialises numpy arrays as base64 typed arrays
        y = np.frombuffer(base64.b64decode(y["bdata"]), dtype=np.dtype(y["dtype"]))
    return np.asarray(y, dtype=float)


def test_default_inputs_match_closed_form():
    # Defaults: S = K = 100, T = 1, r = 5%, sigma = 20%.
    call, put = _cards(_run())
    assert _money(call[0]) == pytest.approx(10.4506, abs=1e-4)
    assert _money(put[0]) == pytest.approx(5.5735, abs=1e-4)


def test_zero_vol_cards_are_finite_and_non_negative():
    call, put = _cards(_run(**{"Volatility (%)": 0.0}))
    # Deterministic limit at S = K = 100, r = 5%, T = 1: call = 100 - 100 e^{-0.05}, put = 0.
    assert _money(call[0]) == pytest.approx(100.0 - 100.0 * math.exp(-0.05), abs=1e-4)
    assert _money(put[0]) == pytest.approx(0.0, abs=1e-4)
    for text in call + put:
        assert "nan" not in text.lower() and "inf" not in text.lower(), text
    for price in (call[0], put[0]):
        assert not price.startswith("$-"), price


@pytest.mark.parametrize("vol_pct", [0.0, 3.0, 20.0])
def test_heatmap_vol_axis_is_ascending(vol_pct):
    axis = _vol_axis_pct(_run(**{"Volatility (%)": vol_pct}))
    assert len(axis) == 25
    assert np.all(np.diff(axis) > 0), axis
    if vol_pct >= 10.0:
        # Away from the floor the grid spans 0.5 sigma .. 1.5 sigma as before.
        assert axis[0] == pytest.approx(0.5 * vol_pct, abs=0.1)
        assert axis[-1] == pytest.approx(1.5 * vol_pct, abs=0.1)
