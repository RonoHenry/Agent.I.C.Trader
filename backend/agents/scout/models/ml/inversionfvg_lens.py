from .base_detector import ICTDetector
import pandas as pd

class ImpliedFVGDetector(ICTDetector):
    def __init__(self, symbol: str, timeframe: str, higher_timeframe: str, lookback: int = 100):
        super().__init__(symbol, timeframe, lookback)
        self.higher_timeframe = higher_timeframe

    def detect(self) -> list[dict]:
        higher_candles = self.mt5.get_data(self.symbol, self.higher_timeframe, self.lookback)
        higher_df = pd.DataFrame(higher_candles)
        fvgs = []
        for i in range(2, len(higher_df)):
            candle_1 = higher_df.iloc[i - 2]
            candle_3 = higher_df.iloc[i]
            if candle_1['high'] < candle_3['low']:
                fvgs.append({'type': 'bearish_ifvg', 'range': (candle_1['high'], candle_3['low'])})
            elif candle_1['low'] > candle_3['high']:
                fvgs.append({'type': 'bullish_ifvg', 'range': (candle_3['high'], candle_1['low'])})
        self.candles = self.candles or self.fetch_data()
        setups = []
        for fvg in fvgs:
            fvg_range = fvg['range']
            for i in range(len(self.candles)):
                candle = self.candles.iloc[i]
                if fvg_range[0] <= candle['high'] and candle['low'] <= fvg_range[1]:
                    setups.append({
                        'type': fvg['type'],
                        'time': candle['time'],
                        'range': fvg_range
                    })
                    break
        return setups