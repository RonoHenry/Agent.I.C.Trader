import pandas as pd
import numpy as np
from .base_detector import ICTDetector

class LiquiditySweepLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect Liquidity Sweeps based on ICT concepts.
        Identifies rapid moves through stop-loss zones.
        """
        if not all(col in market_data for col in ["high", "low", "close"]):
            return {"setup": "LiquiditySweep", "confidence": 0.0, "levels": []}

        levels = []
        for i in range(2, len(market_data) - 1):
            if (market_data["high"].iloc[i] > market_data["high"].iloc[i-1] and
                market_data["close"].iloc[i+1] < market_data["low"].iloc[i-1]):
                levels.append({
                    "type": "bearish_sweep",
                    "price": market_data["high"].iloc[i],
                    "index": i,
                    "time": market_data.index[i]
                })
            if (market_data["low"].iloc[i] < market_data["low"].iloc[i-1] and
                market_data["close"].iloc[i+1] > market_data["high"].iloc[i-1]):
                levels.append({
                    "type": "bullish_sweep",
                    "price": market_data["low"].iloc[i],
                    "index": i,
                    "time": market_data.index[i]
                })

        confidence = min(0.75, len(levels) * 0.1) if levels else 0.5
        return {"setup": "LiquiditySweep", "confidence": confidence, "levels": levels}