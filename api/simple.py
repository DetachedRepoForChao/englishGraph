"""
简化的Vercel入口点 - 用于调试
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

# 创建简单的FastAPI应用
app = FastAPI(title="K12英语知识图谱系统 - 简化版")

@app.get("/")
async def root():
    return {"message": "K12英语知识图谱系统正在运行", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "系统运行正常"}

@app.get("/test-env")
async def test_environment():
    """测试环境变量"""
    return {
        "neo4j_uri": os.getenv("NEO4J_URI", "未设置"),
        "neo4j_username": os.getenv("NEO4J_USERNAME", "未设置"),
        "neo4j_password_set": bool(os.getenv("NEO4J_PASSWORD")),
        "python_path": os.getcwd()
    }

@app.get("/api/test")
async def api_test():
    return {"message": "API测试成功", "endpoint": "/api/test"}

# 这是Vercel需要的应用实例
