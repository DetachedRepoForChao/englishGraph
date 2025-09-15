#!/usr/bin/env python3
"""
导出本地数据库的完整脚本
用于手动同步到云端数据库
"""
import os
import json
from backend.services.database import neo4j_service

def export_database():
    """导出本地数据库的完整数据"""
    
    # 连接数据库
    if not neo4j_service.connect():
        print("❌ 数据库连接失败")
        return
    
    print("✅ 数据库连接成功")
    
    export_data = {
        "knowledge_points": [],
        "relationships": [],
        "questions": [],
        "annotations": []
    }
    
    with neo4j_service.driver.session() as session:
        
        # 1. 导出所有知识点
        print("📊 导出知识点...")
        result = session.run("""
            MATCH (kp:KnowledgePoint)
            RETURN kp.id as id, kp.name as name, kp.description as description,
                   kp.difficulty as difficulty, kp.grade_levels as grade_levels,
                   kp.learning_objectives as learning_objectives,
                   kp.cefr_level as cefr_level, kp.keywords as keywords,
                   kp.source as source
            ORDER BY kp.name
        """)
        
        for record in result:
            kp_data = {
                "id": record["id"],
                "name": record["name"],
                "description": record["description"],
                "difficulty": record["difficulty"],
                "grade_levels": record["grade_levels"] or [],
                "learning_objectives": record["learning_objectives"] or [],
                "cefr_level": record["cefr_level"],
                "keywords": record["keywords"] or [],
                "source": record["source"]
            }
            export_data["knowledge_points"].append(kp_data)
        
        print(f"   📝 导出 {len(export_data['knowledge_points'])} 个知识点")
        
        # 2. 导出知识点层级关系
        print("🔗 导出层级关系...")
        result = session.run("""
            MATCH (parent:KnowledgePoint)-[:HAS_SUB_POINT]->(child:KnowledgePoint)
            RETURN parent.id as parent_id, parent.name as parent_name,
                   child.id as child_id, child.name as child_name
            ORDER BY parent.name, child.name
        """)
        
        for record in result:
            rel_data = {
                "parent_id": record["parent_id"],
                "parent_name": record["parent_name"],
                "child_id": record["child_id"],
                "child_name": record["child_name"],
                "relationship_type": "HAS_SUB_POINT"
            }
            export_data["relationships"].append(rel_data)
        
        print(f"   🔗 导出 {len(export_data['relationships'])} 个层级关系")
        
        # 3. 导出题目数据（前100个）
        print("❓ 导出题目数据...")
        result = session.run("""
            MATCH (q:Question)
            RETURN q.id as id, q.content as content, q.question_type as question_type,
                   q.difficulty as difficulty, q.answer as answer, q.options as options,
                   q.source as source, q.grade_level as grade_level
            ORDER BY q.id
            LIMIT 100
        """)
        
        for record in result:
            question_data = {
                "id": record["id"],
                "content": record["content"],
                "question_type": record["question_type"],
                "difficulty": record["difficulty"],
                "answer": record["answer"],
                "options": record["options"] or [],
                "source": record["source"],
                "grade_level": record["grade_level"]
            }
            export_data["questions"].append(question_data)
        
        print(f"   ❓ 导出 {len(export_data['questions'])} 个题目")
        
        # 4. 导出题目-知识点关联
        print("🏷️ 导出标注关系...")
        result = session.run("""
            MATCH (q:Question)-[:TESTS]->(kp:KnowledgePoint)
            RETURN q.id as question_id, kp.id as knowledge_point_id, kp.name as knowledge_point_name
            ORDER BY q.id
            LIMIT 200
        """)
        
        for record in result:
            annotation_data = {
                "question_id": record["question_id"],
                "knowledge_point_id": record["knowledge_point_id"],
                "knowledge_point_name": record["knowledge_point_name"],
                "relationship_type": "TESTS"
            }
            export_data["annotations"].append(annotation_data)
        
        print(f"   🏷️ 导出 {len(export_data['annotations'])} 个标注关系")
    
    # 保存到文件
    output_file = "database_export.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据导出完成！")
    print(f"📁 导出文件: {output_file}")
    print(f"📊 统计信息:")
    print(f"   - 知识点: {len(export_data['knowledge_points'])} 个")
    print(f"   - 层级关系: {len(export_data['relationships'])} 个")
    print(f"   - 题目: {len(export_data['questions'])} 个")
    print(f"   - 标注关系: {len(export_data['annotations'])} 个")
    
    # 生成同步脚本
    generate_sync_script(export_data)
    
    neo4j_service.close()

def generate_sync_script(export_data):
    """生成云端数据库同步脚本"""
    
    script_content = '''#!/usr/bin/env python3
"""
云端数据库同步脚本
自动生成，用于将本地数据同步到云端
"""
import os
from neo4j import GraphDatabase

def sync_to_cloud():
    """同步数据到云端数据库"""
    
    # 云端数据库连接信息（请根据实际情况修改）
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'knowledge123')
    
    print(f"🔗 连接云端数据库: {NEO4J_URI}")
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            
            print("🧹 清理现有数据...")
            # 可选：清理现有数据（谨慎使用）
            # session.run("MATCH (n) DETACH DELETE n")
            
            print("📝 同步知识点...")
'''
    
    # 添加知识点创建脚本
    script_content += f'''
            # 创建知识点
            knowledge_points = {json.dumps(export_data["knowledge_points"], ensure_ascii=False, indent=12)}
            
            for kp in knowledge_points:
                session.run("""
                    MERGE (kp:KnowledgePoint {{id: $id}})
                    SET kp.name = $name,
                        kp.description = $description,
                        kp.difficulty = $difficulty,
                        kp.grade_levels = $grade_levels,
                        kp.learning_objectives = $learning_objectives,
                        kp.cefr_level = $cefr_level,
                        kp.keywords = $keywords,
                        kp.source = $source
                """, kp)
            
            print(f"   ✅ 同步了 {{len(knowledge_points)}} 个知识点")
'''
    
    # 添加关系创建脚本
    script_content += f'''
            print("🔗 同步层级关系...")
            # 创建层级关系
            relationships = {json.dumps(export_data["relationships"], ensure_ascii=False, indent=12)}
            
            for rel in relationships:
                session.run("""
                    MATCH (parent:KnowledgePoint {{id: $parent_id}})
                    MATCH (child:KnowledgePoint {{id: $child_id}})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """, rel)
            
            print(f"   ✅ 同步了 {{len(relationships)}} 个层级关系")
'''
    
    script_content += '''
            print("✅ 数据同步完成！")
            
    except Exception as e:
        print(f"❌ 同步失败: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    sync_to_cloud()
'''
    
    # 保存同步脚本
    sync_script_file = "sync_to_cloud.py"
    with open(sync_script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"📜 生成同步脚本: {sync_script_file}")
    print(f"💡 使用方法:")
    print(f"   1. 设置云端数据库环境变量")
    print(f"   2. 运行: python3 {sync_script_file}")

if __name__ == "__main__":
    export_database()
