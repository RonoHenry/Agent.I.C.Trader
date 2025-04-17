def get_ict_prompt(data: str, concepts: list = None) -> str:
    """Generate a prompt for ICT analysis."""
    if concepts is None:
        concepts = ["Fair Value Gap", "Order Block", "Killzone"]

    concept_definitions = {
        "Fair Value Gap": (
            "A Fair Value Gap (FVG) is a price imbalance where a strong impulsive move creates a gap between candles, "
            "typically a three-candle pattern. For a bullish FVG, the high of the first candle is below the low of the third. "
            "For a bearish FVG, the low of the first candle is above the high of the third. FVGs are zones where price may return."
        ),
        "Order Block": (
            "An Order Block is a consolidation zone before a strong price move, often the last candle before an impulsive breakout. "
            "Bullish Order Blocks are at swing lows before an upmove; bearish ones are at swing highs before a downmove."
        ),
        "Killzone": (
            "A Killzone is a high-volatility period (e.g., London Open 2:00-5:00 AM EST, NY Open 8:00-11:00 AM EST) "
            "where price often makes significant moves or reversals."
        )
    }

    definitions = "\n".join([f"{concept}: {concept_definitions.get(concept, 'No definition available')}" for concept in concepts])
    prompt = (
        f"You are an expert in Inner Circle Trader (ICT) methodology for trading. Below are definitions of key ICT concepts:\n\n"
        f"{definitions}\n\n"
        f"Given the following market data in OHLCV format (Open, High, Low, Close, Volume):\n{data}\n\n"
        f"Analyze the data to identify potential ICT setups for the specified concepts: {', '.join(concepts)}. "
        f"Provide a concise summary of any setups found, including the timeframe, price levels, and type (bullish/bearish). "
        f"If no setups are identified, explain why. Return the response in a structured format:\n"
        f"- Setup: [Concept]\n- Type: [Bullish/Bearish]\n- Price Level: [Price range]\n- Timeframe: [e.g., H1]\n- Details: [Brief explanation]"
    )
    return prompt