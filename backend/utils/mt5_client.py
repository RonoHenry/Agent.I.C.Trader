# backend/utils/mt5_client.py
import MetaTrader5 as mt5
from backend.config.settings import settings

TIMEFRAME_MAP = {
    "Monthly": mt5.TIMEFRAME_MN1,
    "Weekly": mt5.TIMEFRAME_W1,
    "Daily": mt5.TIMEFRAME_D1,
    "H12": mt5.TIMEFRAME_H12,
    "H8": mt5.TIMEFRAME_H8,
    "H6": mt5.TIMEFRAME_H6,
    "H4": mt5.TIMEFRAME_H4,
    "H3": mt5.TIMEFRAME_H3,
    "H2": mt5.TIMEFRAME_H2,
    "H1": mt5.TIMEFRAME_H1,
    "M30": mt5.TIMEFRAME_M30,
    "M15": mt5.TIMEFRAME_M15,
    "M5": mt5.TIMEFRAME_M5,
    "M3": mt5.TIMEFRAME_M3
}

def init_mt5():
    print(f"Attempting MT5 init with: Login={settings.MT5_LOGIN}, Server={settings.MT5_SERVER}")
    if not mt5.initialize(path=r"C:\Program Files\MetaTrader 5\terminal64.exe", timeout=10000):
        print(f"Init failed: {mt5.last_error()}")
        return False
    if not mt5.login(settings.MT5_LOGIN, settings.MT5_PASSWORD, settings.MT5_SERVER):
        print(f"Login failed: {mt5.last_error()}")
        return False
    print(f"Logged into MT5 - Account #{settings.MT5_LOGIN}")
    return True

def get_candle_data(symbol="EURUSD", timeframe="M15", count=10):
    if not init_mt5():
        return None
    tf = TIMEFRAME_MAP.get(timeframe, mt5.TIMEFRAME_M15)  # Default to M15
    print(f"Fetching {count} candles for {symbol} on {timeframe}")
    candles = mt5.copy_rates_from_pos(symbol, tf, 0, count)
    if candles is None:
        print(f"Failed to fetch candles: {mt5.last_error()}")
    mt5.shutdown()
    return candles