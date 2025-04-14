from fastapi import FastAPI
from ..agents.scout.scanner import Scanner

app = FastAPI()

@app.get("/scan/{symbol}/{timeframe}")
async def scan_market(symbol: str, timeframe: str):
    scanner = Scanner()
    try:
        results = scanner.scan(symbol, timeframe)
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}