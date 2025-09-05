#!/usr/bin/env python3
"""
加载示例数据脚本
导入示例题目和知识点关联数据
"""
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.database import neo4j_service
from backend.models.schema import Question
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_sample_questions():
    """加载示例题目数据"""
    logger.info("开始加载示例题目数据...")
    
    # 连接数据库
    if not neo4j_service.connect():
        logger.error("无法连接到Neo4j数据库")
        return False
    
    try:
        # 读取示例题目数据
        sample_file = "data/sample_questions/sample_questions.json"
        with open(sample_file, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        
        # 获取现有知识点映射
        knowledge_points = neo4j_service.search_knowledge_points("")
        kp_name_to_id = {kp['name']: kp['id'] for kp in knowledge_points}
        
        logger.info(f"找到 {len(knowledge_points)} 个知识点")
        logger.info(f"准备导入 {len(questions_data)} 道题目")
        
        imported_count = 0
        for q_data in questions_data:
            try:
                # 创建题目对象
                question = Question(
                    content=q_data['content'],
                    question_type=q_data['question_type'],
                    options=q_data.get('options', []),
                    answer=q_data['answer'],
                    analysis=q_data.get('analysis'),
                    source=q_data.get('source'),
                    difficulty=q_data.get('difficulty', 'medium')
                )
                
                # 创建题目
                question_id = neo4j_service.create_question(question)
                logger.info(f"创建题目: {question.content[:50]}... (ID: {question_id})")
                
                # 关联知识点
                knowledge_point_names = q_data.get('knowledge_points', [])
                for kp_name in knowledge_point_names:
                    if kp_name in kp_name_to_id:
                        kp_id = kp_name_to_id[kp_name]
                        neo4j_service.link_question_to_knowledge(question_id, kp_id, 1.0)
                        logger.info(f"  关联知识点: {kp_name}")
                    else:
                        logger.warning(f"  知识点不存在: {kp_name}")
                
                imported_count += 1
                
            except Exception as e:
                logger.error(f"导入题目失败: {e}")
                continue
        
        logger.info(f"成功导入 {imported_count} 道题目")
        return True
        
    except Exception as e:
        logger.error(f"加载示例数据失败: {e}")
        return False
    
    finally:
        neo4j_service.close()


def create_additional_knowledge_relations():
    """创建额外的知识点关系"""
    logger.info("创建知识点前置关系...")
    
    if not neo4j_service.connect():
        logger.error("无法连接到Neo4j数据库")
        return False
    
    try:
        # 获取知识点映射
        knowledge_points = neo4j_service.search_knowledge_points("")
        kp_name_to_id = {kp['name']: kp['id'] for kp in knowledge_points}
        
        # 定义前置关系
        prerequisite_relations = [
            ("现在进行时", "一般现在时"),  # 学现在进行时需要先掌握一般现在时
            ("现在完成时", "一般过去时"),  # 学现在完成时需要先掌握一般过去时
            ("被动语态", "一般现在时"),   # 学被动语态需要先掌握基本时态
            ("定语从句", "一般现在时"),   # 学定语从句需要先掌握基本语法
            ("宾语从句", "一般现在时"),   # 学宾语从句需要先掌握基本语法
        ]
        
        # 创建前置关系
        for target_kp, prerequisite_kp in prerequisite_relations:
            if target_kp in kp_name_to_id and prerequisite_kp in kp_name_to_id:
                target_id = kp_name_to_id[target_kp]
                prerequisite_id = kp_name_to_id[prerequisite_kp]
                
                # 创建REQUIRES关系
                with neo4j_service.driver.session() as session:
                    cypher = """
                    MATCH (target:KnowledgePoint {id: $target_id})
                    MATCH (prereq:KnowledgePoint {id: $prerequisite_id})
                    CREATE (target)-[:REQUIRES {strength: 0.8}]->(prereq)
                    """
                    session.run(cypher, {
                        "target_id": target_id,
                        "prerequisite_id": prerequisite_id
                    })
                
                logger.info(f"创建前置关系: {target_kp} -> {prerequisite_kp}")
        
        logger.info("知识点前置关系创建完成")
        return True
        
    except Exception as e:
        logger.error(f"创建知识点关系失败: {e}")
        return False
    
    finally:
        neo4j_service.close()


def verify_data():
    """验证导入的数据"""
    logger.info("验证导入的数据...")
    
    if not neo4j_service.connect():
        logger.error("无法连接到Neo4j数据库")
        return False
    
    try:
        with neo4j_service.driver.session() as session:
            # 统计知识点数量
            result = session.run("MATCH (kp:KnowledgePoint) RETURN count(kp) as count")
            kp_count = result.single()["count"]
            
            # 统计题目数量
            result = session.run("MATCH (q:Question) RETURN count(q) as count")
            q_count = result.single()["count"]
            
            # 统计标注关系数量
            result = session.run("MATCH (:Question)-[r:TESTS]->(:KnowledgePoint) RETURN count(r) as count")
            relation_count = result.single()["count"]
            
            # 统计层级关系数量
            result = session.run("MATCH (:KnowledgePoint)-[r:HAS_SUB_POINT]->(:KnowledgePoint) RETURN count(r) as count")
            hierarchy_count = result.single()["count"]
            
            # 统计前置关系数量
            result = session.run("MATCH (:KnowledgePoint)-[r:REQUIRES]->(:KnowledgePoint) RETURN count(r) as count")
            requires_count = result.single()["count"]
            
            logger.info(f"数据统计:")
            logger.info(f"  知识点数量: {kp_count}")
            logger.info(f"  题目数量: {q_count}")
            logger.info(f"  标注关系数量: {relation_count}")
            logger.info(f"  层级关系数量: {hierarchy_count}")
            logger.info(f"  前置关系数量: {requires_count}")
            
            # 查看一些示例查询
            logger.info("\n示例查询结果:")
            
            # 查找考查"一般现在时"的题目
            result = session.run("""
                MATCH (q:Question)-[r:TESTS]->(kp:KnowledgePoint {name: '一般现在时'})
                RETURN q.content as content, r.weight as weight
                LIMIT 3
            """)
            
            logger.info("考查'一般现在时'的题目:")
            for record in result:
                content = record["content"][:50] + "..." if len(record["content"]) > 50 else record["content"]
                logger.info(f"  - {content} (权重: {record['weight']})")
        
        logger.info("数据验证完成")
        return True
        
    except Exception as e:
        logger.error(f"数据验证失败: {e}")
        return False
    
    finally:
        neo4j_service.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="加载示例数据脚本")
    parser.add_argument("--verify-only", action="store_true", help="仅验证数据，不导入")
    
    args = parser.parse_args()
    
    if args.verify_only:
        verify_data()
    else:
        # 加载示例题目
        if load_sample_questions():
            logger.info("示例题目加载成功")
        else:
            logger.error("示例题目加载失败")
            sys.exit(1)
        
        # 创建知识点关系
        if create_additional_knowledge_relations():
            logger.info("知识点关系创建成功")
        else:
            logger.error("知识点关系创建失败")
        
        # 验证数据
        verify_data()
