import logging
import pandas as pd
from llama_index.core.tools import FunctionTool
from brain import summarize_home_loan_application
from config import Config
import joblib
import os
logger = logging.getLogger(__name__)

# Valid DTI categories
VALID_CATEGORIES = [
    "<20%", "20%-<30%", "30%-<36%", "36", "37", "38", "39", "40", "41", "42", 
    "43", "44", "45", "46", "47", "48", "49", "50%-60%", ">60%"
]

def calculate_dti_ratio(annual_income, loan_amount, loan_term):
    """
    Calculate the Debt-to-Income (DTI) Ratio.

    Parameters:
        annual_income (float): The borrower's annual income.
        loan_amount (float): The requested loan amount.
        loan_term_years (int): The loan term in years.

    Returns:
        float: Debt-to-Income (DTI) Ratio as a percentage.
    """
    annual_interest_rate = 0.07
    monthly_income = annual_income / 12
    # Monthly interest rate
    monthly_interest_rate = annual_interest_rate / 12

    # Calculate monthly loan payment using the amortization formula
    monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**loan_term) / \
                      ((1 + monthly_interest_rate)**loan_term - 1)

    # Calculate DTI ratio
    dti_ratio = (monthly_payment / monthly_income) * 100

    return dti_ratio

def map_dti_to_category(dti: float) -> str:
    """
    Maps a numeric DTI value to a categorical range.
    """
    if dti < 20:
        return "<20%"
    elif 20 <= dti < 30:
        return "20%-<30%"
    elif 30 <= dti < 36:
        return "30%-<36%"
    elif 36 <= dti <= 60:
        return f"{int(dti)}"
    else:
        return ">60%"
    
def calculate_metrics_fields(inputs: dict) -> dict:
    """
    Calculates missing fields like DTI and LTV if not provided.
    """
    # Calculate DTI if missing
    if "debt_to_income_ratio" not in inputs or not inputs["debt_to_income_ratio"]:
        if "income" in inputs and "loan_amount" in inputs:
            income = float(inputs["income"])
            loan_amount = float(inputs["loan_amount"])
            dti = calculate_dti_ratio(inputs["income"],
                                      inputs['loan_amount'],
                                      inputs['loan_term'])
            inputs["debt_to_income_ratio"] = map_dti_to_category(dti)
    
    # Calculate LTV if missing
    if "loan_to_value_ratio" not in inputs or not inputs["loan_to_value_ratio"]:
        if "loan_amount" in inputs and "property_value" in inputs:
            loan_amount = float(inputs["loan_amount"])
            property_value = float(inputs["property_value"])
            ltv = (loan_amount / property_value) * 100
            inputs["loan_to_value_ratio"] = round(ltv, 2)
    
    return inputs

def preprocessing_data(df_):
    loan_purpose_mapping = {
        'Home purchase'    : 0,
        'Home improvement' : 1,
        'Refinancing'      : 2,
        'Cash-out refinancing': 3,
        'Other purpose': 4,
        'Not applicable': 5
    }

    ordinal_mapping = {
        '<20%': 10, '20%-<30%': 25, '30%-<36%': 33, '36': 36, 
        '37': 37, '38': 38, '39': 39, '40': 40, '41': 41, 
        '42': 42, '43': 43, '44': 44, '45': 45, '46': 46,
        '47': 47, '48': 48, '49': 49, '50%-60%': 55, '>60%': 75.0
    }

    numeric_features = ['income', 'loan_amount',
                'loan_term', 'property_value', 
                'loan_to_value_ratio', 
                'loan_purpose_encoded',
                'debt_to_income_ratio_encoded']

    df_org_preprocess = df_.copy()

    df_org_preprocess['loan_purpose_encoded']         = df_org_preprocess['loan_purpose'].map(loan_purpose_mapping)
    df_org_preprocess['debt_to_income_ratio_encoded'] = df_org_preprocess['debt_to_income_ratio'].map(ordinal_mapping)

    for feature in numeric_features:
        df_org_preprocess[feature] = pd.to_numeric(df_org_preprocess[feature], errors='coerce')
    df_org_preprocess = df_org_preprocess.dropna()

    return df_org_preprocess[numeric_features]

def load_model():
    # Get the model path from the environment variable or default path
    # Check if the model file exists
    if not os.path.exists(Config.XGBOOST_MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at: {Config.XGBOOST_MODEL_PATH}")

    # Load and return the model
    try:
        return joblib.load(Config.XGBOOST_MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Failed to load the model due to: {e}")
    
def home_loan_recommandation(inputs: dict):
    try:
        # Calculate metrics and preprocess the input data
        json_data_input = calculate_metrics_fields(inputs)
        df_data_input = pd.DataFrame([json_data_input])
        preprocess_data = preprocessing_data(df_data_input)
        # Load the model
        model = load_model()
        if model is None:
            raise ValueError("Model loading failed. Ensure the model path is correct and the file exists.")

        # Make prediction
        prediction = model.predict(preprocess_data)
        status = "Approved" if prediction[0] == 0 else "Rejected"
        return summarize_home_loan_application(inputs, status)

    except Exception as e:
        return f"An error occurred: {e}"