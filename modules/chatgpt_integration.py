"""
ChatGPT Integration Module for ZeroTraceGPT Image Creator
Provides prompt enhancement and image improvement features
"""

import os
import requests
import json
import base64
import time
from typing import Optional, Dict, Any
import gradio as gr

class ChatGPTIntegration:
    def __init__(self):
        self.api_key = self._load_api_key()
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.last_request_time = 0
        self.min_request_interval = 2  # Minimum 2 seconds between requests
    
    def _load_api_key(self) -> str:
        """Load API key from apikey.txt file"""
        try:
            with open("apikey.txt", "r") as f:
                api_key = f.read().strip()
            if not api_key:
                raise ValueError("API key is empty")
            return api_key
        except FileNotFoundError:
            raise FileNotFoundError("apikey.txt file not found. Please create it with your OpenAI API key.")
        except Exception as e:
            raise Exception(f"Error loading API key: {str(e)}")
    
    def _rate_limit_protection(self):
        """Ensure minimum time between API requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_api_request(self, payload: dict, max_retries: int = 3) -> dict:
        """Make API request with retry logic and rate limiting"""
        for attempt in range(max_retries):
            try:
                self._rate_limit_protection()
                response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
                
                if response.status_code == 429:
                    # Rate limited - wait longer and retry
                    wait_time = min(60, (2 ** attempt) * 5)  # Exponential backoff, max 60 seconds
                    if attempt < max_retries - 1:
                        time.sleep(wait_time)
                        continue
                    else:
                        return {"error": f"Rate limited. Please wait {wait_time} seconds and try again."}
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    return {"error": f"Error connecting to ChatGPT API: {str(e)}"}
            except Exception as e:
                return {"error": f"Unexpected error: {str(e)}"}
        
        return {"error": "Max retries exceeded"}
    
    def enhance_prompt(self, original_prompt: str, style_preference: str = "photorealistic", enhancement_percentage: int = 50) -> str:
        """
        Enhance a prompt using ChatGPT for better image generation
        
        Args:
            original_prompt: The original user prompt
            style_preference: Style preference (photorealistic, artistic, anime, etc.)
            enhancement_percentage: Enhancement intensity (10-100%)
        
        Returns:
            Enhanced prompt string
        """
        if not original_prompt.strip():
            return "Please enter a prompt to enhance."
        
        try:
            # Calculate enhancement intensity based on percentage
            if enhancement_percentage <= 30:
                enhancement_level = "subtle"
                detail_multiplier = "1.2-1.5x"
            elif enhancement_percentage <= 60:
                enhancement_level = "moderate"
                detail_multiplier = "1.5-2x"
            elif enhancement_percentage <= 80:
                enhancement_level = "strong"
                detail_multiplier = "2-2.5x"
            else:
                enhancement_level = "maximum"
                detail_multiplier = "2.5-3x"

            system_prompt = f"""You are an expert AI image generation prompt engineer. Your task is to enhance user prompts to create better, more detailed, and more effective prompts for AI image generation.

Enhancement Level: {enhancement_level} ({enhancement_percentage}%)
Detail Multiplier: {detail_multiplier}

Guidelines:
1. Add specific details about lighting, composition, and mood
2. Include technical photography terms when appropriate
3. Specify art style, medium, and quality descriptors
4. Add environmental and atmospheric details
5. Keep the core concept but make it more vivid and descriptive
6. Use comma-separated tags for better AI model understanding
7. Enhancement intensity: {enhancement_level} - aim for {detail_multiplier} more detailed than the original
8. Style preference: {style_preference}

Examples:
- "cat" → "beautiful orange tabby cat, sitting gracefully on a windowsill, soft natural lighting, detailed fur texture, photorealistic, high quality, 8K resolution"
- "landscape" → "breathtaking mountain landscape at sunset, golden hour lighting, dramatic clouds, lush green valleys, photorealistic, cinematic composition, high detail"

