# Black-Scholes Option Pricing Dashboard

A professional tool for pricing European options and visualizing the Greeks using the Black-Scholes model.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Key Features

- **Real-time Option Pricing**: Calculate Call and Put prices instantly using the Black-Scholes formula
- **Complete Greeks Analysis**: Delta, Gamma, Theta, Vega, and Rho for both option types
- **Interactive Heatmaps**: Visualize price sensitivity across Spot Price and Volatility dimensions
- **Calculation History**: SQLite-backed storage of recent calculations for reference
- **Clean UI**: Polished metric cards and responsive layout

## Tech Stack

- **Backend**: Python 3.10+, NumPy, SciPy
- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Database**: SQLite

## Installation

```bash
git clone https://github.com/yourusername/black-scholes-dashboard.git
cd black-scholes-dashboard

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

**Parameters:**
- **Spot Price**: Current price of the underlying asset
- **Strike Price**: Option exercise price
- **Time to Expiry**: Time remaining until expiration (in years)
- **Volatility**: Annualized volatility (%)
- **Risk-Free Rate**: Annualized risk-free interest rate (%)

## Project Structure

```
black-scholes-dashboard/
├── app.py           # Streamlit application
├── model.py         # Black-Scholes pricing engine
├── database.py      # SQLite persistence layer
├── requirements.txt
└── README.md
```

## License

MIT
