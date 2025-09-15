"""
轻量级NLP辅助标注服务 (用于Vercel部署)
提供基于关键词匹配的知识点推荐功能
集成增强知识库和详细特征分析
"""
import re
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)


class NLPService:
    """轻量级NLP辅助标注服务类"""
    
    def __init__(self):
        self.keyword_patterns = self._build_keyword_patterns()
        # 导入增强知识库
        try:
            from backend.services.enhanced_knowledge_base import enhanced_knowledge_base
            self.enhanced_kb = enhanced_knowledge_base
        except ImportError:
            logger.warning("无法导入增强知识库，使用基础版本")
            self.enhanced_kb = None
        
    def _build_keyword_patterns(self) -> Dict[str, List[str]]:
        """构建基于题干特征的关键词模式库"""
        return {
            "一般现在时": [
                # 时间标志词 - 题干中的关键特征
                "always", "usually", "often", "sometimes", "never", "seldom", "rarely",
                "every day", "every week", "every month", "every year", "every morning",
                "总是", "通常", "经常", "有时", "从不", "每天", "每周", "每月", "每年",
                # 语境标志
                "habit", "routine", "daily", "weekly", "monthly",
                "习惯", "日常", "平时", "一般情况下",
                # 句式特征（不包含答案选项）
                "she _____ to", "he _____ to", "it _____ to", "they _____ to"
            ],
            "一般过去时": [
                # 明确的过去时间标志
                "yesterday", "last week", "last month", "last year", "last night",
                "ago", "in 1990", "in the past", "when I was young",
                "昨天", "上周", "上个月", "去年", "以前", "过去", "当时",
                # 过去语境
                "used to", "long ago", "once upon a time", "in those days"
            ],
            "现在进行时": [
                # 强烈的现在进行时标志 - 这些是题干中的关键词
                "look!", "listen!", "now", "right now", "at the moment", 
                "at present", "currently", "these days", "this week",
                "看!", "听!", "现在", "正在", "此刻", "目前", "这些天",
                # 语境标志
                "can you see", "can you hear", "what is happening",
                "正在发生", "正在进行", "此时此刻"
            ],
            "现在完成时": [
                "already", "yet", "just", "ever", "never", "since", "for",
                "已经", "还", "刚刚", "曾经", "从未", "自从", "持续",
                "have done", "has done", "have been", "has been", "have finished", "has finished",
                "过去分词", "完成时态", "finished", "done", "lived", "worked", "studied"
            ],
            "被动语态": [
                "be动词", "过去分词", "by", "被动", "passive voice",
                "was cleaned", "were cleaned", "is cleaned", "are cleaned",
                "was written", "were written", "is written", "are written",
                "was made", "were made", "is made", "are made",
                "cleaned", "written", "made", "done", "finished"
            ],
            "定语从句": [
                "who", "which", "that", "whom", "whose", "where", "when",
                "the man who", "the book which", "the place where", "the time when",
                "关系代词", "关系副词", "定语从句", "先行词",
                "_____ who", "_____ which", "_____ that"
            ],
            "宾语从句": [
                "that", "what", "when", "where", "why", "how", "if", "whether",
                "I think that", "I know that", "I believe that", "I wonder if",
                "宾语从句", "从句", "连接词", "引导词"
            ],
            
            "非谓语动词": [
                "concerning", "concerned about", "being concerned", "to concern",
                "interested in", "excited about", "surprised at", "worried about",
                "being", "to be", "to do", "doing", "done",
                "现在分词", "过去分词", "不定式", "动名词", "非谓语动词"
            ],
            "比较级和最高级": [
                "than", "more", "most", "better", "best", "bigger", "biggest",
                "比较级", "最高级", "更", "最", "er", "est",
                "more beautiful", "most beautiful", "better than", "the best"
            ],
            "介词": [
                "in", "on", "at", "by", "for", "with", "to", "from", "of", "about",
                "在", "用", "关于", "从", "到", "和", "为了",
                "介词", "介词短语", "时间介词", "地点介词", "方式介词"
            ],
            "动词时态": [
                "时态", "tense", "动词变化", "时间状语", "时态选择",
                "过去", "现在", "将来", "完成", "进行", "一般"
            ],
            "倒装句": [
                "never", "seldom", "rarely", "hardly", "scarcely", "barely",
                "no sooner", "not only", "not until", "only", "so", "neither", "nor",
                "here", "there", "now", "then", "thus", "hence", "therefore",
                "倒装", "inversion", "部分倒装", "完全倒装",
                "助动词", "情态动词", "be动词", "do", "does", "did", "have", "has", "had"
            ],
            "虚拟语气": [
                "if", "wish", "hope", "suggest", "demand", "insist", "require",
                "would", "could", "should", "might", "were", "had", "were to",
                "虚拟语气", "subjunctive", "假设", "条件句", "非真实条件"
            ],
            "情态动词": [
                "can", "could", "may", "might", "must", "should", "would", "will",
                "shall", "ought to", "have to", "be able to", "be supposed to",
                "情态动词", "modal verbs", "能力", "可能性", "必要性", "推测"
            ]
        }
    
    def suggest_knowledge_points(self, question_content: str, question_type: str = "选择题") -> List[Dict[str, Any]]:
        """
        推荐知识点 - 专注于题干分析，不分析选项
        
        Args:
            question_content: 题目内容
            question_type: 题目类型
            
        Returns:
            推荐的知识点列表，按置信度排序
        """
        try:
            # 提取题干进行主要分析
            question_stem = self._extract_question_stem(question_content)
            processed_text = self._preprocess_text(question_stem)
            
            # 首先获取数据库中的知识点来获取ID
            from backend.services.database import neo4j_service
            
            # 确保数据库连接
            if not neo4j_service.driver:
                neo4j_service.connect()
            
            # 获取所有知识点的ID映射
            kp_id_map = {}
            try:
                if neo4j_service.driver:
                    with neo4j_service.driver.session() as session:
                        result = session.run("MATCH (kp:KnowledgePoint) RETURN kp.id as id, kp.name as name")
                        for record in result:
                            kp_id_map[record["name"]] = record["id"]
            except Exception as e:
                logger.warning(f"获取知识点ID映射失败: {e}")
            
            # 为每个知识点计算匹配分数
            suggestions = []
            
            # 检查所有知识点 (增强库 + 关键词模式)
            knowledge_points_to_check = set()
            
            # 添加增强知识库中的知识点
            if self.enhanced_kb:
                knowledge_points_to_check.update(self.enhanced_kb.knowledge_base.keys())
            
            # 添加关键词模式中的知识点
            knowledge_points_to_check.update(self.keyword_patterns.keys())
            
            knowledge_points_to_check = list(knowledge_points_to_check)
            
            for kp_name in knowledge_points_to_check:
                # 使用增强知识库进行分析 (如果知识点在增强库中)
                if self.enhanced_kb and kp_name in self.enhanced_kb.knowledge_base:
                    analysis_result = self.enhanced_kb.analyze_question_features(question_stem, kp_name)
                    
                    # 提高阈值，只返回有意义的匹配
                    if analysis_result["confidence"] > 0.25 or analysis_result["linguistic_score"] > 0.5:
                        # 获取知识点ID
                        kp_id = kp_id_map.get(kp_name, f"kp_{kp_name.replace(' ', '_')}")
                        
                        # 收集所有匹配的关键词
                        all_matched_keywords = []
                        feature_details = []
                        
                        for category, feature_info in analysis_result["matched_features"].items():
                            category_name = {
                                "strong_indicators": "强标志词",
                                "time_markers": "时间标志",
                                "grammar_features": "语法特征", 
                                "sentence_patterns": "句式模式",
                                "context_clues": "语境线索",
                                "chinese_markers": "中文标志"
                            }.get(category, category)
                            
                            words = feature_info["words"]
                            all_matched_keywords.extend(words)
                            feature_details.append(f"{category_name}: {', '.join(words)}")
                        
                        # 生成详细推理
                        reasoning_parts = []
                        if feature_details:
                            reasoning_parts.extend(feature_details)
                        if analysis_result["linguistic_score"] > 0.3:
                            reasoning_parts.append(f"语言特征: {analysis_result['linguistic_score']:.2f}")
                        
                        suggestion = {
                            "knowledge_point_id": kp_id,
                            "knowledge_point_name": kp_name,
                            "knowledge_point": kp_name,
                            "confidence": analysis_result["confidence"],
                            "matched_keywords": all_matched_keywords,
                            "reason": "; ".join(reasoning_parts),
                            "reasoning": "; ".join(reasoning_parts),
                            "linguistic_score": analysis_result["linguistic_score"],
                            "grade_levels": analysis_result["grade_levels"],
                            "difficulty": analysis_result["difficulty"],
                            "learning_objectives": analysis_result["learning_objectives"],
                            "feature_analysis": analysis_result["matched_features"]
                        }
                        suggestions.append(suggestion)
                
                # 对于不在增强库中的知识点，使用基础算法
                elif kp_name in self.keyword_patterns:
                    keyword_score, matched_keywords = self._keyword_matching_score(processed_text, kp_name)
                    linguistic_score = self._analyze_linguistic_features(question_stem, kp_name)
                    type_score = self._question_type_score(question_type, kp_name)
                    
                    # 优化分数计算逻辑
                    if linguistic_score > 0.5:
                        # 语言特征强时，优先考虑语言特征
                        total_score = linguistic_score * 0.7 + keyword_score * 0.2 + type_score * 0.1
                    elif keyword_score > 0.3:
                        # 关键词匹配较好时，平衡考虑
                        total_score = keyword_score * 0.6 + linguistic_score * 0.3 + type_score * 0.1
                    else:
                        # 基础匹配
                        total_score = keyword_score * 0.5 + linguistic_score * 0.3 + type_score * 0.2
                    
                    if total_score > 0.15:  # 提高阈值，减少误匹配
                        kp_id = kp_id_map.get(kp_name, f"kp_{kp_name.replace(' ', '_')}")
                        
                        # 生成更详细的推理信息
                        reasoning_parts = []
                        if matched_keywords:
                            reasoning_parts.append(f"关键词: {', '.join(matched_keywords)}")
                        if linguistic_score > 0.3:
                            reasoning_parts.append(f"语言特征: {linguistic_score:.2f}")
                        if type_score > 0.1:
                            reasoning_parts.append(f"题型匹配: {type_score:.2f}")
                        
                        suggestion = {
                            "knowledge_point_id": kp_id,
                            "knowledge_point_name": kp_name,
                            "knowledge_point": kp_name,
                            "confidence": min(total_score, 1.0),
                            "matched_keywords": matched_keywords,
                            "reason": "; ".join(reasoning_parts) if reasoning_parts else "基础匹配",
                            "reasoning": "; ".join(reasoning_parts) if reasoning_parts else "基础匹配",
                            "linguistic_score": linguistic_score,
                            "keyword_score": keyword_score,
                            "type_score": type_score
                        }
                        suggestions.append(suggestion)
            
            # 按置信度排序
            suggestions.sort(key=lambda x: x["confidence"], reverse=True)
            
            # 返回前10个建议
            return suggestions[:10]
            
        except Exception as e:
            logger.error(f"知识点推荐失败: {e}")
            return []
    
    def _preprocess_text(self, text: str) -> str:
        """预处理文本"""
        # 移除特殊字符，保留中英文和数字
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        # 转换为小写
        text = text.lower()
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _extract_question_stem(self, question_content: str) -> str:
        """提取题干，排除选项干扰 - 优化版本"""
        # 多种选项模式匹配
        option_patterns = [
            r'\s+[ABCD][\.\)]\s+',  # A. B) C. D)
            r'\s+[ABCD]\s+',        # A B C D
            r'[ABCD][\.\)]\s*',     # A. B) C. D)
            r'[ABCD]\s*$',          # 末尾的A B C D
        ]
        
        question_stem = question_content
        
        # 尝试匹配各种选项模式
        for pattern in option_patterns:
            match = re.search(pattern, question_content, re.IGNORECASE)
            if match:
                # 找到选项开始位置，提取题干
                question_stem = question_content[:match.start()].strip()
                break
        
        # 进一步清理题干
        # 移除常见的题目编号和标记
        question_stem = re.sub(r'^\d+[\.\)]\s*', '', question_stem)  # 移除题号
        question_stem = re.sub(r'^[（\(]\d+[）\)]\s*', '', question_stem)  # 移除括号题号
        
        # 清理多余的空格和标点
        question_stem = re.sub(r'\s+', ' ', question_stem).strip()
        question_stem = re.sub(r'[.,;!?]+$', '', question_stem)  # 移除末尾标点
        
        # 确保题干不为空
        if not question_stem or len(question_stem.strip()) < 3:
            # 如果提取失败，返回原始内容的前半部分
            words = question_content.split()
            if len(words) > 5:
                question_stem = ' '.join(words[:len(words)//2])
            else:
                question_stem = question_content
        
        return question_stem
    
    def _extract_options(self, question_content: str) -> List[str]:
        """提取题目选项"""
        options = []
        # 更简单的方式：直接查找选项部分
        option_part = re.search(r'A\.\s*(.*)', question_content, re.IGNORECASE | re.DOTALL)
        if option_part:
            option_text = option_part.group(1)
            # 按选项标识符分割
            parts = re.split(r'[BCD]\.\s*', option_text)
            for part in parts:
                cleaned = part.strip()
                if cleaned and not re.match(r'^[ABCD][\.\)]', cleaned):
                    options.append(cleaned)
        return options
    
    def _analyze_linguistic_features(self, question_stem: str, knowledge_point: str) -> float:
        """分析语言特征（基于LabelLLM思想）"""
        stem_lower = question_stem.lower()
        
        # 时态特征分析
        if knowledge_point == "一般现在时":
            # 检查频率副词和时间表达
            frequency_indicators = ["always", "usually", "often", "sometimes", "every day", "every week"]
            if any(indicator in stem_lower for indicator in frequency_indicators):
                return 0.9
            # 检查一般性陈述
            if "every" in stem_lower or "always" in stem_lower:
                return 0.8
            return 0.0
        
        elif knowledge_point == "现在进行时":
            # 检查现在进行时的强标志词
            progressive_indicators = ["look!", "listen!", "now", "right now", "at the moment"]
            if any(indicator in stem_lower for indicator in progressive_indicators):
                return 0.95  # 非常高的置信度
            # 检查现在语境
            if "now" in stem_lower or "look" in stem_lower or "listen" in stem_lower:
                return 0.9
            return 0.0
        
        elif knowledge_point == "一般过去时":
            # 检查过去时间标志
            past_indicators = ["yesterday", "last week", "last month", "ago", "in 1990"]
            if any(indicator in stem_lower for indicator in past_indicators):
                return 0.9
            return 0.0
        
        elif knowledge_point == "现在完成时":
            # 检查完成时标志，但排除倒装句的情况
            perfect_indicators = ["already", "yet", "just", "since", "for"]
            if any(indicator in stem_lower for indicator in perfect_indicators):
                return 0.9
            
            # 检查ever/never在完成时语境中的使用
            if "ever" in stem_lower and ("have" in stem_lower or "has" in stem_lower):
                return 0.9
            if "never" in stem_lower and ("have" in stem_lower or "has" in stem_lower):
                return 0.9
            
            return 0.0
        
        elif knowledge_point == "被动语态":
            # 检查被动语态标志
            if " by " in stem_lower:
                return 0.95  # by是被动语态的强标志
            # 检查被动语境
            passive_contexts = ["was", "were", "is", "are", "been"]
            if any(ctx + " " in stem_lower for ctx in passive_contexts):
                return 0.3
            return 0.0
        
        elif knowledge_point == "比较级和最高级":
            # 检查比较结构
            if " than " in stem_lower:
                return 0.95  # than是比较级的强标志
            comparison_words = ["more", "most", "better", "best", "bigger", "biggest"]
            if any(word in stem_lower for word in comparison_words):
                return 0.8
            return 0.0
        
        elif knowledge_point == "定语从句":
            # 检查关系代词
            relative_pronouns = ["who", "which", "that", "whom", "whose", "where", "when"]
            if any(pronoun + " " in stem_lower for pronoun in relative_pronouns):
                return 0.9
            return 0.0
        
        elif knowledge_point == "非谓语动词":
            # 检查非谓语动词特征
            score = 0.0
            
            # 现在分词特征
            if "concerning" in stem_lower:
                score = max(score, 0.9)
            
            # 过去分词+介词结构
            if "concerned about" in stem_lower:
                score = max(score, 0.95)
            
            # being + 分词结构
            if "being concerned" in stem_lower:
                score = max(score, 0.85)
            
            return score
        
        elif knowledge_point == "宾语从句":
            # 检查宾语从句引导词
            object_clause_indicators = ["that", "what", "when", "where", "why", "how", "if", "whether"]
            # 检查常见句式
            clause_patterns = ["i think that", "i know that", "i wonder if", "tell me what"]
            if any(pattern in stem_lower for pattern in clause_patterns):
                return 0.9
            if any(indicator + " " in stem_lower for indicator in object_clause_indicators):
                return 0.6
            return 0.0
        
        elif knowledge_point == "倒装句":
            # 检查倒装句标志词和结构
            inversion_indicators = ["never", "seldom", "rarely", "hardly", "scarcely", "barely", "no sooner", "not only", "not until", "only"]
            if any(indicator in stem_lower for indicator in inversion_indicators):
                return 0.95  # 提高倒装句的优先级
            
            # 检查部分倒装结构 (助动词/情态动词/be动词 + 主语)
            partial_inversion_patterns = [
                r'\b(do|does|did|have|has|had|will|would|can|could|may|might|must|should|is|are|was|were)\s+\w+',
                r'\b(never|seldom|rarely|hardly|scarcely|barely)\s+\w+',
                r'\b(not only|not until|only)\s+\w+'
            ]
            
            for pattern in partial_inversion_patterns:
                if re.search(pattern, stem_lower):
                    return 0.9
            
            # 检查完全倒装结构 (地点/时间副词 + 动词 + 主语)
            full_inversion_patterns = [
                r'\b(here|there|now|then|thus|hence|therefore)\s+\w+',
                r'\b(up|down|in|out|away|back)\s+\w+'
            ]
            
            for pattern in full_inversion_patterns:
                if re.search(pattern, stem_lower):
                    return 0.85
            
            return 0.0
        
        elif knowledge_point == "虚拟语气":
            # 检查虚拟语气标志词和结构
            subjunctive_indicators = ["if", "wish", "hope", "suggest", "demand", "insist", "require", "would", "could", "should", "might", "were", "had"]
            if any(indicator in stem_lower for indicator in subjunctive_indicators):
                return 0.8
            
            # 检查虚拟语气特殊结构
            subjunctive_patterns = [
                r'\bif\s+\w+\s+(were|had|would|could|should)',
                r'\b(wish|hope)\s+\w+\s+(were|had|would|could|should)',
                r'\b(suggest|demand|insist|require)\s+that',
                r'\b(would|could|should|might)\s+\w+'
            ]
            
            for pattern in subjunctive_patterns:
                if re.search(pattern, stem_lower):
                    return 0.9
            
            return 0.0
        
        elif knowledge_point == "情态动词":
            # 检查情态动词
            modal_verbs = ["can", "could", "may", "might", "must", "should", "would", "will", "shall", "ought to", "have to", "be able to", "be supposed to"]
            if any(modal in stem_lower for modal in modal_verbs):
                return 0.8
            
            # 检查情态动词的特殊用法
            modal_patterns = [
                r'\b(can|could|may|might|must|should|would|will|shall)\s+\w+',
                r'\b(ought to|have to|be able to|be supposed to)\s+\w+',
                r'\bmust\s+have\s+\w+',  # 推测用法
                r'\b(can|could|may|might)\s+have\s+\w+'  # 可能性推测
            ]
            
            for pattern in modal_patterns:
                if re.search(pattern, stem_lower):
                    return 0.9
            
            return 0.0
        
        return 0.0
    
    def _keyword_matching_score(self, question_text: str, knowledge_point: str) -> Tuple[float, List[str]]:
        """计算关键词匹配分数 - 优化版本"""
        patterns = self.keyword_patterns.get(knowledge_point, [])
        matched_keywords = []
        score = 0.0
        
        # 定义强标志词权重
        strong_indicators = {
            # 时态强标志词
            "every day": 5.0, "yesterday": 5.0, "now": 5.0, "already": 5.0, 
            "look!": 5.0, "listen!": 5.0, "right now": 5.0, "at the moment": 5.0,
            "last week": 5.0, "last month": 5.0, "ago": 5.0, "since": 5.0, "for": 5.0,
            
            # 语法结构强标志词
            "by": 5.0, "than": 5.0, "who": 5.0, "which": 5.0, "that": 5.0,
            "concerning": 5.0, "concerned about": 5.0, "being concerned": 5.0,
            
            # 倒装句强标志词
            "never": 5.0, "seldom": 5.0, "rarely": 5.0, "hardly": 5.0, "scarcely": 5.0,
            "no sooner": 5.0, "not only": 5.0, "not until": 5.0, "only": 5.0,
            
            # 虚拟语气强标志词
            "if": 4.0, "wish": 4.0, "would": 4.0, "could": 4.0, "should": 4.0,
            "were": 4.0, "had": 4.0, "suggest": 4.0, "demand": 4.0,
            
            # 情态动词强标志词
            "can": 4.0, "could": 4.0, "may": 4.0, "might": 4.0, "must": 4.0,
            "will": 4.0, "would": 4.0, "should": 4.0, "shall": 4.0
        }
        
        for pattern in patterns:
            pattern_lower = pattern.lower()
            text_lower = question_text.lower()
            
            # 精确匹配，避免误匹配
            matched = False
            if len(pattern_lower) <= 3:  # 短词需要词边界匹配
                if re.search(r'\b' + re.escape(pattern_lower) + r'\b', text_lower):
                    matched_keywords.append(pattern)
                    matched = True
            else:  # 长词或短语可以直接匹配
                if pattern_lower in text_lower:
                    matched_keywords.append(pattern)
                    matched = True
            
            # 只有匹配了才计算权重
            if matched:
                # 根据关键词重要性分配权重
                if pattern in strong_indicators:
                    score += strong_indicators[pattern]
                elif len(pattern) > 10:  # 非常长的短语
                    score += 3.0
                elif len(pattern) > 5:  # 长关键词
                    score += 2.0
                else:  # 普通关键词
                    score += 1.0
        
        # 改进的归一化分数计算
        if patterns:
            # 计算理论最大分数
            max_possible_score = 0
            for pattern in patterns:
                if pattern in strong_indicators:
                    max_possible_score += strong_indicators[pattern]
                elif len(pattern) > 10:
                    max_possible_score += 3.0
                elif len(pattern) > 5:
                    max_possible_score += 2.0
                else:
                    max_possible_score += 1.0
            
            # 归一化分数
            raw_score = score / max_possible_score if max_possible_score > 0 else 0
            
            # 多关键词匹配奖励
            if len(matched_keywords) > 1:
                bonus = min(len(matched_keywords) * 0.05, 0.2)  # 最多20%奖励
                normalized_score = min(raw_score + bonus, 1.0)
            else:
                normalized_score = min(raw_score, 1.0)
        else:
            normalized_score = 0.0
        
        return normalized_score, matched_keywords
    
    def _question_type_score(self, question_type: str, knowledge_point: str) -> float:
        """基于题目类型计算额外分数 - 优化版本"""
        type_mappings = {
            "选择题": {
                "一般现在时": 0.4,
                "一般过去时": 0.4,
                "现在进行时": 0.4,
                "现在完成时": 0.3,
                "被动语态": 0.3,
                "比较级和最高级": 0.3,
                "定语从句": 0.2,
                "宾语从句": 0.2,
                "介词": 0.2,
                "动词时态": 0.3,
                "非谓语动词": 0.3,
                "倒装句": 0.2,
                "虚拟语气": 0.2,
                "情态动词": 0.3
            },
            "填空题": {
                "一般现在时": 0.5,
                "一般过去时": 0.5,
                "现在完成时": 0.4,
                "介词": 0.5,
                "动词时态": 0.4,
                "被动语态": 0.3,
                "非谓语动词": 0.4,
                "情态动词": 0.4
            },
            "阅读理解": {
                "定语从句": 0.4,
                "宾语从句": 0.4,
                "动词时态": 0.3,
                "比较级和最高级": 0.2,
                "倒装句": 0.3,
                "虚拟语气": 0.3,
                "情态动词": 0.2
            },
            "翻译题": {
                "时态": 0.4,
                "被动语态": 0.3,
                "非谓语动词": 0.3,
                "倒装句": 0.2,
                "虚拟语气": 0.2,
                "情态动词": 0.3
            }
        }
        
        if question_type in type_mappings:
            for keyword, boost in type_mappings[question_type].items():
                if keyword in knowledge_point:
                    return boost
        
        return 0.0


# 全局实例
nlp_service = NLPService()
