from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from symptoms import Symptoms
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Ollama with DeepSeek
try:
    llm = Ollama(model="deepseek-r1:7b")
    logger.info("Successfully initialized Ollama LLM")
except Exception as e:
    logger.error(f"Failed to initialize Ollama LLM: {str(e)}")
    raise

def get_available_symptoms() -> list[str]:
    """Get all available symptoms from the Symptoms model."""
    return list(Symptoms.__fields__.keys())

# Create prompt template
prompt = PromptTemplate(
    input_variables=["message", "available_symptoms"],
    template="""Analyze the following message and list all medical symptoms mentioned. 
    Match each symptom to the exact symptom name from the provided list.
    Return only the exact symptom names, one per line, without any additional text or formatting.
    
    Available Symptoms:
    {available_symptoms}
    
    Message: {message}
    """
)

# Create LLM chain
chain = LLMChain(llm=llm, prompt=prompt)

def get_llm_response(prompt: str) -> str:
    try:
        response = chain.run(prompt)
        return response.strip()
    except Exception as e:
        logger.error(f"Error getting LLM response: {str(e)}")
        return ""

def extract_symptoms_with_llm(message: str) -> list:
    try:
        # Get available symptoms
        available_symptoms = get_available_symptoms()
        
        # Get response from LLM
        response = get_llm_response({
            "message": message,
            "available_symptoms": "\n".join(available_symptoms)
        })
        
        # Split response into lines and clean up
        symptoms = [s.strip().lower() for s in response.split('\n') if s.strip()]
        
        # Filter to only include valid symptoms
        valid_symptoms = [s for s in symptoms if s in available_symptoms]
        
        logger.info(f"Extracted symptoms: {valid_symptoms}")
        return valid_symptoms
    except Exception as e:
        logger.error(f"Error extracting symptoms: {str(e)}")
        return []

def extract_symptoms(message: str) -> tuple[str, list[str]]:
    """
    Extract symptoms from user message using LLM with RAG.
    Returns the raw response and extracted symptoms.
    """
    try:
        # Get available symptoms
        available_symptoms = get_available_symptoms()
        logger.info(f"Available symptoms: {available_symptoms}")
        
        # Create prompt for symptom extraction with RAG
        prompt = f"""
        You are a medical symptom extractor. Your task is to extract symptoms from the user's message and match them with the provided list of possible symptoms.

        User Message: {message}

        Available Symptoms:
        {', '.join(available_symptoms)}

        Instructions:
        1. Extract symptoms from the message that match or are similar to the ones in the list above
        2. Return ONLY the exact symptom names from the list
        3. One symptom per line
        4. Do not include any explanations or additional text
        5. If a symptom is mentioned in a different form, match it to the closest one in the list
        6. Only return symptoms that exist in the list above

        Example:
        Message: "I have a high temperature and my head hurts and feeling cold"
        Response:
        high_fever
        headache
        cold_hands_and feets
        """
        
        # Get response from LLM
        response = get_llm_response(prompt)
        logger.info(f"LLM Response: {response}")
        
        # Split response into lines and clean each symptom
        symptoms = [s.strip() for s in response.split('\n') if s.strip()]
        
        # Validate symptoms against available list
        valid_symptoms = [s for s in symptoms if s in available_symptoms]
        logger.info(f"Validated symptoms: {valid_symptoms}")
        
        return response, valid_symptoms
        
    except Exception as e:
        logger.error(f"Error in extract_symptoms: {str(e)}")
        return "", [] 