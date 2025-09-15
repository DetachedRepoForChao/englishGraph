#!/usr/bin/env python3
"""
基于connectDB.py的简化同步脚本
直接使用您的数据库连接信息进行同步
"""
from neo4j import GraphDatabase

# 使用与connectDB.py相同的连接信息
URI = "neo4j+ssc://383b0a61.databases.neo4j.io"
AUTH = ("neo4j", "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI")

def sync_knowledge_points():
    """同步关键知识点"""
    
    print("🚀 开始同步知识点到云端数据库...")
    print(f"🔗 连接: {URI}")
    
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            # 验证连接
            driver.verify_connectivity()
            print("✅ 数据库连接成功")
            
            with driver.session() as session:
                
                # 1. 创建情态动词知识点
                print("📝 创建情态动词知识点...")
                session.run("""
                    MERGE (kp:KnowledgePoint {name: '情态动词'})
                    SET kp.id = 'kp_modal_verbs',
                        kp.description = '情态动词表示说话人的态度、推测、能力、必要性等',
                        kp.difficulty = 'medium',
                        kp.grade_levels = ['初中二年级', '初中三年级', '高中一年级'],
                        kp.learning_objectives = ['掌握情态动词的基本用法', '理解情态动词的推测用法'],
                        kp.keywords = ['can', 'could', 'may', 'might', 'must', 'should', 'would', 'will', 'shall'],
                        kp.source = 'enhanced'
                """)
                print("   ✅ 情态动词创建成功")
                
                # 2. 创建倒装句知识点
                print("📝 创建倒装句知识点...")
                session.run("""
                    MERGE (kp:KnowledgePoint {name: '倒装句'})
                    SET kp.id = 'kp_inversion',
                        kp.description = '倒装句是指将谓语动词或助动词提到主语之前的句子结构',
                        kp.difficulty = 'hard',
                        kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
                        kp.learning_objectives = ['掌握部分倒装的结构', '理解完全倒装的使用场景'],
                        kp.keywords = ['never', 'seldom', 'rarely', 'hardly', 'scarcely', 'barely', 'no sooner', 'not only'],
                        kp.source = 'enhanced'
                """)
                print("   ✅ 倒装句创建成功")
                
                # 3. 创建虚拟语气知识点
                print("📝 创建虚拟语气知识点...")
                session.run("""
                    MERGE (kp:KnowledgePoint {name: '虚拟语气'})
                    SET kp.id = 'kp_subjunctive',
                        kp.description = '虚拟语气表示假设、愿望、建议等非真实的情况',
                        kp.difficulty = 'hard',
                        kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
                        kp.learning_objectives = ['掌握虚拟语气的基本形式', '理解虚拟语气的使用场景'],
                        kp.keywords = ['if', 'wish', 'would', 'could', 'should', 'were', 'had'],
                        kp.source = 'enhanced'
                """)
                print("   ✅ 虚拟语气创建成功")
                
                # 4. 创建基础知识点
                print("📝 创建基础知识点...")
                basic_kps = [
                    {
                        "name": "英语语法", "id": "kp_115430",
                        "description": "英语语法知识点的根节点", "difficulty": "medium"
                    },
                    {
                        "name": "词类语法", "id": "kp_390008",
                        "description": "词类语法相关知识点", "difficulty": "medium"
                    },
                    {
                        "name": "句型结构", "id": "kp_222812",
                        "description": "句型结构相关知识点", "difficulty": "medium"
                    },
                    {
                        "name": "动词时态", "id": "kp_573225",
                        "description": "动词时态相关知识点", "difficulty": "medium"
                    }
                ]
                
                for kp in basic_kps:
                    session.run("""
                        MERGE (kp:KnowledgePoint {name: $name})
                        SET kp.id = $id,
                            kp.description = $description,
                            kp.difficulty = $difficulty,
                            kp.source = 'system'
                    """, kp)
                    print(f"   ✅ {kp['name']} 创建成功")
                
                # 5. 建立层级关系
                print("🔗 建立层级关系...")
                relationships = [
                    ("英语语法", "词类语法"),
                    ("英语语法", "句型结构"), 
                    ("英语语法", "动词时态"),
                    ("词类语法", "情态动词"),
                    ("句型结构", "倒装句"),
                    ("动词时态", "虚拟语气")
                ]
                
                for parent, child in relationships:
                    session.run("""
                        MATCH (parent:KnowledgePoint {name: $parent})
                        MATCH (child:KnowledgePoint {name: $child})
                        MERGE (parent)-[:HAS_SUB_POINT]->(child)
                    """, {"parent": parent, "child": child})
                    print(f"   🔗 {parent} → {child}")
                
                # 6. 验证结果
                print("🔍 验证同步结果...")
                result = session.run("""
                    MATCH (kp:KnowledgePoint) 
                    WHERE kp.name IN ['情态动词', '倒装句', '虚拟语气']
                    RETURN kp.name as name, kp.id as id
                    ORDER BY kp.name
                """)
                
                print("   📊 关键知识点:")
                for record in result:
                    print(f"      ✅ {record['name']} (ID: {record['id']})")
                
                # 统计总数
                total_result = session.run("MATCH (kp:KnowledgePoint) RETURN count(kp) as count")
                total_count = total_result.single()["count"]
                print(f"   📊 知识点总数: {total_count}")
                
                rel_result = session.run("MATCH ()-[:HAS_SUB_POINT]->() RETURN count(*) as count")
                rel_count = rel_result.single()["count"]
                print(f"   📊 关系总数: {rel_count}")
                
        print("🎉 数据库同步完成！")
        return True
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return False

