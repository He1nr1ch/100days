import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

# Set up the Streamlit page
st.set_page_config(page_title="S&P 500 Stock Tracker", layout="wide")
st.title("S&P 500 Stock Price Tracker")

# Add user input options
ticker = st.sidebar.text_input("Stock Ticker", value="^GSPC")
start_date = st.sidebar.date_input("Start Date", value=datetime(2025, 1, 20))
interval_options = {"Daily": "1d", "Weekly": "1wk", "Monthly": "1mo"}
selected_interval = st.sidebar.selectbox("Interval", options=list(interval_options.keys()))
interval = interval_options[selected_interval]

# Add a button to refresh data
if st.sidebar.button("Refresh Data"):
    st.experimental_rerun()

try:
    # Download data
    data = yf.download(ticker, start=start_date, interval=interval)

    # Check if data is valid
    if data.empty:
        st.error("No data fetched. Check ticker or internet connection.")
    else:
        # Choose appropriate column
        price_column = 'Adj Close' if 'Adj Close' in data.columns else 'Close'

        # Calculate percentage change
        first_price = data[price_column].iloc[0].item()
        last_price = data[price_column].iloc[-1].item()
        percent_change = ((last_price - first_price) / first_price) * 100

        # Determine color based on percentage change
        change_color = 'green' if percent_change >= 0 else 'red'

        # Display metrics
        st.metric(
            label=f"Current {price_column} Price", 
            value=f"${last_price:.2f}", 
            delta=f"{percent_change:.2f}%"
        )

        # Create a figure for the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data.index, data[price_column], label=f'S&P 500 {price_column}', color='blue')

        # Add percentage change annotation
        ax.annotate(f'{percent_change:.2f}%', 
                    xy=(data.index[-1], last_price),
                    xytext=(data.index[-1], last_price * 1.05),
                    fontsize=24,
                    fontweight='bold',
                    color=change_color)

        ax.set_title(f'S&P 500 {price_column} - From {start_date} Onwards')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price (USD)')
        ax.grid(True)
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(fig)

        # Display the data table
        st.subheader("Historical Data")
        st.dataframe(data)

except Exception as e:
    st.error(f"An error occurred: {e}")
