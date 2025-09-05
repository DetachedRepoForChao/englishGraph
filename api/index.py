"""
Vercel Serverless Function Entry Point
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api.main import app

# Export the FastAPI app for Vercel
handler = app
