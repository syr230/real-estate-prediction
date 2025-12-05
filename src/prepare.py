import pandas as pd
import numpy as np
import os


def prepare(input_path: str, output_path: str = "data/cleaned.csv") -> pd.DataFrame:
    df = pd.read_csv(input_path)
    df = df.copy()

    # Price per sqft
    df['Price_per_SqFt'] = (df['Price_in_Lakhs'] * 100000) / df['Size_in_SqFt']

    # Age
    df['Age'] = 2025 - df['Year_Built']

    # Simple encoding for Public_Transport_Accessibility
    df['PT_Score'] = df['Public_Transport_Accessibility'].map({
        'High': 2,
        'Medium': 1,
        'Low': 0
    }).fillna(0)

    # Amenities count
    def amenities_count(x):
        if pd.isna(x) or x in ('', 'None'):
            return 0
        return len(str(x).split(';'))

    df['Amenities_Count'] = df['Amenities'].apply(amenities_count)

    # Target: Future price after 5 years by applying a simple growth model with small noise
    base_rate = 0.08
    np.random.seed(42)
    df['Future_Price_5Y'] = (df['Price_in_Lakhs'] * ((1 + base_rate) ** 5)) * (1 + np.random.normal(0, 0.02, size=len(df)))
    df['Future_Price_5Y'] = df['Future_Price_5Y'].round(2)

    # Binary label: Good_Investment - synthetic rule (appreciation over 5 years > 8%)
    df['AppreciationPct'] = (df['Future_Price_5Y'] - df['Price_in_Lakhs']) / df['Price_in_Lakhs']
    df['Good_Investment'] = (df['AppreciationPct'] >= 0.08).astype(int)

    # Select useful columns and save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == '__main__':
    prepare('data/india_housing_prices.csv', 'data/cleaned.csv')
