import uvicorn
from fastapi import FastAPI
import numpy as np
import pandas as pd
from symptoms import Symptoms
from sklearn.metrics.pairwise import cosine_similarity
import heapq
import logging
from symptom_extractor import extract_symptoms_with_llm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

@app.post('/extract-symptoms')
async def extract_symptoms(message: str):
    try:
        symptoms = extract_symptoms_with_llm(message)
        return {
            "message": message,
            "symptoms": symptoms
        }
    except Exception as e:
        logger.error(f"Error in extract-symptoms endpoint: {str(e)}")
        return {"error": str(e)}

# Load training data
dataset = pd.read_csv('Training.csv')
dataset = dataset.drop(columns=['fluid_overload.1'])
grouped_df = dataset.drop(columns=['prognosis']).groupby(dataset['prognosis']).mean()

# Load additional data
description = pd.read_csv('description.csv')
diets = pd.read_csv('diets.csv')
medications = pd.read_csv('medications.csv')
workout = pd.read_csv('workout_df.csv')

def get_recommendation(df, disease, column_name):
    try:
        filtered = df[df['Disease'] == disease]
        if not filtered.empty:
            return filtered[column_name].iloc[0]
    except Exception as e:
        print(f"Error getting {column_name} for {disease}: {str(e)}")
    return f"No {column_name} recommendations available"

@app.post('/predict')
def predict_disease(data: Symptoms):
    # Convert Symptoms model to dictionary
    data = data.dict()
    
    # Create symptom vector
    arr = []
    for value in data.values():
        arr.append(value)
    
    # Create pandas Series with symptoms
    received_symptoms = pd.Series(arr, index=dataset.columns[:-1])
    
    # Calculate cosine similarity for each disease
    top_5_heap = []
    for disease, row in grouped_df.iterrows():
        similarity = cosine_similarity([row.values], [received_symptoms.values])[0][0]
        
        if len(top_5_heap) < 5:
            heapq.heappush(top_5_heap, (similarity, disease))
        else:
            heapq.heappushpop(top_5_heap, (similarity, disease))
    
    # Sort by similarity score
    top_5_sorted = sorted(top_5_heap, key=lambda x: -x[0])
    
    # Create prediction dictionary
    prediction = {}
    for similarity, disease in top_5_sorted:
        prediction[disease] = {
            "similarity_score": float(similarity),
            "description": get_recommendation(description, disease, 'Description'),
            "diet": get_recommendation(diets, disease, 'Diet'),
            "medications": get_recommendation(medications, disease, 'Medication'),
            "workout": get_recommendation(workout, disease, 'Workout')
        }
    
    return prediction

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


