# backend/utils/mt5_client.py
import MetaTrader5 as mt5
from backend.config.settings import settings

def init_mt5():
    if not mt5.initialize():
        raise ConnectionError(f"MT5 init failed: {mt5.last_error()}")
    if not mt5.login(settings.MT5_LOGIN, settings.MT5_PASSWORD, settings.MT5_SERVER):
        raise ConnectionError(f"MT5 login failed: {mt5.last_error()}")
    print(f"Logged into MT5 - Account #{settings.MT5_LOGIN}")

def get_candle_data(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M15, count=10):
    init_mt5()
    candles = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if candles is None:
        raise ValueError(f"Failed to fetch candles: {mt5.last_error()}")
    mt5.shutdown()
    return candles

def map_pixels_to_prices(wick_pixels, body_pixel, candles):
    latest_candle = candles[-1]
    high, low, open, close = latest_candle["high"], latest_candle["low"], latest_candle["open"], latest_candle["close"]
    wick_range = wick_pixels[1] - wick_pixels[0] if isinstance(wick_pixels, tuple) else 0
    price_range = high - low
    if wick_range > 0:
        wick_high = high
        wick_low = high - (price_range * (wick_pixels[1] - wick_pixels[0]) / wick_range)
    else:
        wick_high, wick_low = high, low
    body_price = close if body_pixel == "N/A" else low + (price_range * (body_pixel - wick_pixels[0]) / wick_range)
    return {"wick_high": wick_high, "wick_low": wick_low, "body": body_price}