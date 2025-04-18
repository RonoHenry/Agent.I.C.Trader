import pandas as pd
from backend.data_clients.mt5_client import MT5Client

class ICTDetector:
    def __init__(self, symbol: str, timeframe: str, lookback: int = 100):
        self.symbol = symbol
        self.timeframe = timeframe
        self.lookback = lookback
        self.mt5 = MT5Client()
        self.candles = None

    def fetch_data(self) -> pd.DataFrame:
        """Fetch OHLCV data from MT5."""
        return self.mt5.get_data(self.symbol, self.timeframe, self.lookback)

    def _identify_fractals(self, candles: pd.DataFrame) -> pd.DataFrame:
        """Identify bullish and bearish fractals."""
        candles['bullish_fractal'] = (
            (candles['low'] < candles['low'].shift(1)) &
            (candles['low'] < candles['low'].shift(-1)) &
            (candles['low'] < candles['low'].shift(2)) &
            (candles['low'] < candles['low'].shift(-2))
        )
        candles['bearish_fractal'] = (
            (candles['high'] > candles['high'].shift(1)) &
            (candles['high'] > candles['high'].shift(-1)) &
            (candles['high'] > candles['high'].shift(2)) &
            (candles['high'] > candles['high'].shift(-2))
        )
        return candles