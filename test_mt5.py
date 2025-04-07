from backend.config.groq_config import settings
import MetaTrader5 as mt5

print("Starting MT5 test")

# Initialize MT5
if not mt5.initialize():
    print(f"Initialization failed: {mt5.last_error()}")
    quit()
print("MT5 initialized")

# Login to MT5 using settings
if not mt5.login(settings.MT5_LOGIN, settings.MT5_PASSWORD, settings.MT5_SERVER):
    print(f"Login failed: {mt5.last_error()}")
    quit()
print("Logged in")

# Print account info
account_info = mt5.account_info()
if account_info is None:
    print(f"Failed to retrieve account info: {mt5.last_error()}")
else:
    print(f"Account Info: {account_info}")

# Shutdown MT5
mt5.shutdown()