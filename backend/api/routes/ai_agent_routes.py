"""
AI Agent自动标注相关API路由
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from pydantic import BaseModel

from backend.services.ai_agent_service import ai_agent_service
from backend.services.database import neo4j_service
from backend.models.schema import Question

router = APIRouter()


class AutoAnnotationRequest(BaseModel):
    """自动标注请求模型"""
    question: Question


class BatchAutoAnnotationRequest(BaseModel):
    """批量自动标注请求模型"""
    questions: List[Question]


class AIAgentConfigRequest(BaseModel):
    """AI Agent配置请求模型"""
    confidence_threshold: float = 0.3
    max_auto_annotations: int = 5
    learning_enabled: bool = True


class AnnotationFeedback(BaseModel):
    """标注反馈模型"""
    question_id: str
    annotations: List[Dict[str, Any]]  # [{"kp_id": "xx", "is_correct": True}]


@router.post("/auto-annotate")
async def auto_annotate_single_question(request: AutoAnnotationRequest):
    """自动标注单个题目"""
    try:
        result = await ai_agent_service.auto_annotate_question(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"自动标注失败: {str(e)}")


@router.post("/batch-auto-annotate")
async def batch_auto_annotate_questions(request: BatchAutoAnnotationRequest, 
                                      background_tasks: BackgroundTasks):
    """批量自动标注题目"""
    try:
        # 如果题目数量较多，使用后台任务
        if len(request.questions) > 10:
            background_tasks.add_task(
                ai_agent_service.batch_auto_annotate, 
                request.questions
            )
            return {
                "message": f"已启动后台批量标注任务，共 {len(request.questions)} 道题目",
                "status": "background_task_started"
            }
        else:
            # 直接处理少量题目
            result = await ai_agent_service.batch_auto_annotate(request.questions)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量自动标注失败: {str(e)}")


@router.post("/smart-import")
async def smart_import_questions(questions_data: List[Dict[str, Any]]):
    """
    智能导入题目并自动标注
    支持从外部数据源导入题目时自动进行标注
    """
    try:
        imported_questions = []
        annotation_results = []
        
        for q_data in questions_data:
            # 创建题目对象
            question = Question(**q_data)
            
            # 保存题目到数据库
            question_id = neo4j_service.create_question(question)
            question.id = question_id
            imported_questions.append(question)
            
            # 自动标注
            annotation_result = await ai_agent_service.auto_annotate_question(question)
            annotation_results.append(annotation_result)
        
        return {
            "imported_count": len(imported_questions),
            "annotation_results": annotation_results,
            "status": "completed",
            "message": f"成功导入并标注 {len(imported_questions)} 道题目"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"智能导入失败: {str(e)}")


@router.get("/config")
async def get_ai_agent_config():
    """获取AI Agent当前配置"""
    try:
        config = ai_agent_service.get_configuration()
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取配置失败: {str(e)}")


@router.put("/config")
async def update_ai_agent_config(request: AIAgentConfigRequest):
    """更新AI Agent配置"""
    try:
        config_dict = request.dict()
        ai_agent_service.update_configuration(config_dict)
        
        return {
            "message": "AI Agent配置更新成功",
            "new_config": ai_agent_service.get_configuration()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"配置更新失败: {str(e)}")


@router.post("/feedback")
async def submit_annotation_feedback(feedback: AnnotationFeedback):
    """提交标注反馈，用于改进AI Agent"""
    try:
        result = await ai_agent_service.evaluate_annotation_quality(
            feedback.question_id,
            {"annotations": feedback.annotations}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"反馈提交失败: {str(e)}")


@router.post("/trigger-auto-annotation/{question_id}")
async def trigger_auto_annotation(question_id: str):
    """为已存在的题目触发自动标注"""
    try:
        # 获取题目信息
        question_data = neo4j_service.get_question(question_id)
        if not question_data:
            raise HTTPException(status_code=404, detail="题目不存在")
        
        # 创建题目对象
        question = Question(**question_data)
        question.id = question_id
        
        # 执行自动标注
        result = await ai_agent_service.auto_annotate_question(question)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"触发自动标注失败: {str(e)}")


@router.get("/stats")
async def get_auto_annotation_stats():
    """获取自动标注统计信息"""
    try:
        # 这里可以实现统计逻辑
        # 暂时返回模拟数据
        return {
            "total_auto_annotations": 0,
            "success_rate": 0.0,
            "average_confidence": 0.0,
            "most_annotated_knowledge_points": [],
            "recent_activity": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")


@router.post("/retrain")
async def retrain_ai_agent(background_tasks: BackgroundTasks):
    """重新训练AI Agent（基于用户反馈）"""
    try:
        # 这里可以实现重新训练逻辑
        background_tasks.add_task(_retrain_agent_task)
        
        return {
            "message": "AI Agent重训练任务已启动",
            "status": "background_task_started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动重训练失败: {str(e)}")


async def _retrain_agent_task():
    """重新训练AI Agent的后台任务"""
    # 这里实现实际的重训练逻辑
    # 1. 收集用户反馈数据
    # 2. 分析标注准确率
    # 3. 调整模型参数
    # 4. 更新关键词匹配规则
    pass
