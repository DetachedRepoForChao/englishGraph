#!/usr/bin/env python3
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

            # 创建知识点
            knowledge_points = [
            {
                        "id": "kp_588066",
                        "name": "一般现在时",
                        "description": "表示经常性、习惯性的动作或状态",
                        "difficulty": "easy",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "一般现在时",
                                    "present simple"
                        ],
                        "source": null
            },
            {
                        "id": "kp_2925",
                        "name": "一般过去时",
                        "description": "表示过去发生的动作或状态",
                        "difficulty": "easy",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "一般过去时",
                                    "past simple"
                        ],
                        "source": null
            },
            {
                        "id": "kp_472230",
                        "name": "介词",
                        "description": "表示名词、代词等与句中其他词的关系的词",
                        "difficulty": "medium",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "in",
                                    "on",
                                    "at",
                                    "by",
                                    "for",
                                    "with",
                                    "from",
                                    "to",
                                    "of",
                                    "about",
                                    "under",
                                    "over",
                                    "above",
                                    "below",
                                    "between",
                                    "among",
                                    "through",
                                    "interested in",
                                    "good at",
                                    "afraid of",
                                    "proud of",
                                    "famous for",
                                    "介词",
                                    "前置词",
                                    "preposition",
                                    "介词短语",
                                    "固定搭配",
                                    "_____ in",
                                    "_____ on",
                                    "_____ at",
                                    "_____ by",
                                    "_____ for",
                                    "A) in B) on C) at D) by",
                                    "介词选择",
                                    "介词填空"
                        ],
                        "source": null
            },
            {
                        "id": "kp_inversion",
                        "name": "倒装句",
                        "description": "倒装句是指将谓语动词或助动词提到主语之前的句子结构",
                        "difficulty": "hard",
                        "grade_levels": [
                                    "高中一年级",
                                    "高中二年级",
                                    "高中三年级"
                        ],
                        "learning_objectives": [
                                    "掌握部分倒装的结构",
                                    "理解完全倒装的使用场景"
                        ],
                        "cefr_level": null,
                        "keywords": [],
                        "source": null
            },
            {
                        "id": "kp_573225",
                        "name": "动词时态",
                        "description": "动词的各种时态形式",
                        "difficulty": "medium",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "动词",
                                    "时态",
                                    "tense"
                        ],
                        "source": null
            },
            {
                        "id": "kp_969701",
                        "name": "定语从句",
                        "description": "用来修饰名词或代词的从句",
                        "difficulty": "hard",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "who",
                                    "which",
                                    "that",
                                    "whom",
                                    "whose",
                                    "where",
                                    "when",
                                    "关系代词",
                                    "先行词"
                        ],
                        "source": null
            },
            {
                        "id": "kp_980608",
                        "name": "宾语从句",
                        "description": "在句子中作宾语的从句",
                        "difficulty": "hard",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "that",
                                    "whether",
                                    "if",
                                    "what",
                                    "when",
                                    "where",
                                    "why",
                                    "how",
                                    "宾语从句",
                                    "引导词"
                        ],
                        "source": null
            },
            {
                        "id": "kp_modal_verbs",
                        "name": "情态动词",
                        "description": "情态动词表示说话人的态度、推测、能力、必要性等",
                        "difficulty": "medium",
                        "grade_levels": [
                                    "初中二年级",
                                    "初中三年级",
                                    "高中一年级"
                        ],
                        "learning_objectives": [
                                    "掌握情态动词的基本用法",
                                    "理解情态动词的推测用法"
                        ],
                        "cefr_level": null,
                        "keywords": [],
                        "source": null
            },
            {
                        "id": "kp_793115",
                        "name": "比较级和最高级",
                        "description": "形容词和副词的比较形式",
                        "difficulty": "medium",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "than",
                                    "more",
                                    "most",
                                    "-er",
                                    "-est",
                                    "better",
                                    "best",
                                    "比较级",
                                    "最高级"
                        ],
                        "source": null
            },
            {
                        "id": "kp_441152",
                        "name": "现在完成时",
                        "description": "表示过去发生的动作对现在造成的影响或结果",
                        "difficulty": "medium",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "have",
                                    "has",
                                    "already",
                                    "yet",
                                    "just",
                                    "ever",
                                    "never",
                                    "since",
                                    "for"
                        ],
                        "source": null
            },
            {
                        "id": "kp_605632",
                        "name": "现在进行时",
                        "description": "表示现在正在进行的动作",
                        "difficulty": "medium",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "现在进行时",
                                    "present continuous"
                        ],
                        "source": null
            },
            {
                        "id": "kp_115430",
                        "name": "英语语法",
                        "description": "英语语法基础知识",
                        "difficulty": "medium",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "语法",
                                    "grammar"
                        ],
                        "source": null
            },
            {
                        "id": "kp_subjunctive",
                        "name": "虚拟语气",
                        "description": "虚拟语气表示假设、愿望、建议等非真实的情况",
                        "difficulty": "hard",
                        "grade_levels": [
                                    "高中一年级",
                                    "高中二年级",
                                    "高中三年级"
                        ],
                        "learning_objectives": [
                                    "掌握虚拟语气的基本形式",
                                    "理解虚拟语气的使用场景"
                        ],
                        "cefr_level": null,
                        "keywords": [],
                        "source": null
            },
            {
                        "id": "kp_199751",
                        "name": "被动语态",
                        "description": "表示主语是动作的承受者",
                        "difficulty": "hard",
                        "grade_levels": [],
                        "learning_objectives": [],
                        "cefr_level": null,
                        "keywords": [
                                    "be动词",
                                    "过去分词",
                                    "by",
                                    "was",
                                    "were",
                                    "is",
                                    "are",
                                    "被动",
                                    "passive"
                        ],
                        "source": null
            }
]
            
            for kp in knowledge_points:
                session.run("""
                    MERGE (kp:KnowledgePoint {id: $id})
                    SET kp.name = $name,
                        kp.description = $description,
                        kp.difficulty = $difficulty,
                        kp.grade_levels = $grade_levels,
                        kp.learning_objectives = $learning_objectives,
                        kp.cefr_level = $cefr_level,
                        kp.keywords = $keywords,
                        kp.source = $source
                """, kp)
            
            print(f"   ✅ 同步了 {len(knowledge_points)} 个知识点")

            print("🔗 同步层级关系...")
            # 创建层级关系
            relationships = [
            {
                        "parent_id": "kp_573225",
                        "parent_name": "动词时态",
                        "child_id": "kp_588066",
                        "child_name": "一般现在时",
                        "relationship_type": "HAS_SUB_POINT"
            },
            {
                        "parent_id": "kp_573225",
                        "parent_name": "动词时态",
                        "child_id": "kp_2925",
                        "child_name": "一般过去时",
                        "relationship_type": "HAS_SUB_POINT"
            },
            {
                        "parent_id": "kp_573225",
                        "parent_name": "动词时态",
                        "child_id": "kp_605632",
                        "child_name": "现在进行时",
                        "relationship_type": "HAS_SUB_POINT"
            },
            {
                        "parent_id": "kp_115430",
                        "parent_name": "英语语法",
                        "child_id": "kp_inversion",
                        "child_name": "倒装句",
                        "relationship_type": "HAS_SUB_POINT"
            },
            {
                        "parent_id": "kp_115430",
                        "parent_name": "英语语法",
                        "child_id": "kp_573225",
                        "child_name": "动词时态",
                        "relationship_type": "HAS_SUB_POINT"
            },
            {
                        "parent_id": "kp_115430",
                        "parent_name": "英语语法",
                        "child_id": "kp_modal_verbs",
                        "child_name": "情态动词",
                        "relationship_type": "HAS_SUB_POINT"
            },
            {
                        "parent_id": "kp_115430",
                        "parent_name": "英语语法",
                        "child_id": "kp_subjunctive",
                        "child_name": "虚拟语气",
                        "relationship_type": "HAS_SUB_POINT"
            }
]
            
            for rel in relationships:
                session.run("""
                    MATCH (parent:KnowledgePoint {id: $parent_id})
                    MATCH (child:KnowledgePoint {id: $child_id})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """, rel)
            
            print(f"   ✅ 同步了 {len(relationships)} 个层级关系")

            print("✅ 数据同步完成！")
            
    except Exception as e:
        print(f"❌ 同步失败: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    sync_to_cloud()
