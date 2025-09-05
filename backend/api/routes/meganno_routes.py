"""
MEGAnno+ 集成API路由
提供与MEGAnno+平台集成的增强标注功能
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from pydantic import BaseModel

from backend.services.meganno_integration import meganno_service
from backend.models.schema import Question

router = APIRouter()


class MEGAnnoConfig(BaseModel):
    """MEGAnno+配置模型"""
    meganno_endpoint: str = "http://localhost:8001"
    integration_enabled: bool = True
    confidence_boost_factor: float = 0.2
    human_feedback_weight: float = 0.3


class EnhancedAnnotationRequest(BaseModel):
    """增强标注请求模型"""
    question: Question
    enable_meganno: bool = True


class BatchEnhancedAnnotationRequest(BaseModel):
    """批量增强标注请求模型"""
    questions: List[Question]
    enable_meganno: bool = True


class MEGAnnoTaskRequest(BaseModel):
    """MEGAnno+任务创建请求"""
    questions: List[Question]
    task_name: str = None
    enable_expert_review: bool = True


@router.post("/enhanced-annotate")
async def enhanced_auto_annotate(request: EnhancedAnnotationRequest):
    """
    MEGAnno+增强的自动标注
    结合AI Agent和MEGAnno+的人机协作能力
    """
    try:
        if request.enable_meganno and meganno_service.integration_enabled:
            result = await meganno_service.enhanced_auto_annotate(request.question)
        else:
            # 降级到普通AI Agent标注
            from backend.services.ai_agent_service import ai_agent_service
            result = await ai_agent_service.auto_annotate_question(request.question)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"增强标注失败: {str(e)}")


@router.post("/batch-enhanced-annotate")
async def batch_enhanced_annotate(request: BatchEnhancedAnnotationRequest,
                                background_tasks: BackgroundTasks):
    """
    批量MEGAnno+增强标注
    """
    try:
        if len(request.questions) > 20:
            # 大批量任务使用后台处理
            background_tasks.add_task(
                meganno_service.batch_enhanced_annotation,
                request.questions
            )
            return {
                "message": f"已启动后台批量增强标注任务，共 {len(request.questions)} 道题目",
                "status": "background_task_started",
                "estimated_completion_time": len(request.questions) * 2
            }
        else:
            # 小批量直接处理
            result = await meganno_service.batch_enhanced_annotation(request.questions)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量增强标注失败: {str(e)}")


@router.post("/create-meganno-task")
async def create_meganno_task(request: MEGAnnoTaskRequest):
    """
    在MEGAnno+中创建标注任务
    """
    try:
        result = await meganno_service.create_meganno_annotation_task(request.questions)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建MEGAnno+任务失败: {str(e)}")


@router.get("/config")
async def get_meganno_config():
    """获取MEGAnno+集成配置"""
    try:
        return {
            "meganno_endpoint": meganno_service.meganno_endpoint,
            "integration_enabled": meganno_service.integration_enabled,
            "confidence_boost_factor": meganno_service.confidence_boost_factor,
            "human_feedback_weight": meganno_service.human_feedback_weight
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取配置失败: {str(e)}")


@router.put("/config")
async def update_meganno_config(config: MEGAnnoConfig):
    """更新MEGAnno+集成配置"""
    try:
        config_dict = config.dict()
        meganno_service.configure_meganno_integration(config_dict)
        
        return {
            "message": "MEGAnno+集成配置更新成功",
            "new_config": config_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"配置更新失败: {str(e)}")


@router.get("/statistics")
async def get_integration_statistics():
    """获取MEGAnno+集成统计信息"""
    try:
        stats = meganno_service.get_integration_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"统计信息获取失败: {str(e)}")


@router.post("/compare-annotation-quality")
async def compare_annotation_quality(questions: List[Question]):
    """
    比较AI Agent和MEGAnno+增强后的标注质量
    """
    try:
        comparison_results = []
        
        for question in questions[:5]:  # 限制比较数量
            # AI Agent标注
            from backend.services.ai_agent_service import ai_agent_service
            ai_result = await ai_agent_service.auto_annotate_question(question)
            
            # MEGAnno+增强标注
            enhanced_result = await meganno_service.enhanced_auto_annotate(question)
            
            # 比较结果
            ai_suggestions = ai_result.get("suggestions", [])
            enhanced_suggestions = enhanced_result.get("enhanced_suggestions", [])
            
            ai_top_confidence = ai_suggestions[0]["confidence"] if ai_suggestions else 0
            enhanced_top_confidence = enhanced_suggestions[0]["enhanced_confidence"] if enhanced_suggestions else 0
            
            comparison_results.append({
                "question_content": question.content[:50] + "...",
                "ai_agent": {
                    "top_suggestion": ai_suggestions[0]["knowledge_point_name"] if ai_suggestions else "无",
                    "confidence": ai_top_confidence,
                    "suggestions_count": len(ai_suggestions)
                },
                "meganno_enhanced": {
                    "top_suggestion": enhanced_suggestions[0]["knowledge_point_name"] if enhanced_suggestions else "无",
                    "enhanced_confidence": enhanced_top_confidence,
                    "human_verified": enhanced_suggestions[0].get("human_verified", False) if enhanced_suggestions else False,
                    "improvement": enhanced_top_confidence - ai_top_confidence
                }
            })
        
        # 计算总体改进
        improvements = [r["meganno_enhanced"]["improvement"] for r in comparison_results]
        average_improvement = sum(improvements) / len(improvements) if improvements else 0
        
        return {
            "comparison_results": comparison_results,
            "summary": {
                "total_compared": len(comparison_results),
                "average_confidence_improvement": round(average_improvement, 3),
                "significant_improvements": len([i for i in improvements if i > 0.1]),
                "recommendation": "MEGAnno+集成显著提升标注质量" if average_improvement > 0.1 else "改进效果一般"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"质量比较失败: {str(e)}")


@router.post("/simulate-expert-feedback")
async def simulate_expert_feedback(question_content: str, knowledge_point: str):
    """
    模拟专家反馈 (用于演示MEGAnno+的人工验证功能)
    """
    try:
        expert_feedback = await meganno_service._simulate_expert_feedback(question_content, knowledge_point)
        return {
            "question_content": question_content,
            "knowledge_point": knowledge_point,
            "expert_feedback": expert_feedback,
            "recommendation": "采用此标注" if expert_feedback["expert_verified"] else "需要进一步审核"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"专家反馈模拟失败: {str(e)}")


@router.get("/integration-health")
async def check_integration_health():
    """检查MEGAnno+集成健康状态"""
    try:
        health_status = {
            "integration_enabled": meganno_service.integration_enabled,
            "meganno_endpoint": meganno_service.meganno_endpoint,
            "last_check_time": datetime.now().isoformat()
        }
        
        # 尝试连接MEGAnno+服务 (模拟)
        try:
            # 实际应用中这里应该ping MEGAnno+服务
            # response = requests.get(f"{meganno_service.meganno_endpoint}/health", timeout=5)
            # meganno_healthy = response.status_code == 200
            meganno_healthy = True  # 模拟连接成功
            
            health_status.update({
                "meganno_service_status": "healthy" if meganno_healthy else "unhealthy",
                "integration_status": "active" if meganno_healthy and meganno_service.integration_enabled else "inactive"
            })
        except Exception:
            health_status.update({
                "meganno_service_status": "unreachable",
                "integration_status": "inactive"
            })
        
        return health_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"健康检查失败: {str(e)}")