def test_api():
    """测试API功能"""
    
    print("\n🧪 测试API功能...")
    
    import requests
    import time
    
    api_url = "https://english-knowledge-graph-75dzfwqux-chao-wangs-projects-dfded257.vercel.app/api/annotation/suggest"
    
    test_cases = [
        {
            "content": "You must finish your homework before going out.",
            "expected": "情态动词",
            "description": "情态动词识别"
        },
        {
            "content": "Never have I seen such a beautiful sunset.",
            "expected": "倒装句", 
            "description": "倒装句识别"
        },
        {
            "content": "Look! The children are playing in the playground.",
            "expected": "现在进行时",
            "description": "基础语法识别"
        }
    ]
    
    success_count = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 测试 {i}: {test['description']}")
        print(f"   📝 输入: {test['content'][:50]}...")
        
        try:
            response = requests.post(api_url, json={
                "question_content": test["content"],
                "question_type": "选择题"
            }, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                suggestions = data.get('suggestions', [])
                
                if suggestions:
                    top = suggestions[0]
                    name = top['knowledge_point_name']
                    confidence = top['confidence']
                    
                    print(f"   📊 结果: {name} (置信度: {confidence:.3f})")
                    
                    if name == test['expected']:
                        print(f"   ✅ 测试通过")
                        success_count += 1
                    else:
                        print(f"   ⚠️ 期望: {test['expected']}, 实际: {name}")
                else:
                    print(f"   ❌ 无识别结果")
            else:
                print(f"   ❌ API请求失败 (状态码: {response.status_code})")
                
        except Exception as e:
            print(f"   ❌ 测试异常: {e}")
        
        time.sleep(2)
    
    print(f"\n📊 API测试结果: {success_count}/{len(test_cases)} 通过")
    
    if success_count == len(test_cases):
        print("🎉 所有测试通过！系统工作完美")
    elif success_count >= len(test_cases) * 0.8:
        print("✅ 大部分测试通过，系统基本正常")
    else:
        print("⚠️ 测试通过率较低，可能需要等待缓存刷新")
    
    return success_count >= len(test_cases) * 0.8

def main():
    """主函数"""
    
    print("🚀 基于connectDB.py的数据库同步工具")
    print("=" * 60)
    
    # 同步数据
    if sync_knowledge_points():
        print("✅ 数据同步成功")
        
        # 测试API
        if test_api():
            print("\n🎊 完成！所有功能正常工作")
        else:
            print("\n⚠️ API测试未完全通过，请等待5-10分钟后重试")
    else:
        print("❌ 数据同步失败")

if __name__ == "__main__":
    main()
