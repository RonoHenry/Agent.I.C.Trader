import unittest
from backend.utils.mt5_client import MT5Client
import MetaTrader5 as mt5
import argparse

class TestMT5Client(unittest.TestCase):
    def setUp(self):
        parser = argparse.ArgumentParser(description="MT5 Client Test")
        parser.add_argument("--login", type=int, default=102183587, help="MT5 account login number")
        parser.add_argument("--password", type=str, default="8*04M^d?", help="MT5 account password")
        parser.add_argument("--server", type=str, default="FBS-Demo", help="MT5 server name")
        args = parser.parse_args()

        self.client = MT5Client(login=args.login, password=args.password, server=args.server)

    def test_connect(self):
        self.assertTrue(self.client.connect(), "Failed to connect to MT5")
        self.assertTrue(self.client.connected, "Client not marked as connected")

    def test_get_ohlc_data(self):
        self.assertTrue(self.client.connect(), "Failed to connect to MT5")
        data = self.client.get_ohlc_data("EURUSD", mt5.TIMEFRAME_M15, 10)
        self.assertIsNotNone(data, "Failed to fetch OHLC data")
        self.assertEqual(len(data), 10, "Incorrect number of candles fetched")
        self.assertTrue('time' in data.columns, "Time column missing in OHLC data")
        self.client.disconnect()

    def tearDown(self):
        self.client.disconnect()

if __name__ == "__main__":
    unittest.main()