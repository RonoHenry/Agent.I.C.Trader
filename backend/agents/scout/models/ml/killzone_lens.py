import pandas as pd
from datetime import time
from .base_detector import ICTDetector

class KillzoneLens:
    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect ICT Killzones (high-probability trading times).
        Focuses on London/NY sessions (e.g., 2-5 AM/7-10 AM EST).
        """
        if not hasattr(market_data.index, "time"):
            return {"setup": "Killzone", "confidence": 0.0, "periods": []}

        periods = []
        for i, timestamp in enumerate(market_data.index):
            t = timestamp.time()
            if (time(2, 0) <= t <= time(5, 0)) or (time(7, 0) <= t <= time(10, 0)):
                periods.append({
                    "time": timestamp,
                    "index": i,
                    "session": "London" if t <= time(5, 0) else "New York"
                })

        confidence = min(0.7, len(periods) * 0.05) if periods else 0.5
        return {"setup": "Killzone", "confidence": confidence, "periods": periods}