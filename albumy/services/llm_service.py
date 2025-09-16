# -*- coding: utf-8 -*-
"""
LLM Service for Albumy

This module provides LLM-powered functionality for the Albumy application,
specifically for generating alternative text for images using Google's Gemini API.

Functions:
    get_llm_response(image_data: bytes) -> str: Get raw LLM response for image
    generate_alt_text(image_data: bytes) -> str: Generate accessibility-friendly alt text
    generate_alt_text_from_file(file_path: str) -> str: Generate alt text from file path

Dependencies:
    - google-genai: Google's Gemini API client
    - PIL (Pillow): Image processing
    - python-dotenv: Environment variable loading

Environment Variables:
    - GEMINI_API_KEY: Google Gemini API key (required)

Author: Steve Zhou
Date: 2025-08-28
"""
from google import genai
from PIL import Image
import io
import os
import logging
from flask import current_app
from dotenv import load_dotenv

# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def _get_gemini_client():
    """Get or create Gemini client with proper error handling"""
    try:
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            logger.error("GEMINI_API_KEY environment variable is not set")
            return None
        
        return genai.Client(api_key=gemini_api_key)
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        return None

def get_llm_response(image_data: bytes) -> str:
    """
    Get LLM response for image data.
    
    Args:
        image_data: Raw image bytes
        
    Returns:
        Generated text response or empty string on error
    """
    try:
        # Get Gemini client
        gemini_client = _get_gemini_client()
        if not gemini_client:
            return ""
        
        # Open and process the image
        image = Image.open(io.BytesIO(image_data))
        
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[image, "Tell me what is in this image?"]
        )
        
        return response.text.strip()
        
    except Exception as e:
        logger.error(f"Error generating LLM response: {e}")
        return ""

def generate_alt_text(image_data: bytes) -> str:
    """
    Generate alternative text for an image using LLM.
    
    Args:
        image_data: Raw image bytes
        
    Returns:
        Generated alt text or default text on error
    """
    try:
        # Get Gemini client
        gemini_client = _get_gemini_client()
        if not gemini_client:
            return "Image description not available"
        
        # Open and process the image
        image = Image.open(io.BytesIO(image_data))
        
        # More specific prompt for alt text generation
        prompt = """Please describe this image in a concise way that would be helpful for someone using a screen reader. 
        Focus on the main subject, action, and important details. Keep it under 125 characters if possible.
        Format as simple, descriptive text without technical jargon."""
        
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[image, prompt]
        )
        
        alt_text = response.text.strip()
        
        # Ensure the alt text is not too long (HTML alt attributes should be concise)
        if len(alt_text) > 500:
            alt_text = alt_text[:497] + "..."
        
        return alt_text if alt_text else "Image description not available"
        
    except Exception as e:
        logger.error(f"Error generating alt text: {e}")
        return "Image description not available"

def generate_alt_text_from_file(file_path: str) -> str:
    """
    Generate alternative text for an image from file path.
    
    Args:
        file_path: Path to the image file
        
    Returns:
        Generated alt text or default text on error
    """
    try:
        with open(file_path, 'rb') as f:
            image_data = f.read()
        return generate_alt_text(image_data)
    except Exception as e:
        logger.error(f"Error reading image file {file_path}: {e}")
        return "Image description not available"

def generate_sassy_description_from_file(file_path: str) -> str:
    """
    SZ: Generate a sassy, fun description for an image from file path.
    
    Args:
        file_path: Path to the image file
        
    Returns:
        Generated sassy description or default text on error
    """
    try:
        # Get Gemini client
        gemini_client = _get_gemini_client()
        if not gemini_client:
            return "Another day, another photo! 📸"
        
        # Read and process the image
        with open(file_path, 'rb') as f:
            image_data = f.read()
        
        image = Image.open(io.BytesIO(image_data))
        
        # SZ: Prompt for generating sassy, fun descriptions
        prompt = """Look at this image and write a fun, sassy, and engaging description that would make someone want to like and comment on this post. 
        Be creative, use emojis if appropriate, and keep it under 200 characters. 
        Make it feel personal and relatable, like something you'd see on a popular social media post.
        Don't be too formal - be casual and entertaining!"""
        
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[image, prompt]
        )
        
        description = response.text.strip()
        
        # Ensure the description is not too long
        if len(description) > 500:
            description = description[:497] + "..."
        
        return description if description else "Another day, another photo! 📸"
        
    except Exception as e:
        logger.error(f"Error generating sassy description: {e}")
        return "Another day, another photo! 📸"