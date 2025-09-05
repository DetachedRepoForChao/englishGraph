#!/usr/bin/env python3
"""
开源词库增强模块
使用NLTK WordNet和spaCy来丰富关键词库
"""

import nltk
import spacy
from typing import Dict, List, Set, Tuple
import logging

logger = logging.getLogger(__name__)

class WordNetEnhancer:
    """使用开源词库增强关键词匹配"""
    
    def __init__(self):
        self.nlp = None
        self.wordnet_loaded = False
        self._initialize_nltk()
        self._initialize_spacy()
    
    def _initialize_nltk(self):
        """初始化NLTK"""
        try:
            # 下载必要的NLTK数据
            nltk.download('wordnet', quiet=True)
            nltk.download('brown', quiet=True)
            nltk.download('reuters', quiet=True)
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            self.wordnet_loaded = True
            logger.info("NLTK WordNet 初始化成功")
        except Exception as e:
            logger.warning(f"NLTK 初始化失败: {e}")
    
    def _initialize_spacy(self):
        """初始化spaCy"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy 模型加载成功")
        except OSError:
            logger.warning("spaCy 英文模型未安装，请运行: python -m spacy download en_core_web_sm")
        except Exception as e:
            logger.warning(f"spaCy 初始化失败: {e}")
    
    def get_synonyms(self, word: str) -> Set[str]:
        """获取同义词"""
        synonyms = set()
        if not self.wordnet_loaded:
            return synonyms
        
        try:
            from nltk.corpus import wordnet
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonyms.add(lemma.name().replace('_', ' '))
        except Exception as e:
            logger.warning(f"获取同义词失败 {word}: {e}")
        
        return synonyms
    
    def get_related_words(self, word: str) -> Set[str]:
        """获取相关词汇"""
        related = set()
        if not self.wordnet_loaded:
            return related
        
        try:
            from nltk.corpus import wordnet
            for syn in wordnet.synsets(word):
                # 上位词
                for hyper in syn.hypernyms():
                    for lemma in hyper.lemmas():
                        related.add(lemma.name().replace('_', ' '))
                # 下位词
                for hypo in syn.hyponyms():
                    for lemma in hypo.lemmas():
                        related.add(lemma.name().replace('_', ' '))
                # 部分词
                for part in syn.part_meronyms():
                    for lemma in part.lemmas():
                        related.add(lemma.name().replace('_', ' '))
        except Exception as e:
            logger.warning(f"获取相关词汇失败 {word}: {e}")
        
        return related
    
    def get_grammatical_forms(self, word: str) -> Set[str]:
        """获取语法形式变化"""
        forms = set()
        if not self.nlp:
            return forms
        
        try:
            doc = self.nlp(word)
            for token in doc:
                # 词根形式
                forms.add(token.lemma_)
                # 词性标注
                forms.add(f"{token.lemma_}_{token.pos_}")
        except Exception as e:
            logger.warning(f"获取语法形式失败 {word}: {e}")
        
        return forms
    
    def enhance_knowledge_point_keywords(self, knowledge_point: str, base_keywords: List[str]) -> List[str]:
        """增强知识点的关键词库"""
        enhanced_keywords = set(base_keywords)
        
        # 为每个基础关键词生成增强词汇
        for keyword in base_keywords:
            # 同义词
            synonyms = self.get_synonyms(keyword)
            enhanced_keywords.update(synonyms)
            
            # 相关词汇
            related = self.get_related_words(keyword)
            enhanced_keywords.update(related)
            
            # 语法形式
            forms = self.get_grammatical_forms(keyword)
            enhanced_keywords.update(forms)
        
        # 过滤和清理
        filtered_keywords = self._filter_keywords(enhanced_keywords, knowledge_point)
        
        logger.info(f"知识点 '{knowledge_point}' 关键词从 {len(base_keywords)} 个增强到 {len(filtered_keywords)} 个")
        return list(filtered_keywords)
    
    def _filter_keywords(self, keywords: Set[str], knowledge_point: str) -> Set[str]:
        """过滤关键词"""
        filtered = set()
        
        for keyword in keywords:
            # 长度过滤
            if len(keyword) < 2 or len(keyword) > 50:
                continue
            
            # 特殊字符过滤
            if any(char in keyword for char in ['<', '>', '{', '}', '[', ']', '(', ')']):
                continue
            
            # 数字过滤（保留一些重要的）
            if keyword.isdigit() and int(keyword) > 100:
                continue
            
            # 相关性过滤（简单实现）
            if self._is_relevant(keyword, knowledge_point):
                filtered.add(keyword.lower())
        
        return filtered
    
    def _is_relevant(self, keyword: str, knowledge_point: str) -> bool:
        """判断关键词是否相关"""
        # 简单的相关性判断
        knowledge_lower = knowledge_point.lower()
        
        # 包含知识点的核心词汇
        core_words = ['时态', '语态', '从句', '语法', '词汇', '比较', '被动', '进行', '完成', '过去', '现在', '将来']
        if any(word in keyword.lower() for word in core_words):
            return True
        
        # 包含知识点的英文关键词
        english_core = ['tense', 'voice', 'clause', 'grammar', 'comparison', 'passive', 'progressive', 'perfect', 'past', 'present', 'future']
        if any(word in keyword.lower() for word in english_core):
            return True
        
        return True  # 默认保留，让后续处理决定
    
    def generate_enhanced_keyword_patterns(self, base_patterns: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """生成增强的关键词模式库"""
        enhanced_patterns = {}
        
        for knowledge_point, keywords in base_patterns.items():
            enhanced_keywords = self.enhance_knowledge_point_keywords(knowledge_point, keywords)
            enhanced_patterns[knowledge_point] = enhanced_keywords
        
        return enhanced_patterns

# 使用示例
def demo_wordnet_enhancement():
    """演示词库增强功能"""
    enhancer = WordNetEnhancer()
    
    # 测试同义词
    print("🔍 同义词测试:")
    synonyms = enhancer.get_synonyms("play")
    print(f"play 的同义词: {list(synonyms)[:10]}")
    
    # 测试相关词汇
    print("\n🔗 相关词汇测试:")
    related = enhancer.get_related_words("tense")
    print(f"tense 的相关词汇: {list(related)[:10]}")
    
    # 测试语法形式
    print("\n📝 语法形式测试:")
    forms = enhancer.get_grammatical_forms("playing")
    print(f"playing 的语法形式: {list(forms)}")
    
    # 测试知识点增强
    print("\n🎯 知识点增强测试:")
    base_keywords = ["play", "playing", "plays", "played"]
    enhanced = enhancer.enhance_knowledge_point_keywords("现在进行时", base_keywords)
    print(f"现在进行时增强关键词: {enhanced[:20]}")

if __name__ == "__main__":
    demo_wordnet_enhancement()
