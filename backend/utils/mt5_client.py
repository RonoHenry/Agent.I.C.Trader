# backend/utils/mt5_client.py
import MetaTrader5 as mt5
from backend.config.settings import settings

def init_mt5():
    if not mt5.initialize(login=int(settings.MT5_LOGIN), password=settings.MT5_PASSWORD, server=settings.MT5_SERVER):
        raise Exception("MT5 init failed")
    return mt5

def get_candles(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M15, count=10):
    mt5 = init_mt5()
    candles = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    mt5.shutdown()
    return candles