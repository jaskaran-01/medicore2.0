from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from symptoms import Symptoms
import json

# Load environment variables
load_dotenv()

app = FastAPI(title="Medical Diagnosis Chatbot")

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client.medical_diagnosis

# Collections
symptoms_collection = db.symptoms
diseases_collection = db.diseases
workouts_collection = db.workouts
precautions_collection = db.precautions
diets_collection = db.diets
descriptions_collection = db.descriptions

def import_csv_to_mongodb():
    """Import CSV files to MongoDB collections"""
    # Import symptoms
    symptoms_df = pd.read_csv('symptoms.csv')
    symptoms_collection.insert_many(symptoms_df.to_dict('records'))
    
    # Import workouts
    workouts_df = pd.read_csv('workout_df.csv')
    workouts_collection.insert_many(workouts_df.to_dict('records'))
    
    # Import precautions
    precautions_df = pd.read_csv('precautions_df.csv')
    precautions_collection.insert_many(precautions_df.to_dict('records'))
    
    # Import diets
    diets_df = pd.read_csv('diets.csv')
    diets_collection.insert_many(diets_df.to_dict('records'))
    
    # Import descriptions
    descriptions_df = pd.read_csv('description.csv')
    descriptions_collection.insert_many(descriptions_df.to_dict('records'))

def extract_symptoms(text: str) -> List[str]:
    """Extract symptoms from user input using Ollama"""
    ollama_url = "http://localhost:11434/api/generate"
    prompt = f"""
    Extract medical symptoms from the following text. Only return symptoms that are in the Symptoms class.
    Return them as a JSON list of strings.
    
    Text: {text}
    """
    
    response = requests.post(ollama_url, json={
        "model": "deepseek-r1:14b",
        "prompt": prompt,
        "stream": False
    })
    
    try:
        symptoms = json.loads(response.json()['response'])
        return symptoms
    except:
        return []

def get_disease_info(symptoms: List[str]) -> Dict:
    """Get disease information based on symptoms"""
    # Query MongoDB for matching diseases
    disease = diseases_collection.find_one({"symptoms": {"$all": symptoms}})
    if not disease:
        return None
    
    # Get related information
    workout = workouts_collection.find_one({"disease": disease['name']})
    precaution = precautions_collection.find_one({"disease": disease['name']})
    diet = diets_collection.find_one({"disease": disease['name']})
    description = descriptions_collection.find_one({"disease": disease['name']})
    
    return {
        "disease": disease['name'],
        "description": description['description'] if description else None,
        "workout": workout['workout'] if workout else None,
        "precautions": precaution['precautions'] if precaution else None,
        "diet": diet['diet'] if diet else None
    }

def get_google_info(disease: str) -> str:
    """Get additional information from Google"""
    # This is a placeholder. You'll need to implement proper Google search API integration
    return f"Additional information about {disease} from Google"

@app.post("/diagnose")
async def diagnose(text: str):
    """Endpoint for medical diagnosis"""
    # Extract symptoms
    symptoms = extract_symptoms(text)
    if not symptoms:
        raise HTTPException(status_code=400, detail="No valid symptoms found in the input")
    
    # Get disease information
    disease_info = get_disease_info(symptoms)
    if not disease_info:
        raise HTTPException(status_code=404, detail="No matching disease found")
    
    # Get additional information from Google
    google_info = get_google_info(disease_info['disease'])
    
    return {
        "symptoms": symptoms,
        "disease_info": disease_info,
        "additional_info": google_info
    }

@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB with CSV data on startup"""
    if symptoms_collection.count_documents({}) == 0:
        import_csv_to_mongodb()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 