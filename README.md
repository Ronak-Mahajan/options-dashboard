# Black-Scholes Option Pricing Dashboard

> **Status: archived reference.** This is a 2025 single-page Streamlit
> calculator for European Black-Scholes prices and Greeks. Its successor is
> [neural-options-lab](https://github.com/Ronak-Mahajan/neural-options-lab),
> which has closed-form and neural pricers, autograd Greeks, implied-vol and
> price surfaces, live SPY and Deribit BTC chains, tests, CI and a hosted demo.
> This repo is kept as a small, self-contained pricer; it is not developed further.

A Streamlit tool for pricing European options and visualizing the Greeks using the Black-Scholes model.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![CI](https://github.com/Ronak-Mahajan/options-dashboard/actions/workflows/ci.yml/badge.svg)

## Key Features

- **Option Pricing**: Call and Put prices recomputed on every input change using the Black-Scholes closed form.
- **Complete Greeks Analysis**: Delta, Gamma, Theta, Vega, and Rho for both option types.
  - *Note: Theta is calculated daily, and Vega/Rho are per 1% move (trader convention).*
- **P&L Grid**: Colour the spot-by-volatility grid by price minus an original purchase price.
- **Interactive Heatmaps**: Visualize price sensitivity across Spot Price and Volatility dimensions.
- **Calculation History**: SQLite-backed storage of recent calculations.
- **Clean UI**: iOS-style design with metric cards and responsive layout.

## Tech Stack

- **Backend**: Python 3.10+, NumPy, SciPy, Pandas
- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Database**: SQLite

## Installation

Prerequisites: Python 3.10 or newer.

```bash
# Clone the repository
git clone https://github.com/Ronak-Mahajan/options-dashboard.git
cd options-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

The SQLite file `calculations.db` is created automatically the first time the
app imports `database.py`; there is no separate initialization step.

## Usage

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

**Parameters:**

- **Spot Price**: Current price of the underlying asset.
- **Strike Price**: Option exercise price.
- **Time to Expiry**: Time remaining until expiration (in years).
- **Volatility**: Annualized volatility (%). At 0% the pricer returns the
  deterministic limit `max(S - K e^{-rT}, 0)` for the call and
  `max(K e^{-rT} - S, 0)` for the put.
- **Risk-Free Rate**: Annualized risk-free interest rate (%).

The **Calculate** button saves the current inputs and outputs to the history
table; prices and Greeks themselves update live as you change any input.

## Tests

```bash
pip install pytest
python -m pytest tests/
```

- `tests/test_model.py` checks the closed form against itself: put-call parity,
  a textbook reference price (Hull: S=42, K=40, r=10%, sigma=20%, T=0.5 gives
  call 4.76 and put 0.81), the sigma=0 deterministic limit, finite Greeks at
  sigma=0, and central finite differences for all five Greeks.
- `tests/test_app.py` runs the Streamlit script headlessly through
  `streamlit.testing.v1.AppTest` and checks the metric cards (default inputs
  give call 10.4506 / put 5.5735; sigma=0 shows no nan, inf or negative
  price) and that the heatmap volatility axis is ascending.

The same suite runs on every push in `.github/workflows/ci.yml`.

## Project Structure

```
options-dashboard/
├── app.py                    # Streamlit application
├── model.py                  # Black-Scholes pricing engine
├── database.py               # SQLite persistence layer
├── tests/
│   ├── test_model.py         # closed-form checks
│   └── test_app.py           # headless AppTest checks
├── .github/workflows/ci.yml  # runs the tests on every push
├── .streamlit/config.toml    # light theme
├── requirements.txt
├── LICENSE
└── README.md
```

## Limitations

- No market data and no implied-volatility inversion: every number is a
  function of the five hand-typed inputs, and the tests check the closed form
  against itself, not against quotes. For those features use
  [neural-options-lab](https://github.com/Ronak-Mahajan/neural-options-lab).
- The P&L grid subtracts one purchase price from both the call and the put
  surface; it is a scenario colouring, not a position P&L.

## License

MIT. See [LICENSE](LICENSE).
