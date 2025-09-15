"""
知识点相关API路由
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from backend.services.database import neo4j_service
from backend.models.schema import KnowledgePoint

router = APIRouter()


@router.post("/", response_model=Dict[str, str])
async def create_knowledge_point(kp: KnowledgePoint):
    """创建知识点"""
    try:
        kp_id = neo4j_service.create_knowledge_point(kp)
        return {"id": kp_id, "message": "知识点创建成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")


@router.get("/search")
async def search_knowledge_points(keyword: str):
    """搜索知识点"""
    try:
        results = neo4j_service.search_knowledge_points(keyword)
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")


@router.get("/{kp_id}")
async def get_knowledge_point(kp_id: str):
    """获取单个知识点"""
    try:
        kp = neo4j_service.get_knowledge_point(kp_id)
        if not kp:
            raise HTTPException(status_code=404, detail="知识点不存在")
        return kp
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.post("/{parent_id}/children/{child_id}")
async def create_knowledge_hierarchy(parent_id: str, child_id: str):
    """创建知识点层级关系"""
    try:
        neo4j_service.create_knowledge_hierarchy(parent_id, child_id)
        return {"message": "层级关系创建成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")


@router.get("/hierarchy/tree")
async def get_knowledge_hierarchy():
    """获取知识点层级树"""
    try:
        hierarchy = neo4j_service.get_knowledge_hierarchy()
        return {"hierarchy": hierarchy}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/{kp_id}/prerequisites")
async def get_prerequisite_knowledge(kp_id: str):
    """获取前置知识点推荐"""
    try:
        prerequisites = neo4j_service.recommend_prerequisite_knowledge(kp_id)
        return {"prerequisites": prerequisites}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.post("/add-missing-kps")
async def add_missing_knowledge_points():
    """添加缺失的知识点到数据库"""
    try:
        # 确保数据库连接
        if not neo4j_service.driver:
            neo4j_service.connect()
        
        with neo4j_service.driver.session() as session:
            # 添加情态动词
            session.run("""
                MERGE (kp:KnowledgePoint {name: '情态动词'})
                SET kp.id = 'kp_modal_verbs',
                    kp.description = '情态动词表示说话人的态度、推测、能力、必要性等',
                    kp.difficulty = 'medium',
                    kp.grade_levels = ['初中二年级', '初中三年级', '高中一年级'],
                    kp.learning_objectives = ['掌握情态动词的基本用法', '理解情态动词的推测用法']
            """)
            
            # 添加倒装句
            session.run("""
                MERGE (kp:KnowledgePoint {name: '倒装句'})
                SET kp.id = 'kp_inversion',
                    kp.description = '倒装句是指将谓语动词或助动词提到主语之前的句子结构',
                    kp.difficulty = 'hard',
                    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
                    kp.learning_objectives = ['掌握部分倒装的结构', '理解完全倒装的使用场景']
            """)
            
            # 添加虚拟语气
            session.run("""
                MERGE (kp:KnowledgePoint {name: '虚拟语气'})
                SET kp.id = 'kp_subjunctive',
                    kp.description = '虚拟语气表示假设、愿望、建议等非真实的情况',
                    kp.difficulty = 'hard',
                    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
                    kp.learning_objectives = ['掌握虚拟语气的基本形式', '理解虚拟语气的使用场景']
            """)
            
            # 建立层级关系
            session.run("""
                MATCH (parent:KnowledgePoint {name: '英语语法'})
                MATCH (child:KnowledgePoint {name: '情态动词'})
                MERGE (parent)-[:HAS_SUB_POINT]->(child)
            """)
            
            session.run("""
                MATCH (parent:KnowledgePoint {name: '英语语法'})
                MATCH (child:KnowledgePoint {name: '倒装句'})
                MERGE (parent)-[:HAS_SUB_POINT]->(child)
            """)
            
            session.run("""
                MATCH (parent:KnowledgePoint {name: '英语语法'})
                MATCH (child:KnowledgePoint {name: '虚拟语气'})
                MERGE (parent)-[:HAS_SUB_POINT]->(child)
            """)
            
            # 验证添加结果
            result = session.run("""
                MATCH (kp:KnowledgePoint) 
                WHERE kp.name IN ['情态动词', '倒装句', '虚拟语气']
                RETURN kp.name as name, kp.id as id
                ORDER BY kp.name
            """)
            added = list(result)
            
        return {
            "message": "成功添加缺失的知识点",
            "added_knowledge_points": [dict(record) for record in added]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加知识点失败: {str(e)}")


@router.get("/debug-nlp")
async def debug_nlp_service():
    """调试NLP服务状态"""
    try:
        from backend.services.nlp_service_light import nlp_service
        
        # 检查数据库连接
        db_connected = neo4j_service.driver is not None
        if not db_connected:
            db_connected = neo4j_service.connect()
        
        # 获取知识点ID映射
        kp_id_map = {}
        if db_connected and neo4j_service.driver:
            with neo4j_service.driver.session() as session:
                result = session.run("MATCH (kp:KnowledgePoint) RETURN kp.id as id, kp.name as name LIMIT 10")
                kp_id_map = {record["name"]: record["id"] for record in result}
        
        # 测试NLP服务
        test_question = "You must finish your homework before going out."
        suggestions = nlp_service.suggest_knowledge_points(test_question, "选择题")
        
        return {
            "database_connected": db_connected,
            "knowledge_point_mapping": kp_id_map,
            "test_question": test_question,
            "suggestions_count": len(suggestions),
            "suggestions": suggestions[:3] if suggestions else []
        }
        
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@router.post("/sync-database")
async def sync_database():
    """同步数据库，确保云端有所有必要的知识点"""
    try:
        # 确保数据库连接
        if not neo4j_service.driver:
            neo4j_service.connect()
        
        sync_results = []
        
        with neo4j_service.driver.session() as session:
            # 检查并添加情态动词
            result = session.run("MATCH (kp:KnowledgePoint {name: '情态动词'}) RETURN kp.id as id")
            existing = result.single()
            if not existing:
                # 添加情态动词知识点
                session.run("""
                    CREATE (kp:KnowledgePoint {
                        id: 'kp_modal_verbs_sync',
                        name: '情态动词',
                        description: '情态动词表示说话人的态度、推测、能力、必要性等',
                        difficulty: 'medium',
                        grade_levels: ['初中二年级', '初中三年级', '高中一年级'],
                        learning_objectives: ['掌握情态动词的基本用法', '理解情态动词的推测用法']
                    })
                """)
                # 建立层级关系
                session.run("""
                    MATCH (parent:KnowledgePoint {name: '词类语法'})
                    MATCH (child:KnowledgePoint {name: '情态动词'})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """)
                sync_results.append({"action": "created", "knowledge_point": "情态动词", "id": "kp_modal_verbs_sync"})
            else:
                sync_results.append({"action": "exists", "knowledge_point": "情态动词", "id": existing["id"]})
            
            # 检查并添加倒装句
            result = session.run("MATCH (kp:KnowledgePoint {name: '倒装句'}) RETURN kp.id as id")
            existing = result.single()
            if not existing:
                session.run("""
                    CREATE (kp:KnowledgePoint {
                        id: 'kp_inversion_sync',
                        name: '倒装句',
                        description: '倒装句是指将谓语动词或助动词提到主语之前的句子结构',
                        difficulty: 'hard',
                        grade_levels: ['高中一年级', '高中二年级', '高中三年级'],
                        learning_objectives: ['掌握部分倒装的结构', '理解完全倒装的使用场景']
                    })
                """)
                session.run("""
                    MATCH (parent:KnowledgePoint {name: '句型结构'})
                    MATCH (child:KnowledgePoint {name: '倒装句'})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """)
                sync_results.append({"action": "created", "knowledge_point": "倒装句", "id": "kp_inversion_sync"})
            else:
                sync_results.append({"action": "exists", "knowledge_point": "倒装句", "id": existing["id"]})
            
            # 检查并添加虚拟语气
            result = session.run("MATCH (kp:KnowledgePoint {name: '虚拟语气'}) RETURN kp.id as id")
            existing = result.single()
            if not existing:
                session.run("""
                    CREATE (kp:KnowledgePoint {
                        id: 'kp_subjunctive_sync',
                        name: '虚拟语气',
                        description: '虚拟语气表示假设、愿望、建议等非真实的情况',
                        difficulty: 'hard',
                        grade_levels: ['高中一年级', '高中二年级', '高中三年级'],
                        learning_objectives: ['掌握虚拟语气的基本形式', '理解虚拟语气的使用场景']
                    })
                """)
                session.run("""
                    MATCH (parent:KnowledgePoint {name: '动词时态'})
                    MATCH (child:KnowledgePoint {name: '虚拟语气'})
                    MERGE (parent)-[:HAS_SUB_POINT]->(child)
                """)
                sync_results.append({"action": "created", "knowledge_point": "虚拟语气", "id": "kp_subjunctive_sync"})
            else:
                sync_results.append({"action": "exists", "knowledge_point": "虚拟语气", "id": existing["id"]})
        
        return {
            "message": "数据库同步完成",
            "sync_results": sync_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据库同步失败: {str(e)}")
