import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def preprocess_mt5_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess MT5 OHLCV data for analysis.
    
    Args:
        data (pd.DataFrame): Raw MT5 data with columns ['time', 'open', 'high', 'low', 'close', 'volume']
    
    Returns:
        pd.DataFrame: Preprocessed data with cleaned and formatted columns
    """
    try:
        # Ensure expected columns
        expected_columns = ['time', 'open', 'high', 'low', 'close', 'volume']
        if not all(col in data.columns for col in expected_columns):
            logger.error(f"Missing expected columns in data: {data.columns}")
            raise ValueError("DataFrame missing required OHLCV columns")

        # Convert 'time' to datetime if not already
        if not pd.api.types.is_datetime64_any_dtype(data['time']):
            data['time'] = pd.to_datetime(data['time'])

        # Set 'time' as index
        data = data.set_index('time')

        # Handle missing values
        data = data.fillna(method='ffill')  # Forward fill for continuity

        # Ensure numeric types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            data[col] = pd.to_numeric(data[col], errors='coerce')

        logger.info("MT5 data preprocessed successfully")
        return data

    except Exception as e:
        logger.error(f"Error preprocessing MT5 data: {str(e)}")
        raise