# quantspica/gui/app.py

import streamlit as st
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv

from quantspica.data_engine.loaders import MarketDataLoader

# Load environment variables from .env file
load_dotenv()

st.set_page_config(layout="wide")
st.title("QuantSpica — Market Viewer")

symbol = st.text_input("Symbol", value="AAPL")

col1, col2 = st.columns(2)
with col1:
    load_button = st.button("Load Data")
with col2:
    refresh_button = st.button("Refresh from API")

if load_button or refresh_button:
    loader = MarketDataLoader(
        api_key=os.getenv("ALPACA_API_KEY"),
        secret_key=os.getenv("ALPACA_API_SECRET"),
    )

    if refresh_button:
        # Force fetch from API
        st.warning("Fetching fresh data from API...")
        df = loader.fetch_daily_bars(
            symbol,
            start=datetime(2018, 1, 1),
            end=datetime.now()
        )
        loader.save(df, symbol)
        st.success("Data refreshed from API!")
    else:
        # Try to load cached data first
        try:
            df = loader.load(symbol)
            st.info("Loaded cached data.")
        except FileNotFoundError:
            st.warning("No cached data found. Attempting to fetch...")
            df = loader.fetch_daily_bars(
                symbol,
                start=datetime(2018, 1, 1),
                end=datetime.now()
            )
            loader.save(df, symbol)

    fig = px.line(df, x="date", y="close", title=f"{symbol} Adjusted Close Price")
    fig.update_layout(yaxis_title="Adjusted Close ($)", xaxis_title="Date")
    st.plotly_chart(fig, use_container_width=True)
