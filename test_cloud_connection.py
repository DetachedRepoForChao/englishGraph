#!/usr/bin/env python3
"""
测试Neo4j AuraDB连接
"""
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 云数据库配置
CLOUD_NEO4J_URI = "neo4j+s://383b0a61.databases.neo4j.io"
CLOUD_NEO4J_USERNAME = "neo4j"
CLOUD_NEO4J_PASSWORD = "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI"

def test_connection():
    """测试连接"""
    try:
        logger.info("尝试连接Neo4j AuraDB...")
        logger.info(f"URI: {CLOUD_NEO4J_URI}")
        logger.info(f"Username: {CLOUD_NEO4J_USERNAME}")
        
        # 尝试不同的连接方式
        driver = GraphDatabase.driver(
            CLOUD_NEO4J_URI,
            auth=(CLOUD_NEO4J_USERNAME, CLOUD_NEO4J_PASSWORD),
            database="neo4j"  # 明确指定数据库名
        )
        
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            logger.info(f"连接成功! 测试结果: {record['test']}")
            
            # 测试数据库状态
            result = session.run("MATCH (n) RETURN count(n) as node_count")
            count = result.single()["node_count"]
            logger.info(f"当前数据库中有 {count} 个节点")
        
        driver.close()
        return True
        
    except Exception as e:
        logger.error(f"连接失败: {e}")
        logger.error(f"错误类型: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_connection()
