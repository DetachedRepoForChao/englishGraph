#!/usr/bin/env python3
"""
简单词库增强模块
使用预定义的词汇扩展和规则来丰富关键词库
"""

import re
from typing import Dict, List, Set
import logging

logger = logging.getLogger(__name__)

class SimpleWordEnhancer:
    """简单词库增强器"""
    
    def __init__(self):
        # 预定义的词汇扩展规则
        self.word_expansions = {
            # 时态相关
            "tense": ["tenses", "temporal", "time", "timing"],
            "present": ["current", "now", "today", "contemporary"],
            "past": ["previous", "former", "earlier", "before"],
            "future": ["coming", "upcoming", "next", "ahead"],
            
            # 语态相关
            "voice": ["voices", "vocal", "spoken", "oral"],
            "passive": ["passively", "inactive", "receptive"],
            "active": ["actively", "dynamic", "energetic"],
            
            # 语法相关
            "grammar": ["grammatical", "syntax", "structure", "rules"],
            "clause": ["clauses", "sentence", "phrase", "expression"],
            "verb": ["verbs", "action", "doing", "movement"],
            "noun": ["nouns", "subject", "object", "thing"],
            "adjective": ["adjectives", "descriptive", "qualifying"],
            "adverb": ["adverbs", "modifying", "describing"],
            
            # 比较相关
            "comparison": ["compare", "comparing", "relative", "relative"],
            "comparative": ["more", "less", "better", "worse"],
            "superlative": ["most", "least", "best", "worst"],
            
            # 时间相关
            "always": ["forever", "constantly", "continuously", "perpetually"],
            "usually": ["normally", "typically", "generally", "commonly"],
            "often": ["frequently", "regularly", "repeatedly", "many times"],
            "sometimes": ["occasionally", "at times", "now and then", "once in a while"],
            "never": ["not ever", "at no time", "not once", "under no circumstances"],
            
            # 频率相关
            "every day": ["daily", "each day", "day by day", "day after day"],
            "every week": ["weekly", "each week", "week by week"],
            "every month": ["monthly", "each month", "month by month"],
            "every year": ["yearly", "annually", "each year", "year by year"],
            
            # 动作相关
            "play": ["playing", "played", "plays", "game", "games", "sport", "sports"],
            "work": ["working", "worked", "works", "job", "jobs", "labor", "effort"],
            "study": ["studying", "studied", "studies", "learn", "learning", "education"],
            "go": ["going", "went", "goes", "move", "moving", "travel", "traveling"],
            "do": ["doing", "did", "does", "perform", "performing", "accomplish"],
            
            # 状态相关
            "be": ["being", "was", "were", "is", "are", "am", "exist", "existing"],
            "have": ["having", "had", "has", "possess", "possessing", "own", "owning"],
            "get": ["getting", "got", "gains", "obtain", "obtaining", "receive", "receiving"],
            
            # 地点相关
            "school": ["schools", "education", "academy", "institute", "university"],
            "home": ["house", "household", "residence", "dwelling", "place"],
            "playground": ["playgrounds", "park", "recreation", "play area", "court"],
            
            # 人物相关
            "children": ["kids", "youngsters", "youth", "minors", "students"],
            "people": ["persons", "individuals", "humans", "persons", "folk"],
            "teacher": ["teachers", "instructor", "educator", "professor", "tutor"],
            "student": ["students", "pupil", "learner", "scholar", "apprentice"]
        }
        
        # 语法形式变化规则
        self.grammar_rules = {
            # 动词时态变化
            "play": ["plays", "playing", "played"],
            "work": ["works", "working", "worked"],
            "study": ["studies", "studying", "studied"],
            "go": ["goes", "going", "went"],
            "do": ["does", "doing", "did"],
            "be": ["is", "are", "am", "was", "were", "being", "been"],
            "have": ["has", "having", "had"],
            "get": ["gets", "getting", "got"],
            
            # 名词复数
            "child": ["children"],
            "person": ["people"],
            "book": ["books"],
            "table": ["tables"],
            "school": ["schools"],
            "playground": ["playgrounds"],
            
            # 形容词比较级
            "good": ["better", "best"],
            "bad": ["worse", "worst"],
            "big": ["bigger", "biggest"],
            "small": ["smaller", "smallest"],
            "beautiful": ["more beautiful", "most beautiful"],
            "interesting": ["more interesting", "most interesting"]
        }
    
    def expand_keywords(self, keywords: List[str]) -> Set[str]:
        """扩展关键词"""
        expanded = set(keywords)
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            
            # 直接扩展
            if keyword_lower in self.word_expansions:
                expanded.update(self.word_expansions[keyword_lower])
            
            # 语法形式变化
            if keyword_lower in self.grammar_rules:
                expanded.update(self.grammar_rules[keyword_lower])
            
            # 部分匹配扩展
            for base_word, expansions in self.word_expansions.items():
                if base_word in keyword_lower or keyword_lower in base_word:
                    expanded.update(expansions)
        
        return expanded
    
    def generate_question_patterns(self, base_keywords: List[str]) -> Set[str]:
        """生成题目模式"""
        patterns = set()
        
        for keyword in base_keywords:
            # 填空题模式
            patterns.add(f"_____ {keyword}")
            patterns.add(f"{keyword} _____")
            
            # 选择题模式
            patterns.add(f"A) {keyword}")
            patterns.add(f"B) {keyword}")
            patterns.add(f"C) {keyword}")
            patterns.add(f"D) {keyword}")
            
            # 组合模式
            for other_keyword in base_keywords[:5]:  # 限制组合数量
                if keyword != other_keyword:
                    patterns.add(f"{keyword} {other_keyword}")
                    patterns.add(f"{other_keyword} {keyword}")
        
        return patterns
    
    def enhance_knowledge_point_keywords(self, knowledge_point: str, base_keywords: List[str]) -> List[str]:
        """增强知识点的关键词库"""
        enhanced = set(base_keywords)
        
        # 基础扩展
        expanded = self.expand_keywords(base_keywords)
        enhanced.update(expanded)
        
        # 生成题目模式
        question_patterns = self.generate_question_patterns(base_keywords)
        enhanced.update(question_patterns)
        
        # 根据知识点类型添加特定词汇
        enhanced.update(self._get_knowledge_specific_keywords(knowledge_point))
        
        # 过滤和清理
        filtered = self._filter_keywords(enhanced, knowledge_point)
        
        logger.info(f"知识点 '{knowledge_point}' 关键词从 {len(base_keywords)} 个增强到 {len(filtered)} 个")
        return list(filtered)
    
    def _get_knowledge_specific_keywords(self, knowledge_point: str) -> Set[str]:
        """获取知识点特定的关键词"""
        specific_keywords = set()
        
        if "现在进行时" in knowledge_point:
            specific_keywords.update([
                "be + doing", "am + doing", "is + doing", "are + doing",
                "present continuous", "progressive tense", "ongoing action",
                "happening now", "in progress", "currently doing"
            ])
        elif "现在完成时" in knowledge_point:
            specific_keywords.update([
                "have + done", "has + done", "present perfect", "completed action",
                "past action with present result", "experience", "achievement"
            ])
        elif "一般现在时" in knowledge_point:
            specific_keywords.update([
                "simple present", "habitual action", "general truth", "routine",
                "third person singular", "base form", "infinitive"
            ])
        elif "一般过去时" in knowledge_point:
            specific_keywords.update([
                "simple past", "past tense", "completed action", "yesterday",
                "last week", "ago", "past time", "historical fact"
            ])
        elif "被动语态" in knowledge_point:
            specific_keywords.update([
                "be + past participle", "passive voice", "subject receives action",
                "by + agent", "was done", "were done", "is done", "are done"
            ])
        elif "定语从句" in knowledge_point:
            specific_keywords.update([
                "relative clause", "who", "which", "that", "whose", "whom",
                "defining clause", "non-defining clause", "restrictive clause"
            ])
        elif "宾语从句" in knowledge_point:
            specific_keywords.update([
                "object clause", "noun clause", "that clause", "if clause",
                "whether clause", "wh- clause", "reported speech"
            ])
        elif "比较级" in knowledge_point or "最高级" in knowledge_point:
            specific_keywords.update([
                "comparison", "comparative", "superlative", "than", "more than",
                "less than", "as...as", "the most", "the least", "er", "est"
            ])
        
        return specific_keywords
    
    def _filter_keywords(self, keywords: Set[str], knowledge_point: str) -> Set[str]:
        """过滤关键词"""
        filtered = set()
        
        for keyword in keywords:
            # 长度过滤
            if len(keyword) < 2 or len(keyword) > 100:
                continue
            
            # 特殊字符过滤
            if any(char in keyword for char in ['<', '>', '{', '}', '[', ']', '(', ')', '\\', '/']):
                continue
            
            # 纯数字过滤
            if keyword.isdigit():
                continue
            
            # 空字符串过滤
            if not keyword.strip():
                continue
            
            filtered.add(keyword.strip())
        
        return filtered
    
    def generate_enhanced_patterns(self, base_patterns: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """生成增强的关键词模式库"""
        enhanced_patterns = {}
        
        for knowledge_point, keywords in base_patterns.items():
            enhanced_keywords = self.enhance_knowledge_point_keywords(knowledge_point, keywords)
            enhanced_patterns[knowledge_point] = enhanced_keywords
        
        return enhanced_patterns

# 使用示例
def demo_simple_enhancement():
    """演示简单词库增强功能"""
    enhancer = SimpleWordEnhancer()
    
    # 测试关键词扩展
    print("🔍 关键词扩展测试:")
    test_keywords = ["play", "tense", "always"]
    for keyword in test_keywords:
        expanded = enhancer.expand_keywords([keyword])
        print(f"{keyword} → {list(expanded)[:10]}")
    
    # 测试知识点增强
    print("\n🎯 知识点增强测试:")
    base_keywords = ["play", "playing", "plays", "played"]
    enhanced = enhancer.enhance_knowledge_point_keywords("现在进行时", base_keywords)
    print(f"现在进行时增强关键词: {enhanced[:20]}")

if __name__ == "__main__":
    demo_simple_enhancement()
