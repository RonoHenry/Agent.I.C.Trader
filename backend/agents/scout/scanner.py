import pandas as pd
from pathlib import Path
from backend.data_clients.mt5_client import MT5Client
from backend.utils.preprocessor import preprocess_mt5_data
from backend.llm.gemini_client import GeminiClient
from backend.llm.prompts import get_ict_prompt
from backend.agents.scout.models.ml.orderblock_lens import OrderBlockLens
from backend.agents.scout.models.ml.fairvaluegap_lens import FairValueGapLens
from backend.agents.scout.models.ml.killzone_lens import KillzoneLens
from backend.agents.scout.models.ml.liquiditysweep_lens import LiquiditySweepLens
from backend.agents.scout.models.ml.Candleprofile_lens import CandleProfileLens
from backend.agents.scout.models.ml.Midnightopen_lens import MidnightOpenLens
from backend.agents.scout.models.ml.Ny08_30pen_lens import Ny08_30PenLens
from backend.agents.scout.models.ml.breakerblock_lens import BreakerBlockLens
from backend.agents.scout.models.ml.cotreport_lens import COTReportLens
from backend.agents.scout.models.ml.crt_lens import CRTLens
from backend.agents.scout.models.ml.fractal_lens import FractalLens
from backend.agents.scout.models.ml.ict_ensemble_lens import ICTEnsembleLens
from backend.agents.scout.models.ml.inversionfvg_lens import InversionFVGLens
from backend.agents.scout.models.ml.opening_gaps_lens import OpeningGapsLens
from backend.agents.scout.models.ml.ote_lens import OTELens
from backend.agents.scout.models.ml.powerof3_lens import PowerOf3Lens
from backend.agents.scout.models.ml.quarterly_theory_lens import QuarterlyTheoryLens
from backend.agents.scout.models.ml.seasonaltendency_lens import SeasonalTendencyLens
from backend.agents.scout.models.ml.smtdivergence_lens import SMTDivergenceLens
from backend.agents.scout.models.ml.std_projection_lens import StdProjectionLens
from backend.agents.scout.models.dspy.setup_lens import ICTSetupLens
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scanner:
    def __init__(self):
        self.ml_lenses = {
            "OrderBlock": OrderBlockLens(),
            "FairValueGap": FairValueGapLens(),
            "Killzone": KillzoneLens(),
            "LiquiditySweep": LiquiditySweepLens(),
            "CandleProfile": CandleProfileLens(),
            "MidnightOpen": MidnightOpenLens(),
            "Ny08_30Pen": Ny08_30PenLens(),
            "BreakerBlock": BreakerBlockLens(),
            "COTReport": COTReportLens(),
            "CRT": CRTLens(),
            "Fractal": FractalLens(),
            "ICTEnsemble": ICTEnsembleLens(),
            "InversionFVG": InversionFVGLens(),
            "OpeningGaps": OpeningGapsLens(),
            "OTE": OTELens(),
            "PowerOf3": PowerOf3Lens(),
            "QuarterlyTheory": QuarterlyTheoryLens(),
            "SeasonalTendency": SeasonalTendencyLens(),
            "SMTDivergence": SMTDivergenceLens(),
            "StdProjection": StdProjectionLens(),
        }
        self.dspy_lens = ICTSetupLens()
        self.gemini = GeminiClient()
        logger.info("Scanner initialized with ML, DSPy, and Gemini")

    def scan(self, symbol: str, timeframe: str, count: int = 1000, concepts: list = None) -> dict:
        """Scan market data for ICT setups using ML, DSPy, and Gemini."""
        if concepts is None:
            concepts = ["Fair Value Gap", "Order Block", "Killzone"]

        # Fetch and preprocess MT5 data
        market_data = self.fetch_mt5_data(symbol, timeframe, count)
        market_data = preprocess_mt5_data(market_data)

        # Run ML lenses
        ml_results = {name: lens.predict(market_data) for name, lens in self.ml_lenses.items()}

        # Run DSPy lens
        dspy_results = {setup: self.dspy_lens(market_data, setup) for setup in ml_results}

        # Run Gemini analysis
        gemini_results = {}
        try:
            data_str = market_data.tail(5).to_string()
            prompt = get_ict_prompt(data_str, concepts)
            gemini_response = self.gemini.generate_content(prompt)
            gemini_results = {"Gemini": {"analysis": gemini_response, "confidence": 0.7}}  # Placeholder confidence
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            gemini_results = {"Gemini": {"error": str(e), "confidence": 0.0}}

        # Combine results
        return self.combine_results(ml_results, dspy_results, gemini_results)

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

    def combine_results(self, ml_results: dict, dspy_results: dict, gemini_results: dict) -> dict:
        """Combine ML, DSPy, and Gemini results with weighted confidence."""
        combined = {}
        for setup in ml_results:
            ml_conf = ml_results[setup].get("confidence", 0.5)
            dspy_conf = dspy_results[setup].get("confidence", 0.5)
            gemini_conf = gemini_results.get("Gemini", {}).get("confidence", 0.5)
            combined[setup] = {
                "ml": ml_results[setup],
                "dspy": dspy_results[setup],
                "gemini": gemini_results.get("Gemini", {"analysis": "N/A", "confidence": 0.0}),
                "confidence": (ml_conf + dspy_conf + gemini_conf) / 3  # Equal weighting
            }
        return combined

if __name__ == "__main__":
    scanner = Scanner()
    result = scanner.scan(symbol="EURUSD", timeframe="H1", count=100, concepts=["Fair Value Gap"])
    print(result)