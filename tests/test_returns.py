import numpy as np
import pandas as pd
from volforecast.returns import log_returns, realized_vol

def test_log_returns_value():
    r = log_returns(pd.Series([100.0, 110.0]))
    assert np.isclose(r.iloc[0], np.log(1.1))

def test_constant_price_zero_vol():
    r = log_returns(pd.Series([100.0] * 30))
    assert (realized_vol(r, 20).dropna() == 0).all()
