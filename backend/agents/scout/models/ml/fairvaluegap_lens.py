# backend/agents/scout/models/fvg_detector.py
import numpy as np

def detect_fvg(candles):
    for i in range(1, len(candles) - 1):
        prev_candle = candles[i - 1]
        curr_candle = candles[i]
        next_candle = candles[i + 1]
        # FVG: Gap between prev high and next low (bullish) or prev low and next high (bearish)
        if prev_candle["high"] < next_candle["low"] and curr_candle["close"] > prev_candle["high"]:
            return {"type": "Bullish FVG", "level": (prev_candle["high"], next_candle["low"]), "confidence": 0.85}
        elif prev_candle["low"] > next_candle["high"] and curr_candle["close"] < prev_candle["low"]:
            return {"type": "Bearish FVG", "level": (next_candle["high"], prev_candle["low"]), "confidence": 0.85}
    return None