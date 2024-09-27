# load_and_test_model.py

import pandas as pd
import joblib

# Load the saved model
loaded_model = joblib.load('bankruptcy_model.pkl')

# Create a new data sample for prediction (replace with appropriate feature names)
new_data = pd.DataFrame({
    ' Current Liability to Current Assets': [0.118250477],
    ' Liability-Assets Flag': [0],
    ' Total expense/Assets': [0.064855708],
    ' Cash/Current Liability': [0.000147336],
    ' Fixed Assets Turnover Frequency': [0.000116501],
    ' Fixed Assets to Assets': [0.424205762],
    ' Net Value Growth Rate': [0.000326977],
    ' Revenue per person': [0.034164182],
    ' Total assets to GNP price': [0.00921944],
    ' Quick Asset Turnover Rate': [65500000000],
    ' Tax rate (A)': [0],
    ' Cash/Total Assets': [0.004094406],
})

# Predict using the loaded model
new_prediction = loaded_model.predict(new_data)

# Output the prediction result (0 = Non-bankrupt, 1 = Bankrupt)
print(f"Predicted Bankruptcy: {new_prediction}")
