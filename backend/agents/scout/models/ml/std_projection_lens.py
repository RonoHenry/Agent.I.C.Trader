import pandas as pd
import numpy as np

class StdProjectionLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Calculate standard price projections in ICT.
        Uses volatility-based targets.
        """
        if not all(col in market_data for col in ["close"]):
            return {"setup": "StdProjection", "confidence": 0.0, "targets": []}

        targets = []
        volatility = market_data["close"].pct_change().rolling(20).std()
        for i in range(20, len(market_data)):
            target = market_data["close"].iloc[i] * (1 + volatility.iloc[i])
            targets.append({
                "target_price": target,
                "index": i,
                "time": market_data.index[i]
            })

        confidence = 0.7 if targets else 0.5
        return {"setup": "StdProjection", "confidence": confidence, "targets": targets}