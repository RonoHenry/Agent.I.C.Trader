# mt5_test.py
import MetaTrader5 as mt5

print("Starting MT5 test")
if not mt5.initialize():
    print(f"Init failed: {mt5.last_error()}")
    quit()
print("MT5 initialized")
if not mt5.login(101305635, "]bb1Xj2/", "FBS-Demo1"):  # Try variant
    print(f"Login failed: {mt5.last_error()}")
    quit()
print("Logged in")
print(f"Account Info: {mt5.account_info()}")
mt5.shutdown()