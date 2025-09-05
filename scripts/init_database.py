#!/usr/bin/env python3
"""
数据库初始化脚本
用于初始化Neo4j数据库，创建约束、索引，并导入基础数据
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.database import neo4j_service
from backend.models.schema import KnowledgePoint, SAMPLE_KNOWLEDGE_POINTS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """初始化数据库"""
    logger.info("开始初始化数据库...")
    
    # 连接数据库
    if not neo4j_service.connect():
        logger.error("无法连接到Neo4j数据库，请确保Neo4j服务正在运行")
        return False
    
    try:
        # 初始化数据库结构
        logger.info("创建约束和索引...")
        neo4j_service.initialize_database()
        
        # 导入基础知识点
        logger.info("导入基础知识点...")
        knowledge_point_ids = {}
        
        for kp_data in SAMPLE_KNOWLEDGE_POINTS:
            kp = KnowledgePoint(**kp_data)
            kp_id = neo4j_service.create_knowledge_point(kp)
            knowledge_point_ids[kp.name] = kp_id
            logger.info(f"创建知识点: {kp.name} (ID: {kp_id})")
        
        # 创建知识点层级关系
        logger.info("创建知识点层级关系...")
        hierarchy_relations = [
            ("英语语法", "动词时态"),
            ("动词时态", "一般现在时"),
            ("动词时态", "一般过去时"),
            ("动词时态", "现在进行时")
        ]
        
        for parent_name, child_name in hierarchy_relations:
            if parent_name in knowledge_point_ids and child_name in knowledge_point_ids:
                neo4j_service.create_knowledge_hierarchy(
                    knowledge_point_ids[parent_name],
                    knowledge_point_ids[child_name]
                )
                logger.info(f"创建层级关系: {parent_name} -> {child_name}")
        
        logger.info("数据库初始化完成！")
        return True
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return False
    
    finally:
        neo4j_service.close()


def clear_and_reinit():
    """清空数据库并重新初始化"""
    logger.warning("警告：这将清空所有数据！")
    response = input("确定要继续吗？(y/N): ")
    
    if response.lower() != 'y':
        logger.info("操作已取消")
        return
    
    if not neo4j_service.connect():
        logger.error("无法连接到Neo4j数据库")
        return
    
    try:
        logger.info("清空数据库...")
        neo4j_service.clear_database()
        neo4j_service.close()
        
        logger.info("重新初始化...")
        init_database()
        
    except Exception as e:
        logger.error(f"操作失败: {e}")
    finally:
        neo4j_service.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="数据库初始化脚本")
    parser.add_argument("--clear", action="store_true", help="清空数据库并重新初始化")
    
    args = parser.parse_args()
    
    if args.clear:
        clear_and_reinit()
    else:
        init_database()
