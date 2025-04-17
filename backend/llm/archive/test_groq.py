# test_groq.py
from backend.llm.gemini_client import explain_setup

print("Testing Groq API")
try:
    mock_setup = {
        "symbol": "EURUSD",
        "timeframe": "M15",
        "setup": {"type": "Power of 3: Manipulation", "wick": [150, 200], "body": 175, "text": "manip", "confidence": 0.7},
        "prices": {"wick_high": 1.0880, "wick_low": 1.0870, "body": 1.0875}
    }
    explanation = explain_setup(mock_setup)
    print("Groq Explanation:")
    print(explanation)
except Exception as e:
    print(f"Groq error: {e}")