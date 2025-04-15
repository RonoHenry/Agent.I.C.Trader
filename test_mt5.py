import pandas as pd
from backend.data_clients.mt5_client import MT5Client

client = MT5Client()
timeframes = ["D1", "H4", "H1", "M15"]
symbol = "EURUSD"
bars = 100

for tf in timeframes:
    try:
        df = client.get_data(symbol, tf, bars)
        print(f"\n{tf} Data (Last 5 bars):")
        print(df.tail())
        df.to_csv(f"data/market_data/historical/{symbol}_{tf}.csv")
    except Exception as e:
        print(f"Failed to fetch {tf}: {e}")