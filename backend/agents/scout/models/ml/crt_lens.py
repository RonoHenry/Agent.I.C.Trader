import pandas as pd
import numpy as np

class CRTLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect Central Range Theory zones in ICT.
        Identifies mean-reverting price zones.
        """
        if not all(col in market_data for col in ["open", "close"]):
            return {"setup": "CRT", "confidence": 0.0, "zones": []}

        zones = []
        mean_price = market_data[["open", "close"]].mean(axis=1).rolling(20).mean()
        for i in range(20, len(market_data)):
            if abs(market_data["close"].iloc[i] - mean_price.iloc[i]) < mean_price.iloc[i] * 0.01:
                zones.append({
                    "price": mean_price.iloc[i],
                    "index": i,
                    "time": market_data.index[i]
                })

        confidence = min(0.7, len(zones) * 0.05) if zones else 0.5
        return {"setup": "CRT", "confidence": confidence, "zones": zones}