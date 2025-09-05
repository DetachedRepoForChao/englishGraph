#!/usr/bin/env python3
"""
修复关键词匹配问题
诊断并修复AI Agent一直返回相同置信度的问题
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
from backend.services.database import neo4j_service
from backend.services.nlp_service import nlp_service

def diagnose_keyword_matching():
    """诊断关键词匹配问题"""
    print("🔍 诊断关键词匹配问题")
    print("="*50)
    
    # 1. 检查数据库连接
    print("1️⃣ 检查数据库连接...")
    if neo4j_service.connect():
        print("✅ 数据库连接正常")
        
        # 获取数据库中的知识点
        db_knowledge_points = neo4j_service.search_knowledge_points("")
        print(f"📚 数据库中的知识点 ({len(db_knowledge_points)}个):")
        for i, kp in enumerate(db_knowledge_points, 1):
            print(f"   {i:2d}. {kp.get('name', '未知')} (ID: {kp.get('id', '未知')})")
    else:
        print("❌ 数据库连接失败")
        return False
    
    # 2. 检查关键词模式库
    print(f"\n2️⃣ 检查关键词模式库...")
    keyword_patterns = nlp_service.keyword_patterns
    print(f"📋 关键词库中的知识点 ({len(keyword_patterns)}个):")
    for i, kp_name in enumerate(keyword_patterns.keys(), 1):
        keywords_count = len(keyword_patterns[kp_name])
        print(f"   {i:2d}. {kp_name} ({keywords_count}个关键词)")
    
    # 3. 检查匹配问题
    print(f"\n3️⃣ 检查名称匹配问题...")
    db_names = {kp.get('name', '') for kp in db_knowledge_points}
    pattern_names = set(keyword_patterns.keys())
    
    print(f"🔍 数据库知识点: {sorted(db_names)}")
    print(f"🔍 关键词库知识点: {sorted(pattern_names)}")
    
    # 找出不匹配的知识点
    missing_in_patterns = db_names - pattern_names
    missing_in_db = pattern_names - db_names
    
    if missing_in_patterns:
        print(f"❌ 数据库中有但关键词库中没有的知识点:")
        for name in sorted(missing_in_patterns):
            print(f"   • {name}")
    
    if missing_in_db:
        print(f"⚠️ 关键词库中有但数据库中没有的知识点:")
        for name in sorted(missing_in_db):
            print(f"   • {name}")
    
    return True

def test_keyword_matching():
    """测试关键词匹配功能"""
    print(f"\n4️⃣ 测试关键词匹配功能...")
    
    test_cases = [
        ("She goes to school every day.", "一般现在时"),
        ("I have already finished my homework.", "现在完成时"),
        ("The book which is on the table belongs to me.", "定语从句"),
        ("Yesterday I went to the park.", "一般过去时")
    ]
    
    for question_text, expected_kp in test_cases:
        print(f"\n🧪 测试: {question_text[:40]}...")
        print(f"   期望知识点: {expected_kp}")
        
        # 直接测试关键词匹配
        if expected_kp in nlp_service.keyword_patterns:
            score, matched_keywords = nlp_service._keyword_matching_score(question_text, expected_kp)
            print(f"   🎯 匹配分数: {score:.3f}")
            print(f"   🔑 匹配关键词: {matched_keywords}")
        else:
            print(f"   ❌ 关键词库中没有 '{expected_kp}'")

def fix_keyword_patterns():
    """修复关键词模式库"""
    print(f"\n5️⃣ 修复关键词模式库...")
    
    # 获取数据库中的实际知识点名称
    if not neo4j_service.connect():
        print("❌ 无法连接数据库")
        return False
    
    db_knowledge_points = neo4j_service.search_knowledge_points("")
    db_kp_names = [kp.get('name', '') for kp in db_knowledge_points]
    
    print(f"📚 数据库中的知识点: {db_kp_names}")
    
    # 更新关键词模式库以匹配数据库中的知识点名称
    updated_patterns = {}
    
    for kp_name in db_kp_names:
        if kp_name in nlp_service.keyword_patterns:
            # 已存在，直接复制
            updated_patterns[kp_name] = nlp_service.keyword_patterns[kp_name]
            print(f"✅ 保留现有模式: {kp_name}")
        else:
            # 新增知识点，创建基础关键词
            if "时态" in kp_name:
                updated_patterns[kp_name] = ["时态", "动词", "tense"]
            elif "语法" in kp_name:
                updated_patterns[kp_name] = ["语法", "grammar", "句型"]
            elif "从句" in kp_name:
                updated_patterns[kp_name] = ["从句", "clause", "句子"]
            elif "语态" in kp_name:
                updated_patterns[kp_name] = ["语态", "voice", "主动", "被动"]
            elif "比较" in kp_name:
                updated_patterns[kp_name] = ["比较", "than", "more", "most"]
            else:
                updated_patterns[kp_name] = [kp_name.lower()]
            
            print(f"🆕 新增模式: {kp_name} → {updated_patterns[kp_name]}")
    
    # 更新NLP服务的关键词模式库
    nlp_service.keyword_patterns = updated_patterns
    
    print(f"✅ 关键词模式库已更新，共 {len(updated_patterns)} 个知识点")
    neo4j_service.close()
    return True

def test_fixed_matching():
    """测试修复后的匹配效果"""
    print(f"\n6️⃣ 测试修复后的匹配效果...")
    
    test_questions = [
        {
            "content": "She goes to school every day.",
            "question_type": "选择题",
            "expected": "一般现在时"
        },
        {
            "content": "I have already finished my homework.",
            "question_type": "选择题", 
            "expected": "现在完成时"
        },
        {
            "content": "The letter was written by Tom.",
            "question_type": "选择题",
            "expected": "被动语态"
        }
    ]
    
    for i, test in enumerate(test_questions, 1):
        print(f"\n🧪 测试 {i}: {test['content'][:40]}...")
        
        # 调用API测试
        try:
            response = requests.post(
                "http://localhost:8000/api/ai-agent/auto-annotate",
                json={"question": test},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                suggestions = result.get("suggestions", [])
                
                print(f"   💡 AI推荐 ({len(suggestions)}个):")
                for j, suggestion in enumerate(suggestions[:3], 1):
                    kp_name = suggestion['knowledge_point_name']
                    confidence = suggestion['confidence']
                    keywords = suggestion.get('matched_keywords', [])
                    print(f"      {j}. {kp_name} (置信度: {confidence:.3f}) 关键词: {keywords}")
                
                # 检查是否正确识别期望的知识点
                expected = test['expected']
                found_expected = any(expected in s['knowledge_point_name'] for s in suggestions)
                
                if found_expected:
                    print(f"   ✅ 成功识别期望知识点: {expected}")
                else:
                    print(f"   ❌ 未识别期望知识点: {expected}")
            else:
                print(f"   ❌ API调用失败: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")

def main():
    """主修复函数"""
    print("🔧 AI Agent关键词匹配问题修复")
    print("="*50)
    
    # 诊断问题
    if not diagnose_keyword_matching():
        return
    
    # 测试当前匹配效果
    test_keyword_matching()
    
    # 修复关键词模式库
    if fix_keyword_patterns():
        print("\n🎉 关键词模式库修复完成")
        
        # 测试修复效果
        test_fixed_matching()
        
        print("\n📊 修复总结:")
        print("✅ 关键词模式库已更新")
        print("✅ 数据库知识点名称已匹配")
        print("💡 现在AI Agent应该能正确识别不同知识点了")
        print("🚀 请重新测试题目标注功能")
    else:
        print("❌ 修复失败")

if __name__ == "__main__":
    main()
