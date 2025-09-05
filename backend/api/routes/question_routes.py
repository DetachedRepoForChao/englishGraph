"""
题目相关API路由
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.services.database import neo4j_service
from backend.models.schema import Question

router = APIRouter()


@router.post("/", response_model=Dict[str, str])
async def create_question(question: Question):
    """创建题目"""
    try:
        question_id = neo4j_service.create_question(question)
        return {"id": question_id, "message": "题目创建成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")


@router.post("/{question_id}/knowledge/{kp_id}")
async def link_question_to_knowledge(question_id: str, kp_id: str, weight: float = 1.0):
    """将题目链接到知识点"""
    try:
        neo4j_service.link_question_to_knowledge(question_id, kp_id, weight)
        return {"message": "题目知识点关联成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"关联失败: {str(e)}")


@router.get("/by-knowledge/{kp_name}")
async def get_questions_by_knowledge(kp_name: str):
    """根据知识点查找题目"""
    try:
        questions = neo4j_service.find_questions_by_knowledge_point(kp_name)
        return {"questions": questions, "count": len(questions)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/{question_id}/knowledge")
async def get_question_knowledge_points(question_id: str):
    """获取题目相关的知识点"""
    try:
        knowledge_points = neo4j_service.find_knowledge_points_by_question(question_id)
        return {"knowledge_points": knowledge_points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")
