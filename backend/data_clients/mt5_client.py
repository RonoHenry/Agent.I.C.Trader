import pandas as pd
from pathlib import Path
try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None
try:
    from backend.utils.logger import logging
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)

class MT5Client:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.connected = False

    def initialize(self):
        if not mt5:
            self.logger.error("MetaTrader5 not installed")
            raise ImportError("MetaTrader5 not installed")
        if not mt5.initialize():
            error = mt5.last_error()
            self.logger.error(f"MT5 init failed: {error}")
            raise ConnectionError(f"MT5 init failed: {error}")
        self.connected = True
        self.logger.info("MT5 connected via terminal")

    def get_data(self, symbol: str, timeframe: str, bars: int = 1000) -> pd.DataFrame:
        if not self.connected:
            self.initialize()
        try:
            tf_map = {
                "M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5,
                "M15": mt5.TIMEFRAME_M15, "M30": mt5.TIMEFRAME_M30,
                "H1": mt5.TIMEFRAME_H1, "H2": mt5.TIMEFRAME_H2,
                "H3": mt5.TIMEFRAME_H3, "H4": mt5.TIMEFRAME_H4,
                "H6": mt5.TIMEFRAME_H6, "H8": mt5.TIMEFRAME_H8,
                "H12": mt5.TIMEFRAME_H12, "D1": mt5.TIMEFRAME_D1
            }
            if timeframe not in tf_map:
                self.logger.error(f"Unsupported timeframe: {timeframe}")
                raise ValueError(f"Unsupported timeframe: {timeframe}")
            if not mt5.symbol_select(symbol, True):
                self.logger.error(f"Symbol {symbol} not available")
                raise ValueError(f"Symbol {symbol} not available")
            rates = mt5.copy_rates_from_pos(symbol, tf_map[timeframe], 0, bars)
            if rates is None or len(rates) == 0:
                self.logger.error(f"No data for {symbol} {timeframe}")
                raise ValueError("No data returned")
            df = pd.DataFrame(rates)
            df["time"] = pd.to_datetime(df["time"], unit="s")
            df.set_index("time", inplace=True)
            df = df[["open", "high", "low", "close", "tick_volume"]]
            df.rename(columns={"tick_volume": "volume"}, inplace=True)
            if timeframe in ["Quarterly", "Monthly", "Weekly"]:
                rule = "3M" if timeframe == "Quarterly" else "M" if timeframe == "Monthly" else "W"
                df = df.resample(rule).agg({
                    "open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"
                }).dropna()
            self.logger.info(f"Fetched {len(df)} bars for {symbol} {timeframe}")
            return df
        except Exception as e:
            self.logger.error(f"MT5 fetch error: {str(e)}")
            raise
        finally:
            if self.connected:
                mt5.shutdown()
                self.connected = False
                self.logger.info("MT5 closed")