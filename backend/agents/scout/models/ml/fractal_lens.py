import pandas as pd
import numpy as np
from .base_detector import ICTDetector

class FractalLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect Fractal patterns for ICT structure analysis.
        """
        if not all(col in market_data for col in ["high", "low"]):
            return {"setup": "Fractal", "confidence": 0.0, "points": []}

        points = []
        for i in range(2, len(market_data) - 2):
            if (market_data["high"].iloc[i] > market_data["high"].iloc[i-2:i].max() and
                market_data["high"].iloc[i] > market_data["high"].iloc[i+1:i+3].max()):
                points.append({
                    "type": "fractal_high",
                    "price": market_data["high"].iloc[i],
                    "index": i,
                    "time": market_data.index[i]
                })
            if (market_data["low"].iloc[i] < market_data["low"].iloc[i-2:i].min() and
                market_data["low"].iloc[i] < market_data["low"].iloc[i+1:i+3].min()):
                points.append({
                    "type": "fractal_low",
                    "price": market_data["low"].iloc[i],
                    "index": i,
                    "time": market_data.index[i]
                })

        confidence = min(0.8, len(points) * 0.1) if points else 0.5
        return {"setup": "Fractal", "confidence": confidence, "points": points}