#!/usr/bin/env python3
"""
同步所有新增知识点到云端数据库
"""
from neo4j import GraphDatabase

# 使用正确的URI
URI = "neo4j+ssc://383b0a61.databases.neo4j.io"
AUTH = ("neo4j", "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI")

def sync_all_new_knowledge_points():
    """同步所有新增知识点"""
    
    print("🚀 同步所有新增知识点到云端...")
    
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            print("✅ 数据库连接成功")
            
            with driver.session() as session:
                
                # 所有新增知识点
                new_knowledge_points = [
                    {
                        "name": "There be句型", "id": "kp_there_be",
                        "description": "There be句型表示某处存在某物",
                        "difficulty": "easy",
                        "grade_levels": ["小学四年级", "小学五年级", "小学六年级"],
                        "learning_objectives": ["掌握There be句型的结构", "理解单复数一致性"],
                        "keywords": ["there is", "there are", "there was", "there were", "three apples"]
                    },
                    {
                        "name": "be动词", "id": "kp_be_verbs",
                        "description": "be动词的各种形式和用法",
                        "difficulty": "easy",
                        "grade_levels": ["小学二年级", "小学三年级", "小学四年级"],
                        "learning_objectives": ["掌握be动词的形式变化", "理解主谓一致"],
                        "keywords": ["is", "are", "was", "were", "am", "be"]
                    },
                    {
                        "name": "第三人称单数", "id": "kp_third_person",
                        "description": "第三人称单数动词变化规则",
                        "difficulty": "easy",
                        "grade_levels": ["小学三年级", "小学四年级", "小学五年级"],
                        "learning_objectives": ["掌握第三人称单数变化规则", "理解主谓一致"],
                        "keywords": ["he", "she", "it", "watches", "goes", "every evening"]
                    },
                    {
                        "name": "词汇", "id": "kp_vocabulary",
                        "description": "基础词汇和反义词",
                        "difficulty": "easy",
                        "grade_levels": ["小学一年级", "小学二年级", "小学三年级"],
                        "learning_objectives": ["掌握基础词汇", "理解反义词概念"],
                        "keywords": ["young", "old", "opposite", "反义词"]
                    },
                    {
                        "name": "数量表达", "id": "kp_quantity",
                        "description": "可数名词和不可数名词的数量表达",
                        "difficulty": "easy",
                        "grade_levels": ["小学四年级", "小学五年级", "小学六年级"],
                        "learning_objectives": ["掌握可数名词复数形式", "理解数量词的用法"],
                        "keywords": ["how many", "how much", "books", "there are five"]
                    }
                ]
                
                print("📝 创建新知识点...")
                for kp in new_knowledge_points:
                    session.run("""
                        MERGE (kp:KnowledgePoint {name: $name})
                        SET kp.id = $id,
                            kp.description = $description,
                            kp.difficulty = $difficulty,
                            kp.grade_levels = $grade_levels,
                            kp.learning_objectives = $learning_objectives,
                            kp.keywords = $keywords,
                            kp.source = 'system'
                    """, kp)
                    print(f"   ✅ {kp['name']}")
                
                # 建立层级关系
                print("🔗 建立层级关系...")
                relationships = [
                    ("句型结构", "There be句型"),
                    ("词类语法", "be动词"),
                    ("动词时态", "第三人称单数"),
                    ("主题词汇", "词汇"),
                    ("词类语法", "数量表达")
                ]
                
                for parent, child in relationships:
                    session.run("""
                        MATCH (parent:KnowledgePoint {name: $parent})
                        MATCH (child:KnowledgePoint {name: $child})
                        MERGE (parent)-[:HAS_SUB_POINT]->(child)
                    """, {"parent": parent, "child": child})
                    print(f"   🔗 {parent} → {child}")
                
                # 验证结果
                print("🔍 验证同步结果...")
                result = session.run("""
                    MATCH (kp:KnowledgePoint) 
                    WHERE kp.id IN ['kp_there_be', 'kp_be_verbs', 'kp_third_person', 'kp_vocabulary', 'kp_quantity']
                    RETURN kp.name as name, kp.id as id
                    ORDER BY kp.name
                """)
                
                print("   📊 新增知识点:")
                for record in result:
                    print(f"      ✅ {record['name']} (ID: {record['id']})")
                
        print("🎉 所有新知识点同步完成！")
        return True
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        return False

if __name__ == "__main__":
    sync_all_new_knowledge_points()
