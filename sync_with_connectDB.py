#!/usr/bin/env python3
"""
基于connectDB.py的云端数据库同步脚本
使用您提供的数据库连接信息同步本地数据到云端
"""
import json
import logging
from neo4j import GraphDatabase

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 使用与connectDB.py相同的连接信息
URI = "neo4j+s://383b0a61.databases.neo4j.io"
AUTH = ("neo4j", "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI")

def test_connection():
    """测试数据库连接"""
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            logger.info("✅ 数据库连接测试成功")
            return True
    except Exception as e:
        logger.error(f"❌ 数据库连接失败: {e}")
        return False

def sync_key_knowledge_points():
    """同步关键知识点"""
    
    # 关键知识点数据
    key_knowledge_points = [
        {
            "name": "英语语法",
            "id": "kp_115430",
            "description": "英语语法知识点的根节点",
            "difficulty": "medium",
            "grade_levels": ["小学", "初中", "高中"],
            "learning_objectives": ["掌握英语语法基础", "理解语法规则"],
            "keywords": [],
            "source": "system"
        },
        {
            "name": "情态动词",
            "id": "kp_modal_verbs",
            "description": "情态动词表示说话人的态度、推测、能力、必要性等",
            "difficulty": "medium",
            "grade_levels": ["初中二年级", "初中三年级", "高中一年级"],
            "learning_objectives": ["掌握情态动词的基本用法", "理解情态动词的推测用法"],
            "keywords": ["can", "could", "may", "might", "must", "should", "would", "will", "shall"],
            "source": "enhanced"
        },
        {
            "name": "倒装句",
            "id": "kp_inversion",
            "description": "倒装句是指将谓语动词或助动词提到主语之前的句子结构",
            "difficulty": "hard",
            "grade_levels": ["高中一年级", "高中二年级", "高中三年级"],
            "learning_objectives": ["掌握部分倒装的结构", "理解完全倒装的使用场景"],
            "keywords": ["never", "seldom", "rarely", "hardly", "scarcely", "barely", "no sooner", "not only"],
            "source": "enhanced"
        },
        {
            "name": "虚拟语气",
            "id": "kp_subjunctive",
            "description": "虚拟语气表示假设、愿望、建议等非真实的情况",
            "difficulty": "hard",
            "grade_levels": ["高中一年级", "高中二年级", "高中三年级"],
            "learning_objectives": ["掌握虚拟语气的基本形式", "理解虚拟语气的使用场景"],
            "keywords": ["if", "wish", "would", "could", "should", "were", "had"],
            "source": "enhanced"
        },
        {
            "name": "现在进行时",
            "id": "kp_605632",
            "description": "表示现在正在进行的动作",
            "difficulty": "medium",
            "grade_levels": ["小学四年级", "小学五年级", "小学六年级"],
            "learning_objectives": ["掌握现在进行时的构成", "理解现在进行时的使用场景"],
            "keywords": ["look", "listen", "now", "right now", "at the moment"],
            "source": "system"
        },
        {
            "name": "现在完成时",
            "id": "kp_441152",
            "description": "表示过去发生的动作对现在造成的影响",
            "difficulty": "medium",
            "grade_levels": ["初中一年级", "初中二年级", "初中三年级"],
            "learning_objectives": ["理解现在完成时的含义", "掌握过去分词的变化规则"],
            "keywords": ["already", "yet", "just", "ever", "never", "since", "for"],
            "source": "system"
        },
        {
            "name": "一般现在时",
            "id": "kp_588066",
            "description": "表示经常性、习惯性的动作或状态",
            "difficulty": "easy",
            "grade_levels": ["小学三年级", "小学四年级", "小学五年级"],
            "learning_objectives": ["掌握一般现在时的基本用法", "理解第三人称单数变化规则"],
            "keywords": ["always", "usually", "often", "sometimes", "never", "every day"],
            "source": "system"
        },
        {
            "name": "词类语法",
            "id": "kp_390008",
            "description": "词类语法相关知识点",
            "difficulty": "medium",
            "grade_levels": ["小学", "初中", "高中"],
            "learning_objectives": ["掌握各种词类的用法", "理解词法规则"],
            "keywords": [],
            "source": "system"
        },
        {
            "name": "句型结构",
            "id": "kp_222812",
            "description": "句型结构相关知识点",
            "difficulty": "medium",
            "grade_levels": ["初中", "高中"],
            "learning_objectives": ["掌握各种句型结构", "理解句法规则"],
            "keywords": [],
            "source": "system"
        },
        {
            "name": "动词时态",
            "id": "kp_573225",
            "description": "动词时态相关知识点",
            "difficulty": "medium",
            "grade_levels": ["小学四年级", "小学五年级", "小学六年级", "初中"],
            "learning_objectives": ["掌握各种时态的用法", "理解时态的语法规则"],
            "keywords": [],
            "source": "system"
        },
        {
            "name": "非谓语动词",
            "id": "kp_302914",
            "description": "非谓语动词包括不定式、动名词和分词",
            "difficulty": "hard",
            "grade_levels": ["高中一年级", "高中二年级", "高中三年级"],
            "learning_objectives": ["掌握非谓语动词的形式", "理解非谓语动词的用法"],
            "keywords": ["concerning", "concerned about", "being concerned", "to concern"],
            "source": "enhanced"
        }
    ]
    
    # 层级关系
    relationships = [
        {"parent_name": "英语语法", "child_name": "词类语法"},
        {"parent_name": "英语语法", "child_name": "句型结构"},
        {"parent_name": "英语语法", "child_name": "动词时态"},
        {"parent_name": "词类语法", "child_name": "情态动词"},
        {"parent_name": "句型结构", "child_name": "倒装句"},
        {"parent_name": "动词时态", "child_name": "虚拟语气"},
        {"parent_name": "动词时态", "child_name": "现在进行时"},
        {"parent_name": "动词时态", "child_name": "现在完成时"},
        {"parent_name": "动词时态", "child_name": "一般现在时"},
        {"parent_name": "动词时态", "child_name": "非谓语动词"}
    ]
    
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                
                logger.info("📝 开始同步知识点...")
                success_count = 0
                
                # 同步知识点
                for kp in key_knowledge_points:
                    try:
                        session.run("""
                            MERGE (kp:KnowledgePoint {name: $name})
                            SET kp.id = $id,
                                kp.description = $description,
                                kp.difficulty = $difficulty,
                                kp.grade_levels = $grade_levels,
                                kp.learning_objectives = $learning_objectives,
                                kp.keywords = $keywords,
                                kp.source = $source
                        """, kp)
                        success_count += 1
                        logger.info(f"   ✅ {kp['name']} (ID: {kp['id']})")
                    except Exception as e:
                        logger.error(f"   ❌ {kp['name']} 同步失败: {e}")
                
                logger.info(f"📊 知识点同步完成: {success_count}/{len(key_knowledge_points)}")
                
                # 同步层级关系
                logger.info("🔗 开始同步层级关系...")
                rel_success_count = 0
                
                for rel in relationships:
                    try:
                        session.run("""
                            MATCH (parent:KnowledgePoint {name: $parent_name})
                            MATCH (child:KnowledgePoint {name: $child_name})
                            MERGE (parent)-[:HAS_SUB_POINT]->(child)
                        """, rel)
                        rel_success_count += 1
                        logger.info(f"   🔗 {rel['parent_name']} → {rel['child_name']}")
                    except Exception as e:
                        logger.error(f"   ❌ 关系同步失败 {rel['parent_name']} → {rel['child_name']}: {e}")
                
                logger.info(f"🔗 关系同步完成: {rel_success_count}/{len(relationships)}")
                
                return success_count == len(key_knowledge_points) and rel_success_count == len(relationships)
                
    except Exception as e:
        logger.error(f"❌ 同步过程失败: {e}")
        return False

