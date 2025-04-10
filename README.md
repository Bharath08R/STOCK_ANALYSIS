📊 Stock Market Analysis Project

A complete pipeline for extracting, cleaning, and visualizing stock market data using Python, Streamlit and Power BI.

🚀 Project Overview

This project builds an end-to-end stock analysis solution, starting from raw YAML data files to advanced insights via Streamlit and Power BI dashboards. Key insights include:

Top gainers and losers

Volatility and cumulative return trends

Sector-wise performance

Monthly performance breakdown

Stock correlation heatmaps

📂 Folder Structure

project_root/
├── final_csvs/               # One CSV per stock (after transformation)
├── combined_data.csv/        # all in one CSV
├── exported_for_powerbi.csv  # Consolidated and udated CSV for Power BI
├── stockvisual.py            # Streamlit dashboard
├── stock1.ipynb              # Yaml file to CSV file conversion
├── Sector_data.csv           # Reference CSV with COMPANY and sector info
└── README.md                 # This file

🛠️ 1. Data Extraction

Raw YAML files are organized by month and contain daily stock data for various tickers.

A Python script reads all YAML files recursively, groups the data by Ticker, and saves them as individual CSV files.

Script: stock1.ipynb

Key Tasks:

Traverse nested directories

Parse each YAML file

Combine data by Ticker

Export one CSV per ticker

🧹 2. Data Cleaning & Merging

Script: stock1.ipynb

This script:

Merges all stock CSVs into one

Calculates key metrics:

Daily returns

Cumulative return

Yearly return

Monthly tags

Adds metadata: COMPANY, sector

Exports a final CSV: exported_for_powerbi.csv

📊 3. Streamlit Dashboard

Script: stockvisual.py

Interactive dashboard built with Streamlit that features:

📈 Top 10 Gainers & Losers

📉 Most Volatile Stocks

🧮 Market Summary

🔄 Cumulative Return Over Time

🏭 Sector-Wise Average Return

📅 Monthly Movers

🔥 Stock Correlation Heatmap

Run it with:streamlit run stockvisual.py

📈 4. Power BI Visualization

Using the exported_for_powerbi.csv file:

Key Visuals:

Bar chart: Top 10 Gainers & Losers

Line chart: Cumulative Return per Ticker

Sector performance by average yearly return

Monthly movers: top/bottom 5 per month

Heatmap (via Python visual): Stock correlation

Advanced DAX Examples:

Volatility = STDEVX.P(FILTER(StockData, NOT(ISBLANK(StockData[daily_return]))), StockData[daily_return])

Monthly Return =
VAR First = CALCULATE(FIRSTNONBLANK(StockData[close], 1), ALLEXCEPT(StockData, StockData[Ticker], StockData[month]))
VAR Last = CALCULATE(LASTNONBLANK(StockData[close], 1), ALLEXCEPT(StockData, StockData[Ticker], StockData[month]))
RETURN DIVIDE(Last - First, First)

✅ Requirements

Python 3.8+

pandas, PyYAML, seaborn, matplotlib, streamlit

Power BI Desktop

📌 Credits

Stock price data: YAML feeds

Sector info: Provided CSV mapping

Visuals powered by Streamlit & Power BI

📬 Contact

For questions or enhancements, reach out via GitHub or your data team lead.
