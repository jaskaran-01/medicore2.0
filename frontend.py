from flask import Flask, render_template, request, jsonify
import requests
import json
from typing import Dict, List
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API URL
BACKEND_URL = "http://localhost:8000"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        message = request.json.get('message')
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Call backend API
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={"message": message}
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Backend API error'}), response.status_code

        data = response.json()
        
        # Format the response for debugging
        debug_info = {
            'input': {
                'message': message,
                'timestamp': response.headers.get('Date', 'N/A'),
                'response_time': response.elapsed.total_seconds()
            },
            'symptoms': {
                'extracted': data.get('extracted_symptoms', []),
                'assumed': data.get('assumed_symptoms', [])
            },
            'diseases': []
        }

        # Process each disease prediction
        for pred in data.get('predictions', []):
            disease_info = {
                'name': pred['disease'],
                'similarity_score': pred['similarity_score'],
                'symptoms': {
                    'matched': pred['matched_symptoms'],
                    'all': pred['all_symptoms']
                },
                'recommendations': {
                    'medications': pred['medications'],
                    'precautions': pred['precautions'],
                    'diet': pred['diet'],
                    'workout': pred['workout']
                }
            }
            debug_info['diseases'].append(disease_info)

        return jsonify(debug_info)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 