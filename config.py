import os
from dotenv import load_dotenv
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for handling environment variables and LangChain settings."""
    
    @staticmethod
    def get_google_api_key() -> Optional[str]:
        """Retrieve the GOOGLE_API_KEY from environment variables."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in the .env file.")
        return api_key

    @staticmethod
    def get_chat_model(temperature: float = 0.7, model: str = "gemini-2.0-flash") -> ChatGoogleGenerativeAI:
        """
        Initialize and return a ChatGoogleGenerativeAI instance.
        
        Args:
            temperature (float): Temperature for response generation (0-1)
            model (str): Gemini model to use
        
        Returns:
            ChatGoogleGenerativeAI: Configured chat model instance
        """
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=Config.get_google_api_key(),
            temperature=temperature,
            convert_system_message_to_human=True
        )
# Example usage and testing
"""if __name__ == "__main__":
    try:
        # Test the configuration
        api_key = Config.get_google_api_key()
        print(f"API Key loaded: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
        
        # Test chat model initialization
        chat_model = Config.get_chat_model()
        print(f"Chat model initialized: {chat_model.model_name}")
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")"""