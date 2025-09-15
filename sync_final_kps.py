#!/usr/bin/env python3
"""
同步最终的知识点到云端数据库
"""
from neo4j import GraphDatabase

# 使用正确的URI
URI = "neo4j+ssc://383b0a61.databases.neo4j.io"
AUTH = ("neo4j", "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI")

def sync_final_knowledge_points():
    """同步最终知识点"""
    
    print("🚀 同步最终知识点到云端...")
    
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            print("✅ 数据库连接成功")
            
            with driver.session() as session:
                
                # 添加疑问句知识点
                print("📝 添加疑问句知识点...")
                session.run("""
                    MERGE (kp:KnowledgePoint {name: '疑问句'})
                    SET kp.id = 'kp_questions',
                        kp.description = '疑问句的构成和语法规则',
                        kp.difficulty = 'medium',
                        kp.grade_levels = ['小学四年级', '小学五年级', '小学六年级', '初中一年级'],
                        kp.learning_objectives = ['掌握疑问句的构成', '理解助动词在疑问句中的作用'],
                        kp.keywords = ['question', 'do you', 'did you', 'have you', 'are you', 'choose the correct'],
                        kp.source = 'system'
                """)
                print("   ✅ 疑问句创建成功")
                
                # 添加条件句知识点
                print("📝 添加条件句知识点...")
                session.run("""
                    MERGE (kp:KnowledgePoint {name: '条件句'})
                    SET kp.id = 'kp_conditionals',
                        kp.description = '条件句表示假设和条件关系',
                        kp.difficulty = 'medium',
                        kp.grade_levels = ['初中二年级', '初中三年级', '高中一年级'],
                        kp.learning_objectives = ['掌握条件句的结构', '理解if从句的时态规则'],
                        kp.keywords = ['if', 'unless', 'when', 'tomorrow', 'will stay', 'if it rains'],
                        kp.source = 'system'
                """)
                print("   ✅ 条件句创建成功")
                
                # 建立层级关系
                print("🔗 建立层级关系...")
                session.run("""
                    MATCH (parent:KnowledgePoint {name: '句型结构'})
                    MATCH (child:KnowledgePoint {name: '疑问句'})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """)
                print("   🔗 句型结构 → 疑问句")
                
                session.run("""
                    MATCH (parent:KnowledgePoint {name: '句型结构'})
                    MATCH (child:KnowledgePoint {name: '条件句'})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """)
                print("   🔗 句型结构 → 条件句")
                
                # 验证所有关键知识点
                print("🔍 验证所有关键知识点...")
                result = session.run("""
                    MATCH (kp:KnowledgePoint) 
                    WHERE kp.name IN ['情态动词', '倒装句', '介词', '冠词', '代词', '连词', 
                                     'There be句型', 'be动词', '第三人称单数', '词汇', 
                                     '数量表达', '疑问句', '条件句']
                    RETURN kp.name as name, kp.id as id
                    ORDER BY kp.name
                """)
                
                print("   📊 所有关键知识点:")
                count = 0
                for record in result:
                    count += 1
                    print(f"      ✅ {record['name']} (ID: {record['id']})")
                
                print(f"   📊 总计: {count} 个关键知识点")
                
        print("🎉 最终知识点同步完成！")
        return True
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return False

if __name__ == "__main__":
    sync_final_knowledge_points()
