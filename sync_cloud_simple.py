#!/usr/bin/env python3
"""
简化的云端数据库同步脚本
手动同步关键知识点到云端
"""
import requests
import json

# 云端API地址
API_BASE = "https://english-knowledge-graph-75dzfwqux-chao-wangs-projects-dfded257.vercel.app"

def sync_via_api():
    """通过API同步关键知识点"""
    
    print("🔗 通过API同步云端数据库...")
    
    # 关键知识点数据
    key_knowledge_points = [
        {
            "id": "kp_modal_verbs",
            "name": "情态动词",
            "description": "情态动词表示说话人的态度、推测、能力、必要性等",
            "difficulty": "medium",
            "grade_levels": ["初中二年级", "初中三年级", "高中一年级"],
            "learning_objectives": ["掌握情态动词的基本用法", "理解情态动词的推测用法"],
            "keywords": ["can", "could", "may", "might", "must", "should", "would", "will", "shall"]
        },
        {
            "id": "kp_inversion",
            "name": "倒装句",
            "description": "倒装句是指将谓语动词或助动词提到主语之前的句子结构",
            "difficulty": "hard",
            "grade_levels": ["高中一年级", "高中二年级", "高中三年级"],
            "learning_objectives": ["掌握部分倒装的结构", "理解完全倒装的使用场景"],
            "keywords": ["never", "seldom", "rarely", "hardly", "scarcely", "barely", "no sooner", "not only"]
        },
        {
            "id": "kp_subjunctive",
            "name": "虚拟语气",
            "description": "虚拟语气表示假设、愿望、建议等非真实的情况",
            "difficulty": "hard",
            "grade_levels": ["高中一年级", "高中二年级", "高中三年级"],
            "learning_objectives": ["掌握虚拟语气的基本形式", "理解虚拟语气的使用场景"],
            "keywords": ["if", "wish", "would", "could", "should", "were", "had"]
        }
    ]
    
    # 层级关系
    relationships = [
        {"parent_name": "词类语法", "child_name": "情态动词"},
        {"parent_name": "句型结构", "child_name": "倒装句"},
        {"parent_name": "动词时态", "child_name": "虚拟语气"}
    ]
    
    print("📝 创建知识点...")
    for kp in key_knowledge_points:
        try:
            # 这里您需要手动在云端数据库中执行以下Cypher查询
            cypher_query = f"""
MERGE (kp:KnowledgePoint {{name: '{kp['name']}'}})
SET kp.id = '{kp['id']}',
    kp.description = '{kp['description']}',
    kp.difficulty = '{kp['difficulty']}',
    kp.grade_levels = {json.dumps(kp['grade_levels'])},
    kp.learning_objectives = {json.dumps(kp['learning_objectives'])},
    kp.keywords = {json.dumps(kp['keywords'])}
"""
            print(f"   📄 {kp['name']}: {cypher_query}")
            
        except Exception as e:
            print(f"   ❌ 创建 {kp['name']} 失败: {e}")
    
    print("\n🔗 建立层级关系...")
    for rel in relationships:
        cypher_query = f"""
MATCH (parent:KnowledgePoint {{name: '{rel['parent_name']}'}})
MATCH (child:KnowledgePoint {{name: '{rel['child_name']}'}})
MERGE (parent)-[:HAS_SUB_POINT]->(child)
"""
        print(f"   🔗 {rel['parent_name']} -> {rel['child_name']}: {cypher_query}")

def generate_manual_script():
    """生成手动执行的Cypher脚本"""
    
    script_content = """
// 手动同步脚本 - 在Neo4j Browser中执行

// 1. 创建情态动词知识点
MERGE (kp:KnowledgePoint {name: '情态动词'})
SET kp.id = 'kp_modal_verbs',
    kp.description = '情态动词表示说话人的态度、推测、能力、必要性等',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中二年级', '初中三年级', '高中一年级'],
    kp.learning_objectives = ['掌握情态动词的基本用法', '理解情态动词的推测用法'],
    kp.keywords = ['can', 'could', 'may', 'might', 'must', 'should', 'would', 'will', 'shall'];

// 2. 创建倒装句知识点
MERGE (kp:KnowledgePoint {name: '倒装句'})
SET kp.id = 'kp_inversion',
    kp.description = '倒装句是指将谓语动词或助动词提到主语之前的句子结构',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握部分倒装的结构', '理解完全倒装的使用场景'],
    kp.keywords = ['never', 'seldom', 'rarely', 'hardly', 'scarcely', 'barely', 'no sooner', 'not only'];

// 3. 创建虚拟语气知识点
MERGE (kp:KnowledgePoint {name: '虚拟语气'})
SET kp.id = 'kp_subjunctive',
    kp.description = '虚拟语气表示假设、愿望、建议等非真实的情况',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握虚拟语气的基本形式', '理解虚拟语气的使用场景'],
    kp.keywords = ['if', 'wish', 'would', 'could', 'should', 'were', 'had'];

// 4. 建立层级关系 - 情态动词
MATCH (parent:KnowledgePoint {name: '词类语法'})
MATCH (child:KnowledgePoint {name: '情态动词'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

// 5. 建立层级关系 - 倒装句
MATCH (parent:KnowledgePoint {name: '句型结构'})
MATCH (child:KnowledgePoint {name: '倒装句'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

// 6. 建立层级关系 - 虚拟语气
MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '虚拟语气'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

// 7. 验证创建结果
MATCH (kp:KnowledgePoint) 
WHERE kp.name IN ['情态动词', '倒装句', '虚拟语气']
RETURN kp.name as name, kp.id as id
ORDER BY kp.name;
"""
    
    with open("manual_sync.cypher", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("📜 生成手动同步脚本: manual_sync.cypher")
    print("💡 使用方法:")
    print("   1. 登录到您的Neo4j AuraDB控制台")
    print("   2. 打开Neo4j Browser")
    print("   3. 复制并执行 manual_sync.cypher 中的Cypher语句")

if __name__ == "__main__":
    print("🚀 云端数据库同步工具")
    print("=" * 50)
    
    sync_via_api()
    print("\n" + "=" * 50)
    generate_manual_script()
    
    print(f"\n✅ 同步脚本已生成！")
    print(f"📁 文件清单:")
    print(f"   - database_export.json (完整数据导出)")
    print(f"   - sync_to_cloud.py (自动同步脚本)")
    print(f"   - manual_sync.cypher (手动同步脚本)")
    print(f"   - sync_cloud_simple.py (当前脚本)")
