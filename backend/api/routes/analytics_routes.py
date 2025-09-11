"""
数据分析相关API路由
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from backend.services.analytics_service import analytics_service

router = APIRouter()


class StudentAnswer(BaseModel):
    """学生答题记录模型"""
    question_id: str
    is_correct: bool


class WeakPointAnalysisRequest(BaseModel):
    """薄弱点分析请求模型"""
    student_answers: List[StudentAnswer]


class LearningPathRequest(BaseModel):
    """学习路径推荐请求模型"""
    target_knowledge_points: List[str]


@router.get("/coverage")
async def get_knowledge_coverage():
    """获取知识点覆盖分析"""
    try:
        result = analytics_service.get_knowledge_coverage_analysis()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/difficulty-distribution")
async def get_difficulty_distribution():
    """获取题目难度分布"""
    try:
        result = analytics_service.get_difficulty_distribution()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/type-distribution")
async def get_question_type_distribution():
    """获取题目类型分布"""
    try:
        result = analytics_service.get_question_type_distribution()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/hierarchy")
async def get_knowledge_hierarchy():
    """获取知识点层级结构分析"""
    try:
        result = analytics_service.get_knowledge_hierarchy_analysis()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/correlations")
async def get_knowledge_correlations():
    """获取知识点关联分析"""
    try:
        result = analytics_service.get_knowledge_correlation_analysis()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.post("/learning-path")
async def recommend_learning_path(request: LearningPathRequest):
    """生成学习路径推荐"""
    try:
        result = analytics_service.generate_learning_path_recommendation(
            request.target_knowledge_points
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐生成失败: {str(e)}")


@router.post("/weak-points")
async def analyze_weak_points(request: WeakPointAnalysisRequest):
    """分析学生薄弱知识点"""
    try:
        # 转换数据格式
        student_answers = [
            {"question_id": ans.question_id, "is_correct": ans.is_correct}
            for ans in request.student_answers
        ]
        
        result = analytics_service.analyze_student_weak_points(student_answers)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/comprehensive-report")
async def get_comprehensive_report():
    """获取综合分析报告"""
    try:
        result = analytics_service.get_comprehensive_report()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"报告生成失败: {str(e)}")


@router.get("/ai-agent-accuracy")
async def get_ai_agent_accuracy(
    page: int = 1,
    page_size: int = 15,
    difficulty: str = None,
    question_type: str = None
):
    """获取AI Agent标注准确率分析（支持分页）"""
    try:
        result = analytics_service.get_ai_agent_accuracy_analysis_paginated(
            page=page,
            page_size=page_size,
            difficulty=difficulty,
            question_type=question_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"准确率分析失败: {str(e)}")


@router.get("/dashboard-stats")
async def get_dashboard_stats():
    """获取仪表板统计数据"""
    try:
        coverage = analytics_service.get_knowledge_coverage_analysis()
        difficulty = analytics_service.get_difficulty_distribution()
        
        # 计算标注覆盖率
        total_kps = coverage["summary"].get("total_knowledge_points", 0)
        covered_kps = coverage["summary"].get("covered_knowledge_points", 0)
        coverage_rate = (covered_kps / total_kps * 100) if total_kps > 0 else 0
        
        # 正确统计已标注题目数（避免重复计算）
        from backend.services.database import neo4j_service
        if not neo4j_service.driver:
            neo4j_service.connect()
        
        with neo4j_service.driver.session() as session:
            annotated_result = session.run("MATCH (q:Question)-[:TESTS]->() RETURN count(DISTINCT q) as count")
            annotated_questions = annotated_result.single()["count"]
        
        return {
            "total_knowledge_points": total_kps,
            "total_questions": difficulty.get("total_questions", 0),
            "annotated_questions": annotated_questions,
            "annotation_coverage": round(coverage_rate, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计查询失败: {str(e)}")
