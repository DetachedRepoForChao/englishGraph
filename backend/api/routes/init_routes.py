"""
数据库初始化路由
"""
from fastapi import APIRouter, HTTPException
from backend.services.database import neo4j_service
from backend.models.schema import KnowledgePoint
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/init-database")
async def init_database():
    """初始化数据库"""
    try:
        # 连接数据库
        neo4j_service.connect()
        
        # 创建约束和索引
        neo4j_service.create_constraints()
        neo4j_service.create_indexes()
        
        # 添加基础知识点
        knowledge_points = [
            KnowledgePoint(
                name="一般现在时",
                description="表示经常性、习惯性的动作或状态",
                level="初中一年级",
                difficulty="easy",
                keywords=["always", "usually", "often", "sometimes", "never", "every day", "every week"]
            ),
            KnowledgePoint(
                name="现在进行时", 
                description="表示现在正在进行的动作",
                level="初中一年级",
                difficulty="easy",
                keywords=["now", "at the moment", "look!", "listen!", "am doing", "is doing", "are doing"]
            ),
            KnowledgePoint(
                name="现在完成时",
                description="表示过去发生的动作对现在造成的影响或结果", 
                level="初中二年级",
                difficulty="medium",
                keywords=["already", "yet", "just", "ever", "never", "since", "for", "have done", "has done"]
            ),
            KnowledgePoint(
                name="一般过去时",
                description="表示过去发生的动作或状态",
                level="初中一年级", 
                difficulty="easy",
                keywords=["yesterday", "last week", "ago", "was", "were", "did", "went", "played"]
            ),
            KnowledgePoint(
                name="被动语态",
                description="表示主语是动作的承受者",
                level="初中三年级",
                difficulty="hard", 
                keywords=["be动词", "过去分词", "by", "was done", "were done", "is made", "are made"]
            ),
            KnowledgePoint(
                name="定语从句",
                description="用来修饰名词或代词的从句",
                level="高中一年级",
                difficulty="hard",
                keywords=["which", "that", "who", "whom", "whose", "where", "when"]
            ),
            KnowledgePoint(
                name="宾语从句", 
                description="在句子中作宾语的从句",
                level="高中一年级",
                difficulty="hard",
                keywords=["that", "whether", "if", "what", "when", "where", "why", "how"]
            ),
            KnowledgePoint(
                name="比较级和最高级",
                description="形容词和副词的比较形式",
                level="初中二年级",
                difficulty="medium",
                keywords=["than", "more", "most", "less", "least", "-er", "-est", "better", "best"]
            ),
            KnowledgePoint(
                name="介词",
                description="表示名词、代词等与句中其他词的关系的词",
                level="初中一年级",
                difficulty="medium",
                keywords=["in", "on", "at", "by", "for", "with", "from", "to", "of", "about", "interested in"]
            )
        ]
        
        created_count = 0
        for kp in knowledge_points:
            try:
                neo4j_service.create_knowledge_point(kp)
                created_count += 1
            except Exception as e:
                logger.warning(f"创建知识点 {kp.name} 失败: {e}")
        
        neo4j_service.close()
        
        return {
            "success": True,
            "message": f"数据库初始化完成，创建了 {created_count} 个知识点",
            "created_knowledge_points": created_count
        }
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise HTTPException(status_code=500, detail=f"数据库初始化失败: {str(e)}")

@router.get("/health")
async def health_check():
    """健康检查"""
    try:
        neo4j_service.connect()
        neo4j_service.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@router.post("/load-opensource-data")
async def load_opensource_data():
    """加载开源英语教育数据"""
    try:
        from backend.services.open_source_data import open_source_integrator
        
        # 确保数据库连接
        if not neo4j_service.driver:
            if not neo4j_service.connect():
                raise HTTPException(status_code=500, detail="数据库连接失败")
        
        # 获取开源数据
        knowledge_points = open_source_integrator.get_all_knowledge_points()
        questions = open_source_integrator.get_all_questions()
        
        # 导入知识点
        imported_kp = 0
        with neo4j_service.driver.session() as session:
            for i, kp in enumerate(knowledge_points):
                kp_id = f"kp_opensource_{i+1:03d}"
                
                # 检查是否已存在
                existing = session.run("MATCH (kp:KnowledgePoint {name: $name}) RETURN kp", {"name": kp['name']})
                if existing.single() is None:
                    session.run("""
                        CREATE (kp:KnowledgePoint {
                            id: $id,
                            name: $name,
                            description: $description,
                            difficulty: $difficulty,
                            keywords: $keywords,
                            grade_levels: $grade_levels,
                            source: $source,
                            cefr_level: $cefr_level
                        })
                    """, {
                        "id": kp_id,
                        "name": kp['name'],
                        "description": kp['description'],
                        "difficulty": kp['difficulty'],
                        "keywords": kp['keywords'],
                        "grade_levels": kp['grade_levels'],
                        "source": kp.get('source', 'Open Source'),
                        "cefr_level": kp.get('cefr_level', 'A1')
                    })
                    imported_kp += 1
        
        # 导入题目
        imported_q = 0
        with neo4j_service.driver.session() as session:
            for i, q in enumerate(questions):
                q_id = f"q_opensource_{i+1:03d}"
                
                # 检查是否已存在
                existing = session.run("MATCH (q:Question {content: $content}) RETURN q", {"content": q['content']})
                if existing.single() is None:
                    session.run("""
                        CREATE (q:Question {
                            id: $id,
                            content: $content,
                            question_type: $question_type,
                            options: $options,
                            answer: $answer,
                            analysis: $analysis,
                            difficulty: $difficulty,
                            source: $source,
                            grade_level: $grade_level
                        })
                    """, {
                        "id": q_id,
                        "content": q['content'],
                        "question_type": q['question_type'],
                        "options": q['options'],
                        "answer": q['answer'],
                        "analysis": q.get('analysis', ''),
                        "difficulty": q['difficulty'],
                        "source": q.get('source', 'Open Source'),
                        "grade_level": q.get('grade_level', '未设置')
                    })
                    
                    # 创建关系
                    for kp_name in q.get("knowledge_points", []):
                        session.run("""
                            MATCH (q:Question {id: $q_id})
                            MATCH (kp:KnowledgePoint {name: $kp_name})
                            MERGE (q)-[:TESTS {weight: 0.8}]->(kp)
                        """, {"q_id": q_id, "kp_name": kp_name})
                    
                    imported_q += 1
        
        return {
            "status": "completed",
            "imported_knowledge_points": imported_kp,
            "imported_questions": imported_q,
            "total_knowledge_points": len(knowledge_points),
            "total_questions": len(questions),
            "message": f"成功导入 {imported_kp} 个知识点和 {imported_q} 道题目"
        }
        
    except Exception as e:
        logger.error(f"开源数据加载失败: {e}")
        raise HTTPException(status_code=500, detail=f"开源数据加载失败: {str(e)}")
