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
