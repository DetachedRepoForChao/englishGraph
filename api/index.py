"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 使用轻量版NLP服务
import backend.services.nlp_service_light as nlp_service_module
sys.modules['backend.services.nlp_service'] = nlp_service_module

from backend.api.main import app

# Export the FastAPI app for Vercel
handler = app
