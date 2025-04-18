import pandas as pd
from pathlib import Path
from backend.data_clients.mt5_client import MT5Client
from backend.utils.preprocessor import preprocess_mt5_data
from backend.llm.gemini_client import GeminiClient
from backend.llm.prompts import get_ict_prompt
from backend.agents.scout.models.ml.orderblock_lens import OrderBlockDetector
from backend.agents.scout.models.ml.fairvaluegap_lens import FVGDetector
from backend.agents.scout.models.ml.killzone_lens import KillzoneDetector
from backend.agents.scout.models.ml.liquiditysweep_lens import LiquiditySweepDetector
from backend.agents.scout.models.ml.candleprofile_lens import ProfileDetector
from backend.agents.scout.models.ml.open_lens import OpenDetector
from backend.agents.scout.models.ml.breakerblock_lens import BreakerDetector
from backend.agents.scout.models.ml.cot_lens import COTDetector
from backend.agents.scout.models.ml.crt_lens import CRTDetector
from backend.agents.scout.models.ml.fractal_lens import FractalDetector
from backend.agents.scout.models.ml.inversionfvg_lens import ImpliedFVGDetector
from backend.agents.scout.models.ml.gap_lens import GapDetector
from backend.agents.scout.models.ml.ote_lens import OTEDetector
from backend.agents.scout.models.ml.powerof3_lens import PowerOfThreeDetector
from backend.agents.scout.models.ml.quarterly_lens import QuarterlyDetector
from backend.agents.scout.models.ml.seasonal_lens import SeasonalDetector
from backend.agents.scout.models.ml.smtdivergence_lens import SMTDivergenceDetector
from backend.agents.scout.models.ml.stddev_lens import StdDevDetector
from backend.agents.scout.models.ml.ict_ensemble_lens import ICTEnsemble
from backend.agents.scout.models.dspy.setup_lens import ICTSetupLens
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scanner:
    def __init__(self, symbol: str = "EURUSD", timeframe: str = "H1"):
        self.symbol = symbol
        self.timeframe = timeframe
        self.lenses = {
            "OrderBlock": OrderBlockDetector(symbol, timeframe),
            "FairValueGap": FVGDetector(symbol, timeframe),
            "Killzone": KillzoneDetector(symbol, timeframe),
            "LiquiditySweep": LiquiditySweepDetector(symbol, timeframe),
            "CandleProfile": ProfileDetector(symbol, timeframe),
            "Open": OpenDetector(symbol, timeframe),
            "BreakerBlock": BreakerDetector(symbol, timeframe),
            "COT": COTDetector(symbol, timeframe),
            "CRT": CRTDetector(symbol, timeframe),
            "Fractal": FractalDetector(symbol, timeframe),
            "InversionFVG": ImpliedFVGDetector(symbol, timeframe, higher_timeframe="H4"),
            "Gap": GapDetector(symbol, timeframe),
            "OTE": OTEDetector(symbol, timeframe),
            "PowerOf3": PowerOfThreeDetector(symbol, timeframe),
            "Quarterly": QuarterlyDetector(symbol, timeframe),
            "Seasonal": SeasonalDetector(symbol, timeframe),
            "SMTDivergence": SMTDivergenceDetector(symbol, correlated_symbol="GBPUSD", timeframe=timeframe),
            "StdDev": StdDevDetector(symbol, timeframe),
            "ICTEnsemble": ICTEnsemble(symbol, timeframe),
        }
        self.dspy_lens = ICTSetupLens()
        self.gemini = GeminiClient()
        logger.info("Scanner initialized with lenses, DSPy, and Gemini")

    def scan(self, symbol: str = None, timeframe: str = None, count: int = 1000, concepts: list = None) -> dict:
        """Scan market data for ICT setups using lenses, DSPy, and Gemini."""
        symbol = symbol or self.symbol
        timeframe = timeframe or self.timeframe
        if concepts is None:
            concepts = ["Fair Value Gap", "Order Block", "Killzone"]

        # Fetch and preprocess MT5 data
        market_data = self.fetch_mt5_data(symbol, timeframe, count)
        market_data = preprocess_mt5_data(market_data)

        # Run lenses
        lens_results = {}
        for name, lens in self.lenses.items():
            try:
                lens.candles = market_data  # Inject preprocessed data
                lens_results[name] = lens.detect()
            except Exception as e:
                logger.error(f"Error in {name} lens: {str(e)}")
                lens_results[name] = []

        # Run DSPy lens (assuming it processes lens outputs)
        dspy_results = {setup: self.dspy_lens(market_data, setup) for setup in lens_results}

        # Run Gemini analysis
        gemini_results = {}
        try:
            data_str = market_data.tail(5).to_string()
            prompt = get_ict_prompt(data_str, concepts, lens_results)
            gemini_response = self.gemini.generate_content(prompt)
            gemini_results = {"Gemini": {"analysis": gemini_response, "confidence": 0.7}}  # Placeholder confidence
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            gemini_results = {"Gemini": {"error": str(e), "confidence": 0.0}}

        # Combine results
        return self.combine_results(lens_results, dspy_results, gemini_results)

    def fetch_mt5_data(self, symbol: str, timeframe: str, count: int = 1000) -> pd.DataFrame:
        """Fetch MT5 data with CSV fallback."""
        try:
            client = MT5Client()
            return client.get_data(symbol, timeframe, count)
        except Exception as e:
            logger.error(f"MT5 error: {str(e)}")
            fallback_path = Path(f"data/market_data/historical/{symbol}_{timeframe}.csv")
            if fallback_path.exists():
                logger.info(f"Using fallback: {fallback_path}")
                return pd.read_csv(fallback_path, parse_dates=["time"], index_col="time")
            raise

    def combine_results(self, lens_results: dict, dspy_results: dict, gemini_results: dict) -> dict:
        """Combine lens, DSPy, and Gemini results with weighted confidence."""
        combined = {}
        for setup in lens_results:
            lens_conf = len(lens_results[setup]) > 0 if lens_results[setup] else 0.5  # Simplified confidence
            dspy_conf = dspy_results[setup].get("confidence", 0.5)
            gemini_conf = gemini_results.get("Gemini", {}).get("confidence", 0.5)
            combined[setup] = {
                "lens": lens_results[setup],
                "dspy": dspy_results[setup],
                "gemini": gemini_results.get("Gemini", {"analysis": "N/A", "confidence": 0.0}),
                "confidence": (lens_conf + dspy_conf + gemini_conf) / 3
            }
        return combined

if __name__ == "__main__":
    scanner = Scanner()
    result = scanner.scan(count=100, concepts=["Fair Value Gap"])
    print(result)