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

## Project Structure

```
options-dashboard/
├── app.py           # Streamlit application
├── model.py         # Black-Scholes pricing engine
├── database.py      # SQLite persistence layer
├── requirements.txt
├── LICENSE
└── README.md
```

## Limitations

- No market data, no implied-volatility inversion and no tests: every number
  is a function of the five hand-typed inputs. For those features use
  [neural-options-lab](https://github.com/Ronak-Mahajan/neural-options-lab).
- The P&L grid subtracts one purchase price from both the call and the put
  surface; it is a scenario colouring, not a position P&L.

## License

MIT. See [LICENSE](LICENSE).
