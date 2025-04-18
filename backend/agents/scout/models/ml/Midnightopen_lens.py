import pandas as pd
from datetime import time
from .base_detector import ICTDetector

class MidnightOpenLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Identify Midnight Open levels for ICT price action.
        Marks daily open at 00:00.
        """
        if not hasattr(market_data.index, "time"):
            return {"setup": "MidnightOpen", "confidence": 0.0, "levels": []}

        levels = []
        for i, timestamp in enumerate(market_data.index):
            if timestamp.time() == time(0, 0):
                levels.append({
                    "price": market_data["open"].iloc[i],
                    "index": i,
                    "time": timestamp
                })

        confidence = 0.6 if levels else 0.5
        return {"setup": "MidnightOpen", "confidence": confidence, "levels": levels}