"""Returns and realized volatility."""
import numpy as np
import pandas as pd

def log_returns(close: pd.Series) -> pd.Series:
    """ln(P_t / P_{t-1}); first value dropped."""
    return np.log(close / close.shift(1)).dropna()

def realized_vol(returns: pd.Series, window: int = 20) -> pd.Series:
    """Rolling std of returns, annualized (252 trading days)."""
    return returns.rolling(window).std() * np.sqrt(252)
