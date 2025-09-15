#!/usr/bin/env python3
"""
同步本地数据到Neo4j云端数据库
使用提供的云端数据库连接信息
"""
import json
from neo4j import GraphDatabase
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 云端数据库连接信息
NEO4J_URI = "neo4j+s://383b0a61.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI"

def connect_to_cloud():
    """连接到云端数据库"""
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        # 测试连接
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            test_value = result.single()["test"]
            if test_value == 1:
                logger.info("✅ 云端数据库连接成功")
                return driver
    except Exception as e:
        logger.error(f"❌ 云端数据库连接失败: {e}")
        return None

def sync_knowledge_points(driver):
    """同步关键知识点到云端"""
    
    # 从导出文件读取本地数据
    try:
        with open('database_export.json', 'r', encoding='utf-8') as f:
            export_data = json.load(f)
    except FileNotFoundError:
        logger.error("❌ 找不到 database_export.json 文件，请先运行 export_database.py")
        return False
    
    with driver.session() as session:
        
        logger.info("📝 同步知识点到云端...")
        
        # 同步所有知识点
        knowledge_points = export_data.get('knowledge_points', [])
        success_count = 0
        
        for kp in knowledge_points:
            try:
                session.run("""
                    MERGE (kp:KnowledgePoint {name: $name})
                    SET kp.id = $id,
                        kp.description = $description,
                        kp.difficulty = $difficulty,
                        kp.grade_levels = $grade_levels,
                        kp.learning_objectives = $learning_objectives,
                        kp.cefr_level = $cefr_level,
                        kp.keywords = $keywords,
                        kp.source = $source
                """, {
                    'name': kp['name'],
                    'id': kp['id'],
                    'description': kp['description'],
                    'difficulty': kp['difficulty'],
                    'grade_levels': kp['grade_levels'] or [],
                    'learning_objectives': kp['learning_objectives'] or [],
                    'cefr_level': kp['cefr_level'],
                    'keywords': kp['keywords'] or [],
                    'source': kp['source']
                })
                success_count += 1
                logger.info(f"   ✅ {kp['name']} (ID: {kp['id']})")
                
            except Exception as e:
                logger.error(f"   ❌ 同步 {kp['name']} 失败: {e}")
        
        logger.info(f"📊 知识点同步完成: {success_count}/{len(knowledge_points)}")
        
        # 同步层级关系
        logger.info("🔗 同步层级关系...")
        relationships = export_data.get('relationships', [])
        rel_success_count = 0
        
        for rel in relationships:
            try:
                session.run("""
                    MATCH (parent:KnowledgePoint {id: $parent_id})
                    MATCH (child:KnowledgePoint {id: $child_id})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """, {
                    'parent_id': rel['parent_id'],
                    'child_id': rel['child_id']
                })
                rel_success_count += 1
                logger.info(f"   🔗 {rel['parent_name']} → {rel['child_name']}")
                
            except Exception as e:
                logger.error(f"   ❌ 关系同步失败 {rel['parent_name']} → {rel['child_name']}: {e}")
        
        logger.info(f"🔗 关系同步完成: {rel_success_count}/{len(relationships)}")
        
        return True

def verify_sync(driver):
    """验证同步结果"""
    
    with driver.session() as session:
        
        logger.info("🔍 验证同步结果...")
        
        # 检查关键知识点
        key_knowledge_points = ['情态动词', '倒装句', '虚拟语气', '现在进行时', '现在完成时']
        
        for kp_name in key_knowledge_points:
            result = session.run("""
                MATCH (kp:KnowledgePoint {name: $name})
                RETURN kp.id as id, kp.name as name
            """, {'name': kp_name})
            
            record = result.single()
            if record:
                logger.info(f"   ✅ {record['name']} (ID: {record['id']})")
            else:
                logger.warning(f"   ⚠️ 未找到: {kp_name}")
        
        # 统计总数
        result = session.run("MATCH (kp:KnowledgePoint) RETURN count(kp) as count")
        total_kps = result.single()["count"]
        
        result = session.run("MATCH ()-[:HAS_SUB_POINT]->() RETURN count(*) as count")
        total_rels = result.single()["count"]
        
        logger.info(f"📊 云端数据库统计:")
        logger.info(f"   - 知识点总数: {total_kps}")
        logger.info(f"   - 层级关系总数: {total_rels}")
        
        return total_kps > 0

def test_nlp_recognition(driver):
    """测试NLP识别功能"""
    
    logger.info("🧪 测试NLP识别功能...")
    
    # 测试用例
    test_cases = [
        {
            "content": "You must finish your homework before going out.",
            "expected": "情态动词"
        },
        {
            "content": "Never have I seen such a beautiful sunset.",
            "expected": "倒装句"
        },
        {
            "content": "Look! The children are playing in the playground.",
            "expected": "现在进行时"
        }
    ]
    
    import requests
    import time
    
    # 等待部署完成
    api_url = "https://english-knowledge-graph-75dzfwqux-chao-wangs-projects-dfded257.vercel.app/api/annotation/suggest"
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(api_url, json={
                "question_content": test_case["content"],
                "question_type": "选择题"
            }, timeout=10)
            
            if response.status_code == 200:
                suggestions = response.json().get('suggestions', [])
                if suggestions:
                    top_suggestion = suggestions[0]
                    logger.info(f"   🧪 测试 {i}: {top_suggestion['knowledge_point_name']} (置信度: {top_suggestion['confidence']:.3f})")
                    
                    if top_suggestion['knowledge_point_name'] == test_case['expected']:
                        logger.info(f"      ✅ 识别正确")
                    else:
                        logger.warning(f"      ⚠️ 期望: {test_case['expected']}, 实际: {top_suggestion['knowledge_point_name']}")
                else:
                    logger.warning(f"   ⚠️ 测试 {i}: 无识别结果")
            else:
                logger.error(f"   ❌ 测试 {i}: API请求失败 ({response.status_code})")
                
        except Exception as e:
            logger.error(f"   ❌ 测试 {i}: {e}")
        
        # 避免请求过快
        time.sleep(1)

def main():
    """主函数"""
    
    logger.info("🚀 开始同步本地数据到Neo4j云端数据库")
    logger.info("=" * 60)
    logger.info(f"🔗 云端数据库: {NEO4J_URI}")
    logger.info(f"👤 用户名: {NEO4J_USERNAME}")
    logger.info("=" * 60)
    
    # 连接云端数据库
    driver = connect_to_cloud()
    if not driver:
        logger.error("❌ 无法连接云端数据库，退出")
        return
    
    try:
        # 同步数据
        if sync_knowledge_points(driver):
            logger.info("✅ 数据同步成功")
            
            # 验证同步结果
            if verify_sync(driver):
                logger.info("✅ 数据验证通过")
                
                # 测试NLP功能
                test_nlp_recognition(driver)
                
                logger.info("🎉 所有操作完成！")
            else:
                logger.error("❌ 数据验证失败")
        else:
            logger.error("❌ 数据同步失败")
            
    finally:
        driver.close()
        logger.info("🔒 数据库连接已关闭")

if __name__ == "__main__":
    main()
