#!/usr/bin/env python3
"""
直接初始化Neo4j AuraDB数据库
"""
import sys
import os
import uuid
import logging

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 云数据库配置
CLOUD_NEO4J_URI = "neo4j+s://383b0a61.databases.neo4j.io"
CLOUD_NEO4J_USERNAME = "neo4j"
CLOUD_NEO4J_PASSWORD = "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI"

class AuraDBInitializer:
    def __init__(self):
        self.driver = None
    
    def connect(self):
        """连接AuraDB"""
        try:
            logger.info("🔌 连接Neo4j AuraDB...")
            self.driver = GraphDatabase.driver(
                CLOUD_NEO4J_URI,
                auth=(CLOUD_NEO4J_USERNAME, CLOUD_NEO4J_PASSWORD)
            )
            
            # 测试连接
            with self.driver.session(database="neo4j") as session:
                result = session.run("RETURN 1 as test")
                result.single()
            
            logger.info("✅ AuraDB连接成功!")
            return True
            
        except Exception as e:
            logger.error(f"❌ AuraDB连接失败: {e}")
            return False
    
    def clear_database(self):
        """清空数据库"""
        try:
            logger.info("🗑️ 清空数据库...")
            with self.driver.session(database="neo4j") as session:
                session.run("MATCH (n) DETACH DELETE n")
            logger.info("✅ 数据库已清空")
            return True
        except Exception as e:
            logger.error(f"❌ 清空数据库失败: {e}")
            return False
    
    def create_constraints(self):
        """创建约束"""
        try:
            logger.info("🔧 创建约束...")
            with self.driver.session(database="neo4j") as session:
                constraints = [
                    "CREATE CONSTRAINT knowledge_point_id IF NOT EXISTS FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE",
                    "CREATE CONSTRAINT question_id IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE"
                ]
                
                for constraint in constraints:
                    try:
                        session.run(constraint)
                    except Exception as e:
                        logger.warning(f"约束创建警告: {e}")
            
            logger.info("✅ 约束创建完成")
            return True
        except Exception as e:
            logger.error(f"❌ 创建约束失败: {e}")
            return False
    
    def init_knowledge_points(self):
        """初始化知识点"""
        logger.info("📚 初始化知识点...")
        
        knowledge_points = [
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "一般现在时",
                "description": "表示经常性、习惯性的动作或状态",
                "level": "小学四年级",
                "difficulty": "easy",
                "keywords": ["always", "usually", "every day", "第三人称单数"]
            },
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "一般过去时",
                "description": "表示过去发生的动作或状态",
                "level": "小学五年级",
                "difficulty": "easy",
                "keywords": ["yesterday", "last week", "ago", "过去式"]
            },
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "现在进行时",
                "description": "表示现在正在进行的动作",
                "level": "小学六年级",
                "difficulty": "medium",
                "keywords": ["now", "at present", "be doing", "正在"]
            },
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "现在完成时",
                "description": "表示过去发生的动作对现在造成的影响",
                "level": "初中一年级",
                "difficulty": "medium",
                "keywords": ["have done", "already", "yet", "since"]
            },
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "被动语态",
                "description": "表示动作的承受者作为主语",
                "level": "初中二年级",
                "difficulty": "hard",
                "keywords": ["be done", "by", "被动", "过去分词"]
            },
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "定语从句",
                "description": "修饰名词或代词的从句",
                "level": "初中三年级",
                "difficulty": "hard",
                "keywords": ["who", "which", "that", "关系代词"]
            },
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "宾语从句",
                "description": "作宾语的从句",
                "level": "初中三年级",
                "difficulty": "hard",
                "keywords": ["that", "what", "if", "whether"]
            },
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "比较级和最高级",
                "description": "形容词和副词的比较形式",
                "level": "小学六年级",
                "difficulty": "medium",
                "keywords": ["than", "more", "most", "er", "est"]
            },
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "介词",
                "description": "表示名词、代词等与其他词的关系",
                "level": "小学三年级",
                "difficulty": "easy",
                "keywords": ["in", "on", "at", "for", "with"]
            },
            {
                "id": f"kp_{uuid.uuid4().hex[:6]}",
                "name": "动词时态",
                "description": "动词的时间和状态变化",
                "level": "小学四年级",
                "difficulty": "medium",
                "keywords": ["时态", "tense", "动词变化"]
            }
        ]
        
        try:
            with self.driver.session(database="neo4j") as session:
                for kp in knowledge_points:
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
                    logger.info(f"✅ 创建知识点: {kp['name']}")
            
            logger.info(f"📚 完成创建 {len(knowledge_points)} 个知识点")
            return knowledge_points
            
        except Exception as e:
            logger.error(f"❌ 创建知识点失败: {e}")
            return []
    
    def init_questions(self, knowledge_points):
        """初始化题目"""
        logger.info("📝 初始化题目...")
        
        questions = [
            {
                "id": f"q_{uuid.uuid4().hex[:6]}",
                "content": "She _____ to school every day.",
                "question_type": "选择题",
                "options": ["go", "goes", "going", "gone"],
                "answer": "B",
                "analysis": "主语是第三人称单数，动词用goes",
                "difficulty": "easy",
                "source": "教材示例",
                "kp_name": "一般现在时"
            },
            {
                "id": f"q_{uuid.uuid4().hex[:6]}",
                "content": "Yesterday I _____ to the park.",
                "question_type": "选择题",
                "options": ["go", "goes", "went", "going"],
                "answer": "C",
                "analysis": "yesterday表示过去时间，用过去式went",
                "difficulty": "easy",
                "source": "教材示例",
                "kp_name": "一般过去时"
            },
            {
                "id": f"q_{uuid.uuid4().hex[:6]}",
                "content": "Look! The children _____ in the playground.",
                "question_type": "选择题",
                "options": ["play", "plays", "are playing", "played"],
                "answer": "C",
                "analysis": "Look!表示正在发生，用现在进行时",
                "difficulty": "medium",
                "source": "教材示例",
                "kp_name": "现在进行时"
            },
            {
                "id": f"q_{uuid.uuid4().hex[:6]}",
                "content": "I _____ already _____ my homework.",
                "question_type": "选择题",
                "options": ["have, finished", "has, finished", "had, finished", "will, finish"],
                "answer": "A",
                "analysis": "already是现在完成时的标志词",
                "difficulty": "medium",
                "source": "教材示例",
                "kp_name": "现在完成时"
            },
            {
                "id": f"q_{uuid.uuid4().hex[:6]}",
                "content": "The letter _____ by Tom yesterday.",
                "question_type": "选择题",
                "options": ["wrote", "was written", "is written", "writes"],
                "answer": "B",
                "analysis": "by表示被动语态，yesterday表示过去时",
                "difficulty": "hard",
                "source": "教材示例",
                "kp_name": "被动语态"
            },
            {
                "id": f"q_{uuid.uuid4().hex[:6]}",
                "content": "This apple is _____ than that one.",
                "question_type": "选择题",
                "options": ["sweet", "sweeter", "sweetest", "more sweet"],
                "answer": "B",
                "analysis": "than表示比较，用比较级sweeter",
                "difficulty": "medium",
                "source": "教材示例",
                "kp_name": "比较级和最高级"
            }
        ]
        
        # 创建知识点名称到ID的映射
        kp_map = {kp["name"]: kp["id"] for kp in knowledge_points}
        
        try:
            with self.driver.session(database="neo4j") as session:
                for q in questions:
                    # 创建题目
                    kp_name = q.pop("kp_name")
                    session.run("""
                        CREATE (q:Question {
                            id: $id,
                            content: $content,
                            question_type: $question_type,
                            options: $options,
                            answer: $answer,
                            analysis: $analysis,
                            difficulty: $difficulty,
                            source: $source
                        })
                    """, q)
                    
                    # 创建关系
                    if kp_name in kp_map:
                        session.run("""
                            MATCH (q:Question {id: $question_id})
                            MATCH (kp:KnowledgePoint {id: $kp_id})
                            CREATE (q)-[:TESTS {weight: 0.8}]->(kp)
                        """, {
                            "question_id": q["id"],
                            "kp_id": kp_map[kp_name]
                        })
                    
                    logger.info(f"✅ 创建题目: {q['content'][:30]}...")
            
            logger.info(f"📝 完成创建 {len(questions)} 道题目")
            return True
            
        except Exception as e:
            logger.error(f"❌ 创建题目失败: {e}")
            return False
    
    def verify_data(self):
        """验证数据"""
        logger.info("🔍 验证数据...")
        
        try:
            with self.driver.session(database="neo4j") as session:
                # 统计数据
                kp_count = session.run("MATCH (kp:KnowledgePoint) RETURN count(kp) as count").single()["count"]
                q_count = session.run("MATCH (q:Question) RETURN count(q) as count").single()["count"]
                rel_count = session.run("MATCH ()-[r:TESTS]->() RETURN count(r) as count").single()["count"]
                
                logger.info("📊 数据统计:")
                logger.info(f"   知识点: {kp_count} 个")
                logger.info(f"   题目: {q_count} 道")
                logger.info(f"   关系: {rel_count} 个")
                
                return kp_count > 0 and q_count > 0
                
        except Exception as e:
            logger.error(f"❌ 验证失败: {e}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()
            logger.info("🔌 数据库连接已关闭")

def main():
    """主函数"""
    logger.info("🚀 开始初始化Neo4j AuraDB...")
    
    initializer = AuraDBInitializer()
    
    try:
        # 1. 连接数据库
        if not initializer.connect():
            return False
        
        # 2. 清空数据库
        if not initializer.clear_database():
            return False
        
        # 3. 创建约束
        if not initializer.create_constraints():
            return False
        
        # 4. 初始化知识点
        knowledge_points = initializer.init_knowledge_points()
        if not knowledge_points:
            return False
        
        # 5. 初始化题目
        if not initializer.init_questions(knowledge_points):
            return False
        
        # 6. 验证数据
        if not initializer.verify_data():
            return False
        
        logger.info("🎉 Neo4j AuraDB初始化完成！")
        logger.info("🌐 现在可以访问Vercel应用查看数据了")
        return True
        
    except Exception as e:
        logger.error(f"❌ 初始化过程出错: {e}")
        return False
    
    finally:
        initializer.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
