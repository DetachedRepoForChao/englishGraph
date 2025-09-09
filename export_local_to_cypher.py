#!/usr/bin/env python3
"""
导出本地Neo4j数据到Cypher脚本
用于同步到云数据库
"""
import sys
import os
import json
import logging
from neo4j import GraphDatabase

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 本地数据库配置
LOCAL_NEO4J_URI = "bolt://localhost:7687"
LOCAL_NEO4J_USERNAME = "neo4j"
LOCAL_NEO4J_PASSWORD = "knowledge123"

class LocalDataExporter:
    def __init__(self):
        self.driver = None
    
    def connect(self):
        """连接本地数据库"""
        try:
            logger.info("🔌 连接本地Neo4j数据库...")
            self.driver = GraphDatabase.driver(
                LOCAL_NEO4J_URI, 
                auth=(LOCAL_NEO4J_USERNAME, LOCAL_NEO4J_PASSWORD)
            )
            
            # 测试连接
            with self.driver.session() as session:
                session.run("RETURN 1")
            
            logger.info("✅ 本地数据库连接成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ 本地数据库连接失败: {e}")
            return False
    
    def export_knowledge_points(self):
        """导出知识点数据"""
        logger.info("📚 导出知识点数据...")
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (kp:KnowledgePoint)
                    RETURN kp.id as id, kp.name as name, kp.description as description,
                           kp.level as level, kp.difficulty as difficulty, kp.keywords as keywords
                    ORDER BY kp.name
                """)
                
                knowledge_points = []
                for record in result:
                    kp_data = {
                        "id": record["id"],
                        "name": record["name"],
                        "description": record["description"] or "",
                        "level": record["level"] or "未设置",
                        "difficulty": record["difficulty"] or "medium",
                        "keywords": record["keywords"] or []
                    }
                    knowledge_points.append(kp_data)
                
                logger.info(f"✅ 导出了 {len(knowledge_points)} 个知识点")
                return knowledge_points
                
        except Exception as e:
            logger.error(f"❌ 导出知识点失败: {e}")
            return []
    
    def export_questions(self):
        """导出题目数据"""
        logger.info("📝 导出题目数据...")
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (q:Question)
                    RETURN q.id as id, q.content as content, q.question_type as question_type,
                           q.options as options, q.answer as answer, q.analysis as analysis,
                           q.source as source, q.difficulty as difficulty
                    ORDER BY q.id
                """)
                
                questions = []
                for record in result:
                    q_data = {
                        "id": record["id"],
                        "content": record["content"],
                        "question_type": record["question_type"] or "选择题",
                        "options": record["options"] or [],
                        "answer": record["answer"] or "",
                        "analysis": record["analysis"] or "",
                        "source": record["source"] or "本地导入",
                        "difficulty": record["difficulty"] or "medium"
                    }
                    questions.append(q_data)
                
                logger.info(f"✅ 导出了 {len(questions)} 道题目")
                return questions
                
        except Exception as e:
            logger.error(f"❌ 导出题目失败: {e}")
            return []
    
    def export_relationships(self):
        """导出关系数据"""
        logger.info("🔗 导出关系数据...")
        
        try:
            with self.driver.session() as session:
                # 导出TESTS关系
                tests_result = session.run("""
                    MATCH (q:Question)-[r:TESTS]->(kp:KnowledgePoint)
                    RETURN q.id as question_id, kp.id as kp_id, r.weight as weight
                """)
                
                tests_relationships = []
                for record in tests_result:
                    rel_data = {
                        "question_id": record["question_id"],
                        "kp_id": record["kp_id"],
                        "weight": record["weight"] or 0.8
                    }
                    tests_relationships.append(rel_data)
                
                # 导出层级关系
                hierarchy_result = session.run("""
                    MATCH (parent:KnowledgePoint)-[r:HAS_SUB_POINT]->(child:KnowledgePoint)
                    RETURN parent.id as parent_id, child.id as child_id
                """)
                
                hierarchy_relationships = []
                for record in hierarchy_result:
                    hier_data = {
                        "parent_id": record["parent_id"],
                        "child_id": record["child_id"]
                    }
                    hierarchy_relationships.append(hier_data)
                
                logger.info(f"✅ 导出了 {len(tests_relationships)} 个TESTS关系")
                logger.info(f"✅ 导出了 {len(hierarchy_relationships)} 个层级关系")
                
                return {
                    "tests": tests_relationships,
                    "hierarchy": hierarchy_relationships
                }
                
        except Exception as e:
            logger.error(f"❌ 导出关系失败: {e}")
            return {"tests": [], "hierarchy": []}
    
    def generate_cypher_script(self, knowledge_points, questions, relationships):
        """生成Cypher初始化脚本"""
        logger.info("📝 生成Cypher脚本...")
        
        cypher_lines = []
        
        # 添加头部注释
        cypher_lines.extend([
            "// K12英语知识图谱系统 - 完整数据同步脚本",
            "// 从本地数据库导出，用于同步到Neo4j AuraDB",
            f"// 导出时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"// 数据统计: {len(knowledge_points)}个知识点, {len(questions)}道题目, {len(relationships['tests'])}个关系",
            "",
            "// ===== 第1步: 清空数据库 =====",
            "MATCH (n) DETACH DELETE n;",
            "",
            "// ===== 第2步: 创建约束 =====",
            "CREATE CONSTRAINT knowledge_point_id IF NOT EXISTS FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE;",
            "CREATE CONSTRAINT question_id IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE;",
            "",
            "// ===== 第3步: 创建知识点 ====="
        ])
        
        # 生成知识点创建语句
        for kp in knowledge_points:
            # 转义字符串中的引号
            name = kp['name'].replace("'", "\\'")
            description = kp['description'].replace("'", "\\'")
            level = kp['level'].replace("'", "\\'")
            
            # 处理关键词数组
            keywords_str = json.dumps(kp['keywords'], ensure_ascii=False)
            
            cypher_lines.append(f"""
CREATE (kp_{kp['id'].replace('-', '_')}:KnowledgePoint {{
    id: '{kp['id']}',
    name: '{name}',
    description: '{description}',
    level: '{level}',
    difficulty: '{kp['difficulty']}',
    keywords: {keywords_str}
}});""")
        
        cypher_lines.append("\n// ===== 第4步: 创建题目 =====")
        
        # 生成题目创建语句
        for q in questions:
            # 转义字符串
            content = q['content'].replace("'", "\\'")
            analysis = q['analysis'].replace("'", "\\'") if q['analysis'] else ""
            source = q['source'].replace("'", "\\'") if q['source'] else ""
            
            # 处理选项数组
            options_str = json.dumps(q['options'], ensure_ascii=False)
            
            cypher_lines.append(f"""
CREATE (q_{q['id'].replace('-', '_')}:Question {{
    id: '{q['id']}',
    content: '{content}',
    question_type: '{q['question_type']}',
    options: {options_str},
    answer: '{q['answer']}',
    analysis: '{analysis}',
    source: '{source}',
    difficulty: '{q['difficulty']}'
}});""")
        
        cypher_lines.append("\n// ===== 第5步: 创建题目-知识点关系 =====")
        
        # 生成TESTS关系
        for rel in relationships['tests']:
            cypher_lines.append(f"""
MATCH (q:Question {{id: '{rel['question_id']}'}})
MATCH (kp:KnowledgePoint {{id: '{rel['kp_id']}'}})
CREATE (q)-[:TESTS {{weight: {rel['weight']}}}]->(kp);""")
        
        # 生成层级关系（如果有）
        if relationships['hierarchy']:
            cypher_lines.append("\n// ===== 第6步: 创建知识点层级关系 =====")
            for hier in relationships['hierarchy']:
                cypher_lines.append(f"""
MATCH (parent:KnowledgePoint {{id: '{hier['parent_id']}'}})
MATCH (child:KnowledgePoint {{id: '{hier['child_id']}'}})
CREATE (parent)-[:HAS_SUB_POINT]->(child);""")
        
        cypher_lines.extend([
            "",
            "// ===== 第7步: 验证数据 =====",
            "MATCH (kp:KnowledgePoint) RETURN count(kp) as knowledge_points_count;",
            "MATCH (q:Question) RETURN count(q) as questions_count;",
            "MATCH ()-[r:TESTS]->() RETURN count(r) as tests_relationships_count;",
            "MATCH ()-[r:HAS_SUB_POINT]->() RETURN count(r) as hierarchy_relationships_count;",
            "",
            "// ===== 第8步: 查看数据样本 =====",
            "MATCH (n) RETURN n LIMIT 10;"
        ])
        
        return "\n".join(cypher_lines)
    
    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()
            logger.info("🔌 数据库连接已关闭")

