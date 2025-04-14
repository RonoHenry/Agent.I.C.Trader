import pandas as pd
import numpy as np

class SMTDivergenceLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect Smart Money Divergence in ICT.
        Looks for price/RSI divergence.
        """
        if not all(col in market_data for col in ["close"]):
            return {"setup": "SMTDivergence", "confidence": 0.0, "signals": []}

        rsi = market_data["close"].pct_change().rolling(14).mean() * 100
        signals = []
        for i in range(2, len(market_data) - 1):
            if (market_data["close"].iloc[i] > market_data["close"].iloc[i-1] and
                rsi.iloc[i] < rsi.iloc[i-1]):
                signals.append({
                    "type": "bearish_divergence",
                    "index": i,
                    "time": market_data.index[i]
                })
            if (market_data["close"].iloc[i] < market_data["close"].iloc[i-1] and
                rsi.iloc[i] > rsi.iloc[i-1]):
                signals.append({
                    "type": "bullish_divergence",
                    "index": i,
                    "time": market_data.index[i]
                })

        confidence = min(0.75, len(signals) * 0.1) if signals else 0.5
        return {"setup": "SMTDivergence", "confidence": confidence, "signals": signals}