import MetaTrader5 as mt5
import pandas as pd
from ..utils.logger import logging
from ..config.settings import MT5_CONFIG

class MT5Client:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.connected = False
        self.initialize()

    def initialize(self):
        try:
            if not mt5.initialize(**MT5_CONFIG, timeout=30):
                self.logger.error(f"MT5 init failed: {mt5.last_error()}")
                raise ConnectionError("MT5 init failed")
            self.connected = True
            self.logger.info("MT5 connected")
        except Exception as e:
            self.logger.error(f"MT5 error: {str(e)}")
            raise

    def get_data(self, symbol: str, timeframe: str, bars: int = 1000) -> pd.DataFrame:
        if not self.connected:
            self.initialize()
        try:
            timeframe_map = {
                "M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5,
                "H1": mt5.TIMEFRAME_H1, "H4": mt5.TIMEFRAME_H4, "D1": mt5.TIMEFRAME_D1
            }
            if timeframe not in timeframe_map:
                raise ValueError(f"Unsupported timeframe: {timeframe}")
            if not mt5.symbol_select(symbol, True):
                self.logger.error(f"Symbol {symbol} not available")
                raise ValueError(f"Symbol {symbol} not available")
            rates = mt5.copy_rates_from_pos(symbol, timeframe_map[timeframe], 0, bars)
            if rates is None or len(rates) == 0:
                self.logger.error(f"No data for {symbol} {timeframe}")
                raise ValueError("No data returned")
            df = pd.DataFrame(rates)
            df["time"] = pd.to_datetime(df["time"], unit="s")
            df.set_index("time", inplace=True)
            df = df[["open", "high", "low", "close", "tick_volume"]]
            df.rename(columns={"tick_volume": "volume"}, inplace=True)
            self.logger.info(f"Fetched {len(df)} bars for {symbol} {timeframe}")
            return df
        except Exception as e:
            self.logger.error(f"MT5 fetch error: {str(e)}")
            raise

    def __del__(self):
        if self.connected:
            mt5.shutdown()
            self.logger.info("MT5 closed")