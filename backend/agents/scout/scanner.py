import pandas as pd
from pathlib import Path
from ...data_clients.mt5_client import MT5Client
from ...utils.preprocessor import preprocess_mt5_data
from .models.ml.orderblock_lens import OrderBlockLens
from .models.ml.fairvaluegap_lens import FairValueGapLens
from .models.ml.killzone_lens import KillzoneLens
from .models.ml.liquiditysweep_lens import LiquiditySweepLens
from .models.ml.Candleprofile_lens import CandleProfileLens
from .models.ml.Midnightopen_lens import MidnightOpenLens
from .models.ml.Ny08_30pen_lens import Ny08_30PenLens
from .models.ml.breakerblock_lens import BreakerBlockLens
from .models.ml.cotreport_lens import COTReportLens
from .models.ml.crt_lens import CRTLens
from .models.ml.fractal_lens import FractalLens
from .models.ml.ict_ensemble_lens import ICTEnsembleLens
from .models.ml.inversionfvg_lens import InversionFVGLens
from .models.ml.opening_gaps_lens import OpeningGapsLens
from .models.ml.ote_lens import OTELens
from .models.ml.powerof3_lens import PowerOf3Lens
from .models.ml.quarterly_theory_lens import QuarterlyTheoryLens
from .models.ml.seasonaltendency_lens import SeasonalTendencyLens
from .models.ml.smtdivergence_lens import SMTDivergenceLens
from .models.ml.std_projection_lens import StdProjectionLens
from .models.dspy.setup_lens import ICTSetupLens

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

    def scan(self, symbol: str, timeframe: str) -> dict:
        market_data = self.fetch_mt5_data(symbol, timeframe)
        market_data = preprocess_mt5_data(market_data)
        ml_results = {name: lens.predict(market_data) for name, lens in self.ml_lenses.items()}
        dspy_results = {setup: self.dspy_lens(market_data, setup) for setup in ml_results}
        return self.combine_results(ml_results, dspy_results)

    def fetch_mt5_data(self, symbol: str, timeframe: str) -> pd.DataFrame:
        try:
            client = MT5Client()
            return client.get_data(symbol, timeframe, bars=1000)
        except Exception as e:
            print(f"MT5 error: {str(e)}")
            fallback_path = Path(f"data/market_data/historical/{symbol}_{timeframe}.csv")
            if fallback_path.exists():
                print(f"Using fallback: {fallback_path}")
                return pd.read_csv(fallback_path, parse_dates=["time"], index_col="time")
            raise

    def combine_results(self, ml_results: dict, dspy_results: dict) -> dict:
        combined = {}
        for setup in ml_results:
            ml_conf = ml_results[setup].get("confidence", 0.5)
            dspy_conf = dspy_results[setup].get("confidence", 0.5)
            combined[setup] = {
                "ml": ml_results[setup],
                "dspy": dspy_results[setup],
                "confidence": 0.5 * ml_conf + 0.5 * dspy_conf
            }
        return combined