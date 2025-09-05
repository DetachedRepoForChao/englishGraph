#!/usr/bin/env python3
"""
添加介词知识点到数据库
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.database import neo4j_service
from backend.models.schema import KnowledgePoint
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_preposition_knowledge():
    """添加介词知识点"""
    print("🚀 开始添加介词知识点...")
    
    try:
        # 创建介词知识点
        preposition_data = {
            "name": "介词",
            "description": "表示名词、代词等与句中其他词的关系的词",
            "level": "初中一年级",
            "difficulty": "medium",
            "keywords": [
                "in", "on", "at", "by", "for", "with", "from", "to", "of", "about",
                "interested in", "good at", "afraid of", "proud of", "famous for",
                "介词", "前置词", "preposition", "介词短语", "固定搭配"
            ]
        }
        
        # 创建知识点对象
        kp = KnowledgePoint(
            name=preposition_data["name"],
            description=preposition_data["description"],
            level=preposition_data["level"],
            difficulty=preposition_data["difficulty"],
            keywords=preposition_data["keywords"]
        )
        
        # 添加到数据库
        result = neo4j_service.create_knowledge_point(kp)
        
        print(f"✅ 介词知识点添加成功: {result}")
        
        # 验证添加结果
        knowledge_points = neo4j_service.search_knowledge_points("介词")
        print(f"📚 验证结果: 找到 {len(knowledge_points)} 个相关知识点")
        for kp in knowledge_points:
            print(f"  - {kp['name']}: {kp['description']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 添加介词知识点失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    add_preposition_knowledge()
