import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from model import BlackScholes
import database as db

st.set_page_config(
    page_title="Black-Scholes Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("Black-Scholes Option Pricing Dashboard")

with st.sidebar:
    st.header("Parameters")
    S = st.number_input("Spot Price ($)", min_value=0.01, value=100.0, step=1.0)
    K = st.number_input("Strike Price ($)", min_value=0.01, value=100.0, step=1.0)
    T = st.number_input("Time to Expiry (Years)", min_value=0.0, value=1.0, step=0.01)
    sigma = st.number_input("Volatility (%)", min_value=0.1, value=20.0, step=0.5) / 100
    r = st.number_input("Risk-Free Rate (%)", min_value=0.0, value=5.0, step=0.1) / 100

    calculate = st.button("Calculate", type="primary", use_container_width=True)

bs = BlackScholes(S, K, T, r, sigma)
call_price = bs.call_price()
put_price = bs.put_price()
call_greeks = bs.call_greeks()
put_greeks = bs.put_greeks()

if calculate:
    db.save_calculation(S, K, T, r, sigma, call_price, put_price)

col_call, col_put = st.columns(2)

with col_call:
    st.subheader("📗 Call Option")
    st.metric("Price", f"${call_price:,.4f}")
    g = call_greeks
    c1, c2, c3 = st.columns(3)
    c1.metric("Delta", f"{g.delta:.4f}")
    c2.metric("Gamma", f"{g.gamma:.4f}")
    c3.metric("Theta", f"{g.theta:.4f}")
    c4, c5, _ = st.columns(3)
    c4.metric("Vega", f"{g.vega:.4f}")
    c5.metric("Rho", f"{g.rho:.4f}")

with col_put:
    st.subheader("📕 Put Option")
    st.metric("Price", f"${put_price:,.4f}")
    g = put_greeks
    c1, c2, c3 = st.columns(3)
    c1.metric("Delta", f"{g.delta:.4f}")
    c2.metric("Gamma", f"{g.gamma:.4f}")
    c3.metric("Theta", f"{g.theta:.4f}")
    c4, c5, _ = st.columns(3)
    c4.metric("Vega", f"{g.vega:.4f}")
    c5.metric("Rho", f"{g.rho:.4f}")

st.divider()


def generate_heatmap(option_type: str) -> go.Figure:
    spot_range = np.linspace(S * 0.7, S * 1.3, 25)
    vol_range = np.linspace(max(0.05, sigma * 0.5), sigma * 1.5, 25)

    prices = np.zeros((len(vol_range), len(spot_range)))
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            model = BlackScholes(spot, K, T, r, vol)
            prices[i, j] = model.call_price() if option_type == "Call" else model.put_price()

    fig = go.Figure(
        data=go.Heatmap(
            z=prices,
            x=np.round(spot_range, 2),
            y=np.round(vol_range * 100, 1),
            colorscale=[[0, "#d32f2f"], [0.5, "#ffeb3b"], [1, "#388e3c"]],
            colorbar=dict(title="Price ($)"),
            hovertemplate="Spot: $%{x}<br>Vol: %{y}%<br>Price: $%{z:.2f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"{option_type} Price Sensitivity",
        xaxis_title="Spot Price ($)",
        yaxis_title="Volatility (%)",
        height=450,
    )
    return fig


st.subheader("Price Sensitivity Heatmaps")
heatmap_col1, heatmap_col2 = st.columns(2)

with heatmap_col1:
    st.plotly_chart(generate_heatmap("Call"), use_container_width=True)

with heatmap_col2:
    st.plotly_chart(generate_heatmap("Put"), use_container_width=True)

st.divider()

st.subheader("Calculation History")
history = db.fetch_recent(10)

if history:
    df = pd.DataFrame(history)
    df.columns = ["Timestamp", "Spot", "Strike", "Expiry", "Rate", "Vol", "Call", "Put"]
    df["Rate"] = (df["Rate"] * 100).round(2).astype(str) + "%"
    df["Vol"] = (df["Vol"] * 100).round(2).astype(str) + "%"
    df["Call"] = df["Call"].apply(lambda x: f"${x:,.4f}")
    df["Put"] = df["Put"].apply(lambda x: f"${x:,.4f}")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No calculations yet. Adjust parameters and click Calculate.")
