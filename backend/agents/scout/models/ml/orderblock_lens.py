import pandas as pd
import numpy as np

class OrderBlockLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect Order Blocks based on ICT concepts.
        Identifies high-volume areas with price rejection.
        """
        if not all(col in market_data for col in ["open", "high", "low", "close", "volume"]):
            return {"setup": "OrderBlock", "confidence": 0.0, "levels": []}

        swings = []
        for i in range(2, len(market_data) - 2):
            if (market_data["high"].iloc[i] > market_data["high"].iloc[i-1] and
                market_data["high"].iloc[i] > market_data["high"].iloc[i+1]):
                swings.append(("high", i, market_data["high"].iloc[i]))
            if (market_data["low"].iloc[i] < market_data["low"].iloc[i-1] and
                market_data["low"].iloc[i] < market_data["low"].iloc[i+1]):
                swings.append(("low", i, market_data["low"].iloc[i]))

        levels = []
        for swing_type, idx, price in swings:
            volume = market_data["volume"].iloc[idx]
            if volume > market_data["volume"].rolling(20).mean().iloc[idx] * 1.5:
                levels.append({
                    "type": swing_type,
                    "price": price,
                    "index": idx,
                    "time": market_data.index[idx]
                })

        confidence = min(0.8, len(levels) * 0.1) if levels else 0.5
        return {"setup": "OrderBlock", "confidence": confidence, "levels": levels}