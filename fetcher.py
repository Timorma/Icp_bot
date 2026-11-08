import datetime
import pandas as pd
import numpy as np

def fetch_market_data(symbol: str, timeframe: str = "1h", limit: int = 300) -> pd.DataFrame:
    np.random.seed(hash(symbol) % 2026)
    base_price = 2000.0 if "XAU" in symbol.upper() else (65000.0 if "BTC" in symbol.upper() else 1.0850)
    
    dates = [datetime.datetime.now() - datetime.timedelta(hours=i) for i in range(limit)][::-1]
    
    returns = np.random.normal(0, 0.002, limit)
    price_paths = base_price * np.exp(np.cumsum(returns))
    
    highs = price_paths * (1 + np.abs(np.random.normal(0, 0.0015, limit)))
    lows = price_paths * (1 - np.abs(np.random.normal(0, 0.0015, limit)))
    opens = np.roll(price_paths, 1)
    opens[0] = price_paths[0]
    volumes = np.random.randint(500, 5000, limit)
    
    df = pd.DataFrame({
        'datetime': dates,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': price_paths,
        'volume': volumes
    })
    return df
