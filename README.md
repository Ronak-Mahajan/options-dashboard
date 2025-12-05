# Black-Scholes Option Pricing Dashboard

A professional tool for pricing European options and visualizing the Greeks using the Black-Scholes model.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Key Features

- **Real-time Option Pricing**: Calculate Call and Put prices instantly using the Black-Scholes formula.
- **Complete Greeks Analysis**: Delta, Gamma, Theta, Vega, and Rho for both option types.
  - *Note: Theta is calculated daily, and Vega/Rho are per 1% move (trader convention).*
- **P&L Simulator**: Calculate Profit and Loss based on an original purchase price.
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
git clone [https://github.com/Ronak-Mahajan/options-dashboard.git](https://github.com/Ronak-Mahajan/options-dashboard.git)
cd options-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python database.py
