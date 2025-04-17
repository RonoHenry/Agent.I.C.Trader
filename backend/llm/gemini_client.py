# backend/llm/grok_client.py
from groq import Groq
from backend.config.settings import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def explain_setup(setup):
    if not setup:
        return "No setup detected."
    
    prompt = (
        f"Explain this trading setup from a screenshot: "
        f"Symbol: {setup['symbol']}, Timeframe: {setup['timeframe']}, "
        f"Setup: {setup['setup']['type']}, Wick: {setup['setup']['wick']}, "
        f"Body: {setup['setup']['body']}, Text: '{setup['setup']['text']}', "
        f"Confidence: {setup['setup']['confidence']*100}%, "
        f"Prices: Wick High={setup['prices']['wick_high']}, Wick Low={setup['prices']['wick_low']}, Body={setup['prices']['body']}. "
        f"Focus on ICT methodology and Power of 3 (Accumulation, Manipulation, Distribution)."
    )
    
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Groq’s available model (adjust as needed)
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling Groq API: {e}"