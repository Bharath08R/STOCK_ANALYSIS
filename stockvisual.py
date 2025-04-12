import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from glob import glob

st.set_page_config(layout="wide")
st.title("📈 Stock Market Dashboard")

# Load data from the combined CSV
df = pd.read_csv("exported_for_powerbi.csv")

# Preprocessing
df['date'] = pd.to_datetime(df['date'])
df.sort_values(['Ticker', 'date'], inplace=True)
df['prev_close'] = df.groupby('Ticker')['close'].shift(1)
df['daily_return'] = (df['close'] - df['prev_close']) / df['prev_close']
df['month'] = df['date'].dt.to_period('M')

# Yearly return
yearly = df.groupby('Ticker').agg(first_price=('close', 'first'),
                                 last_price=('close', 'last'),
                                 COMPANY=('COMPANY', 'first'),
                                 sector=('sector', 'first')).reset_index()
yearly['yearly_return'] = (yearly['last_price'] - yearly['first_price']) / yearly['first_price']

# Sidebar
st.sidebar.header("Navigation")
option = st.sidebar.radio("Go to", ["Overview", "Volatility", "Cumulative Return", "Sector Performance", "Correlation", "Monthly Movers"])

# 1. Overview
if option == "Overview":
    st.subheader("📊 Market Summary")
    green = yearly[yearly['yearly_return'] > 0].shape[0]
    red = yearly[yearly['yearly_return'] <= 0].shape[0]
    avg_price = df['close'].mean()
    avg_volume = df['volume'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Green Stocks", green)
    col2.metric("Red Stocks", red)
    col3.metric("Avg Volume", f"{avg_volume:,.0f}")

    st.subheader("🏆 Top 10 Gainers")
    st.dataframe(yearly.sort_values('yearly_return', ascending=False).head(10))

    st.subheader("💔 Top 10 Losers")
    st.dataframe(yearly.sort_values('yearly_return').head(10))

# 2. Volatility
elif option == "Volatility":
    st.subheader("📈 Top 10 Most Volatile Stocks")
    vol = df.groupby('Ticker')['daily_return'].std().sort_values(ascending=False).head(10)
    st.bar_chart(vol)

# 3. Cumulative Return
elif option == "Cumulative Return":
    st.subheader("📈 Cumulative Return Over Time")
    df['cumulative_return'] = df.groupby('Ticker')['daily_return'].transform(lambda x: (1 + x.fillna(0)).cumprod())
    top5 = df.groupby('Ticker')['cumulative_return'].last().sort_values(ascending=False).head(5).index
    fig, ax = plt.subplots(figsize=(12,6))
    for t in top5:
        data = df[df['Ticker'] == t]
        ax.plot(data['date'], data['cumulative_return'], label=t)
    ax.set_title("Top 5 Performing Stocks")
    ax.legend()
    st.pyplot(fig)

# 4. Sector Performance
elif option == "Sector Performance":
    st.subheader("🏭 Sector-wise Average Yearly Return")
    sector_perf = yearly.groupby('sector')['yearly_return'].mean().sort_values(ascending=False)
    st.bar_chart(sector_perf)

# 5. Correlation
elif option == "Correlation":
    st.subheader("📊 Correlation Heatmap")
    pivot = df.pivot_table(index='date', columns='Ticker', values='close')
    corr = pivot.pct_change().dropna().corr()
    fig, ax = plt.subplots(figsize=(14,10))
    sns.heatmap(corr, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# 6. Monthly Movers
elif option == "Monthly Movers":
    st.subheader("📅 Monthly Gainers & Losers")
    month_selected = st.selectbox("Select Month", sorted(df['month'].astype(str).unique()))
    month_df = df[df['month'].astype(str) == month_selected]
    monthly = month_df.groupby('Ticker').agg(
        start=('close', 'first'),
        end=('close', 'last'),
        COMPANY=('COMPANY', 'first')
    ).reset_index()
    monthly['return'] = (monthly['end'] - monthly['start']) / monthly['start']
    top5 = monthly.sort_values('return', ascending=False).head(5)
    bottom5 = monthly.sort_values('return').head(5)

    col1, col2 = st.columns(2)
    with col1:
        st.write("Top 5 Gainers")
        st.bar_chart(top5.set_index('COMPANY')['return'])
    with col2:
        st.write("Top 5 Losers")
        st.bar_chart(bottom5.set_index('COMPANY')['return'])
