import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from model import BlackScholes
import database as db

st.set_page_config(
    page_title="Black-Scholes Dashboard",
    page_icon="📈",
    layout="wide",
)


def inject_custom_css() -> None:
    """
    Inject comprehensive iOS/Apple-style CSS for system fonts and refined UI.
    
    This function enforces:
    - System font stack (San Francisco on Mac, Segoe UI on Windows)
    - Apple-style header typography with tight letter-spacing
    - Metric cards with rounded corners and subtle shadows
    - Consistent design across all components
    """
    css = """
    <style>
        /* Global Font Stack - System fonts for platform-native feel */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        }
        
        * {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        }
        
        /* Header Styling - Classic Apple weight and letter-spacing */
        h1, h2, h3, h4, h5, h6 {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }
        
        h1 {
            font-size: 2.4rem !important;
            margin-bottom: 0.5rem !important;
            color: #1D1D1F !important;
        }
        
        h2 {
            font-size: 1.8rem !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
            color: #1D1D1F !important;
        }
        
        h3 {
            font-size: 1.3rem !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.8rem !important;
            color: #1D1D1F !important;
        }
        
        /* Body text */
        p, label, div, span {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
            font-weight: 400 !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
            color: #1D1D1F !important;
        }
        
        /* Metric Cards - White boxes with rounded corners and subtle shadow */
        [data-testid="stMetric"] {
            background-color: #FFFFFF !important;
            border: 1px solid rgba(0, 0, 0, 0.05) !important;
            border-radius: 18px !important;
            padding: 20px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        }
        
        [data-testid="stMetric"]:hover {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12) !important;
            transform: translateY(-4px) !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            color: #86868B !important;
            text-transform: none !important;
            margin-bottom: 8px !important;
            letter-spacing: 0px !important;
        }
        
        [data-testid="stMetricValue"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            font-size: 1.9rem !important;
            font-weight: 700 !important;
            color: #1D1D1F !important;
            letter-spacing: -0.5px !important;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #F5F5F7 !important;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.5rem !important;
        }
        
        /* Number Input Fields */
        [data-testid="stNumberInput"] input {
            border-radius: 12px !important;
            border: 1px solid #E5E5EA !important;
            padding: 12px 14px !important;
            font-size: 1rem !important;
            background-color: #FFFFFF !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }
        
        [data-testid="stNumberInput"] input:focus {
            border-color: #007AFF !important;
            box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1) !important;
            outline: none !important;
        }
        
        /* Text Input Fields */
        input[type="text"], input[type="password"] {
            border-radius: 12px !important;
            border: 1px solid #E5E5EA !important;
            padding: 12px 14px !important;
            font-size: 1rem !important;
            background-color: #FFFFFF !important;
        }
        
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #007AFF !important;
            box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1) !important;
        }
        
        /* Primary Button */
        button[kind="primary"] {
            background-color: #007AFF !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            padding: 12px 20px !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
            transition: all 0.2s ease !important;
        }
        
        button[kind="primary"]:hover {
            background-color: #0051D5 !important;
            box-shadow: 0 6px 12px rgba(0, 122, 255, 0.3) !important;
        }
        
        button[kind="primary"]:active {
            background-color: #0041B8 !important;
            transform: scale(0.98) !important;
        }
        
        /* Secondary Button */
        button[kind="secondary"] {
            background-color: #F5F5F7 !important;
            color: #007AFF !important;
            border: 1px solid #E5E5EA !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }
        
        button[kind="secondary"]:hover {
            background-color: #EBEBF0 !important;
        }
        
        /* Radio Buttons */
        [data-testid="stRadio"] {
            margin-top: 0.5rem !important;
        }
        
        [data-testid="stRadio"] label {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
            font-weight: 500 !important;
            color: #1D1D1F !important;
            margin-left: 8px !important;
        }
        
        /* Checkbox */
        [data-testid="stCheckbox"] label {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
            font-weight: 500 !important;
            color: #1D1D1F !important;
            margin-left: 8px !important;
        }
        
        /* Dividers */
        hr {
            border: none !important;
            height: 1px !important;
            background: rgba(0, 0, 0, 0.08) !important;
            margin: 2rem 0 !important;
        }
        
        /* Dataframe Table */
        [data-testid="stDataframe"] {
            border: 1px solid #E5E5EA !important;
            border-radius: 14px !important;
            overflow: hidden !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        }
        
        /* Info Message */
        [data-testid="stInfo"] {
            background-color: #E8F4FF !important;
            border: 1px solid #B3D9FF !important;
            border-radius: 14px !important;
            padding: 15px !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        }
        
        /* Warning Message */
        [data-testid="stWarning"] {
            background-color: #FFF8E1 !important;
            border: 1px solid #FFD966 !important;
            border-radius: 14px !important;
            padding: 15px !important;
        }
        
        /* Error Message */
        [data-testid="stError"] {
            background-color: #FFE8E8 !important;
            border: 1px solid #FF6B6B !important;
            border-radius: 14px !important;
            padding: 15px !important;
        }
        
        /* Success Message */
        [data-testid="stSuccess"] {
            background-color: #E8F5E9 !important;
            border: 1px solid #81C784 !important;
            border-radius: 14px !important;
            padding: 15px !important;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# Inject iOS/Apple-style CSS at app startup
inject_custom_css()

st.title("Black-Scholes Option Pricing")

with st.sidebar:
    st.markdown("### Parameters")
    S = st.number_input(
        "Spot Price ($)",
        min_value=0.01,
        value=100.0,
        step=1.0,
        help="Current market price of the underlying asset",
    )
    K = st.number_input(
        "Strike Price ($)",
        min_value=0.01,
        value=100.0,
        step=1.0,
        help="Exercise price of the option contract",
    )
    T = st.number_input(
        "Time to Expiry (Years)",
        min_value=0.0,
        value=1.0,
        step=0.01,
        help="Enter 0.5 for 6 months, 0.25 for 3 months, etc.",
    )
    sigma = st.number_input(
        "Volatility (%)",
        min_value=0.0,
        value=20.0,
        step=0.5,
        help="Historical or implied volatility; 0 = no uncertainty",
    ) / 100
    r = st.number_input(
        "Risk-Free Rate (%)",
        min_value=0.0,
        value=5.0,
        step=0.1,
        help="Annual risk-free interest rate (e.g., Treasury yield)",
    ) / 100

    st.markdown("---")
    
    # P&L Simulator
    simulate_pnl = st.checkbox("Simulate P&L", value=False)
    purchase_price = None
    if simulate_pnl:
        purchase_price = st.number_input(
            "Purchase Price ($)",
            min_value=0.0,
            value=5.0,
            step=0.1,
            help="Your original option purchase price",
        )

    st.markdown("---")
    calculate = st.button("Calculate", type="primary", use_container_width=True)

bs = BlackScholes(S, K, T, r, sigma)
call_price = bs.call_price()
put_price = bs.put_price()
call_greeks = bs.call_greeks()
put_greeks = bs.put_greeks()

if calculate:
    db.save_calculation(S, K, T, r, sigma, call_price, put_price)

col_call, col_put = st.columns(2, gap="large")

with col_call:
    st.markdown("### Call Option")
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
    st.markdown("### Put Option")
    st.metric("Price", f"${put_price:,.4f}")
    g = put_greeks
    c1, c2, c3 = st.columns(3)
    c1.metric("Delta", f"{g.delta:.4f}")
    c2.metric("Gamma", f"{g.gamma:.4f}")
    c3.metric("Theta", f"{g.theta:.4f}")
    c4, c5, _ = st.columns(3)
    c4.metric("Vega", f"{g.vega:.4f}")
    c5.metric("Rho", f"{g.rho:.4f}")

st.markdown("---")


def generate_heatmap(option_type: str, chart_style: str, purchase_price: float | None = None, simulate_pnl: bool = False) -> go.Figure:
    spot_range = np.linspace(S * 0.7, S * 1.3, 25)
    vol_range = np.linspace(max(0.05, sigma * 0.5), sigma * 1.5, 25)

    prices = np.zeros((len(vol_range), len(spot_range)))
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            model = BlackScholes(spot, K, T, r, vol)
            prices[i, j] = model.call_price() if option_type == "Call" else model.put_price()

    # Calculate Z-values (P&L or Price)
    z_values = prices
    if simulate_pnl and purchase_price is not None:
        z_values = prices - purchase_price
    
    # Set title and colorbar based on simulation mode
    if simulate_pnl and purchase_price is not None:
        colorbar_title = "P&L ($)"
        chart_title = f"{option_type} P&L Sensitivity"
    else:
        colorbar_title = "Price ($)"
        chart_title = f"{option_type} Price Sensitivity"

    # Determine colorscale based on P&L mode
    if simulate_pnl and purchase_price is not None:
        colorscale = "RdYlGn"
    else:
        colorscale = "Viridis"

    if chart_style == "3D Surface":
        # 3D Surface plot
        fig = go.Figure(
            data=go.Surface(
                z=z_values,
                x=np.round(spot_range, 2),
                y=np.round(vol_range * 100, 1),
                colorscale=colorscale,
                colorbar=dict(title=colorbar_title),
                hovertemplate="Spot: $%{x}<br>Vol: %{y}%<br>Value: $%{z:.2f}<extra></extra>",
            )
        )
        fig.update_layout(
            title=chart_title,
            scene=dict(
                xaxis_title="Spot Price ($)",
                yaxis_title="Volatility (%)",
                zaxis_title=colorbar_title,
                bgcolor="rgba(245, 245, 247, 0.5)",
            ),
            height=550,
            font=dict(family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", size=13),
            margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor="rgba(255, 255, 255, 0.8)",
            paper_bgcolor="rgba(245, 245, 247, 0)",
        )
    else:
        # 2D Heatmap plot (original)
        fig = go.Figure(
            data=go.Heatmap(
                z=z_values,
                x=np.round(spot_range, 2),
                y=np.round(vol_range * 100, 1),
                colorscale=colorscale,
                colorbar=dict(title=colorbar_title),
                hovertemplate="Spot: $%{x}<br>Vol: %{y}%<br>Value: $%{z:.2f}<extra></extra>",
            )
        )
        fig.update_layout(
            title=chart_title,
            xaxis_title="Spot Price ($)",
            yaxis_title="Volatility (%)",
            height=450,
            font=dict(family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", size=13),
            margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor="rgba(255, 255, 255, 0.9)",
            paper_bgcolor="rgba(245, 245, 247, 0)",
        )
    
    return fig


st.markdown("## Sensitivity Analysis")

# Chart style selector
chart_style = st.radio(
    "Chart Style",
    options=["2D Heatmap", "3D Surface"],
    horizontal=True,
    label_visibility="collapsed",
)

heatmap_col1, heatmap_col2 = st.columns(2, gap="large")

with heatmap_col1:
    st.plotly_chart(generate_heatmap("Call", chart_style, purchase_price, simulate_pnl), use_container_width=True)

with heatmap_col2:
    st.plotly_chart(generate_heatmap("Put", chart_style, purchase_price, simulate_pnl), use_container_width=True)

st.markdown("---")

st.markdown("## History")
history = db.fetch_recent(10)

if history:
    df = pd.DataFrame(history)
    df.columns = ["Timestamp", "Spot", "Strike", "Expiry", "Rate", "Vol", "Call", "Put"]
    
    # Format timestamp to YYYY-MM-DD HH:MM
    df["Timestamp"] = pd.to_datetime(df["Timestamp"]).dt.strftime("%Y-%m-%d %H:%M")
    
    df["Rate"] = (df["Rate"] * 100).round(2).astype(str) + "%"
    df["Vol"] = (df["Vol"] * 100).round(2).astype(str) + "%"
    df["Call"] = df["Call"].apply(lambda x: f"${x:,.4f}")
    df["Put"] = df["Put"].apply(lambda x: f"${x:,.4f}")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No calculations yet. Adjust parameters and click Calculate.")
