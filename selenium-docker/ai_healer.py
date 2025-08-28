import os
import openai
from PIL import Image
import base64
from io import BytesIO
import time
from dotenv import load_dotenv
load_dotenv()

class AIHealer:
    def __init__(self, api_key=None):
        """Initialize AI Healer with OpenAI API"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to the constructor.")
        
        openai.api_key = self.api_key
        self.model = "gpt-4-vision-preview"
        self.max_retries = 3
        self.retry_delay = 2

    def analyze_element_issue(self, element, screenshot, context=None):
        """Use AI to analyze why an element interaction failed"""
        # Convert screenshot to base64
        buffered = BytesIO()
        screenshot.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"""
                    I'm having trouble interacting with a web element in my Selenium test.
                    Context: {context or 'No additional context provided'}
                    
                    Please analyze the screenshot and help me understand:
                    1. Why the element might not be interactable
                    2. What selectors I could try instead
                    3. Any potential issues with the page state
                    """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_str}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ]
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to analyze element: {str(e)}"

    def suggest_better_locator(self, driver, element, current_locator):
        """Get AI suggestions for more robust element locators"""
        element_html = driver.execute_script("""
            var element = arguments[0];
            return element.outerHTML;
        """, element)
        
        page_source = driver.page_source[:4000]  # Get first 4000 chars of page source
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert in web automation testing. Suggest more reliable locators for web elements."
            },
            {
                "role": "user",
                "content": f"""
                Current locator strategy: {current_locator}
                
                Element HTML:
                {element_html}
                
                Partial page source:
                {page_source}
                
                Please suggest more reliable locator strategies for this element, 
                ordered by reliability. Consider:
                - data-testid attributes
                - Unique IDs or classes
                - Semantic HTML structure
                - Text content if unique
                """
            }
        ]
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to suggest better locator: {str(e)}"
