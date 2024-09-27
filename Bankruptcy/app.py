from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

app = Flask(__name__)

# Configure the SQLite database (or replace with your database connection string)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bankruptcy_data.db'
db = SQLAlchemy(app)

# Load the trained model
model = joblib.load('bankruptcy_model.pkl')

# Define a model for the user input data and prediction result
class BankruptcyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_liability_to_current_assets = db.Column(db.Float, nullable=False)
    liability_assets_flag = db.Column(db.Integer, nullable=False)
    total_expense_assets = db.Column(db.Float, nullable=False)
    cash_current_liability = db.Column(db.Float, nullable=False)
    fixed_assets_turnover_frequency = db.Column(db.Float, nullable=False)
    fixed_assets_to_assets = db.Column(db.Float, nullable=False)
    net_value_growth_rate = db.Column(db.Float, nullable=False)
    revenue_per_person = db.Column(db.Float, nullable=False)
    total_assets_to_gnp_price = db.Column(db.Float, nullable=False)
    quick_asset_turnover_rate = db.Column(db.Float, nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    cash_total_assets = db.Column(db.Float, nullable=False)
    prediction_result = db.Column(db.String(50), nullable=False)

# Create the database tables inside the application context
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    form_data = request.form

    # Prepare the input data for the model
    input_data = [[
        float(form_data['current_liability_to_current_assets']),
        int(form_data['liability_assets_flag']),
        float(form_data['total_expense_assets']),
        float(form_data['cash_current_liability']),
        float(form_data['fixed_assets_turnover_frequency']),
        float(form_data['fixed_assets_to_assets']),
        float(form_data['net_value_growth_rate']),
        float(form_data['revenue_per_person']),
        float(form_data['total_assets_to_gnp_price']),
        float(form_data['quick_asset_turnover_rate']),
        float(form_data['tax_rate']),
        float(form_data['cash_total_assets'])
    ]]

    # Make the prediction using the loaded model
    prediction = model.predict(input_data)[0]

    # Interpret the prediction result
    prediction_result = 'Bankrupt' if prediction == 1 else 'Non-bankrupt'

    # Save the data along with the prediction result to the database
    new_entry = BankruptcyData(
        current_liability_to_current_assets=float(form_data['current_liability_to_current_assets']),
        liability_assets_flag=int(form_data['liability_assets_flag']),
        total_expense_assets=float(form_data['total_expense_assets']),
        cash_current_liability=float(form_data['cash_current_liability']),
        fixed_assets_turnover_frequency=float(form_data['fixed_assets_turnover_frequency']),
        fixed_assets_to_assets=float(form_data['fixed_assets_to_assets']),
        net_value_growth_rate=float(form_data['net_value_growth_rate']),
        revenue_per_person=float(form_data['revenue_per_person']),
        total_assets_to_gnp_price=float(form_data['total_assets_to_gnp_price']),
        quick_asset_turnover_rate=float(form_data['quick_asset_turnover_rate']),
        tax_rate=float(form_data['tax_rate']),
        cash_total_assets=float(form_data['cash_total_assets']),
        prediction_result=prediction_result
    )

    # Add to the session and commit
    db.session.add(new_entry)
    db.session.commit()

    # Create a timeseries for 12 months for each attribute and plot them
    months = pd.date_range(start='2024-01-01', periods=12, freq='M')
    attributes = {
        'Current Liability to Current Assets': input_data[0][0],
        'Liability-Assets Flag': input_data[0][1],
        'Total Expense / Assets': input_data[0][2],
        'Cash / Current Liability': input_data[0][3],
        'Fixed Assets Turnover Frequency': input_data[0][4],
        'Fixed Assets to Assets': input_data[0][5],
        'Net Value Growth Rate': input_data[0][6],
        'Revenue per Person': input_data[0][7],
        'Total Assets to GNP Price': input_data[0][8],
        'Quick Asset Turnover Rate': input_data[0][9],
        'Tax Rate': input_data[0][10],
        'Cash / Total Assets': input_data[0][11]
    }

    # Plot 12 graphs in subplots
    fig = make_subplots(rows=4, cols=3, subplot_titles=list(attributes.keys()))

    row = 1
    col = 1

    for i, (attribute, value) in enumerate(attributes.items()):
        # Generate synthetic data over 12 months (you can replace this with actual timeseries forecasting if available)
        data = np.random.normal(value, 0.1 * value, size=12)
        fig.add_trace(go.Scatter(x=months, y=data, mode='lines', name=attribute), row=row, col=col)

        col += 1
        if col > 3:
            col = 1
            row += 1

    fig.update_layout(height=900, width=1200, title_text="12 Attribute Time-Series")

    # Convert Plotly figure to JSON to be passed to the HTML template
    graphJSON = fig.to_json()

    return render_template('result.html', prediction=prediction_result, graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)
