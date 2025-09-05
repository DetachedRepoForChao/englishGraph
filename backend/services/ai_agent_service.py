"""
AI Agent自动标注服务
实现新题目进入时的自动智能标注功能
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json
import re

from backend.services.database import neo4j_service
from backend.services.nlp_service import nlp_service
from backend.models.schema import Question, KnowledgePoint

logger = logging.getLogger(__name__)


class AIAgentService:
    """AI Agent自动标注服务类"""
    
    def __init__(self):
        self.confidence_threshold = 0.3  # 自动标注的最低置信度阈值
        self.max_auto_annotations = 5    # 每道题最多自动标注的知识点数量
        self.learning_enabled = True     # 是否启用学习功能
        
    async def auto_annotate_question(self, question: Question) -> Dict[str, Any]:
        """
        自动标注单个题目
        
        Args:
            question: 题目对象
            
        Returns:
            标注结果字典
        """
        try:
            logger.info(f"开始自动标注题目: {question.content[:50]}...")
            
            # 1. 使用NLP服务获取知识点建议
            suggestions = nlp_service.suggest_knowledge_points(
                question.content, 
                question.question_type
            )
            
            # 2. 应用AI Agent的智能决策
            auto_annotations = await self._make_annotation_decisions(
                question, suggestions
            )
            
            # 3. 如果有高置信度的标注，自动应用
            applied_annotations = []
            if auto_annotations:
                applied_annotations = await self._apply_auto_annotations(
                    question, auto_annotations
                )
            
            # 4. 记录标注历史
            await self._log_annotation_history(question, auto_annotations, applied_annotations)
            
            result = {
                "question_id": question.id,
                "suggestions": suggestions,
                "auto_annotations": auto_annotations,
                "applied_annotations": applied_annotations,
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"自动标注完成，应用了 {len(applied_annotations)} 个标注")
            return result
            
        except Exception as e:
            logger.error(f"自动标注失败: {e}")
            return {
                "question_id": question.id,
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _make_annotation_decisions(self, question: Question, 
                                       suggestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        AI Agent智能决策过程
        基于多种因素决定是否自动标注
        """
        auto_annotations = []
        
        for suggestion in suggestions:
            confidence = suggestion.get("confidence", 0.0)
            kp_name = suggestion.get("knowledge_point_name", "")
            kp_id = suggestion.get("knowledge_point_id", "")
            
            # 决策规则
            decision_score = await self._calculate_decision_score(
                question, suggestion, confidence
            )
            
            if decision_score >= self.confidence_threshold:
                # 调整权重
                adjusted_weight = min(decision_score, 1.0)
                
                auto_annotations.append({
                    "knowledge_point_id": kp_id,
                    "knowledge_point_name": kp_name,
                    "confidence": confidence,
                    "decision_score": decision_score,
                    "weight": adjusted_weight,
                    "reason": suggestion.get("reason", ""),
                    "auto_applied": decision_score >= 0.7  # 高置信度自动应用
                })
        
        # 限制数量
        auto_annotations = sorted(auto_annotations, key=lambda x: x["decision_score"], reverse=True)
        return auto_annotations[:self.max_auto_annotations]
    
    async def _calculate_decision_score(self, question: Question, 
                                      suggestion: Dict[str, Any], 
                                      base_confidence: float) -> float:
        """
        计算AI Agent的决策分数
        综合考虑多种因素
        """
        score = base_confidence
        
        try:
            # 1. 题目类型匹配度加权
            type_boost = self._get_question_type_boost(
                question.question_type, 
                suggestion.get("knowledge_point_name", "")
            )
            score += type_boost
            
            # 2. 关键词匹配强度加权
            keyword_boost = self._get_keyword_match_boost(
                question.content,
                suggestion.get("matched_keywords", [])
            )
            score += keyword_boost
            
            # 3. 历史准确率加权（如果启用学习）
            if self.learning_enabled:
                history_boost = await self._get_historical_accuracy_boost(
                    suggestion.get("knowledge_point_id", ""),
                    question.question_type
                )
                score += history_boost
            
            # 4. 题目难度匹配度
            difficulty_boost = self._get_difficulty_match_boost(
                question.difficulty,
                suggestion.get("knowledge_point_name", "")
            )
            score += difficulty_boost
            
            # 5. 应用惩罚因子（避免过度标注）
            penalty = await self._get_over_annotation_penalty(question)
            score -= penalty
            
        except Exception as e:
            logger.warning(f"决策分数计算出现错误: {e}")
        
        return max(0.0, min(1.0, score))  # 限制在0-1之间
    
    def _get_question_type_boost(self, question_type: str, kp_name: str) -> float:
        """根据题目类型和知识点匹配度给出加权"""
        type_mappings = {
            "选择题": {
                "语法": 0.2, "时态": 0.2, "词汇": 0.1, "语态": 0.2
            },
            "填空题": {
                "时态": 0.3, "介词": 0.3, "词形变化": 0.2, "语法": 0.1
            },
            "阅读理解": {
                "阅读技巧": 0.3, "词汇理解": 0.2, "语法理解": 0.1
            },
            "翻译题": {
                "语法": 0.3, "词汇": 0.2, "句型": 0.2
            }
        }
        
        if question_type in type_mappings:
            for keyword, boost in type_mappings[question_type].items():
                if keyword in kp_name:
                    return boost
        
        return 0.0
    
    def _get_keyword_match_boost(self, question_content: str, 
                               matched_keywords: List[str]) -> float:
        """根据关键词匹配情况给出加权"""
        if not matched_keywords:
            return 0.0
        
        # 计算匹配密度
        total_matches = 0
        for keyword in matched_keywords:
            # 统计关键词在题目中出现的次数
            count = question_content.lower().count(keyword.lower())
            total_matches += count
        
        # 根据匹配密度给出加权
        content_length = len(question_content.split())
        match_density = total_matches / max(content_length, 1)
        
        return min(match_density * 0.3, 0.2)  # 最多加0.2分
    
    async def _get_historical_accuracy_boost(self, kp_id: str, 
                                           question_type: str) -> float:
        """根据历史标注准确率给出加权"""
        try:
            # 这里可以查询历史标注的准确率
            # 暂时返回固定值，实际应用中可以基于用户反馈数据计算
            return 0.1
        except Exception:
            return 0.0
    
    def _get_difficulty_match_boost(self, question_difficulty: Optional[str], 
                                  kp_name: str) -> float:
        """根据难度匹配情况给出加权"""
        if not question_difficulty:
            return 0.0
        
        # 简单的难度匹配逻辑
        difficulty_mappings = {
            "easy": ["基础", "简单", "入门"],
            "medium": ["中级", "一般", "标准"],
            "hard": ["高级", "复杂", "困难"]
        }
        
        if question_difficulty in difficulty_mappings:
            keywords = difficulty_mappings[question_difficulty]
            for keyword in keywords:
                if keyword in kp_name:
                    return 0.1
        
        return 0.0
    
    async def _get_over_annotation_penalty(self, question: Question) -> float:
        """计算过度标注的惩罚分数"""
        # 如果题目已经有很多标注，降低新标注的分数
        try:
            existing_annotations = neo4j_service.find_knowledge_points_by_question(question.id)
            annotation_count = len(existing_annotations)
            
            if annotation_count >= 3:
                return 0.1 * (annotation_count - 2)  # 超过3个标注开始惩罚
            
        except Exception:
            pass
        
        return 0.0
    
    async def _apply_auto_annotations(self, question: Question, 
                                    auto_annotations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """应用自动标注"""
        applied = []
        
        for annotation in auto_annotations:
            if annotation.get("auto_applied", False):
                try:
                    # 创建题目如果不存在
                    if not question.id:
                        question.id = neo4j_service.create_question(question)
                    
                    # 应用标注
                    neo4j_service.link_question_to_knowledge(
                        question.id,
                        annotation["knowledge_point_id"],
                        annotation["weight"]
                    )
                    
                    applied.append(annotation)
                    logger.info(f"自动应用标注: {annotation['knowledge_point_name']}")
                    
                except Exception as e:
                    logger.error(f"应用自动标注失败: {e}")
        
        return applied
    
    async def _log_annotation_history(self, question: Question, 
                                    auto_annotations: List[Dict[str, Any]],
                                    applied_annotations: List[Dict[str, Any]]):
        """记录标注历史（用于后续学习和改进）"""
        try:
            history_record = {
                "question_id": question.id,
                "question_content": question.content[:100],  # 只记录前100字符
                "question_type": question.question_type,
                "timestamp": datetime.now().isoformat(),
                "total_suggestions": len(auto_annotations),
                "applied_count": len(applied_annotations),
                "auto_annotations": auto_annotations,
                "applied_annotations": applied_annotations
            }
            
            # 这里可以将记录保存到日志文件或数据库
            logger.info(f"标注历史记录: {json.dumps(history_record, ensure_ascii=False, indent=2)}")
            
        except Exception as e:
            logger.error(f"记录标注历史失败: {e}")
    
    async def batch_auto_annotate(self, questions: List[Question]) -> Dict[str, Any]:
        """批量自动标注题目"""
        logger.info(f"开始批量自动标注 {len(questions)} 道题目")
        
        results = []
        success_count = 0
        error_count = 0
        
        for question in questions:
            try:
                result = await self.auto_annotate_question(question)
                results.append(result)
                
                if result.get("status") == "completed":
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                logger.error(f"批量标注中出现错误: {e}")
                error_count += 1
                results.append({
                    "question_id": getattr(question, 'id', 'unknown'),
                    "error": str(e),
                    "status": "failed"
                })
        
        summary = {
            "total_questions": len(questions),
            "success_count": success_count,
            "error_count": error_count,
            "success_rate": success_count / len(questions) if questions else 0,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"批量标注完成: 成功 {success_count}, 失败 {error_count}")
        return summary
    
    def update_configuration(self, config: Dict[str, Any]):
        """更新AI Agent配置"""
        if "confidence_threshold" in config:
            self.confidence_threshold = max(0.1, min(1.0, config["confidence_threshold"]))
        
        if "max_auto_annotations" in config:
            self.max_auto_annotations = max(1, min(10, config["max_auto_annotations"]))
        
        if "learning_enabled" in config:
            self.learning_enabled = bool(config["learning_enabled"])
        
        logger.info(f"AI Agent配置已更新: 置信度阈值={self.confidence_threshold}, "
                   f"最大标注数={self.max_auto_annotations}, 学习功能={'启用' if self.learning_enabled else '禁用'}")
    
    def get_configuration(self) -> Dict[str, Any]:
        """获取当前配置"""
        return {
            "confidence_threshold": self.confidence_threshold,
            "max_auto_annotations": self.max_auto_annotations,
            "learning_enabled": self.learning_enabled
        }
    
    async def evaluate_annotation_quality(self, question_id: str, 
                                        user_feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估标注质量并用于改进AI Agent
        
        Args:
            question_id: 题目ID
            user_feedback: 用户反馈 {"annotations": [{"kp_id": "xx", "is_correct": True}]}
        """
        try:
            # 获取AI Agent的原始标注
            # 这里应该从历史记录中获取
            
            # 计算准确率
            feedback_annotations = user_feedback.get("annotations", [])
            if not feedback_annotations:
                return {"message": "无有效反馈数据"}
            
            correct_count = sum(1 for ann in feedback_annotations if ann.get("is_correct", False))
            total_count = len(feedback_annotations)
            accuracy = correct_count / total_count if total_count > 0 else 0
            
            # 记录反馈用于后续改进
            feedback_record = {
                "question_id": question_id,
                "accuracy": accuracy,
                "feedback": user_feedback,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"标注质量评估: 题目 {question_id}, 准确率 {accuracy:.2%}")
            
            return {
                "question_id": question_id,
                "accuracy": accuracy,
                "correct_count": correct_count,
                "total_count": total_count,
                "status": "evaluated"
            }
            
        except Exception as e:
            logger.error(f"标注质量评估失败: {e}")
            return {"error": str(e), "status": "failed"}


# 全局AI Agent服务实例
ai_agent_service = AIAgentService()
