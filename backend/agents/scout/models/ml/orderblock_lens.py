import pandas as pd
import numpy as np
from datetime import time
from .base_detector import ICTDetector

class OrderBlockLens:
    def __init__(self):
        self.timeframes = [
            "Quarterly", "Monthly", "Weekly", "Daily",
            "H12", "H8", "H6", "H4", "H3", "H2", "H1", "M30", "M15"
        ]
        self.timeframe_map = {
            "Quarterly": "M1",  # Aggregate M1 for 3 months
            "Monthly": "M1",    # Aggregate M1 for 1 month
            "Weekly": "M1",     # Aggregate M1 for 1 week
            "Daily": "D1",
            "H12": "H12", "H8": "H8", "H6": "H6", "H4": "H4",
            "H3": "H3", "H2": "H2", "H1": "H1", "M30": "M30", "M15": "M15"
        }

    def calculate_equilibrium(self, data: pd.DataFrame) -> pd.Series:
        """Calculate VWAP for premium/discount zones."""
        return ((data["high"] + data["low"] + data["close"]) / 3 * data["volume"]).cumsum() / data["volume"].cumsum()

    def detect_liquidity(self, data: pd.DataFrame) -> list:
        """Identify swing highs/lows for liquidity pools."""
        swings = []
        for i in range(2, len(data) - 2):
            if (data["high"].iloc[i] > data["high"].iloc[i-1] and
                data["high"].iloc[i] > data["high"].iloc[i+1]):
                swings.append(("high", i, data["high"].iloc[i]))
            if (data["low"].iloc[i] < data["low"].iloc[i-1] and
                data["low"].iloc[i] < data["low"].iloc[i+1]):
                swings.append(("low", i, data["low"].iloc[i]))
        return swings

    def power_of_3_phase(self, data: pd.DataFrame, idx: int) -> str:
        """Determine Power of 3 phase."""
        if idx < 20:
            return "Unknown"
        range_bound = (data["high"].iloc[idx-20:idx].max() - data["low"].iloc[idx-20:idx].min()) / data["close"].iloc[idx]
        if range_bound < 0.01:
            return "Accumulation"
        elif data["close"].iloc[idx] < data["low"].iloc[idx-1]:
            return "Manipulation"
        else:
            return "Distribution"

    def amdx_xamd_cycle(self, data: pd.DataFrame, idx: int) -> str:
        """Identify AMDX (bullish) or XAMD (bearish) cycle."""
        if idx < 20:
            return "Unknown"
        trend = data["close"].iloc[idx] - data["close"].iloc[idx-20]
        if trend > 0:
            return "AMDX"
        elif trend < 0:
            return "XAMD"
        return "Neutral"

    def predict(self, market_data: pd.DataFrame) -> dict:
        """
        Detect Order Blocks using a top-down approach across timeframes.
        Considers Time, Premium/Discount, Liquidity, Power of 3, AMDX/XAMD.
        """
        if not all(col in market_data for col in ["open", "high", "low", "close", "volume"]):
            return {"setup": "OrderBlock", "confidence": 0.0, "levels": []}

        results = []
        for tf in self.timeframes:
            # Simulate timeframe data (in practice, fetch via MT5)
            data = market_data.copy()  # Placeholder; real MT5 data would be resampled
            vwap = self.calculate_equilibrium(data)
            swings = self.detect_liquidity(data)

            levels = []
            for swing_type, idx, price in swings:
                # Time: Check if in high-probability session
                is_killzone = False
                if hasattr(data.index, "time"):
                    t = data.index[idx].time()
                    is_killzone = (time(2, 0) <= t <= time(5, 0)) or (time(7, 0) <= t <= time(10, 0))

                # Premium/Discount
                is_premium = price > vwap.iloc[idx]
                is_discount = price < vwap.iloc[idx]

                # Liquidity: High volume confirms swing
                volume = data["volume"].iloc[idx]
                is_liquid = volume > data["volume"].rolling(20).mean().iloc[idx] * 1.5

                # Power of 3
                po3_phase = self.power_of_3_phase(data, idx)

                # AMDX/XAMD
                cycle = self.amdx_xamd_cycle(data, idx)

                # Order Block logic
                if is_liquid and (is_premium or is_discount):
                    level = {
                        "timeframe": tf,
                        "type": swing_type,
                        "price": price,
                        "index": idx,
                        "time": data.index[idx],
                        "premium": is_premium,
                        "discount": is_discount,
                        "killzone": is_killzone,
                        "power_of_3": po3_phase,
                        "cycle": cycle,
                        "executable": tf == "M15"
                    }
                    levels.append(level)

            results.extend(levels)

        confidence = min(0.9, len(results) * 0.05) if results else 0.5
        return {"setup": "OrderBlock", "confidence": confidence, "levels": results}