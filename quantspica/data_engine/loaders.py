# quantspica/data_engine/loaders.py

from pathlib import Path
import pandas as pd
from datetime import datetime
from alpaca.data.timeframe import TimeFrame

try:
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
except ImportError:
    StockHistoricalDataClient = None

DATA_DIR = Path("data/market/daily")


class MarketDataLoader:
    def __init__(self, api_key: str | None = None, secret_key: str | None = None):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.client = None
        if api_key and secret_key:
            self.client = StockHistoricalDataClient(api_key, secret_key)

    def fetch_daily_bars(
        self,
        symbol: str,
        start: datetime,
        end: datetime
    ) -> pd.DataFrame:
        if self.client is None:
            raise RuntimeError("No API credentials provided; cannot fetch data.")

        request = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=TimeFrame.Day,
            start=start,
            end=end,
            adjustment="split"
        )

        bars = self.client.get_stock_bars(request).df
        bars = bars.reset_index()
        bars = bars.rename(columns={"timestamp": "date"})
        bars["symbol"] = symbol

        return bars

    def save(self, df: pd.DataFrame, symbol: str):
        path = DATA_DIR / f"{symbol}.parquet"
        df.to_parquet(path, index=False)

    def load(self, symbol: str) -> pd.DataFrame:
        path = DATA_DIR / f"{symbol}.parquet"
        if not path.exists():
            raise FileNotFoundError(f"No cached data for {symbol}")
        return pd.read_parquet(path)
