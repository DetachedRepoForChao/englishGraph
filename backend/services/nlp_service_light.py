"""
轻量级NLP辅助标注服务 (用于Vercel部署)
提供基于关键词匹配的知识点推荐功能
"""
import re
import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)


class NLPService:
    """轻量级NLP辅助标注服务类"""
    
    def __init__(self):
        self.keyword_patterns = self._build_keyword_patterns()
        
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
            ]
        }
    
    def suggest_knowledge_points(self, question_content: str, question_type: str = "选择题") -> List[Dict[str, Any]]:
        """
        推荐知识点
        
        Args:
            question_content: 题目内容
            question_type: 题目类型
            
        Returns:
            推荐的知识点列表，按置信度排序
        """
        try:
            # 预处理题目内容
            processed_text = self._preprocess_text(question_content)
            
            # 为每个知识点计算匹配分数
            suggestions = []
            for kp_name, patterns in self.keyword_patterns.items():
                keyword_score, matched_keywords = self._keyword_matching_score(processed_text, kp_name)
                
                if keyword_score > 0:
                    # 基于题目类型调整分数
                    type_score = self._question_type_score(question_type, kp_name)
                    
                    # 计算综合分数
                    total_score = keyword_score * 0.7 + type_score * 0.3
                    
                    suggestion = {
                        "knowledge_point": kp_name,
                        "confidence": min(total_score, 1.0),
                        "matched_keywords": matched_keywords,
                        "reasoning": f"关键词匹配: {', '.join(matched_keywords)}"
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
    
    def _keyword_matching_score(self, question_text: str, knowledge_point: str) -> Tuple[float, List[str]]:
        """计算关键词匹配分数"""
        patterns = self.keyword_patterns.get(knowledge_point, [])
        matched_keywords = []
        score = 0.0
        
        for pattern in patterns:
            if pattern.lower() in question_text.lower():
                matched_keywords.append(pattern)
                # 长关键词权重更高
                score += 2.0 if len(pattern) > 5 else 1.0
        
        # 归一化分数
        if patterns:
            max_possible_score = len(patterns) * 2.0
            normalized_score = min(score / max_possible_score, 1.0)
        else:
            normalized_score = 0.0
        
        return normalized_score, matched_keywords
    
    def _question_type_score(self, question_type: str, knowledge_point: str) -> float:
        """基于题目类型计算额外分数"""
        type_mappings = {
            "选择题": {
                "一般现在时": 0.3,
                "一般过去时": 0.3,
                "现在进行时": 0.3,
                "被动语态": 0.2,
                "比较级和最高级": 0.2
            },
            "填空题": {
                "一般现在时": 0.4,
                "一般过去时": 0.4,
                "现在完成时": 0.3,
                "介词": 0.4,
                "动词时态": 0.3
            },
            "阅读理解": {
                "定语从句": 0.3,
                "宾语从句": 0.3,
                "动词时态": 0.2
            }
        }
        
        if question_type in type_mappings:
            for keyword, boost in type_mappings[question_type].items():
                if keyword in knowledge_point:
                    return boost
        
        return 0.0


# 全局实例
nlp_service = NLPService()