def verify_sync():
    """验证同步结果"""
    
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                
                logger.info("🔍 验证同步结果...")
                
                # 检查关键知识点
                key_points = ['情态动词', '倒装句', '虚拟语气', '现在进行时', '现在完成时', '非谓语动词']
                found_points = []
                
                for kp_name in key_points:
                    result = session.run("""
                        MATCH (kp:KnowledgePoint {name: $name})
                        RETURN kp.id as id, kp.name as name
                    """, {"name": kp_name})
                    
                    record = result.single()
                    if record:
                        found_points.append(record['name'])
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
                logger.info(f"   - 关键知识点: {len(found_points)}/{len(key_points)}")
                
                return len(found_points) >= len(key_points) * 0.8  # 至少80%的关键知识点存在
                
    except Exception as e:
        logger.error(f"❌ 验证失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    
    logger.info("🧪 测试API功能...")
    
    import requests
    import time
    
    api_url = "https://english-knowledge-graph-75dzfwqux-chao-wangs-projects-dfded257.vercel.app/api/annotation/suggest"
    
    test_cases = [
        {"content": "You must finish your homework before going out.", "expected": "情态动词"},
        {"content": "Never have I seen such a beautiful sunset.", "expected": "倒装句"},
        {"content": "Look! The children are playing in the playground.", "expected": "现在进行时"}
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(api_url, json={
                "question_content": test_case["content"],
                "question_type": "选择题"
            }, timeout=15)
            
            if response.status_code == 200:
                suggestions = response.json().get('suggestions', [])
                if suggestions:
                    top_suggestion = suggestions[0]
                    logger.info(f"   🧪 测试{i}: {top_suggestion['knowledge_point_name']} (置信度: {top_suggestion['confidence']:.3f})")
                    if top_suggestion['knowledge_point_name'] == test_case['expected']:
                        success_count += 1
                        logger.info(f"      ✅ 识别正确")
                    else:
                        logger.warning(f"      ⚠️ 期望: {test_case['expected']}, 实际: {top_suggestion['knowledge_point_name']}")
                else:
                    logger.warning(f"   ⚠️ 测试{i}: 无识别结果")
            else:
                logger.error(f"   ❌ 测试{i}: API请求失败 ({response.status_code})")
                
        except Exception as e:
            logger.error(f"   ❌ 测试{i}: {e}")
        
        time.sleep(2)
    
    logger.info(f"🧪 API测试完成: {success_count}/{len(test_cases)} 通过")
    return success_count >= len(test_cases) * 0.8

def main():
    """主函数"""
    
    logger.info("🚀 基于connectDB.py的云端数据库同步")
    logger.info("=" * 60)
    logger.info(f"🔗 数据库URI: {URI}")
    logger.info(f"👤 用户名: {AUTH[0]}")
    logger.info("=" * 60)
    
    # 测试连接
    if not test_connection():
        logger.error("❌ 数据库连接失败，退出")
        return False
    
    # 同步数据
    logger.info("\n🔄 开始同步数据...")
    if not sync_key_knowledge_points():
        logger.error("❌ 数据同步失败")
        return False
    
    logger.info("✅ 数据同步成功")
    
    # 验证同步结果
    logger.info("\n🔍 验证同步结果...")
    if not verify_sync():
        logger.warning("⚠️ 数据验证未完全通过")
        return False
    
    logger.info("✅ 数据验证通过")
    
    # 测试API功能
    logger.info("\n🧪 测试API功能...")
    if test_api_endpoints():
        logger.info("✅ API测试通过")
        logger.info("\n🎉 所有操作完成！系统工作正常")
        return True
    else:
        logger.warning("⚠️ API测试未完全通过，请等待5-10分钟后重试")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎊 同步完成！您可以运行以下命令进行进一步测试:")
        print("   python3 test_api_after_sync.py")
    else:
        print("\n⚠️ 同步过程中遇到问题，请检查日志信息")
