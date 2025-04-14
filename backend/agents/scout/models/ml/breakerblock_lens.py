import pandas as pd
import numpy as np

class BreakerBlockLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect Breaker Blocks in ICT framework.
        Identifies failed Order Blocks that turn into support/resistance.
        """
        if not all(col in market_data for col in ["high", "low", "close"]):
            return {"setup": "BreakerBlock", "confidence": 0.0, "levels": []}

        levels = []
        for i in range(3, len(market_data) - 1):
            if (market_data["low"].iloc[i-1] < market_data["low"].iloc[i-2] and
                market_data["close"].iloc[i] > market_data["high"].iloc[i-1]):
                levels.append({
                    "type": "bullish_breaker",
                    "price": market_data["low"].iloc[i-1],
                    "index": i,
                    "time": market_data.index[i]
                })
            if (market_data["high"].iloc[i-1] > market_data["high"].iloc[i-2] and
                market_data["close"].iloc[i] < market_data["low"].iloc[i-1]):
                levels.append({
                    "type": "bearish_breaker",
                    "price": market_data["high"].iloc[i-1],
                    "index": i,
                    "time": market_data.index[i]
                })

        confidence = min(0.75, len(levels) * 0.1) if levels else 0.5
        return {"setup": "BreakerBlock", "confidence": confidence, "levels": levels}