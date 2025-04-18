def get_ict_prompt(data: str, concepts: list = None, lens_results: dict = None) -> str:
    if concepts is None:
        concepts = ["Fair Value Gap", "Order Block", "Killzone"]
    if lens_results is None:
        lens_results = {}

    concept_definitions = {
        "Fair Value Gap": (
            "A Fair Value Gap (FVG) is a price imbalance where a strong impulsive move creates a gap between candles, "
            "typically a three-candle pattern. For a bullish FVG, the high of the first candle is below the low of the third. "
            "For a bearish FVG, the low of the first candle is above the high of the third."
        ),
        "Order Block": (
            "An Order Block is a consolidation zone before a strong price move, often the last candle before an impulsive breakout. "
            "Bullish Order Blocks are at swing lows; bearish ones are at swing highs."
        ),
        "Killzone": (
            "A Killzone is a high-volatility period (e.g., London Open 2:00-5:00 AM EST, NY Open 8:00-11:00 AM EST) "
            "where price often makes significant moves or reversals."
        )
    }

    definitions = "\n".join([f"{c}: {concept_definitions.get(c, 'No definition')}" for c in concepts])
    results_str = "\n".join([f"{name}: {lens_results.get(name, 'No setups detected')}" for name in concepts])
    prompt = (
        f"You are an expert in Inner Circle Trader (ICT) methodology. Below are key ICT concept definitions:\n\n"
        f"{definitions}\n\n"
        f"Market data (OHLCV, last 5 bars):\n{data}\n\n"
        f"Lens results:\n{results_str}\n\n"
        f"Analyze the data and lens results to identify or validate ICT setups for {', '.join(concepts)}. "
        f"Provide a summary of setups found, including timeframe, price levels, and type (bullish/bearish). "
        f"If no setups are valid, explain why. Format:\n"
        f"- Setup: [Concept]\n- Type: [Bullish/Bearish]\n- Price Level: [Price range]\n- Timeframe: [e.g., H1]\n- Details: [Explanation]"
    )
    return prompt