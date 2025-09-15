#!/usr/bin/env python3
"""
在Vercel云端数据库中添加缺失的知识点
"""
import os
import sys
from neo4j import GraphDatabase

def add_missing_knowledge_points():
    """添加缺失的知识点到云端数据库"""
    
    # 从环境变量获取数据库连接信息
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_username = os.getenv('NEO4J_USERNAME', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'knowledge123')
    
    print(f"连接到数据库: {neo4j_uri}")
    
    try:
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
        
        with driver.session() as session:
            # 检查是否已存在这些知识点
            result = session.run("""
                MATCH (kp:KnowledgePoint) 
                WHERE kp.name IN ['情态动词', '倒装句', '虚拟语气']
                RETURN kp.name as name, kp.id as id
            """)
            existing = list(result)
            print(f"已存在的知识点: {existing}")
            
            # 添加情态动词
            session.run("""
                MERGE (kp:KnowledgePoint {name: '情态动词'})
                SET kp.id = 'kp_modal_verbs',
                    kp.description = '情态动词表示说话人的态度、推测、能力、必要性等',
                    kp.difficulty = 'medium',
                    kp.grade_levels = ['初中二年级', '初中三年级', '高中一年级'],
                    kp.learning_objectives = ['掌握情态动词的基本用法', '理解情态动词的推测用法']
            """)
            print("✓ 添加情态动词知识点")
            
            # 添加倒装句
            session.run("""
                MERGE (kp:KnowledgePoint {name: '倒装句'})
                SET kp.id = 'kp_inversion',
                    kp.description = '倒装句是指将谓语动词或助动词提到主语之前的句子结构',
                    kp.difficulty = 'hard',
                    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
                    kp.learning_objectives = ['掌握部分倒装的结构', '理解完全倒装的使用场景']
            """)
            print("✓ 添加倒装句知识点")
            
            # 添加虚拟语气
            session.run("""
                MERGE (kp:KnowledgePoint {name: '虚拟语气'})
                SET kp.id = 'kp_subjunctive',
                    kp.description = '虚拟语气表示假设、愿望、建议等非真实的情况',
                    kp.difficulty = 'hard',
                    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
                    kp.learning_objectives = ['掌握虚拟语气的基本形式', '理解虚拟语气的使用场景']
            """)
            print("✓ 添加虚拟语气知识点")
            
            # 建立层级关系
            session.run("""
                MATCH (parent:KnowledgePoint {name: '英语语法'})
                MATCH (child:KnowledgePoint {name: '情态动词'})
                MERGE (parent)-[:HAS_SUB_POINT]->(child)
            """)
            print("✓ 建立情态动词层级关系")
            
            session.run("""
                MATCH (parent:KnowledgePoint {name: '英语语法'})
                MATCH (child:KnowledgePoint {name: '倒装句'})
                MERGE (parent)-[:HAS_SUB_POINT]->(child)
            """)
            print("✓ 建立倒装句层级关系")
            
            session.run("""
                MATCH (parent:KnowledgePoint {name: '英语语法'})
                MATCH (child:KnowledgePoint {name: '虚拟语气'})
                MERGE (parent)-[:HAS_SUB_POINT]->(child)
            """)
            print("✓ 建立虚拟语气层级关系")
            
            # 验证添加结果
            result = session.run("""
                MATCH (kp:KnowledgePoint) 
                WHERE kp.name IN ['情态动词', '倒装句', '虚拟语气']
                RETURN kp.name as name, kp.id as id
                ORDER BY kp.name
            """)
            added = list(result)
            print(f"\n成功添加的知识点: {added}")
            
        driver.close()
        print("\n✅ 所有知识点添加完成！")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_missing_knowledge_points()
