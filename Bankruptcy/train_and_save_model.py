# train_and_save_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the dataset
df = pd.read_csv('bank1.csv')

# Select features and target (replace with actual feature names and target column)
X = df[[' Current Liability to Current Assets', ' Liability-Assets Flag', ' Total expense/Assets',' Cash/Current Liability',' Fixed Assets Turnover Frequency',' Fixed Assets to Assets',' Net Value Growth Rate',' Revenue per person',' Total assets to GNP price',' Quick Asset Turnover Rate',' Tax rate (A)',' Cash/Total Assets']]
y = df['Bankrupt?']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy}")
print(classification_report(y_test, y_pred))

# Save the trained model
joblib.dump(model,'bankruptcy_model.pkl')
