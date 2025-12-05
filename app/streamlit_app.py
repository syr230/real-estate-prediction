import streamlit as st
import pandas as pd
import os
import sys
import joblib

# Ensure project root is on sys.path so `from src import ...` works when Streamlit
# runs with `app/` as the working directory.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src import utils


st.set_page_config(page_title="Real Estate Investment Advisor", layout='wide')

st.title("Real Estate Investment Advisor")

DATA_PATH = "data/india_housing_prices.csv"

MODELS_DIR = "models"

def load_models(models_dir=MODELS_DIR):
    clf = None
    reg = None
    clf_path = os.path.join(models_dir, 'classifier.joblib')
    reg_path = os.path.join(models_dir, 'regressor.joblib')
    if os.path.exists(clf_path):
        clf = joblib.load(clf_path)
    if os.path.exists(reg_path):
        reg = joblib.load(reg_path)
    return clf, reg


clf_model, reg_model = load_models()

@st.cache_data
def load_and_prepare(path):
    df = utils.load_data(path)
    df = utils.compute_price_per_sqft(df)
    return df


df = load_and_prepare(DATA_PATH)

st.sidebar.header("Input Property Details")
with st.sidebar.form(key='property_form'):
    city = st.selectbox('City', options=sorted(df['City'].unique()))
    size = st.number_input('Size (SqFt)', min_value=200, value=900)
    price = st.number_input('Price (Lakhs)', min_value=1.0, value=50.0)
    bhk = st.selectbox('BHK', options=sorted(df['BHK'].unique()))
    year_built = st.number_input('Year Built', min_value=1900, max_value=2025, value=2015)
    amenities = st.text_input('Amenities (semicolon-separated)', value='')
    submit = st.form_submit_button('Evaluate')

st.header('Dataset sample')
st.dataframe(df.head(10))

median_pps = float(df['Price_per_SqFt'].median())
st.write(f"Median Price per SqFt (derived): Rs {median_pps:.2f}")

if submit:
    input_row = {
        'City': city,
        'Size_in_SqFt': size,
        'Price_in_Lakhs': price,
        'BHK': bhk,
        'Year_Built': year_built,
        'Amenities': amenities
    }
    pps = (price * 100000) / size
    input_row['Price_per_SqFt'] = pps
    # Model-based predictions if models exist
    if reg_model is not None and clf_model is not None:
        feat_order = ['BHK', 'Size_in_SqFt', 'Price_per_SqFt', 'Age', 'Nearby_Schools', 'Nearby_Hospitals', 'PT_Score', 'Amenities_Count']
        feat_vals = {
            'BHK': bhk,
            'Size_in_SqFt': size,
            'Price_per_SqFt': pps,
            'Age': 2025 - year_built,
            'Nearby_Schools': 0,
            'Nearby_Hospitals': 0,
            'PT_Score': 0,
            'Amenities_Count': 0 if amenities in ('', 'None') else len(amenities.split(';'))
        }
        X_input = pd.DataFrame([{k: feat_vals[k] for k in feat_order}])

        reg_pred = reg_model.predict(X_input)[0]
        clf_prob = clf_model.predict_proba(X_input)[0]
        clf_pred = clf_model.predict(X_input)[0]

        st.subheader('Model Prediction Results')
        st.metric('Estimated Price after 5 Years (Lakhs)', f"{reg_pred:.2f}")
        st.write('Model investment probability (NotGood, Good):', [f"{p:.2f}" for p in clf_prob])

        # Feature importance (from regressor)
        if hasattr(reg_model, 'feature_importances_'):
            importances = reg_model.feature_importances_
            imp_df = pd.DataFrame({'feature': feat_order, 'importance': importances}).sort_values('importance', ascending=False)
            st.write('Feature importance (regressor)')
            st.table(imp_df)

    else:
        # fallback heuristics
        future_price = utils.predict_future_price(price)
        decision = utils.is_good_investment(input_row, median_pps)

        st.subheader('Heuristic Results')
        st.metric('Estimated Price after 5 Years (Lakhs)', f"{future_price}")
        st.write('Price per SqFt (input):', f"Rs {pps:.2f}")

        if decision['Good_Investment']:
            st.success(f"Good Investment (score={decision['score']})")
        else:
            st.warning(f"Not a Good Investment (score={decision['score']})")

        st.info('Heuristics used: cheaper-than-median price-per-sqft, BHK>=3, age<=15 years, amenities')
