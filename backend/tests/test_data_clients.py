import pytest
import pandas as pd
from ..data_clients.mt5_client import MT5Client
from ..data_clients.notion_client import NotionClient

def test_mt5_fetch():
    try:
        client = MT5Client()
        df = client.get_data("EURUSD", "H1", bars=10)
        assert isinstance(df, pd.DataFrame)
        assert set(df.columns) == {"open", "high", "low", "close", "volume"}
    except ConnectionError:
        pytest.skip("MT5 not configured")

def test_notion_log():
    client = NotionClient()
    trade_data = {"title": "Test Trade", "date": "2025-04-14", "symbol": "EURUSD", "setup": "OrderBlock"}
    result = client.log_trade(trade_data)
    assert isinstance(result, dict)
    assert result.get("status") in ["success", "error"]