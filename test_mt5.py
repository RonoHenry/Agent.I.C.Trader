import pandas as pd
from pathlib import Path
from ..utils.logger import logging
from ..config.settings import MT5_CONFIG
try:
    import yfinance as yf
except ImportError:
    yf = None

class MT5Client:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.use_yfinance = True  # Toggle for yfinance vs MT5

    def initialize(self):
        if not self.use_yfinance:
            try:
                import MetaTrader5 as mt5
                if not mt5.initialize(**MT5_CONFIG, timeout=30):
                    self.logger.error(f"MT5 init failed: {mt5.last_error()}")
                    raise ConnectionError("MT5 init failed")
                self.logger.info("MT5 connected")
                return True
            except Exception as e:
                self.logger.error(f"MT5 error: {str(e)}")
                raise
        return True

    def get_data(self, symbol: str, timeframe: str, bars: int = 1000) -> pd.DataFrame:
        """
        Fetch OHLCV data using yfinance or MT5.
        Timeframe: M1, M5, M15, M30, H1, H2, H3, H4, H6, H8, H12, D1.
        """
        if self.use_yfinance:
            if not yf:
                raise ImportError("yfinance not installed. Run 'pip install yfinance'")
            try:
                tf_map = {
                    "M1": "1m", "M5": "5m", "M15": "15m", "M30": "30m",
                    "H1": "1h", "H2": "2h", "H3": "3h", "H4": "4h",
                    "H6": "6h", "H8": "8h", "H12": "12h", "D1": "1d"
                }
                if timeframe not in tf_map:
                    raise ValueError(f"Unsupported timeframe: {timeframe}")
                # yfinance uses symbol like EURUSD=X
                yf_symbol = f"{symbol}=X"
                period = "60d" if timeframe in ["M1", "M5", "M15", "M30"] else "730d"
                df = yf.download(yf_symbol, interval=tf_map[timeframe], period=period)
                if df.empty:
                    raise ValueError(f"No data for {symbol} {timeframe}")
                df = df[["Open", "High", "Low", "Close", "Volume"]]
                df.columns = ["open", "high", "low", "close", "volume"]
                df.index.name = "time"
                df = df.tail(bars)
                self.logger.info(f"Fetched {len(df)} bars for {symbol} {timeframe} via yfinance")
                return df
            except Exception as e:
                self.logger.error(f"yfinance error: {str(e)}")
        else:
            try:
                import MetaTrader5 as mt5
                if not hasattr(self, "connected") or not self.connected:
                    self.connected = self.initialize()
                tf_map = {
                    "M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5,
                    "M15": mt5.TIMEFRAME_M15, "M30": mt5.TIMEFRAME_M30,
                    "H1": mt5.TIMEFRAME_H1, "H2": mt5.TIMEFRAME_H2,
                    "H3": mt5.TIMEFRAME_H3, "H4": mt5.TIMEFRAME_H4,
                    "H6": mt5.TIMEFRAME_H6, "H8": mt5.TIMEFRAME_H8,
                    "H12": mt5.TIMEFRAME_H12, "D1": mt5.TIMEFRAME_D1
                }
                if timeframe not in tf_map:
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
                self.logger.info(f"Fetched {len(df)} bars for {symbol} {timeframe} via MT5")
                return df
            except Exception as e:
                self.logger.error(f"MT5 fetch error: {str(e)}")

        # Fallback to CSV
        fallback_path = Path(f"data/market_data/historical/{symbol}_{timeframe}.csv")
        if fallback_path.exists():
            self.logger.info(f"Using fallback: {fallback_path}")
            df = pd.read_csv(fallback_path, parse_dates=["time"], index_col="time")
            return df
        raise ValueError(f"No data available for {symbol} {timeframe}")

    def __del__(self):
        if not self.use_yfinance:
            try:
                import MetaTrader5 as mt5
                if hasattr(self, "connected") and self.connected:
                    mt5.shutdown()
                    self.logger.info("MT5 closed")
            except:
                pass