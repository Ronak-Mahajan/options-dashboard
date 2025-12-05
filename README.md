

````markdown
# Black-Scholes Option Pricing Dashboard

A professional tool for pricing European options and visualizing the Greeks using the Black-Scholes model.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Key Features

- **Real-time Option Pricing**: Calculate Call and Put prices instantly using the Black-Scholes formula.
- **Complete Greeks Analysis**: Delta, Gamma, Theta, Vega, and Rho for both option types.
  - Note: Theta is calculated daily, and Vega/Rho are per 1% move, which is standard in this area.
- **P&L Simulator**: You can calculate Profit and Loss based on an original purchase price.
- **Interactive Heatmaps**: Visualize price sensitivity across Spot Price and Volatility dimensions.
- **Calculation History**: SQLite-backed storage of recent calculations for reference.
- **Clean UI**: Polished metric cards and responsive layout.

## Tech Stack

- **Backend**: Python 3.10+, NumPy, SciPy, Pandas
- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Database**: SQLite

## Installation

You need Python 3.10 or newer, that is the version used here.

```bash
# This gets the project files from the right GitHub place.
git clone [https://github.com/Ronak-Mahajan/options-dashboard.git](https://github.com/Ronak-Mahajan/options-dashboard.git)
cd options-dashboard

python -m venv venv
source venv/bin/activate  # For Windows users: venv\Scripts\activate

# Install all the packages
pip install -r requirements.txt

# This line initializes the 'calculations.db' file and creates the table.
# It is important that you have this database set up first.
python database.py
````

## Usage

You have to run this command to start the app, and then you just go to the URL it shows you in your browser.

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

**Parameters:**

  - **Spot Price**: Current price of the underlying asset.
  - **Strike Price**: Option exercise price.
  - **Time to Expiry**: Time remaining until expiration (in years).
  - **Volatility**: Annualized volatility (%).
  - **Risk-Free Rate**: Annualized risk-free interest rate (%).

## Project Structure

```
options-dashboard/
├── app.py           # Streamlit application
├── model.py         # Black-Scholes pricing engine
├── database.py      # SQLite persistence layer
├── requirements.txt
└── README.md
```

## License

MIT.

```
```
