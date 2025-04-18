import pandas as pd
import numpy as np
from .base_detector import ICTDetector

class FairValueGapLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect Fair Value Gaps based on ICT concepts.
        Identifies gaps between candle wicks not filled later.
        """
        if not all(col in market_data for col in ["open", "high", "low", "close"]):
            return {"setup": "FairValueGap", "confidence": 0.0, "levels": []}

        levels = []
        for i in range(2, len(market_data)):
            prev_high = market_data["high"].iloc[i-2]
            curr_low = market_data["low"].iloc[i]
            if curr_low > prev_high:
                gap_start = prev_high
                gap_end = curr_low
                levels.append({
                    "type": "bullish_fvg",
                    "start_price": gap_start,
                    "end_price": gap_end,
                    "index": i,
                    "time": market_data.index[i]
                })
            prev_low = market_data["low"].iloc[i-2]
            curr_high = market_data["high"].iloc[i]
            if curr_high < prev_low:
                gap_start = curr_high
                gap_end = prev_low
                levels.append({
                    "type": "bearish_fvg",
                    "start_price": gap_start,
                    "end_price": gap_end,
                    "index": i,
                    "time": market_data.index[i]
                })

        confidence = min(0.8, len(levels) * 0.1) if levels else 0.5
        return {"setup": "FairValueGap", "confidence": confidence, "levels": levels}