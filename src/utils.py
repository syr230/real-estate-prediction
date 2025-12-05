import math
from typing import Dict
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def compute_price_per_sqft(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Price_per_SqFt'] = (df['Price_in_Lakhs'] * 100000) / df['Size_in_SqFt']
    return df


def predict_future_price(current_price_lakhs: float, rate: float = 0.08, years: int = 5) -> float:
    # Simple compound growth
    future = current_price_lakhs * ((1 + rate) ** years)
    return round(future, 2)


def is_good_investment(row: Dict, median_pps: float) -> Dict:
    # Simple heuristic rules:
    #  - price_per_sqft cheaper than median -> positive
    #  - BHK >= 3 -> positive
    #  - Built within last 15 years -> positive
    score = 0
    if row.get('Price_per_SqFt', 0) <= median_pps:
        score += 1
    if row.get('BHK', 0) >= 3:
        score += 1
    if 'Year_Built' in row and not pd.isna(row['Year_Built']):
        age = 2025 - int(row['Year_Built'])
        if age <= 15:
            score += 1
    # amenities bonus
    if isinstance(row.get('Amenities', ''), str) and row.get('Amenities') not in ('', 'None'):
        score += 1

    is_good = score >= 2
    return {
        'score': score,
        'Good_Investment': bool(is_good)
    }
