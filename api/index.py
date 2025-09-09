"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 使用轻量版NLP服务
try:
    import backend.services.nlp_service_light as nlp_service_module
    sys.modules['backend.services.nlp_service'] = nlp_service_module
except ImportError as e:
    print(f"Warning: Could not import nlp_service_light: {e}")

# Import FastAPI app
from backend.api.main import app

# Vercel expects 'app' not 'handler'
# This is the ASGI application that Vercel will use
