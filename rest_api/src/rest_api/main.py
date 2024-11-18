import random
from datetime import datetime, timedelta

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="Time Series API",
    description="Service to generate time series data",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)


@app.get("/generate_time_series/", response_model=dict)
async def generate_time_series(length: int):
    """
    Generate a time series with random prices.
    """
    if length <= 0:
        return {"error": "Length must be a positive integer."}

    # Generate timestamps and random prices
    start_time = datetime.now()
    timestamps = [start_time + timedelta(minutes=i) for i in range(length)]
    prices = [random.uniform(10, 100) for _ in range(length)]  # Random prices

    # Create a Pandas DataFrame
    pandas_series = pd.Series(data=prices, index=timestamps)
    series_data = [
        {"time": timestamp.isoformat(), "price": price}
        for timestamp, price in pandas_series.items()
    ]

    return {"series": series_data}