Enhance this prompt with {enhancement_level} intensity while keeping the original intent:"""

            user_prompt = f"Original prompt: '{original_prompt}'\n\nPlease enhance this prompt for better AI image generation results."

            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }

            result = self._make_api_request(payload)
            
            if "error" in result:
                return result["error"]
            
            enhanced_prompt = result["choices"][0]["message"]["content"].strip()
            return enhanced_prompt
            
        except KeyError as e:
            return f"Error parsing ChatGPT response: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def improve_image_prompt(self, original_prompt: str, generated_image_description: str = "", enhancement_percentage: int = 50) -> str:
        """
        Generate an improved prompt based on the original prompt and generated image
        
        Args:
            original_prompt: The original prompt used
            generated_image_description: Description of what was generated
            enhancement_percentage: Enhancement intensity (10-100%)
        
        Returns:
            Improved prompt for better results
        """
        if not original_prompt.strip():
            return "Please provide the original prompt to improve."
        
        try:
            # Calculate enhancement intensity based on percentage
            if enhancement_percentage <= 30:
                enhancement_level = "subtle"
                improvement_focus = "minor adjustments"
            elif enhancement_percentage <= 60:
                enhancement_level = "moderate"
                improvement_focus = "balanced improvements"
            elif enhancement_percentage <= 80:
                enhancement_level = "strong"
                improvement_focus = "significant enhancements"
            else:
                enhancement_level = "maximum"
                improvement_focus = "major improvements"

            system_prompt = f"""You are an expert AI image generation prompt engineer. Your task is to analyze the original prompt and suggest improvements for generating a better version of the image.

Enhancement Level: {enhancement_level} ({enhancement_percentage}%)
Improvement Focus: {improvement_focus}

Guidelines:
1. Identify what might be missing from the original prompt
2. Suggest better lighting, composition, or style descriptions
3. Add technical details that could improve quality
4. Consider different artistic approaches or perspectives
5. Suggest specific improvements for better visual impact
6. Keep the core concept but enhance the execution
7. Provide 2-3 alternative improved prompts
8. Enhancement intensity: {enhancement_level} - focus on {improvement_focus}

Focus on making the prompt more effective for AI image generation with {enhancement_level} intensity."""

            user_prompt = f"""Original prompt: '{original_prompt}'
Generated image description: '{generated_image_description}'

Please suggest improvements to create a better version of this image. Provide specific, actionable improvements to the prompt."""

            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 600,
                "temperature": 0.8
            }

            result = self._make_api_request(payload)
            
            if "error" in result:
                return result["error"]
            
            improved_suggestions = result["choices"][0]["message"]["content"].strip()
            return improved_suggestions
            
        except KeyError as e:
            return f"Error parsing ChatGPT response: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def generate_alternative_prompt(self, original_prompt: str, variation_type: str = "creative") -> str:
        """
        Generate alternative prompts for creative variations
        
        Args:
            original_prompt: The original prompt
            variation_type: Type of variation (creative, artistic, photorealistic, etc.)
        
        Returns:
            Alternative prompt string
        """
        if not original_prompt.strip():
            return "Please provide a prompt to create variations."
        
        try:
            system_prompt = f"""You are a creative AI image generation prompt engineer. Create alternative prompts that explore different artistic interpretations of the original concept.

Guidelines:
1. Keep the core subject/concept
2. Explore different artistic styles, moods, or perspectives
3. Vary lighting, composition, and atmosphere
4. Consider different art movements or techniques
5. Create prompts that would generate visually distinct but related images
6. Variation type: {variation_type}

Provide 3 creative alternative prompts that explore different artistic directions."""

            user_prompt = f"Original prompt: '{original_prompt}'\n\nCreate creative alternative prompts for different artistic interpretations."

            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.9
            }

            result = self._make_api_request(payload)
            
            if "error" in result:
                return result["error"]
            
            alternatives = result["choices"][0]["message"]["content"].strip()
            return alternatives
            
        except KeyError as e:
            return f"Error parsing ChatGPT response: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

# Global instance
chatgpt = ChatGPTIntegration()

def enhance_prompt_ui(original_prompt: str, style_preference: str, enhancement_percentage: int) -> str:
    """UI wrapper for prompt enhancement"""
    return chatgpt.enhance_prompt(original_prompt, style_preference, enhancement_percentage)

def improve_image_prompt_ui(original_prompt: str, image_description: str, enhancement_percentage: int) -> str:
    """UI wrapper for image improvement"""
    return chatgpt.improve_image_prompt(original_prompt, image_description, enhancement_percentage)

def generate_alternative_prompt_ui(original_prompt: str, variation_type: str) -> str:
    """UI wrapper for alternative prompt generation"""
    return chatgpt.generate_alternative_prompt(original_prompt, variation_type)
