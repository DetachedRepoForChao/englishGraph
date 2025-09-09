"""
协作标注服务
集成AI Agent、MEGAnno和LabelLLM的多模型协作标注
"""
import re
import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class CollaborativeAnnotationService:
    """多模型协作标注服务"""
    
    def __init__(self):
        self.confidence_threshold = 0.3
        self.collaboration_enabled = True
        
    async def enhanced_annotation(self, question_content: str, question_type: str = "选择题") -> Dict[str, Any]:
        """
        增强的协作标注流程
        结合AI Agent、MEGAnno和LabelLLM
        """
        try:
            logger.info(f"开始协作标注: {question_content[:50]}...")
            
            # 第一阶段：AI Agent基础分析
            ai_result = await self._ai_agent_analysis(question_content, question_type)
            
            # 第二阶段：LabelLLM语言特征分析
            labelllm_result = await self._labelllm_analysis(question_content, question_type)
            
            # 第三阶段：MEGAnno多模态验证
            meganno_result = await self._meganno_validation(question_content, ai_result, labelllm_result)
            
            # 第四阶段：协作决策融合
            final_result = await self._collaborative_decision(ai_result, labelllm_result, meganno_result)
            
            logger.info(f"协作标注完成，推荐 {len(final_result.get('suggestions', []))} 个知识点")
            return final_result
            
        except Exception as e:
            logger.error(f"协作标注失败: {e}")
            return {"suggestions": [], "error": str(e), "status": "failed"}
    
    async def _ai_agent_analysis(self, question_content: str, question_type: str) -> Dict[str, Any]:
        """AI Agent基础分析"""
        try:
            from backend.services.nlp_service_light import nlp_service
            suggestions = nlp_service.suggest_knowledge_points(question_content, question_type)
            
            return {
                "source": "AI_Agent",
                "suggestions": suggestions,
                "confidence": max([s.get("confidence", 0) for s in suggestions]) if suggestions else 0
            }
        except Exception as e:
            logger.error(f"AI Agent分析失败: {e}")
            return {"source": "AI_Agent", "suggestions": [], "confidence": 0}
    
    async def _labelllm_analysis(self, question_content: str, question_type: str) -> Dict[str, Any]:
        """LabelLLM语言特征分析"""
        try:
            # 基于LabelLLM思想的深度语言分析
            question_stem = self._extract_clean_stem(question_content)
            
            # 语法结构分析
            grammar_features = self._analyze_grammar_structure(question_stem)
            
            # 语义模式识别
            semantic_patterns = self._identify_semantic_patterns(question_stem)
            
            # 语境分析
            context_analysis = self._analyze_context(question_stem, question_type)
            
            # 综合LabelLLM分析结果
            labelllm_suggestions = self._generate_labelllm_suggestions(
                grammar_features, semantic_patterns, context_analysis, question_stem
            )
            
            return {
                "source": "LabelLLM",
                "suggestions": labelllm_suggestions,
                "grammar_features": grammar_features,
                "semantic_patterns": semantic_patterns,
                "context_analysis": context_analysis,
                "confidence": max([s.get("confidence", 0) for s in labelllm_suggestions]) if labelllm_suggestions else 0
            }
            
        except Exception as e:
            logger.error(f"LabelLLM分析失败: {e}")
            return {"source": "LabelLLM", "suggestions": [], "confidence": 0}
    
    def _extract_clean_stem(self, question_content: str) -> str:
        """提取干净的题干"""
        # 移除选项（更全面的正则表达式）
        patterns = [
            r'[ABCD]\)\s*[^)]+(?=\s*[ABCD]\)|$)',  # A) xxx B) xxx格式
            r'[ABCD]\.\s*[^.]+(?=\s*[ABCD]\.|$)',  # A. xxx B. xxx格式
            r'[①②③④]\s*[^①②③④]+(?=\s*[①②③④]|$)',  # 中文编号
            r'\([ABCD]\)[^()]*(?=\([ABCD]\)|$)'      # (A)xxx(B)xxx格式
        ]
        
        stem = question_content
        for pattern in patterns:
            stem = re.sub(pattern, '', stem, flags=re.IGNORECASE | re.MULTILINE)
        
        # 清理空白和标点
        stem = re.sub(r'\s+', ' ', stem).strip()
        stem = re.sub(r'[.,;!?]+$', '', stem)
        
        return stem
    
    def _analyze_grammar_structure(self, question_stem: str) -> Dict[str, Any]:
        """分析语法结构"""
        text_lower = question_stem.lower()
        
        features = {
            "has_relative_clause": bool(re.search(r'\b(who|which|that|whom|whose|where|when|why)\s+', text_lower)),
            "has_passive_structure": bool(re.search(r'\b(was|were|is|are|been)\s+\w+ed\b|\bby\s+\w+', text_lower)),
            "has_comparison": bool(re.search(r'\bthan\b|\bmore\b|\bmost\b|\b\w+er\b|\b\w+est\b', text_lower)),
            "has_perfect_aspect": bool(re.search(r'\b(have|has)\s+\w+ed\b|\b(already|yet|just|ever|never)\b', text_lower)),
            "has_progressive_aspect": bool(re.search(r'\b(am|is|are|was|were)\s+\w+ing\b', text_lower)),
            "has_time_markers": bool(re.search(r'\b(yesterday|today|tomorrow|now|then|always|usually|often|sometimes|never)\b', text_lower)),
            "has_imperative_markers": bool(re.search(r'^(look|listen|watch|see)\s*!', text_lower)),
            "sentence_structure": self._identify_sentence_structure(text_lower)
        }
        
        return features
    
    def _identify_sentence_structure(self, text_lower: str) -> str:
        """识别句子结构"""
        if re.search(r'the\s+\w+\s+___+.*\bis\b', text_lower):
            return "definitive_clause_structure"  # 定语从句结构
        elif re.search(r'look\s*!|listen\s*!', text_lower):
            return "imperative_progressive"  # 祈使句+进行时
        elif re.search(r'\bevery\s+(day|week|month|year)\b', text_lower):
            return "habitual_action"  # 习惯性动作
        elif re.search(r'\byesterday\b|\blast\s+\w+\b|\b\w+\s+ago\b', text_lower):
            return "past_time_reference"  # 过去时间参照
        elif re.search(r'\bthan\b', text_lower):
            return "comparison_structure"  # 比较结构
        elif re.search(r'\bby\s+\w+', text_lower):
            return "passive_agent"  # 被动语态施事
        else:
            return "general_structure"
    
    def _identify_semantic_patterns(self, question_stem: str) -> Dict[str, Any]:
        """识别语义模式"""
        text_lower = question_stem.lower()
        
        patterns = {
            "temporal_focus": self._get_temporal_focus(text_lower),
            "action_type": self._get_action_type(text_lower),
            "subject_focus": self._get_subject_focus(text_lower),
            "grammatical_focus": self._get_grammatical_focus(text_lower)
        }
        
        return patterns
    
    def _get_temporal_focus(self, text: str) -> str:
        """获取时间焦点"""
        if re.search(r'\bnow\b|\bright now\b|\blook\s*!|\blisten\s*!', text):
            return "present_moment"
        elif re.search(r'\byesterday\b|\blast\s+\w+\b|\b\w+\s+ago\b', text):
            return "past_time"
        elif re.search(r'\bevery\b|\balways\b|\busually\b', text):
            return "habitual_time"
        elif re.search(r'\balready\b|\byet\b|\bjust\b|\bever\b|\bnever\b', text):
            return "completed_action"
        else:
            return "neutral"
    
    def _get_action_type(self, text: str) -> str:
        """获取动作类型"""
        if re.search(r'\bis\s+wearing\b|\bare\s+playing\b|\bam\s+doing\b', text):
            return "ongoing_action"
        elif re.search(r'\bby\s+\w+', text):
            return "passive_action"
        else:
            return "general_action"
    
    def _get_subject_focus(self, text: str) -> str:
        """获取主语焦点"""
        if re.search(r'\bthe\s+\w+\s+___+', text):
            return "definite_subject_with_modifier"  # 有修饰的特定主语
        else:
            return "general_subject"
    
    def _get_grammatical_focus(self, text: str) -> str:
        """获取语法焦点"""
        if re.search(r'\b(who|which|that|whom|whose|where|when|why)\b', text):
            return "relative_clause"
        elif re.search(r'\bthan\b', text):
            return "comparison"
        elif re.search(r'\bby\s+\w+', text):
            return "passive_voice"
        else:
            return "verb_tense"
    
    def _generate_labelllm_suggestions(self, grammar_features: Dict, semantic_patterns: Dict, 
                                     context_analysis: Dict, question_stem: str) -> List[Dict[str, Any]]:
        """基于LabelLLM分析生成建议"""
        suggestions = []
        
        # 基于语法结构的强规则推理
        if grammar_features.get("sentence_structure") == "definitive_clause_structure":
            suggestions.append({
                "knowledge_point_name": "定语从句",
                "confidence": 0.95,
                "reason": "检测到定语从句结构: 'the + 名词 + _____ + is'",
                "source": "LabelLLM_Grammar",
                "evidence": ["句子结构分析", "语法模式识别"]
            })
        
        if grammar_features.get("sentence_structure") == "imperative_progressive":
            suggestions.append({
                "knowledge_point_name": "现在进行时", 
                "confidence": 0.95,
                "reason": "检测到祈使句+进行时结构: 'Look!' 引导",
                "source": "LabelLLM_Grammar",
                "evidence": ["祈使标志词", "进行时语境"]
            })
        
        if grammar_features.get("sentence_structure") == "comparison_structure":
            suggestions.append({
                "knowledge_point_name": "比较级和最高级",
                "confidence": 0.95,
                "reason": "检测到比较结构: 'than' 标志",
                "source": "LabelLLM_Grammar", 
                "evidence": ["比较标志词", "比较结构"]
            })
        
        if grammar_features.get("sentence_structure") == "passive_agent":
            suggestions.append({
                "knowledge_point_name": "被动语态",
                "confidence": 0.95,
                "reason": "检测到被动语态: 'by' 施事标志",
                "source": "LabelLLM_Grammar",
                "evidence": ["被动标志词", "施事结构"]
            })
        
        # 基于语义模式的推理
        temporal_focus = semantic_patterns.get("temporal_focus")
        if temporal_focus == "present_moment":
            suggestions.append({
                "knowledge_point_name": "现在进行时",
                "confidence": 0.9,
                "reason": "语义分析: 现在时刻焦点",
                "source": "LabelLLM_Semantic",
                "evidence": ["时间语义", "现在焦点"]
            })
        elif temporal_focus == "habitual_time":
            suggestions.append({
                "knowledge_point_name": "一般现在时",
                "confidence": 0.9,
                "reason": "语义分析: 习惯性时间焦点", 
                "source": "LabelLLM_Semantic",
                "evidence": ["习惯语义", "频率表达"]
            })
        elif temporal_focus == "past_time":
            suggestions.append({
                "knowledge_point_name": "一般过去时",
                "confidence": 0.9,
                "reason": "语义分析: 过去时间焦点",
                "source": "LabelLLM_Semantic", 
                "evidence": ["过去语义", "时间参照"]
            })
        elif temporal_focus == "completed_action":
            suggestions.append({
                "knowledge_point_name": "现在完成时",
                "confidence": 0.9,
                "reason": "语义分析: 完成动作焦点",
                "source": "LabelLLM_Semantic",
                "evidence": ["完成语义", "结果状态"]
            })
        
        return suggestions
    
    async def _meganno_validation(self, question_content: str, ai_result: Dict, labelllm_result: Dict) -> Dict[str, Any]:
        """MEGAnno多模态验证"""
        try:
            # 收集所有候选建议
            all_suggestions = []
            all_suggestions.extend(ai_result.get("suggestions", []))
            all_suggestions.extend(labelllm_result.get("suggestions", []))
            
            # MEGAnno验证逻辑
            validated_suggestions = []
            
            for suggestion in all_suggestions:
                kp_name = suggestion.get("knowledge_point_name", "")
                confidence = suggestion.get("confidence", 0)
                
                # MEGAnno多模态验证
                validation_score = await self._meganno_validate_suggestion(
                    question_content, kp_name, suggestion
                )
                
                if validation_score > 0.3:  # MEGAnno验证通过
                    validated_suggestions.append({
                        **suggestion,
                        "meganno_validation": validation_score,
                        "validated": True
                    })
            
            return {
                "source": "MEGAnno",
                "validated_suggestions": validated_suggestions,
                "validation_count": len(validated_suggestions)
            }
            
        except Exception as e:
            logger.error(f"MEGAnno验证失败: {e}")
            return {"source": "MEGAnno", "validated_suggestions": [], "validation_count": 0}
    
    async def _meganno_validate_suggestion(self, question_content: str, kp_name: str, suggestion: Dict) -> float:
        """MEGAnno单个建议验证"""
        try:
            # 模拟MEGAnno的多模态分析
            validation_factors = []
            
            # 1. 语言一致性检查
            linguistic_consistency = self._check_linguistic_consistency(question_content, kp_name)
            validation_factors.append(("linguistic", linguistic_consistency))
            
            # 2. 教育合理性检查
            educational_validity = self._check_educational_validity(kp_name, suggestion)
            validation_factors.append(("educational", educational_validity))
            
            # 3. 上下文适配性检查
            context_appropriateness = self._check_context_appropriateness(question_content, kp_name)
            validation_factors.append(("context", context_appropriateness))
            
            # 综合验证分数
            total_score = sum(score for _, score in validation_factors) / len(validation_factors)
            
            return min(total_score, 1.0)
            
        except Exception as e:
            logger.error(f"MEGAnno验证单个建议失败: {e}")
            return 0.0
    
    def _check_linguistic_consistency(self, question_content: str, kp_name: str) -> float:
        """检查语言一致性"""
        text_lower = question_content.lower()
        
        # 强一致性规则
        strong_rules = {
            "定语从句": r'\b(who|which|that|whom|whose|where|when|why)\s+',
            "现在进行时": r'\b(look|listen)\s*!|\bnow\b|\bright now\b',
            "被动语态": r'\bby\s+\w+|\b(was|were|is|are)\s+\w+ed\b',
            "比较级和最高级": r'\bthan\b|\bthe\s+\w+est\b|\bmore\s+\w+\b',
            "一般过去时": r'\byesterday\b|\blast\s+\w+\b|\b\w+\s+ago\b',
            "现在完成时": r'\b(already|yet|just|ever|never|since|for)\b',
            "一般现在时": r'\b(always|usually|often|sometimes|never)\b|\bevery\s+(day|week|month|year)\b'
        }
        
        if kp_name in strong_rules:
            if re.search(strong_rules[kp_name], text_lower):
                return 0.95
        
        return 0.1
    
    def _check_educational_validity(self, kp_name: str, suggestion: Dict) -> float:
        """检查教育合理性"""
        # 基于教育经验的合理性检查
        confidence = suggestion.get("confidence", 0)
        
        # 如果置信度很低，教育合理性也低
        if confidence < 0.2:
            return 0.2
        elif confidence < 0.5:
            return 0.6
        else:
            return 0.9
    
    def _check_context_appropriateness(self, question_content: str, kp_name: str) -> float:
        """检查上下文适配性"""
        # 简化的上下文检查
        return 0.7  # 默认中等适配性
    
    async def _collaborative_decision(self, ai_result: Dict, labelllm_result: Dict, meganno_result: Dict) -> Dict[str, Any]:
        """协作决策融合"""
        try:
            # 收集所有验证通过的建议
            final_suggestions = []
            
            # 优先使用LabelLLM的高置信度结果
            labelllm_suggestions = labelllm_result.get("suggestions", [])
            for suggestion in labelllm_suggestions:
                if suggestion.get("confidence", 0) > 0.8:
                    final_suggestions.append({
                        **suggestion,
                        "collaboration_score": suggestion.get("confidence", 0) * 1.1,  # LabelLLM加权
                        "sources": ["LabelLLM"],
                        "validation": "high_confidence"
                    })
            
            # 添加MEGAnno验证通过的AI Agent结果
            validated_suggestions = meganno_result.get("validated_suggestions", [])
            for suggestion in validated_suggestions:
                # 检查是否已经在LabelLLM结果中
                kp_name = suggestion.get("knowledge_point_name", "")
                if not any(s.get("knowledge_point_name") == kp_name for s in final_suggestions):
                    final_suggestions.append({
                        **suggestion,
                        "collaboration_score": suggestion.get("confidence", 0) * suggestion.get("meganno_validation", 1.0),
                        "sources": ["AI_Agent", "MEGAnno"],
                        "validation": "meganno_verified"
                    })
            
            # 按协作分数排序
            final_suggestions.sort(key=lambda x: x.get("collaboration_score", 0), reverse=True)
            
            return {
                "suggestions": final_suggestions[:5],  # 返回前5个
                "collaboration_summary": {
                    "ai_agent_count": len(ai_result.get("suggestions", [])),
                    "labelllm_count": len(labelllm_result.get("suggestions", [])), 
                    "meganno_validated": len(validated_suggestions),
                    "final_count": len(final_suggestions)
                },
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"协作决策失败: {e}")
            return {"suggestions": [], "error": str(e), "status": "failed"}

# 全局协作标注服务实例
collaborative_annotation_service = CollaborativeAnnotationService()
