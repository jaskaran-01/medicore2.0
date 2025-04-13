# Medical Chatbot API

This is a FastAPI-based medical chatbot that uses Ollama's deepseek-r1:7b model to analyze symptoms and provide medical information. The application integrates with MongoDB to store and retrieve medical data.

## Prerequisites

1. Python 3.8 or higher
2. MongoDB installed and running locally
3. Ollama installed and running with deepseek-r1:7b model

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure MongoDB is running on your local machine (default port 27017)

3. Ensure Ollama is running with the deepseek-r1:7b model:
```bash
ollama pull deepseek-r1:7b
```

## Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

2. The server will start on `http://localhost:8000`

## API Endpoints

### POST /chat

Send a POST request with symptoms to get medical information:

```json
{
    "symptoms": ["fever", "headache", "cough"]
}
```

Response:
```json
{
    "disease": "Common Cold",
    "medications": ["Paracetamol", "Ibuprofen"],
    "precautions": ["Rest", "Stay hydrated"],
    "diet": ["Warm fluids", "Light meals"],
    "workout": ["Light stretching", "Short walks"]
}
```

## Data Structure

The application uses the following CSV files:
- symtoms_df.csv: Contains symptom-disease mapping
- medications.csv: Contains disease-medication mapping
- workout_df.csv: Contains disease-workout recommendations
- diets.csv: Contains disease-diet recommendations
- precautions_df.csv: Contains disease-precaution mapping

All data is automatically loaded into MongoDB on application startup.

## Notes

- Make sure all CSV files are present in the same directory as main.py
- The application assumes MongoDB is running on localhost:27017
- The Ollama model should be running and accessible
