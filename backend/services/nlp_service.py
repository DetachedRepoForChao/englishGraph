"""
NLP辅助标注服务
提供基于自然语言处理的知识点推荐功能
"""
import re
import jieba
import logging
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from backend.services.database import neo4j_service

logger = logging.getLogger(__name__)


class NLPService:
    """NLP辅助标注服务类"""
    
    def __init__(self):
        self.keyword_patterns = self._build_keyword_patterns()
        self.tfidf_vectorizer = None
        self.knowledge_points_cache = []
        
    def _build_keyword_patterns(self) -> Dict[str, List[str]]:
        """构建关键词模式库"""
        return {
            "一般现在时": [
                "always", "usually", "often", "sometimes", "never",
                "every day", "every week", "every month", "every year",
                "总是", "通常", "经常", "有时", "从不", "每天", "每周", "每月", "每年",
                "第三人称单数", "动词原形", "does", "do", "goes", "plays", "works", "studies",
                "_____ to", "_____ every", "_____ always", "_____ usually",
                "A) go B) goes", "go/goes", "第三人称单数形式", "动词形式选择"
            ],
            "一般过去时": [
                "yesterday", "last week", "last month", "last year", "ago",
                "昨天", "上周", "上个月", "去年", "以前", "过去",
                "动词过去式", "was", "were", "did", "went", "played", "worked", "studied"
            ],
            "现在进行时": [
                "now", "at the moment", "at present", "currently", "right now", "look!", "listen!",
                "现在", "正在", "此刻", "目前", "现在进行时",
                "am doing", "is doing", "are doing", "am playing", "is playing", "are playing",
                "am working", "is working", "are working", "am studying", "is studying", "are studying",
                "_____ playing", "_____ working", "_____ studying", "A) play B) plays C) are playing",
                "be动词+现在分词", "ing形式", "进行时态", "playing", "working", "studying"
            ],
            "现在完成时": [
                "already", "yet", "just", "ever", "never", "since", "for",
                "已经", "还", "刚刚", "曾经", "从未", "自从", "持续",
                "have", "has", "过去分词", "finished", "done", "lived", "been",
                "interested", "am interested", "is interested", "are interested",
                "be interested in", "been interested", "getting interested",
                "become interested", "grow interested", "remain interested"
            ],
            "定语从句": [
                "which", "that", "who", "whom", "whose", "where", "when",
                "关系代词", "关系副词", "先行词", "从句", "the man who", "the book which"
            ],
            "宾语从句": [
                "that", "whether", "if", "what", "when", "where", "why", "how",
                "宾语从句", "引导词", "陈述语序", "tell me", "ask", "wonder", "know"
            ],
            "被动语态": [
                "be动词", "过去分词", "by", "被动", "passive voice",
                "was cleaned", "were written", "is made", "are done",
                "was written", "were cleaned", "by someone"
            ],
            "比较级和最高级": [
                "than", "more", "most", "less", "least", "-er", "-est",
                "比较级", "最高级", "更", "最",
                "better", "best", "worse", "worst", "bigger", "biggest",
                "more beautiful", "most beautiful", "sweeter", "sweetest"
            ],
            "介词": [
                "in", "on", "at", "by", "for", "with", "from", "to", "of", "about",
                "under", "over", "above", "below", "between", "among", "through",
                "interested in", "good at", "afraid of", "proud of", "famous for",
                "介词", "前置词", "preposition", "介词短语", "固定搭配",
                "_____ in", "_____ on", "_____ at", "_____ by", "_____ for",
                "A) in B) on C) at D) by", "介词选择", "介词填空"
            ],
            "动词时态": [
                "时态", "动词", "tense", "verb", "时间", "temporal",
                "现在时", "过去时", "进行时", "完成时"
            ],
            "英语语法": [
                "语法", "grammar", "句型", "structure", "语法规则", "语法点",
                "syntax", "grammatical", "语法现象"
            ]
        }
    
    def _preprocess_text(self, text: str) -> str:
        """预处理文本"""
        # 移除特殊字符，保留中英文和数字
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        # 转换为小写
        text = text.lower()
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 预处理文本
        processed_text = self._preprocess_text(text)
        
        # 中文分词
        chinese_words = jieba.lcut(processed_text)
        
        # 英文单词提取
        english_words = re.findall(r'[a-zA-Z]+', processed_text)
        
        # 合并关键词
        keywords = chinese_words + english_words
        
        # 过滤长度
        keywords = [word for word in keywords if len(word) > 1]
        
        return keywords
    
    def _keyword_matching_score(self, question_text: str, knowledge_point: str) -> Tuple[float, List[str]]:
        """基于关键词匹配计算分数"""
        if knowledge_point not in self.keyword_patterns:
            return 0.0, []
        
        patterns = self.keyword_patterns[knowledge_point]
        question_lower = question_text.lower()
        
        matched_keywords = []
        score = 0.0
        
        # 特殊语法结构检测
        grammar_structure_bonus = self._detect_grammar_structure(question_lower, knowledge_point)
        
        for pattern in patterns:
            if pattern.lower() in question_lower:
                matched_keywords.append(pattern)
                # 根据关键词重要性给不同权重
                if len(pattern) > 5:  # 长关键词权重更高
                    score += 2.0
                else:
                    score += 1.0
        
        # 添加语法结构加成
        score += grammar_structure_bonus
        
        # 归一化分数
        max_possible_score = len(patterns) * 2.0 + 5.0  # 加上语法结构的最大加成
        normalized_score = min(score / max_possible_score, 1.0) if max_possible_score > 0 else 0.0
        
        return normalized_score, matched_keywords
    
    def _detect_grammar_structure(self, question_text: str, knowledge_point: str) -> float:
        """检测语法结构，给予结构性加成"""
        bonus = 0.0
        
        # 现在完成时结构检测
        if knowledge_point == "现在完成时":
            # 检测 have/has + 过去分词 结构
            if ("have" in question_text or "has" in question_text):
                # 检查是否有典型的完成时标志词
                perfect_indicators = ["already", "just", "ever", "never", "yet", "since", "for"]
                if any(indicator in question_text for indicator in perfect_indicators):
                    bonus += 5.0  # 强结构加成
                elif any(word in question_text for word in ["finished", "done", "completed"]):
                    bonus += 3.0  # 中等结构加成
        
        # 被动语态结构检测  
        elif knowledge_point == "被动语态":
            # 检测 be动词 + by + 过去分词 结构
            if "by" in question_text and any(be_verb in question_text for be_verb in ["was", "were", "is", "are"]):
                bonus += 5.0  # 强被动语态结构
            elif any(be_verb in question_text for be_verb in ["was", "were"]) and not ("have" in question_text or "has" in question_text):
                bonus += 2.0  # 可能的被动语态
        
        # 定语从句结构检测
        elif knowledge_point == "定语从句":
            # 检测关系代词 + 从句结构
            relative_pronouns = ["who", "which", "that", "whom", "whose"]
            if any(pronoun in question_text for pronoun in relative_pronouns):
                bonus += 4.0  # 定语从句结构加成
        
        # 一般现在时结构检测
        elif knowledge_point == "一般现在时":
            # 检测频率副词 + 一般现在时动词
            if "every day" in question_text or "every week" in question_text:
                if any(verb in question_text for verb in ["goes", "plays", "works", "studies"]):
                    bonus += 4.0  # 强一般现在时结构
            
            # 检测填空题中的一般现在时特征
            if "_____" in question_text and "every" in question_text:
                if "goes" in question_text or "A) go B) goes" in question_text:
                    bonus += 6.0  # 填空题的一般现在时结构加成
        
        # 现在进行时结构检测
        elif knowledge_point == "现在进行时":
            # 检测进行时标志词 + be动词 + ing形式
            if "look!" in question_text or "listen!" in question_text:
                if "are playing" in question_text or "is playing" in question_text:
                    bonus += 6.0  # 强现在进行时结构
            elif "now" in question_text or "at the moment" in question_text:
                if any(verb in question_text for verb in ["are playing", "is playing", "am playing"]):
                    bonus += 5.0  # 现在进行时结构
            elif "_____" in question_text and "playing" in question_text:
                if "A) play B) plays C) are playing" in question_text:
                    bonus += 6.0  # 填空题的现在进行时结构
        
        # 一般过去时结构检测
        elif knowledge_point == "一般过去时":
            # 检测过去时间标志 + 过去式动词
            past_time_indicators = ["yesterday", "last week", "last month", "ago"]
            past_verbs = ["went", "played", "worked", "studied", "was", "were"]
            if (any(indicator in question_text for indicator in past_time_indicators) and
                any(verb in question_text for verb in past_verbs)):
                bonus += 4.0  # 强过去时结构
        
        # 介词结构检测
        elif knowledge_point == "介词":
            # 检测介词填空模式
            if "_____" in question_text:
                if any(prep in question_text for prep in ["in", "on", "at", "by", "for", "with", "from", "to", "of", "about"]):
                    bonus += 6.0  # 强介词结构
                elif any(pattern in question_text for pattern in ["interested", "good", "afraid", "proud", "famous"]):
                    bonus += 5.0  # 介词固定搭配
            elif "A) in B) on C) at D) by" in question_text:
                bonus += 6.0  # 介词选择题
        
        return bonus
    
    def _semantic_similarity_score(self, question_text: str, knowledge_point_desc: str) -> float:
        """基于语义相似度计算分数"""
        try:
            if not self.tfidf_vectorizer:
                # 简单的TF-IDF相似度计算
                texts = [question_text, knowledge_point_desc]
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform(texts)
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                return float(similarity)
        except Exception as e:
            logger.warning(f"语义相似度计算失败: {e}")
            
        return 0.0
    
    def suggest_knowledge_points(self, question_content: str, question_type: str) -> List[Dict[str, Any]]:
        """为题目建议知识点"""
        try:
            # 获取所有知识点
            try:
                all_knowledge_points = neo4j_service.search_knowledge_points("")
            except Exception as e:
                logger.warning(f"数据库查询失败，使用内置知识点: {e}")
                all_knowledge_points = []
            
            # 添加内置知识点（如果数据库连接失败）
            if not all_knowledge_points:
                all_knowledge_points = [
                    {"id": "kp_builtin_1", "name": "一般现在时", "description": "表示经常性、习惯性的动作或状态"},
                    {"id": "kp_builtin_2", "name": "现在进行时", "description": "表示现在正在进行的动作"},
                    {"id": "kp_builtin_3", "name": "现在完成时", "description": "表示过去发生的动作对现在造成的影响或结果"},
                    {"id": "kp_builtin_4", "name": "一般过去时", "description": "表示过去发生的动作或状态"},
                    {"id": "kp_builtin_5", "name": "被动语态", "description": "表示主语是动作的承受者"},
                    {"id": "kp_builtin_6", "name": "定语从句", "description": "用来修饰名词或代词的从句"},
                    {"id": "kp_builtin_7", "name": "宾语从句", "description": "在句子中作宾语的从句"},
                    {"id": "kp_builtin_8", "name": "比较级和最高级", "description": "形容词和副词的比较形式"},
                    {"id": "kp_builtin_9", "name": "介词", "description": "表示名词、代词等与句中其他词的关系的词"},
                ]
                logger.info(f"使用内置知识点，共 {len(all_knowledge_points)} 个")
            else:
                logger.info(f"从数据库获取知识点，共 {len(all_knowledge_points)} 个")
            
            suggestions = []
            
            for kp in all_knowledge_points:
                kp_name = kp.get("name", "")
                kp_desc = kp.get("description", "")
                kp_id = kp.get("id", "")
                
                # 关键词匹配分数
                keyword_score, matched_keywords = self._keyword_matching_score(question_content, kp_name)
                
                # 语义相似度分数
                semantic_score = self._semantic_similarity_score(question_content, kp_desc)
                
                # 题目类型匹配分数
                type_score = self._question_type_matching_score(question_type, kp_name)
                
                # 综合分数 - 提高关键词匹配的权重
                total_score = (keyword_score * 0.8 + semantic_score * 0.1 + type_score * 0.1)
                
                # 只返回有实际匹配的建议
                if total_score > 0.05 or (keyword_score > 0.1 and matched_keywords):
                    reason = self._generate_suggestion_reason(
                        matched_keywords, semantic_score, type_score
                    )
                    
                    suggestions.append({
                        "knowledge_point_id": kp_id,
                        "knowledge_point_name": kp_name,
                        "confidence": round(total_score, 3),
                        "reason": reason,
                        "matched_keywords": matched_keywords
                    })
                    
                    # 调试信息
                    if kp_name == "介词":
                        logger.info(f"介词匹配成功: 总分={total_score:.3f}, 关键词分数={keyword_score:.3f}, 匹配={matched_keywords}")
            
            # 按置信度排序
            suggestions.sort(key=lambda x: x["confidence"], reverse=True)
            
            # 返回前5个建议
            return suggestions[:5]
            
        except Exception as e:
            logger.error(f"知识点建议生成失败: {e}")
            return []
    
    def _question_type_matching_score(self, question_type: str, knowledge_point: str) -> float:
        """根据题目类型匹配知识点"""
        # 移除过于通用的匹配，只保留具体的语法点匹配
        type_mappings = {
            "选择题": ["现在完成时", "一般现在时", "一般过去时", "被动语态", "定语从句", "宾语从句"],
            "填空题": ["现在完成时", "一般现在时", "一般过去时", "被动语态", "比较级", "最高级"],
            "阅读理解": ["阅读技巧", "词汇理解"],
            "翻译题": ["句型", "语法结构"],
            "写作题": ["写作技巧", "句型"],
            "听力题": ["听力技巧", "语音", "语调"]
        }
        
        if question_type in type_mappings:
            relevant_keywords = type_mappings[question_type]
            for keyword in relevant_keywords:
                if keyword in knowledge_point:
                    return 0.6  # 降低类型匹配的权重
        
        return 0.0
    
    def _generate_suggestion_reason(self, matched_keywords: List[str], 
                                  semantic_score: float, type_score: float) -> str:
        """生成建议理由"""
        reasons = []
        
        if matched_keywords:
            reasons.append(f"匹配关键词: {', '.join(matched_keywords[:3])}")
        
        if semantic_score > 0.3:
            reasons.append("语义相似度较高")
        
        if type_score > 0.5:
            reasons.append("题目类型匹配")
        
        return "; ".join(reasons) if reasons else "综合分析推荐"
    
    def batch_suggest_for_questions(self, questions: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """批量为题目建议知识点"""
        results = {}
        
        for question in questions:
            question_id = question.get("id")
            content = question.get("content", "")
            question_type = question.get("question_type", "")
            
            suggestions = self.suggest_knowledge_points(content, question_type)
            results[question_id] = suggestions
        
        return results
    
    def update_knowledge_cache(self):
        """更新知识点缓存"""
        try:
            self.knowledge_points_cache = neo4j_service.search_knowledge_points("")
            logger.info(f"知识点缓存已更新，共{len(self.knowledge_points_cache)}个知识点")
        except Exception as e:
            logger.error(f"更新知识点缓存失败: {e}")


# 全局NLP服务实例
nlp_service = NLPService()