def main():
    """主函数"""
    logger.info("🚀 开始导出本地数据...")
    
    exporter = LocalDataExporter()
    
    try:
        # 1. 连接数据库
        if not exporter.connect():
            return False
        
        # 2. 导出知识点
        knowledge_points = exporter.export_knowledge_points()
        if not knowledge_points:
            logger.warning("⚠️ 没有找到知识点数据")
        
        # 3. 导出题目
        questions = exporter.export_questions()
        if not questions:
            logger.warning("⚠️ 没有找到题目数据")
        
        # 4. 导出关系
        relationships = exporter.export_relationships()
        
        # 5. 生成Cypher脚本
        cypher_script = exporter.generate_cypher_script(knowledge_points, questions, relationships)
        
        # 6. 保存到文件
        output_file = "local_data_sync.cypher"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cypher_script)
        
        logger.info(f"📄 Cypher脚本已保存到: {output_file}")
        logger.info("📊 数据统计:")
        logger.info(f"   知识点: {len(knowledge_points)} 个")
        logger.info(f"   题目: {len(questions)} 道")
        logger.info(f"   TESTS关系: {len(relationships['tests'])} 个")
        logger.info(f"   层级关系: {len(relationships['hierarchy'])} 个")
        logger.info("")
        logger.info("🎯 下一步:")
        logger.info("1. 打开 Neo4j AuraDB Browser")
        logger.info("2. 复制并执行生成的Cypher脚本")
        logger.info("3. 验证数据同步成功")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 导出过程出错: {e}")
        return False
    
    finally:
        exporter.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
