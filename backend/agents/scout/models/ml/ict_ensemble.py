from .orderblock_lens import OrderBlockDetector
from .fairvaluegap_lens import FVGDetector
from .liquiditysweep_lens import LiquiditySweepDetector
from .powerof3_lens import PowerOfThreeDetector
from .crt_lens import CRTDetector

class ICTEnsemble:
    def __init__(self, symbol: str, timeframe: str, lookback: int = 100):
        self.symbol = symbol
        self.timeframe = timeframe
        self.lookback = lookback
        self.detectors = {
            'ob': OrderBlockDetector(symbol, timeframe, lookback),
            'fvg': FVGDetector(symbol, timeframe, lookback),
            'liquidity': LiquiditySweepDetector(symbol, timeframe, lookback),
            'po3': PowerOfThreeDetector(symbol, timeframe, lookback),
            'crt': CRTDetector(symbol, timeframe, lookback),
        }

    def _calculate_ped(self, swing_high: float, swing_low: float) -> dict:
        mid = (swing_high + swing_low) / 2
        return {
            'premium': (mid + (swing_high - mid) * 0.5, swing_high),
            'discount': (swing_low, mid - (mid - swing_low) * 0.5)
        }

    def detect(self) -> list[dict]:
        setups = []
        for name, detector in self.detectors.items():
            detector_setups = detector.detect()
            setups.extend(detector_setups)
        filtered_setups = []
        for setup in setups:
            if 'price' in setup:
                ped = self._calculate_ped(
                    swing_high=max([s['price'] for s in setups if 'price' in s], default=setup['price']),
                    swing_low=min([s['price'] for s in setups if 'price' in s], default=setup['price'])
                )
                if setup['type'].startswith('bearish') and ped['premium'][0] <= setup['price'] <= ped['premium'][1]:
                    filtered_setups.append(setup)
                elif setup['type'].startswith('bullish') and ped['discount'][0] <= setup['price'] <= ped['discount'][1]:
                    filtered_setups.append(setup)
        return filtered_setups