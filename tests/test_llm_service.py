# -*- coding: utf-8 -*-
"""
Basic tests for LLM service functionality
"""
import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
import io
from PIL import Image

from tests.base import BaseTestCase
from albumy.services.llm_service import generate_alt_text, get_llm_response, generate_sassy_description_from_file


class LLMServiceTestCase(BaseTestCase):
    """Basic test cases for LLM service"""

    def setUp(self):
        super().setUp()
        # Create a simple test image
        self.test_image = Image.new('RGB', (100, 100), color='red')
        self.test_image_bytes = io.BytesIO()
        self.test_image.save(self.test_image_bytes, format='JPEG')
        self.test_image_bytes.seek(0)
        self.image_data = self.test_image_bytes.getvalue()

    @patch('albumy.services.llm_service._get_gemini_client')
    def test_generate_alt_text_success(self, mock_get_client):
        """Test successful alt text generation"""
        # Mock the Gemini client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "A red square image"
        mock_client.models.generate_content.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = generate_alt_text(self.image_data)
        
        self.assertEqual(result, "A red square image")

    @patch('albumy.services.llm_service._get_gemini_client')
    def test_generate_alt_text_no_client(self, mock_get_client):
        """Test alt text generation when client is not available"""
        mock_get_client.return_value = None
        
        result = generate_alt_text(self.image_data)
        
        self.assertEqual(result, "Image description not available")

    @patch('albumy.services.llm_service._get_gemini_client')
    def test_get_llm_response_success(self, mock_get_client):
        """Test successful LLM response generation"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "This is a red square image"
        mock_client.models.generate_content.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_llm_response(self.image_data)
        
        self.assertEqual(result, "This is a red square image")

    # SZ added tests for sassy description functionality
    @patch('albumy.services.llm_service._get_gemini_client')
    def test_generate_sassy_description_from_file_success(self, mock_get_client):
        """Test successful sassy description generation from file"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Living my best life with this red square! 🔴✨"
        mock_client.models.generate_content.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Create a temporary test file using tempfile for cross-platform compatibility
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(self.image_data)
            temp_file_path = temp_file.name

        try:
            result = generate_sassy_description_from_file(temp_file_path)
            self.assertEqual(result, "Living my best life with this red square! 🔴✨")
        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    @patch('albumy.services.llm_service._get_gemini_client')
    def test_generate_sassy_description_from_file_no_client(self, mock_get_client):
        """Test sassy description generation when client is not available"""
        mock_get_client.return_value = None
        
        result = generate_sassy_description_from_file('/nonexistent/file.jpg')
        
        self.assertEqual(result, "Another day, another photo! 📸")

    def test_service_imports(self):
        """Test that service functions can be imported correctly"""
        try:
            from albumy.services.llm_service import get_llm_response, generate_alt_text, generate_sassy_description_from_file
            self.assertTrue(True)  # Import successful
        except ImportError as e:
            self.fail(f"Failed to import service functions: {e}")


if __name__ == '__main__':
    unittest.main()