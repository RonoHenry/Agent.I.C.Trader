from .base_detector import ICTDetector
import pandas as pd

class SMTDivergenceDetector(ICTDetector):
    def __init__(self, symbol: str, correlated_symbol: str, timeframe: str, lookback: int = 100):
        super().__init__(symbol, timeframe, lookback)
        self.correlated_symbol = correlated_symbol

    def detect(self) -> list[dict]:
        self.candles = self.candles or self.fetch_data()
        correlated_candles = self.mt5.get_data(self.correlated_symbol, self.timeframe, self.lookback)
        correlated_df = pd.DataFrame(correlated_candles)
        setups = []
        for i in range(2, min(len(self.candles), len(correlated_df)) - 2):
            if (self.candles['high'].iloc[i] > self.candles['high'].iloc[i - 1] and
                correlated_df['high'].iloc[i] < correlated_df['high'].iloc[i - 1]):
                setups.append({
                    'type': 'bearish_smt_divergence',
                    'time': self.candles['time'].iloc[i],
                    'symbol': self.symbol,
                    'correlated_symbol': self.correlated_symbol
                })
            elif (self.candles['low'].iloc[i] < self.candles['low'].iloc[i - 1] and
                  correlated_df['low'].iloc[i] > correlated_df['low'].iloc[i - 1]):
                setups.append({
                    'type': 'bullish_smt_divergence',
                    'time': self.candles['time'].iloc[i],
                    'symbol': self.symbol,
                    'correlated_symbol': self.correlated_symbol
                })
        return setups