from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Initialize the FastAPI app
app = FastAPI()

# Load the trained model
model = joblib.load('randomized_search_xgb_model-2.pkl')

# Define the input data structure using Pydantic
class InputData(BaseModel):
    domain: int
    subdomain: int
    top_level_domain: int
    query: int
    fragment: int
    redirect: int
    path: int
    redirect_chain: int
    hsts_header: int
    ssl_stripping: int
    hostname_embedding: int
    javascript_check: int
    shortening_service: int
    has_ip_address: int
    tracking_descriptions: int
    url_encoding: int
    has_executable: int
    tls: int
    contents: int

# Define a mapping from numerical predictions to class labels
class_mapping = {
    0: "Benign",
    1: "Defacement",
    2: "Malware",
    3: "Phishing"
}

# Define a prediction endpoint
@app.post("/predict")
def predict(data: InputData):
    # Convert input data to a dictionary and wrap it in a list
    input_data = data.dict()
    input_df = pd.DataFrame([input_data], columns=[
        'domain', 'subdomain', 'top_level_domain', 'query', 
        'fragment', 'redirect', 'path', 'redirect_chain', 
        'hsts_header', 'ssl_stripping', 'hostname_embedding', 
        'javascript_check', 'shortening_service', 'has_ip_address', 
        'tracking_descriptions', 'url_encoding', 'has_executable', 
        'tls', 'contents'
    ])

    # Make a prediction using the loaded model
    prediction = model.predict(input_df)[0]

    # Map the prediction to the class label
    prediction_label = class_mapping.get(prediction, "Unknown")

    # Return the class label as the prediction
    return prediction_label

# Running the FastAPI app
# uvicorn main:app --reload (Use this command to run the FastAPI app)
