#!/usr/bin/env python3
"""
使用简单词库增强器丰富关键词库
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.simple_word_enhancer import SimpleWordEnhancer
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enhance_keywords_simple():
    """使用简单词库增强器增强关键词"""
    print("🚀 开始使用简单词库增强关键词...")
    
    # 初始化增强器
    enhancer = SimpleWordEnhancer()
    
    # 当前的关键词模式
    current_patterns = {
        "一般现在时": [
            "always", "usually", "often", "sometimes", "never",
            "every day", "every week", "every month", "every year",
            "总是", "通常", "经常", "有时", "从不", "每天", "每周", "每月", "每年",
            "第三人称单数", "动词原形", "does", "do", "goes", "plays", "works", "studies",
            "_____ to", "_____ every", "_____ always", "_____ usually",
            "A) go B) goes", "go/goes", "第三人称单数形式", "动词形式选择"
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
            "have", "has", "过去分词", "finished", "done", "lived", "been"
        ],
        "一般过去时": [
            "yesterday", "last week", "last month", "last year", "ago",
            "昨天", "上周", "上个月", "去年", "以前", "过去",
            "动词过去式", "was", "were", "did", "went", "played", "worked", "studied"
        ],
        "被动语态": [
            "be动词", "过去分词", "by", "被动", "passive voice",
            "was cleaned", "were written", "is made", "are done",
            "was written", "were cleaned", "by someone"
        ],
        "定语从句": [
            "which", "that", "who", "whom", "whose", "where", "when",
            "关系代词", "关系副词", "先行词", "从句", "the man who", "the book which"
        ],
        "宾语从句": [
            "that", "whether", "if", "what", "when", "where", "why", "how",
            "宾语从句", "引导词", "陈述语序", "tell me", "ask", "wonder", "know"
        ],
        "比较级和最高级": [
            "than", "more", "most", "less", "least", "-er", "-est",
            "比较级", "最高级", "更", "最",
            "better", "best", "worse", "worst", "bigger", "biggest",
            "more beautiful", "most beautiful", "sweeter", "sweetest"
        ]
    }
    
    print(f"📚 当前关键词库包含 {len(current_patterns)} 个知识点")
    
    # 增强关键词库
    enhanced_patterns = enhancer.generate_enhanced_patterns(current_patterns)
    
    # 统计增强效果
    total_original = sum(len(keywords) for keywords in current_patterns.values())
    total_enhanced = sum(len(keywords) for keywords in enhanced_patterns.values())
    
    print(f"\n📊 增强效果统计:")
    print(f"原始关键词总数: {total_original}")
    print(f"增强后关键词总数: {total_enhanced}")
    print(f"增加关键词数量: {total_enhanced - total_original}")
    print(f"增长率: {((total_enhanced - total_original) / total_original * 100):.1f}%")
    
    # 显示每个知识点的增强情况
    print(f"\n🎯 各知识点增强详情:")
    for kp, enhanced_keywords in enhanced_patterns.items():
        original_count = len(current_patterns[kp])
        enhanced_count = len(enhanced_keywords)
        print(f"  {kp}: {original_count} → {enhanced_count} (+{enhanced_count - original_count})")
    
    # 保存增强后的关键词库
    output_file = "enhanced_keyword_patterns_simple.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_patterns, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 增强后的关键词库已保存到: {output_file}")
    
    # 显示一些增强示例
    print(f"\n🔍 增强示例:")
    for kp in ["现在进行时", "一般现在时", "被动语态"]:
        if kp in enhanced_patterns:
            original = set(current_patterns[kp])
            enhanced = set(enhanced_patterns[kp])
            new_keywords = enhanced - original
            print(f"\n{kp} 新增关键词 (前15个):")
            for keyword in list(new_keywords)[:15]:
                print(f"  + {keyword}")
    
    return enhanced_patterns

def test_enhanced_keywords():
    """测试增强后的关键词效果"""
    print("\n🧪 测试增强后的关键词效果...")
    
    # 加载增强后的关键词库
    try:
        with open("enhanced_keyword_patterns_simple.json", 'r', encoding='utf-8') as f:
            enhanced_patterns = json.load(f)
        
        print("✅ 增强后的关键词库加载成功")
        
        # 显示一些统计信息
        for kp, keywords in enhanced_patterns.items():
            print(f"  {kp}: {len(keywords)} 个关键词")
        
        # 测试特定关键词
        test_keywords = ["play", "tense", "always", "be + doing"]
        print(f"\n🔍 测试关键词匹配:")
        for keyword in test_keywords:
            matches = []
            for kp, keywords in enhanced_patterns.items():
                if any(keyword.lower() in kw.lower() for kw in keywords):
                    matches.append(kp)
            print(f"  '{keyword}' 匹配知识点: {matches}")
            
    except FileNotFoundError:
        print("❌ 增强后的关键词库文件未找到")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    try:
        enhanced_patterns = enhance_keywords_simple()
        test_enhanced_keywords()
        print("\n✅ 关键词增强完成！")
        print("\n💡 使用建议:")
        print("1. 将增强后的关键词库集成到NLP服务中")
        print("2. 测试标注准确率是否有提升")
        print("3. 根据实际效果调整关键词权重")
    except Exception as e:
        print(f"\n❌ 关键词增强失败: {e}")
        import traceback
        traceback.print_exc()
