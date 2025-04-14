import pandas as pd
from datetime import time

class Ny08_30PenLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Identify NY 8:30 AM open levels for ICT price action.
        """
        if not hasattr(market_data.index, "time"):
            return {"setup": "Ny08_30Pen", "confidence": 0.0, "levels": []}

        levels = []
        for i, timestamp in enumerate(market_data.index):
            if timestamp.time() == time(8, 30):
                levels.append({
                    "price": market_data["open"].iloc[i],
                    "index": i,
                    "time": timestamp
                })

        confidence = 0.65 if levels else 0.5
        return {"setup": "Ny08_30Pen", "confidence": confidence, "levels": levels}