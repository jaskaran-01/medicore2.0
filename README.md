# MediCore 2.0 - AI-Powered Medical Diagnosis Chatbot

MediCore 2.0 is an advanced medical diagnosis chatbot that helps users identify potential health conditions based on their symptoms. The system combines AI-powered symptom analysis with comprehensive medical databases to provide accurate diagnoses and recommendations.

## Features

- 🤖 AI-powered symptom analysis using deepseek-r1:14b model
- 💬 Interactive chat interface with real-time responses
- 📊 Comprehensive disease information including:
  - Symptoms analysis
  - Disease descriptions
  - Recommended workouts
  - Precautions
  - Diet recommendations
- 🖼️ Wikipedia image integration for visual reference
- 🔍 Additional information from Google search
- 🏥 MongoDB database for efficient data storage and retrieval

## Tech Stack

### Backend
- FastAPI (Python web framework)
- MongoDB (Database)
- Ollama (AI model serving)
- deepseek-r1:14b (AI model)

### Frontend
- React with TypeScript
- Material-UI for modern UI components
- Framer Motion for smooth animations
- Axios for API communication

## Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB
- Ollama with deepseek-r1:14b model

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/medicore2.0.git
cd medicore2.0
```

2. Install backend dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Create a `.env` file in the frontend directory

## Configuration

### Backend (.env)
```
MONGODB_URI=mongodb://localhost:27017
OLLAMA_API_URL=http://localhost:11434/api/generate
GOOGLE_API_KEY=your_google_api_key_here
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## Running the Application

1. Start MongoDB:
```bash
mongod
```

2. Start Ollama with deepseek-r1:14b:
```bash
ollama serve
```

3. Start the backend server:
```bash
python main.py
```

4. Start the frontend development server:
```bash
cd frontend
npm start
```

The application will be available at `http://localhost:3000`

## Usage

1. Open the application in your web browser
2. Describe your symptoms in the chat interface
3. The AI will analyze your symptoms and provide:
   - Potential diagnosis
   - Disease description
   - Recommended workouts
   - Precautions
   - Diet recommendations
   - Visual reference from Wikipedia

## Data Sources

- Symptoms database
- Disease descriptions
- Workout recommendations
- Precautions database
- Diet recommendations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
