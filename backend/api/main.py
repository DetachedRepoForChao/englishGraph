"""
FastAPI主应用
提供K12英语知识图谱的API接口
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any, Optional
import logging

from backend.services.database import neo4j_service
from backend.models.schema import KnowledgePoint, Question, QuestionType, DifficultyLevel
from backend.api.routes import knowledge_routes, question_routes, annotation_routes, analytics_routes, ai_agent_routes, meganno_routes, init_routes

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="K12英语知识图谱系统",
    description="基于图数据库的英语题库智能标注与分析系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# 数据库依赖
def get_database():
    """获取数据库连接"""
    if not neo4j_service.driver:
        if not neo4j_service.connect():
            raise HTTPException(status_code=500, detail="数据库连接失败")
    return neo4j_service


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("启动K12英语知识图谱系统...")
    
    # 连接数据库
    if neo4j_service.connect():
        logger.info("数据库连接成功")
    else:
        logger.error("数据库连接失败")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("关闭系统...")
    neo4j_service.close()


# 根路由 - 返回前端页面
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回主页面"""
    with open("frontend/templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# 数据分析测试页面
@app.get("/analytics-test", response_class=HTMLResponse)
async def analytics_test():
    """返回数据分析测试页面"""
    with open("frontend/templates/analytics_test.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# 调试页面
@app.get("/debug", response_class=HTMLResponse)
async def debug_page():
    """返回调试页面"""
    with open("frontend/templates/debug.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# API测试页面
@app.get("/test-api", response_class=HTMLResponse)
async def test_api_page():
    """返回API测试页面"""
    with open("test_frontend_api.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "K12英语知识图谱系统运行正常"}


# 包含其他路由
app.include_router(knowledge_routes.router, prefix="/api/knowledge", tags=["知识点"])
app.include_router(question_routes.router, prefix="/api/questions", tags=["题目"])
app.include_router(annotation_routes.router, prefix="/api/annotation", tags=["标注"])
app.include_router(analytics_routes.router, prefix="/api/analytics", tags=["数据分析"])
app.include_router(ai_agent_routes.router, prefix="/api/ai-agent", tags=["AI智能代理"])
app.include_router(meganno_routes.router, prefix="/api/meganno", tags=["MEGAnno+集成"])
app.include_router(init_routes.router, prefix="/api", tags=["系统初始化"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
