import pandas as pd
from .base_detector import ICTDetector

class OpeningGapsLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect market opening gaps for ICT setups.
        """
        if not all(col in market_data for col in ["open", "close"]):
            return {"setup": "OpeningGaps", "confidence": 0.0, "gaps": []}

        gaps = []
        for i in range(1, len(market_data)):
            if abs(market_data["open"].iloc[i] - market_data["close"].iloc[i-1]) > 0:
                gaps.append({
                    "type": "up_gap" if market_data["open"].iloc[i] > market_data["close"].iloc[i-1] else "down_gap",
                    "start_price": market_data["close"].iloc[i-1],
                    "end_price": market_data["open"].iloc[i],
                    "index": i,
                    "time": market_data.index[i]
                })

        confidence = min(0.7, len(gaps) * 0.05) if gaps else 0.5
        return {"setup": "OpeningGaps", "confidence": confidence, "gaps": gaps}