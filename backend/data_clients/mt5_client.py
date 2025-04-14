import MetaTrader5 as mt5
import pandas as pd
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MT5Client:
    def __init__(self, login, password, server, timeout=30000):
        self.login = login
        self.password = password
        self.server = server
        self.timeout = timeout
        self.connected = False

    def connect(self):
        logger.info(f"Attempting to connect to MT5 with login={self.login}, server={self.server}")
        # Specify the path to the MT5 terminal executable
        terminal_path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"  # Adjust if installed elsewhere
        if not mt5.initialize(login=self.login, password=self.password, server=self.server, timeout=self.timeout, path=terminal_path):
            error_code, error_msg = mt5.last_error()
            logger.error(f"MT5 initialization failed: ({error_code}, '{error_msg}')")
            return False
        if not mt5.login(login=self.login, password=self.password, server=self.server):
            error_code, error_msg = mt5.last_error()
            logger.error(f"MT5 login failed: ({error_code}, '{error_msg}')")
            mt5.shutdown()
            return False
        self.connected = True
        logger.info("MT5 connection successful")
        account_info = mt5.account_info()
        if account_info:
            logger.info(f"Connected to account: {account_info.login}, Broker: {account_info.company}")
        return True

    def disconnect(self):
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logger.info("MT5 connection closed")

    def get_ohlc_data(self, symbol, timeframe, num_candles):
        if not self.connected:
            logger.error("Not connected to MT5")
            return None
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
        if rates is None:
            error_code, error_msg = mt5.last_error()
            logger.error(f"Failed to fetch OHLC data: ({error_code}, '{error_msg}')")
            return None
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df

# Example usage with command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MT5 Client for fetching OHLC data")
    parser.add_argument("--login", type=int, default=102183587, help="MT5 account login number")
    parser.add_argument("--password", type=str, default="8*04M^d?", help="MT5 account password")
    parser.add_argument("--server", type=str, default="FBS-Demo", help="MT5 server name")
    args = parser.parse_args()

    client = MT5Client(login=args.login, password=args.password, server=args.server)
    if client.connect():
        data = client.get_ohlc_data("EURUSD", mt5.TIMEFRAME_M15, 100)
        if data is not None:
            print(data)
        client.disconnect()