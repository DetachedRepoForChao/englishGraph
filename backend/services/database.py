"""
Neo4j数据库连接和操作服务
"""
import os
import logging
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase, Driver, Session
from dotenv import load_dotenv

from backend.models.schema import (
    KnowledgePoint, Question, Textbook, Chapter,
    GraphSchema
)

# 加载环境变量
load_dotenv("config.env")

logger = logging.getLogger(__name__)


class Neo4jService:
    """Neo4j数据库服务类"""
    
    def __init__(self):
        self.driver: Optional[Driver] = None
        # Support both local and Vercel environment variables
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        
    def connect(self) -> bool:
        """连接到Neo4j数据库"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri, 
                auth=(self.username, self.password)
            )
            # 测试连接
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            logger.info("Successfully connected to Neo4j")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        if self.driver:
            self.driver.close()
    
    def initialize_database(self):
        """初始化数据库 - 创建约束和索引"""
        if not self.driver:
            raise Exception("Database not connected")
            
        with self.driver.session() as session:
            # 创建约束
            for constraint in GraphSchema.get_create_constraints_cypher():
                try:
                    session.run(constraint)
                    logger.info(f"Created constraint: {constraint}")
                except Exception as e:
                    logger.warning(f"Constraint may already exist: {e}")
            
            # 创建索引
            for index in GraphSchema.get_create_indexes_cypher():
                try:
                    session.run(index)
                    logger.info(f"Created index: {index}")
                except Exception as e:
                    logger.warning(f"Index may already exist: {e}")
    
    def clear_database(self):
        """清空数据库（谨慎使用）"""
        if not self.driver:
            raise Exception("Database not connected")
            
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.info("Database cleared")
    
    # ===== 知识点操作 =====
    
    def create_knowledge_point(self, kp: KnowledgePoint) -> str:
        """创建知识点"""
        with self.driver.session() as session:
            cypher = """
            CREATE (kp:KnowledgePoint {
                id: $id,
                name: $name,
                description: $description,
                level: $level,
                difficulty: $difficulty,
                keywords: $keywords
            })
            RETURN kp.id as id
            """
            
            # 生成ID如果没有提供
            if not kp.id:
                kp.id = f"kp_{hash(kp.name) % 1000000}"
            
            result = session.run(cypher, {
                "id": kp.id,
                "name": kp.name,
                "description": kp.description,
                "level": kp.level,
                "difficulty": kp.difficulty,
                "keywords": kp.keywords
            })
            
            return result.single()["id"]
    
    def get_knowledge_point(self, kp_id: str) -> Optional[Dict[str, Any]]:
        """获取知识点"""
        with self.driver.session() as session:
            cypher = "MATCH (kp:KnowledgePoint {id: $id}) RETURN kp"
            result = session.run(cypher, {"id": kp_id})
            record = result.single()
            return dict(record["kp"]) if record else None
    
    def search_knowledge_points(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索知识点"""
        with self.driver.session() as session:
            cypher = """
            MATCH (kp:KnowledgePoint)
            WHERE kp.name CONTAINS $keyword 
               OR any(k in kp.keywords WHERE k CONTAINS $keyword)
               OR kp.description CONTAINS $keyword
            RETURN kp
            ORDER BY kp.name
            """
            result = session.run(cypher, {"keyword": keyword})
            return [dict(record["kp"]) for record in result]
    
    def create_knowledge_hierarchy(self, parent_id: str, child_id: str):
        """创建知识点层级关系"""
        with self.driver.session() as session:
            cypher = """
            MATCH (parent:KnowledgePoint {id: $parent_id})
            MATCH (child:KnowledgePoint {id: $child_id})
            CREATE (parent)-[:HAS_SUB_POINT]->(child)
            """
            session.run(cypher, {"parent_id": parent_id, "child_id": child_id})
    
    # ===== 题目操作 =====
    
    def create_question(self, question: Question) -> str:
        """创建题目"""
        with self.driver.session() as session:
            cypher = """
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
            RETURN q.id as id
            """
            
            # 生成ID如果没有提供
            if not question.id:
                question.id = f"q_{hash(question.content) % 1000000}"
            
            result = session.run(cypher, {
                "id": question.id,
                "content": question.content,
                "question_type": question.question_type,
                "options": question.options,
                "answer": question.answer,
                "analysis": question.analysis,
                "source": question.source,
                "difficulty": question.difficulty
            })
            
            return result.single()["id"]
    
    def get_question(self, question_id: str) -> Optional[Dict[str, Any]]:
        """获取题目"""
        with self.driver.session() as session:
            cypher = "MATCH (q:Question {id: $id}) RETURN q"
            result = session.run(cypher, {"id": question_id})
            record = result.single()
            return dict(record["q"]) if record else None
    
    def link_question_to_knowledge(self, question_id: str, kp_id: str, weight: float = 1.0):
        """将题目链接到知识点"""
        with self.driver.session() as session:
            cypher = """
            MATCH (q:Question {id: $question_id})
            MATCH (kp:KnowledgePoint {id: $kp_id})
            CREATE (q)-[:TESTS {weight: $weight}]->(kp)
            """
            session.run(cypher, {
                "question_id": question_id, 
                "kp_id": kp_id, 
                "weight": weight
            })
    
    # ===== 复杂查询 =====
    
    def find_questions_by_knowledge_point(self, kp_name: str) -> List[Dict[str, Any]]:
        """根据知识点查找题目"""
        with self.driver.session() as session:
            cypher = """
            MATCH (q:Question)-[r:TESTS]->(kp:KnowledgePoint)
            WHERE kp.name = $kp_name
            RETURN q, r.weight as weight
            ORDER BY r.weight DESC
            """
            result = session.run(cypher, {"kp_name": kp_name})
            return [{"question": dict(record["q"]), "weight": record["weight"]} 
                   for record in result]
    
    def find_knowledge_points_by_question(self, question_id: str) -> List[Dict[str, Any]]:
        """根据题目查找相关知识点"""
        with self.driver.session() as session:
            cypher = """
            MATCH (q:Question {id: $question_id})-[r:TESTS]->(kp:KnowledgePoint)
            RETURN kp, r.weight as weight
            ORDER BY r.weight DESC
            """
            result = session.run(cypher, {"question_id": question_id})
            return [{"knowledge_point": dict(record["kp"]), "weight": record["weight"]} 
                   for record in result]
    
    def get_knowledge_hierarchy(self) -> List[Dict[str, Any]]:
        """获取知识点层级结构"""
        with self.driver.session() as session:
            cypher = """
            MATCH (parent:KnowledgePoint)-[:HAS_SUB_POINT]->(child:KnowledgePoint)
            RETURN DISTINCT parent.name as parent_name, child.name as child_name,
                   parent.id as parent_id, child.id as child_id
            ORDER BY parent.name, child.name
            """
            result = session.run(cypher)
            return [dict(record) for record in result]
    
    def recommend_prerequisite_knowledge(self, kp_id: str) -> List[Dict[str, Any]]:
        """推荐前置知识点"""
        with self.driver.session() as session:
            cypher = """
            MATCH (target:KnowledgePoint {id: $kp_id})<-[:REQUIRES*1..3]-(prereq:KnowledgePoint)
            RETURN DISTINCT prereq, length(path) as distance
            ORDER BY distance
            """
            result = session.run(cypher, {"kp_id": kp_id})
            return [{"knowledge_point": dict(record["prereq"]), "distance": record["distance"]} 
                   for record in result]


# 全局数据库实例
neo4j_service = Neo4jService()
