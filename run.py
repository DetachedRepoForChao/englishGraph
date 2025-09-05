#!/usr/bin/env python3
"""
K12英语知识图谱系统启动脚本
"""
import os
import sys
import uvicorn
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置环境变量
os.environ.setdefault("PYTHONPATH", str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import neo4j
        import uvicorn
        import jieba
        import sklearn
        logger.info("所有依赖已安装")
        return True
    except ImportError as e:
        logger.error(f"缺少依赖: {e}")
        logger.error("请运行: pip install -r requirements.txt")
        return False


def check_neo4j_connection():
    """检查Neo4j连接"""
    try:
        from backend.services.database import neo4j_service
        if neo4j_service.connect():
            logger.info("Neo4j数据库连接成功")
            neo4j_service.close()
            return True
        else:
            logger.warning("Neo4j数据库连接失败，请检查配置")
            return False
    except Exception as e:
        logger.warning(f"Neo4j连接检查失败: {e}")
        return False


def main():
    """主启动函数"""
    logger.info("启动K12英语知识图谱系统...")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查Neo4j连接
    neo4j_ok = check_neo4j_connection()
    if not neo4j_ok:
        logger.warning("Neo4j连接失败，但系统仍会启动（部分功能可能不可用）")
    
    # 创建必要的目录
    os.makedirs("logs", exist_ok=True)
    
    # 启动服务
    try:
        logger.info("启动FastAPI服务器...")
        logger.info("访问地址: http://localhost:8000")
        logger.info("API文档: http://localhost:8000/docs")
        
        uvicorn.run(
            "backend.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("系统已停止")
    except Exception as e:
        logger.error(f"启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
