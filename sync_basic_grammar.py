#!/usr/bin/env python3
"""
同步基础语法知识点到云端数据库
"""
from neo4j import GraphDatabase

# 使用正确的URI
URI = "neo4j+ssc://383b0a61.databases.neo4j.io"
AUTH = ("neo4j", "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI")

def sync_basic_grammar():
    """同步基础语法知识点"""
    
    print("🚀 同步基础语法知识点到云端...")
    
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            print("✅ 数据库连接成功")
            
            with driver.session() as session:
                
                # 添加冠词知识点
                print("📝 添加冠词知识点...")
                session.run("""
                    MERGE (kp:KnowledgePoint {name: '冠词'})
                    SET kp.id = 'kp_articles',
                        kp.description = '冠词包括定冠词the和不定冠词a/an',
                        kp.difficulty = 'easy',
                        kp.grade_levels = ['小学三年级', '小学四年级', '小学五年级'],
                        kp.learning_objectives = ['掌握a/an的使用规则', '理解the的用法'],
                        kp.keywords = ['a', 'an', 'the', 'elephant', 'apple', 'orange'],
                        kp.source = 'system'
                """)
                print("   ✅ 冠词创建成功")
                
                # 添加代词知识点
                print("📝 添加代词知识点...")
                session.run("""
                    MERGE (kp:KnowledgePoint {name: '代词'})
                    SET kp.id = 'kp_pronouns',
                        kp.description = '代词用来代替名词，避免重复',
                        kp.difficulty = 'easy',
                        kp.grade_levels = ['小学二年级', '小学三年级', '小学四年级'],
                        kp.learning_objectives = ['掌握人称代词的用法', '理解主格和宾格的区别'],
                        kp.keywords = ['he', 'she', 'it', 'they', 'we', 'you', 'i'],
                        kp.source = 'system'
                """)
                print("   ✅ 代词创建成功")
                
                # 添加连词知识点
                print("📝 添加连词知识点...")
                session.run("""
                    MERGE (kp:KnowledgePoint {name: '连词'})
                    SET kp.id = 'kp_conjunctions',
                        kp.description = '连词用来连接词语、短语或句子',
                        kp.difficulty = 'easy',
                        kp.grade_levels = ['小学三年级', '小学四年级', '小学五年级'],
                        kp.learning_objectives = ['掌握并列连词的用法', '理解连词的作用'],
                        kp.keywords = ['and', 'but', 'or', 'because', 'so'],
                        kp.source = 'system'
                """)
                print("   ✅ 连词创建成功")
                
                # 建立层级关系
                print("🔗 建立层级关系...")
                session.run("""
                    MATCH (parent:KnowledgePoint {name: '词类语法'})
                    MATCH (child:KnowledgePoint {name: '冠词'})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """)
                print("   🔗 词类语法 → 冠词")
                
                session.run("""
                    MATCH (parent:KnowledgePoint {name: '词类语法'})
                    MATCH (child:KnowledgePoint {name: '代词'})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """)
                print("   🔗 词类语法 → 代词")
                
                session.run("""
                    MATCH (parent:KnowledgePoint {name: '词类语法'})
                    MATCH (child:KnowledgePoint {name: '连词'})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """)
                print("   🔗 词类语法 → 连词")
                
                # 验证结果
                print("🔍 验证同步结果...")
                result = session.run("""
                    MATCH (kp:KnowledgePoint) 
                    WHERE kp.name IN ['冠词', '代词', '连词', '介词']
                    RETURN kp.name as name, kp.id as id
                    ORDER BY kp.name
                """)
                
                print("   📊 基础语法知识点:")
                for record in result:
                    print(f"      ✅ {record['name']} (ID: {record['id']})")
                
        print("🎉 基础语法知识点同步完成！")
        return True
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return False

if __name__ == "__main__":
    sync_basic_grammar()
