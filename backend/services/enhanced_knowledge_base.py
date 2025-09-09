"""
增强的知识库服务
集成开源数据，提供详细的关键词分析和年级归属
"""
import re
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

class EnhancedKnowledgeBase:
    """增强的英语知识库"""
    
    def __init__(self):
        self.knowledge_base = self._build_enhanced_knowledge_base()
        self.grade_mapping = self._build_grade_mapping()
        
    def _build_enhanced_knowledge_base(self) -> Dict[str, Dict[str, Any]]:
        """构建增强的知识库（集成开源数据）"""
        return {
            "一般现在时": {
                "description": "表示经常性、习惯性的动作或状态",
                "grade_levels": ["小学三年级", "小学四年级", "小学五年级"],
                "difficulty": "easy",
                "keywords": {
                    "time_markers": ["always", "usually", "often", "sometimes", "never", "seldom", "rarely"],
                    "frequency": ["every day", "every week", "every month", "every year", "every morning", "every evening"],
                    "chinese_markers": ["总是", "通常", "经常", "有时", "从不", "每天", "每周"],
                    "sentence_patterns": ["she _____ to", "he _____ to", "it _____ to"],
                    "grammar_features": ["第三人称单数", "动词原形", "does", "do"],
                    "context_clues": ["habit", "routine", "daily", "weekly", "习惯", "日常"]
                },
                "typical_errors": ["第三人称单数遗忘", "动词原形混用"],
                "learning_objectives": ["掌握一般现在时的基本用法", "理解第三人称单数变化规则"]
            },
            
            "现在进行时": {
                "description": "表示现在正在进行的动作或现阶段持续的动作",
                "grade_levels": ["小学四年级", "小学五年级", "小学六年级"],
                "difficulty": "medium",
                "keywords": {
                    "strong_indicators": ["look!", "listen!", "now", "right now", "at the moment", "at present"],
                    "time_markers": ["currently", "these days", "this week", "this month"],
                    "chinese_markers": ["看!", "听!", "现在", "正在", "此刻", "目前", "这些天"],
                    "sentence_patterns": ["look! _____ ing", "listen! _____ ing"],
                    "grammar_features": ["be动词+现在分词", "ing形式", "am/is/are + doing"],
                    "context_clues": ["can you see", "can you hear", "what is happening", "正在发生"]
                },
                "typical_errors": ["be动词遗忘", "现在分词拼写错误"],
                "learning_objectives": ["掌握现在进行时的构成", "理解现在进行时的使用场景"]
            },
            
            "一般过去时": {
                "description": "表示过去发生的动作或存在的状态",
                "grade_levels": ["小学四年级", "小学五年级", "小学六年级"],
                "difficulty": "easy",
                "keywords": {
                    "time_markers": ["yesterday", "last week", "last month", "last year", "last night"],
                    "time_expressions": ["ago", "in 1990", "in the past", "when I was young"],
                    "chinese_markers": ["昨天", "上周", "上个月", "去年", "以前", "过去", "当时"],
                    "grammar_features": ["动词过去式", "was", "were", "did"],
                    "context_clues": ["used to", "long ago", "once upon a time", "in those days"]
                },
                "typical_errors": ["不规则动词过去式", "was/were混用"],
                "learning_objectives": ["掌握规则动词过去式变化", "学会不规则动词过去式"]
            },
            
            "现在完成时": {
                "description": "表示过去发生的动作对现在造成的影响或结果",
                "grade_levels": ["初中一年级", "初中二年级", "初中三年级"],
                "difficulty": "medium",
                "keywords": {
                    "strong_indicators": ["already", "yet", "just", "ever", "never"],
                    "time_markers": ["since", "for", "so far", "up to now", "recently"],
                    "chinese_markers": ["已经", "还", "刚刚", "曾经", "从未", "自从", "持续"],
                    "grammar_features": ["have/has + 过去分词", "have done", "has been"],
                    "sentence_patterns": ["have you ever", "i have already", "she has just"]
                },
                "typical_errors": ["have/has选择错误", "过去分词形式错误"],
                "learning_objectives": ["理解现在完成时的含义", "掌握过去分词的变化规则"]
            },
            
            "被动语态": {
                "description": "表示动作的承受者作为句子的主语",
                "grade_levels": ["初中二年级", "初中三年级", "高中一年级"],
                "difficulty": "hard",
                "keywords": {
                    "strong_indicators": [" by ", "was written by", "is made by", "are cleaned by"],
                    "grammar_features": ["be动词+过去分词", "was/were + done", "is/are + done"],
                    "chinese_markers": ["被", "由...做", "被动", "受到"],
                    "context_clues": ["被动语态", "passive voice"],
                    "typical_structures": ["the book was written", "the house is built", "letters are sent"]
                },
                "typical_errors": ["be动词时态错误", "过去分词形式错误"],
                "learning_objectives": ["理解被动语态的概念", "掌握各种时态的被动语态形式"]
            },
            
            "比较级和最高级": {
                "description": "形容词和副词的比较形式",
                "grade_levels": ["小学五年级", "小学六年级", "初中一年级"],
                "difficulty": "medium",
                "keywords": {
                    "comparison_markers": [" than ", "more than", "less than", "as...as"],
                    "superlative_markers": ["the most", "the best", "the biggest", "the smallest"],
                    "grammar_features": ["-er", "-est", "more", "most", "better", "best"],
                    "chinese_markers": ["比", "更", "最", "比较级", "最高级"],
                    "sentence_patterns": ["A is ___er than B", "A is the ___est", "A is more ___ than B"]
                },
                "typical_errors": ["比较级最高级混用", "不规则变化错误"],
                "learning_objectives": ["掌握形容词比较级变化规则", "学会使用最高级"]
            },
            
            "定语从句": {
                "description": "用来修饰名词或代词的从句",
                "grade_levels": ["初中二年级", "初中三年级", "高中一年级"],
                "difficulty": "hard",
                "keywords": {
                    "relative_pronouns": ["who", "which", "that", "whom", "whose"],
                    "relative_adverbs": ["where", "when", "why"],
                    "sentence_patterns": ["the man who", "the book which", "the place where", "the girl who", "the house which"],
                    "structure_indicators": ["_____ who", "_____ which", "_____ that", "_____ where", "_____ when"],
                    "chinese_markers": ["关系代词", "关系副词", "定语从句", "先行词"],
                    "context_clues": ["修饰", "限定", "说明", "从句"]
                },
                "typical_errors": ["关系代词选择错误", "先行词识别错误"],
                "learning_objectives": ["理解定语从句的作用", "掌握关系代词的用法"]
            },
            
            "宾语从句": {
                "description": "在句子中作宾语的从句",
                "grade_levels": ["初中二年级", "初中三年级", "高中一年级"],
                "difficulty": "hard",
                "keywords": {
                    "conjunctions": ["that", "what", "when", "where", "why", "how", "if", "whether"],
                    "intro_verbs": ["think", "know", "believe", "wonder", "ask", "tell"],
                    "sentence_patterns": ["i think that", "i know what", "i wonder if", "tell me where"],
                    "chinese_markers": ["宾语从句", "连接词", "引导词", "从句"],
                    "context_clues": ["宾语", "从句", "连接"]
                },
                "typical_errors": ["连接词选择错误", "语序错误"],
                "learning_objectives": ["理解宾语从句的概念", "掌握连接词的选择"]
            },
            
            "介词": {
                "description": "表示名词、代词等与其他词的关系",
                "grade_levels": ["小学三年级", "小学四年级", "小学五年级", "小学六年级"],
                "difficulty": "medium",
                "keywords": {
                    "basic_prepositions": ["in", "on", "at", "by", "for", "with", "to", "from", "of", "about"],
                    "place_prepositions": ["under", "over", "above", "below", "between", "among"],
                    "time_prepositions": ["before", "after", "during", "since", "until"],
                    "fixed_phrases": ["interested in", "good at", "afraid of", "proud of", "famous for"],
                    "chinese_markers": ["在", "用", "关于", "从", "到", "和", "为了", "介词", "前置词"]
                },
                "typical_errors": ["时间地点介词混用", "固定搭配错误"],
                "learning_objectives": ["掌握基本介词用法", "学会介词固定搭配"]
            },
            
            "动词时态": {
                "description": "动词的时间和状态变化形式",
                "grade_levels": ["小学四年级", "小学五年级", "小学六年级", "初中一年级"],
                "difficulty": "medium",
                "keywords": {
                    "general_terms": ["时态", "tense", "动词变化", "时间状语"],
                    "tense_types": ["过去", "现在", "将来", "完成", "进行", "一般"],
                    "chinese_markers": ["动词", "时态", "变化", "形式"],
                    "context_clues": ["时间", "状态", "动作"]
                },
                "typical_errors": ["时态混用", "动词变化错误"],
                "learning_objectives": ["理解动词时态概念", "掌握各种时态的用法"]
            },
            
            "虚拟语气": {
                "description": "表示假设、愿望、建议等非真实情况",
                "grade_levels": ["高中一年级", "高中二年级", "高中三年级"],
                "difficulty": "hard",
                "keywords": {
                    "conditional_markers": ["if", "wish", "would", "could", "should", "might"],
                    "subjunctive_patterns": ["if I were", "I wish I were", "would rather"],
                    "chinese_markers": ["虚拟语气", "假设", "愿望", "建议", "非真实"],
                    "context_clues": ["假如", "要是", "但愿", "宁愿"]
                },
                "typical_errors": ["虚拟语气形式错误", "时态搭配错误"],
                "learning_objectives": ["理解虚拟语气的概念", "掌握虚拟语气的各种形式"]
            }
        }
    
    def _build_grade_mapping(self) -> Dict[str, List[str]]:
        """构建年级映射"""
        return {
            "小学": ["小学一年级", "小学二年级", "小学三年级", "小学四年级", "小学五年级", "小学六年级"],
            "初中": ["初中一年级", "初中二年级", "初中三年级"],
            "高中": ["高中一年级", "高中二年级", "高中三年级"]
        }
    
    def get_knowledge_point_info(self, kp_name: str) -> Dict[str, Any]:
        """获取知识点的详细信息"""
        return self.knowledge_base.get(kp_name, {})
    
    def get_all_keywords_for_kp(self, kp_name: str) -> List[str]:
        """获取知识点的所有关键词"""
        kp_info = self.knowledge_base.get(kp_name, {})
        keywords = kp_info.get("keywords", {})
        
        all_keywords = []
        for category, word_list in keywords.items():
            all_keywords.extend(word_list)
        
        return all_keywords
    
    def analyze_question_features(self, question_text: str, kp_name: str) -> Dict[str, Any]:
        """分析题目特征，返回详细的匹配信息"""
        kp_info = self.knowledge_base.get(kp_name, {})
        if not kp_info:
            return {"matched_features": [], "confidence": 0.0, "reasoning": "知识点不存在"}
        
        keywords = kp_info.get("keywords", {})
        matched_features = {}
        total_score = 0.0
        reasoning_parts = []
        
        question_lower = question_text.lower()
        
        # 分析各类关键词匹配
        for category, word_list in keywords.items():
            matched_words = []
            category_score = 0.0
            
            for word in word_list:
                if self._is_word_matched(word, question_lower):
                    matched_words.append(word)
                    # 根据关键词类型给不同权重
                    if category in ["strong_indicators", "time_markers"]:
                        category_score += 0.8
                    elif category in ["grammar_features", "sentence_patterns"]:
                        category_score += 0.6
                    else:
                        category_score += 0.4
            
            if matched_words:
                matched_features[category] = {
                    "words": matched_words,
                    "score": min(category_score, 1.0),
                    "weight": len(matched_words) / len(word_list)
                }
                total_score += category_score
                reasoning_parts.append(f"{category}: {', '.join(matched_words)}")
        
        # 语言特征分析
        linguistic_score = self._analyze_linguistic_patterns(question_text, kp_name)
        if linguistic_score > 0.5:
            reasoning_parts.append(f"语言特征强匹配: {linguistic_score:.2f}")
            total_score += linguistic_score
        
        # 计算最终置信度
        final_confidence = min(total_score / 3.0, 1.0)  # 归一化到0-1
        
        return {
            "matched_features": matched_features,
            "confidence": final_confidence,
            "linguistic_score": linguistic_score,
            "reasoning": "; ".join(reasoning_parts) if reasoning_parts else "无明显特征",
            "grade_levels": kp_info.get("grade_levels", []),
            "difficulty": kp_info.get("difficulty", "medium"),
            "learning_objectives": kp_info.get("learning_objectives", [])
        }
    
    def _is_word_matched(self, word: str, question_lower: str) -> bool:
        """精确的词汇匹配"""
        word_lower = word.lower()
        
        # 对于短词（3个字符以内），使用词边界匹配
        if len(word_lower) <= 3:
            pattern = r'\b' + re.escape(word_lower) + r'\b'
            return bool(re.search(pattern, question_lower))
        else:
            # 长词或短语直接匹配
            return word_lower in question_lower
    
    def _analyze_linguistic_patterns(self, question_text: str, kp_name: str) -> float:
        """分析语言模式（基于语言学规律）"""
        text_lower = question_text.lower()
        
        # 专门的语言特征分析
        if kp_name == "现在进行时":
            # 检查祈使注意标志
            if re.search(r'\blook\s*!|\blisten\s*!', text_lower):
                return 0.95
            # 检查现在时间标志
            if re.search(r'\bnow\b|\bright now\b|\bat the moment\b', text_lower):
                return 0.9
            return 0.0
        
        elif kp_name == "被动语态":
            # 检查被动标志词
            if re.search(r'\sby\s+\w+', text_lower):  # "by someone"结构
                return 0.95
            # 检查被动结构
            if re.search(r'\b(was|were|is|are|been)\s+\w+ed\b', text_lower):
                return 0.8
            return 0.0
        
        elif kp_name == "比较级和最高级":
            # 检查比较结构
            if re.search(r'\bthan\b', text_lower):
                return 0.95
            if re.search(r'\bthe\s+\w+est\b|\bthe most\s+\w+\b', text_lower):
                return 0.9
            return 0.0
        
        elif kp_name == "一般现在时":
            # 检查频率副词
            if re.search(r'\b(always|usually|often|sometimes|never)\b', text_lower):
                return 0.9
            if re.search(r'\bevery\s+(day|week|month|year)\b', text_lower):
                return 0.9
            return 0.0
        
        elif kp_name == "一般过去时":
            # 检查过去时间
            if re.search(r'\byesterday\b|\blast\s+(week|month|year)\b|\b\w+\s+ago\b', text_lower):
                return 0.9
            return 0.0
        
        elif kp_name == "现在完成时":
            # 检查完成时标志
            if re.search(r'\b(already|yet|just|ever|never|since|for)\b', text_lower):
                return 0.9
            return 0.0
        
        elif kp_name == "定语从句":
            # 检查关系代词结构 - 更精确的模式
            if re.search(r'\b(who|which|that|whom|whose)\s+', text_lower):
                return 0.95
            if re.search(r'\b(where|when|why)\s+', text_lower):
                return 0.9
            # 检查典型的定语从句结构
            if re.search(r'the\s+\w+\s+___+\s+(is|are|was|were)', text_lower):
                return 0.8  # "the man _____ is" 这种结构
            return 0.0
        
        elif kp_name == "宾语从句":
            # 检查宾语从句模式
            if re.search(r'\b(think|know|believe|wonder|ask|tell)\s+(that|what|if|whether)\b', text_lower):
                return 0.9
            return 0.0
        
        return 0.0

# 全局实例
enhanced_knowledge_base = EnhancedKnowledgeBase()
