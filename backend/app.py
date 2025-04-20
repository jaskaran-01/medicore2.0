from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import logging
import re
import ast
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the training data
try:
    df = pd.read_csv('Training.csv')
    symptoms = df.columns[:-1]  # All columns except the last one (prognosis)
    diseases = df['prognosis'].unique()
    logger.info(f"Successfully loaded training data with {len(symptoms)} symptoms and {len(diseases)} diseases")
    
    # Create disease vectors
    disease_vectors = {}
    for disease in diseases:
        disease_vectors[disease] = df[df['prognosis'] == disease].iloc[:, :-1].mean().values
except Exception as e:
    logger.error(f"Failed to load training data: {str(e)}")
    raise

# Load workout data
try:
    workout_df = pd.read_csv('workout_df.csv')
    logger.info("Successfully loaded workout data")
except Exception as e:
    logger.error(f"Failed to load workout data: {str(e)}")
    raise

# Load precautions data
try:
    precautions_df = pd.read_csv('precautions_df.csv')
    logger.info("Successfully loaded precautions data")
except Exception as e:
    logger.error(f"Failed to load precautions data: {str(e)}")
    raise

# Initialize OLLAMA with custom base_url
try:
    llm = Ollama(
        model="deepseek-r1:7b",
        base_url="http://localhost:11500"
    )
    logger.info("Successfully initialized OLLAMA with deepseek-r1:7b model on port 11500")
except Exception as e:
    logger.error(f"Failed to initialize OLLAMA: {str(e)}")
    raise

# Create prompt template
symptom_extraction_prompt = PromptTemplate(
    input_variables=["symptoms_list", "message"],
    template="""You are a medical symptom extractor. Your task is to extract ONLY symptoms that are in the provided list.
    
Available symptoms (use EXACTLY these terms):
{symptoms_list}

Rules:
1. ONLY return symptoms that are in the list above
2. Return the symptoms in a Python list format
3. Use the EXACT symptom names from the list
4. If no symptoms match, return an empty list
5. Do not add any explanations or additional text
6. Please do your best to match the symptoms to the message
7. If you feel like a symptom very barely matches, include it.
8. If you feel like a symptom is not at all related to the message, do not include it.
9. Don't overthink the symptoms understand each symptom perfectly.
10.Please note you are an expert medical doctor.
11.Please note that your extraction will help diagnose a disease.
12.Please note that you are extracting symptoms for a medical professional.
13.Please note that you are extracting symptoms for a medical professional.
14.Please note that you are extracting symptoms for a medical professional.
15.Please note that you are extracting symptoms for a medical professional.

Example1 input: "I have a fever and my head hurts and im puking"
Example1 output: ['high_fever', 'headache',"vomiting"]

Example2 input: "im having a headache have body aches and am feeling very cold"
Example2 output: ['headache', 'body_aches',"cold_hands_and_feets"]

Message to analyze: {message}"""
)

def clean_response(response: str) -> str:
    """Remove content within <think> tags from the response."""
    return re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()

def parse_symptoms(response: str) -> list:
    """Convert the response string to a Python list of symptoms."""
    try:
        # Clean the response first
        cleaned = clean_response(response)
        # Parse the string into a Python list
        symptoms_list = ast.literal_eval(cleaned)
        # Ensure it's a list
        if not isinstance(symptoms_list, list):
            raise ValueError("Response is not a list")
        return symptoms_list
    except (SyntaxError, ValueError) as e:
        logger.error(f"Failed to parse symptoms: {str(e)}")
        return []

def calculate_similarity(extracted_symptoms: List[str]) -> List[Dict[str, float]]:
    """Calculate cosine similarity between extracted symptoms and diseases."""
    if not extracted_symptoms:
        return []
        
    # Create symptom vector
    symptom_vector = np.zeros(len(symptoms))
    for symptom in extracted_symptoms:
        if symptom in symptoms:
            symptom_vector[list(symptoms).index(symptom)] = 1
    
    # Calculate similarity with each disease
    similarities = []
    for disease, disease_vector in disease_vectors.items():
        similarity = cosine_similarity([symptom_vector], [disease_vector])[0][0]
        similarities.append({"disease": disease, "similarity": float(similarity)})
    
    # Sort by similarity and return top 5
    return sorted(similarities, key=lambda x: x["similarity"], reverse=True)[:5]

def get_workouts_for_disease(disease: str) -> List[str]:
    """Get workout recommendations for a specific disease."""
    try:
        workouts = workout_df[workout_df['disease'] == disease]['workout'].tolist()
        return workouts
    except Exception as e:
        logger.error(f"Error getting workouts for {disease}: {str(e)}")
        return []

def get_precautions_for_disease(disease: str) -> List[str]:
    """Get precautions for a specific disease."""
    try:
        precautions = []
        row = precautions_df[precautions_df['Disease'] == disease].iloc[0]
        for i in range(1, 5):  # Precaution_1 to Precaution_4
            precaution = row[f'Precaution_{i}']
            if pd.notna(precaution) and precaution.strip():
                precautions.append(precaution)
        return precautions
    except Exception as e:
        logger.error(f"Error getting precautions for {disease}: {str(e)}")
        return []

class MessageRequest(BaseModel):
    message: str

class DiseasePrediction(BaseModel):
    disease: str = Field(..., description="Name of the disease")
    similarity: float = Field(..., description="Similarity score between 0 and 1")
    workouts: List[str] = Field(default_factory=list, description="Recommended workouts for the disease")
    precautions: List[str] = Field(default_factory=list, description="Recommended precautions for the disease")

class PredictionResponse(BaseModel):
    symptoms: List[str] = Field(default_factory=list, description="List of extracted symptoms")
    top_diseases: List[DiseasePrediction] = Field(default_factory=list, description="Top 5 matching diseases with similarity scores")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Symptom Extraction API"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_disease(request: MessageRequest):
    try:
        # Format the prompt with available symptoms
        formatted_prompt = symptom_extraction_prompt.format(
            symptoms_list=", ".join(symptoms),
            message=request.message
        )
        
        # Get response from OLLAMA
        logger.info("Sending request to OLLAMA")
        response = llm.invoke(formatted_prompt)
        logger.info(f"Received response from OLLAMA: {response}")
        
        # Parse the response into a list of symptoms
        symptoms_list = parse_symptoms(response)
        logger.info(f"Parsed symptoms: {symptoms_list}")
        
        # Calculate disease similarities
        raw_similarities = calculate_similarity(symptoms_list)
        logger.info(f"Raw similarities: {raw_similarities}")
        
        # Convert to DiseasePrediction objects with workouts and precautions
        top_diseases = []
        for item in raw_similarities[:3]:  # Only get workouts and precautions for top 3 diseases
            workouts = get_workouts_for_disease(item["disease"])
            precautions = get_precautions_for_disease(item["disease"])
            top_diseases.append(
                DiseasePrediction(
                    disease=item["disease"],
                    similarity=item["similarity"],
                    workouts=workouts,
                    precautions=precautions
                )
            )
        
        return PredictionResponse(
            symptoms=symptoms_list,
            top_diseases=top_diseases
        )
        
    except Exception as e:
        logger.error(f"Error in predict_disease: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="localhost  ", port=8000, reload=True) 