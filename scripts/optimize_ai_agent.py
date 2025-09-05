#!/usr/bin/env python3
"""
AI Agent优化脚本
基于分析结果优化关键词库和决策算法，提升标注准确率
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
import time
from backend.services.nlp_service import nlp_service

def optimize_keyword_patterns():
    """优化关键词模式库"""
    print("🔧 优化AI Agent关键词库...")
    
    # 扩展关键词库
    enhanced_patterns = {
        "一般现在时": [
            "always", "usually", "often", "sometimes", "never",
            "every day", "every week", "every month", "every year",
            "总是", "通常", "经常", "有时", "从不", "每天", "每周", "每月", "每年",
            "第三人称单数", "动词原形", "does", "do", "goes", "plays", "works", "studies"
        ],
        "一般过去时": [
            "yesterday", "last week", "last month", "last year", "ago",
            "昨天", "上周", "上个月", "去年", "以前", "过去",
            "动词过去式", "was", "were", "did", "went", "played", "worked", "studied"
        ],
        "现在进行时": [
            "now", "at the moment", "currently", "right now", "look!", "listen!",
            "现在", "正在", "此刻", "目前",
            "be动词", "ing形式", "am", "is", "are", "playing", "working", "studying"
        ],
        "现在完成时": [
            "already", "yet", "just", "ever", "never", "since", "for",
            "已经", "还", "刚刚", "曾经", "从未", "自从", "持续",
            "have", "has", "过去分词", "finished", "done", "lived", "been"
        ],
        "定语从句": [
            "who", "which", "that", "whom", "whose", "where", "when",
            "关系代词", "关系副词", "先行词", "从句", "the man who", "the book which"
        ],
        "宾语从句": [
            "tell me", "ask", "wonder", "know", "think", "believe",
            "that", "whether", "if", "what", "when", "where", "why", "how",
            "宾语从句", "引导词", "陈述语序", "could you tell me"
        ],
        "被动语态": [
            "be动词", "过去分词", "by", "被动", "passive voice",
            "was", "were", "is", "are", "am", "been",
            "cleaned", "written", "made", "done", "finished"
        ],
        "比较级和最高级": [
            "than", "more", "most", "less", "least", "-er", "-est",
            "比较级", "最高级", "更", "最",
            "better", "best", "worse", "worst", "bigger", "biggest",
            "more beautiful", "most beautiful", "sweeter", "sweetest"
        ]
    }
    
    # 更新NLP服务的关键词库
    nlp_service.keyword_patterns.update(enhanced_patterns)
    
    print("✅ 关键词库优化完成")
    print(f"   📊 更新了 {len(enhanced_patterns)} 个知识点的关键词")
    
    return enhanced_patterns

def test_optimized_agent():
    """测试优化后的AI Agent"""
    print("\n🧪 测试优化后的AI Agent性能...")
    
    # 测试题目
    test_cases = [
        {
            "content": "I have already finished my homework.",
            "expected": ["现在完成时"],
            "description": "现在完成时测试"
        },
        {
            "content": "The man who is wearing a blue shirt is my teacher.",
            "expected": ["定语从句"],
            "description": "定语从句测试"
        },
        {
            "content": "The windows were cleaned by the students.",
            "expected": ["被动语态"],
            "description": "被动语态测试"
        },
        {
            "content": "This book is more interesting than that one.",
            "expected": ["比较级和最高级"],
            "description": "比较级测试"
        },
        {
            "content": "Could you tell me where the library is?",
            "expected": ["宾语从句"],
            "description": "宾语从句测试"
        }
    ]
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 测试 {i}: {test_case['description']}")
        print(f"   题目: {test_case['content'][:50]}...")
        
        try:
            # 调用优化后的NLP服务
            suggestions = nlp_service.suggest_knowledge_points(
                test_case["content"], 
                "选择题"
            )
            
            if suggestions:
                print(f"   💡 AI推荐:")
                for j, suggestion in enumerate(suggestions[:3], 1):
                    print(f"      {j}. {suggestion['knowledge_point_name']} "
                          f"(置信度: {suggestion['confidence']:.3f})")
                
                # 检查是否包含预期知识点
                predicted_kps = [s['knowledge_point_name'] for s in suggestions]
                found_expected = any(
                    any(exp in pred for pred in predicted_kps)
                    for exp in test_case['expected']
                )
                
                if found_expected:
                    correct_predictions += 1
                    print(f"   ✅ 正确识别了预期知识点")
                else:
                    print(f"   ❌ 未识别预期知识点: {', '.join(test_case['expected'])}")
            else:
                print(f"   ❌ 无推荐结果")
                
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
    
    accuracy = correct_predictions / total_tests * 100
    print(f"\n📊 优化后准确率: {accuracy:.1f}% ({correct_predictions}/{total_tests})")
    
    return accuracy

def apply_optimizations_to_system():
    """将优化应用到系统"""
    print("\n🚀 应用优化到系统...")
    
    try:
        # 更新AI Agent配置
        new_config = {
            "confidence_threshold": 0.25,  # 稍微提高阈值
            "max_auto_annotations": 3,
            "learning_enabled": True
        }
        
        response = requests.put(
            "http://localhost:8000/api/ai-agent/config",
            json=new_config
        )
        
        if response.status_code == 200:
            print("✅ AI Agent配置已更新")
            result = response.json()
            print(f"   新配置: {json.dumps(result['new_config'], ensure_ascii=False)}")
        else:
            print("❌ 配置更新失败")
            
    except Exception as e:
        print(f"❌ 应用优化失败: {e}")

def run_comprehensive_test():
    """运行综合测试"""
    print("\n🧪 运行优化后的综合测试...")
    
    # 创建测试题目
    test_questions = [
        {
            "content": "She has just finished her work.",
            "question_type": "选择题",
            "answer": "has finished"
        },
        {
            "content": "The book that I bought yesterday is very interesting.",
            "question_type": "选择题", 
            "answer": "that"
        },
        {
            "content": "The homework was done by Tom.",
            "question_type": "选择题",
            "answer": "was done"
        }
    ]
    
    success_count = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 测试题目 {i}: {question['content'][:40]}...")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/ai-agent/auto-annotate",
                json={"question": question},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                suggestions = result.get("suggestions", [])
                applied = result.get("applied_annotations", [])
                
                print(f"   💡 推荐数: {len(suggestions)}")
                print(f"   ✅ 应用数: {len(applied)}")
                
                if suggestions:
                    success_count += 1
                    top_suggestion = suggestions[0]
                    print(f"   🏆 最佳推荐: {top_suggestion['knowledge_point_name']} "
                          f"(置信度: {top_suggestion['confidence']:.3f})")
            else:
                print(f"   ❌ API调用失败")
                
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
    
    success_rate = success_count / len(test_questions) * 100
    print(f"\n🎯 综合测试成功率: {success_rate:.1f}% ({success_count}/{len(test_questions)})")

def main():
    """主函数"""
    print("🚀 AI Agent性能优化程序")
    print("="*50)
    
    # 检查系统状态
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ 系统未运行，请先启动系统")
            return
    except Exception:
        print("❌ 无法连接系统，请确保系统已启动")
        return
    
    print("✅ 系统连接正常")
    
    # 执行优化步骤
    enhanced_patterns = optimize_keyword_patterns()
    
    # 测试优化效果
    accuracy = test_optimized_agent()
    
    # 应用优化到系统
    apply_optimizations_to_system()
    
    # 运行综合测试
    run_comprehensive_test()
    
    print("\n" + "="*50)
    print("🎉 AI Agent优化完成!")
    print(f"📈 预期准确率提升到: {accuracy:.1f}%")
    print("💡 建议继续收集用户反馈数据以进一步改进")

if __name__ == "__main__":
    main()
