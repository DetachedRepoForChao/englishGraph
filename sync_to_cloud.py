#!/usr/bin/env python3
"""
本地数据同步到Neo4j AuraDB云数据库脚本
"""
import sys
import os
from neo4j import GraphDatabase
import logging
import json
from typing import List, Dict, Any

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 本地数据库配置
LOCAL_NEO4J_URI = "bolt://localhost:7687"
LOCAL_NEO4J_USERNAME = "neo4j"
LOCAL_NEO4J_PASSWORD = "knowledge123"

# 云数据库配置
CLOUD_NEO4J_URI = "neo4j+s://383b0a61.databases.neo4j.io"
CLOUD_NEO4J_USERNAME = "neo4j"
CLOUD_NEO4J_PASSWORD = "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI"

class DataSyncService:
    def __init__(self):
        self.local_driver = None
        self.cloud_driver = None
    
    def connect_databases(self):
        """连接本地和云数据库"""
        try:
            # 连接本地数据库
            logger.info("🔌 连接本地Neo4j数据库...")
            self.local_driver = GraphDatabase.driver(
                LOCAL_NEO4J_URI, 
                auth=(LOCAL_NEO4J_USERNAME, LOCAL_NEO4J_PASSWORD)
            )
            
            # 测试本地连接
            with self.local_driver.session() as session:
                session.run("RETURN 1")
            logger.info("✅ 本地数据库连接成功")
            
            # 连接云数据库
            logger.info("☁️ 连接Neo4j AuraDB云数据库...")
            self.cloud_driver = GraphDatabase.driver(
                CLOUD_NEO4J_URI,
                auth=(CLOUD_NEO4J_USERNAME, CLOUD_NEO4J_PASSWORD)
            )
            
            # 测试云连接
            with self.cloud_driver.session() as session:
                session.run("RETURN 1")
            logger.info("✅ 云数据库连接成功")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据库连接失败: {e}")
            return False
    
    def export_local_data(self):
        """从本地数据库导出所有数据"""
        logger.info("📤 导出本地数据...")
        
        data = {
            "knowledge_points": [],
            "questions": [],
            "relationships": []
        }
        
        try:
            with self.local_driver.session() as session:
                # 导出知识点
                logger.info("📚 导出知识点...")
                kp_result = session.run("""
                    MATCH (kp:KnowledgePoint)
                    RETURN kp.id as id, kp.name as name, kp.description as description,
                           kp.level as level, kp.difficulty as difficulty, kp.keywords as keywords
                """)
                
                for record in kp_result:
                    kp_data = {
                        "id": record["id"],
                        "name": record["name"],
                        "description": record["description"],
                        "level": record["level"],
                        "difficulty": record["difficulty"],
                        "keywords": record["keywords"] or []
                    }
                    data["knowledge_points"].append(kp_data)
                
                logger.info(f"✅ 导出了 {len(data['knowledge_points'])} 个知识点")
                
                # 导出题目
                logger.info("📝 导出题目...")
                q_result = session.run("""
                    MATCH (q:Question)
                    RETURN q.id as id, q.content as content, q.question_type as question_type,
                           q.options as options, q.answer as answer, q.analysis as analysis,
                           q.source as source, q.difficulty as difficulty
                """)
                
                for record in q_result:
                    q_data = {
                        "id": record["id"],
                        "content": record["content"],
                        "question_type": record["question_type"],
                        "options": record["options"] or [],
                        "answer": record["answer"],
                        "analysis": record["analysis"],
                        "source": record["source"],
                        "difficulty": record["difficulty"]
                    }
                    data["questions"].append(q_data)
                
                logger.info(f"✅ 导出了 {len(data['questions'])} 道题目")
                
                # 导出关系
                logger.info("🔗 导出关系...")
                rel_result = session.run("""
                    MATCH (q:Question)-[r:TESTS]->(kp:KnowledgePoint)
                    RETURN q.id as question_id, kp.id as kp_id, r.weight as weight
                """)
                
                for record in rel_result:
                    rel_data = {
                        "question_id": record["question_id"],
                        "kp_id": record["kp_id"],
                        "weight": record["weight"]
                    }
                    data["relationships"].append(rel_data)
                
                logger.info(f"✅ 导出了 {len(data['relationships'])} 个关系")
                
                # 导出知识点层级关系
                hierarchy_result = session.run("""
                    MATCH (parent:KnowledgePoint)-[r:HAS_SUB_POINT]->(child:KnowledgePoint)
                    RETURN parent.id as parent_id, child.id as child_id
                """)
                
                hierarchy_data = []
                for record in hierarchy_result:
                    hierarchy_data.append({
                        "parent_id": record["parent_id"],
                        "child_id": record["child_id"]
                    })
                
                data["hierarchy"] = hierarchy_data
                logger.info(f"✅ 导出了 {len(hierarchy_data)} 个层级关系")
                
            return data
            
        except Exception as e:
            logger.error(f"❌ 导出数据失败: {e}")
            return None
    
    def clear_cloud_database(self):
        """清空云数据库"""
        logger.info("🗑️ 清空云数据库...")
        
        try:
            with self.cloud_driver.session() as session:
                # 删除所有节点和关系
                session.run("MATCH (n) DETACH DELETE n")
                logger.info("✅ 云数据库已清空")
                return True
        except Exception as e:
            logger.error(f"❌ 清空云数据库失败: {e}")
            return False
    
    def import_to_cloud(self, data: Dict[str, Any]):
        """将数据导入到云数据库"""
        logger.info("📥 导入数据到云数据库...")
        
        try:
            with self.cloud_driver.session() as session:
                # 创建约束和索引
                logger.info("🔧 创建约束和索引...")
                constraints = [
                    "CREATE CONSTRAINT knowledge_point_id IF NOT EXISTS FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE",
                    "CREATE CONSTRAINT question_id IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE"
                ]
                
                for constraint in constraints:
                    try:
                        session.run(constraint)
                    except Exception as e:
                        logger.warning(f"约束创建警告: {e}")
                
                # 导入知识点
                logger.info("📚 导入知识点...")
                for kp in data["knowledge_points"]:
                    session.run("""
                        CREATE (kp:KnowledgePoint {
                            id: $id,
                            name: $name,
                            description: $description,
                            level: $level,
                            difficulty: $difficulty,
                            keywords: $keywords
                        })
                    """, kp)
                
                logger.info(f"✅ 导入了 {len(data['knowledge_points'])} 个知识点")
                
                # 导入题目
                logger.info("📝 导入题目...")
                for q in data["questions"]:
                    session.run("""
                        CREATE (q:Question {
                            id: $id,
                            content: $content,
                            question_type: $question_type,
                            options: $options,
                            answer: $answer,
                            analysis: $analysis,
                            source: $source,
                            difficulty: $difficulty
                        })
                    """, q)
                
                logger.info(f"✅ 导入了 {len(data['questions'])} 道题目")
                
                # 创建TESTS关系
                logger.info("🔗 创建题目-知识点关系...")
                for rel in data["relationships"]:
                    session.run("""
                        MATCH (q:Question {id: $question_id})
                        MATCH (kp:KnowledgePoint {id: $kp_id})
                        CREATE (q)-[:TESTS {weight: $weight}]->(kp)
                    """, rel)
                
                logger.info(f"✅ 创建了 {len(data['relationships'])} 个TESTS关系")
                
                # 创建知识点层级关系
                if "hierarchy" in data and data["hierarchy"]:
                    logger.info("🏗️ 创建知识点层级关系...")
                    for hier in data["hierarchy"]:
                        session.run("""
                            MATCH (parent:KnowledgePoint {id: $parent_id})
                            MATCH (child:KnowledgePoint {id: $child_id})
                            CREATE (parent)-[:HAS_SUB_POINT]->(child)
                        """, hier)
                    
                    logger.info(f"✅ 创建了 {len(data['hierarchy'])} 个层级关系")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ 导入数据失败: {e}")
            return False
    
    def verify_sync(self):
        """验证同步结果"""
        logger.info("🔍 验证同步结果...")
        
        try:
            with self.cloud_driver.session() as session:
                # 统计云数据库中的数据
                stats = {}
                
                # 知识点数量
                kp_result = session.run("MATCH (kp:KnowledgePoint) RETURN count(kp) as count")
                stats["knowledge_points"] = kp_result.single()["count"]
                
                # 题目数量
                q_result = session.run("MATCH (q:Question) RETURN count(q) as count")
                stats["questions"] = q_result.single()["count"]
                
                # 关系数量
                rel_result = session.run("MATCH ()-[r:TESTS]->() RETURN count(r) as count")
                stats["relationships"] = rel_result.single()["count"]
                
                # 层级关系数量
                hier_result = session.run("MATCH ()-[r:HAS_SUB_POINT]->() RETURN count(r) as count")
                stats["hierarchy"] = hier_result.single()["count"]
                
                logger.info("📊 云数据库统计:")
                logger.info(f"   知识点: {stats['knowledge_points']} 个")
                logger.info(f"   题目: {stats['questions']} 道")
                logger.info(f"   TESTS关系: {stats['relationships']} 个")
                logger.info(f"   层级关系: {stats['hierarchy']} 个")
                
                return stats
                
        except Exception as e:
            logger.error(f"❌ 验证失败: {e}")
            return None
    
    def close_connections(self):
        """关闭数据库连接"""
        if self.local_driver:
            self.local_driver.close()
        if self.cloud_driver:
            self.cloud_driver.close()
        logger.info("🔌 数据库连接已关闭")

def main():
    """主函数"""
    logger.info("🚀 开始数据同步...")
    
    sync_service = DataSyncService()
    
    try:
        # 1. 连接数据库
        if not sync_service.connect_databases():
            return False
        
        # 2. 导出本地数据
        local_data = sync_service.export_local_data()
        if not local_data:
            return False
        
        # 3. 清空云数据库
        if not sync_service.clear_cloud_database():
            return False
        
        # 4. 导入到云数据库
        if not sync_service.import_to_cloud(local_data):
            return False
        
        # 5. 验证同步结果
        stats = sync_service.verify_sync()
        if not stats:
            return False
        
        logger.info("🎉 数据同步完成！")
        return True
        
    except Exception as e:
        logger.error(f"❌ 同步过程出错: {e}")
        return False
    
    finally:
        sync_service.close_connections()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
