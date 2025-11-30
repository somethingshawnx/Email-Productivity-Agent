import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class LLMService:
    def __init__(self):
        # Initialize Groq client
        try:
            # The client automatically looks for the GROQ_API_KEY environment variable.
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            
            # CRITICAL FIX: Using a currently supported high-performance model.
            self.model = "llama-3.1-8b-instant" 
            
            # Check if API key is actually present, even if client initialized
            if not os.environ.get("GROQ_API_KEY"):
                 raise ValueError("GROQ_API_KEY environment variable not found.")
                 
        except Exception as e:
            print(f"Error initializing Groq client: {e}")
            self.client = None
            
    def process_with_prompt(self, system_prompt: str, content: str, json_mode: bool = False):
        """
        Constructs and sends the LLM request using the user-defined prompt.
        """
        # Check for client availability before making an API call
        if not self.client:
            return "LLM Service not initialized. Check GROQ_API_KEY in .env."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Process the following email content:\n\n{content}"}
        ]
        
        try:
            config_params = {}
            if json_mode:
                # Instruct the model to output a JSON object
                config_params["response_format"] = {"type": "json_object"}
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **config_params
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Safety & Robustness: Handles LLM errors gracefully
            error_message = f"LLM Error during processing: {e}"
            print(error_message)
            
            # Return an error message suitable for the output type
            if json_mode:
                # Return JSON error structure if JSON was requested
                return json.dumps({"error": error_message})
            return f"Error processing content: {e}"