#!/usr/bin/env python3
"""
调试NLP匹配问题
找出为什么关键词匹配不工作的具体原因
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.services.nlp_service import nlp_service
from backend.services.database import neo4j_service

def debug_keyword_matching():
    """调试关键词匹配"""
    print("🔍 调试关键词匹配问题")
    print("="*50)
    
    # 测试题目
    test_question = "She goes to school every day."
    
    print(f"📝 测试题目: {test_question}")
    print(f"🔑 预处理后: {nlp_service._preprocess_text(test_question)}")
    
    # 检查知识点库
    print(f"\n📚 关键词模式库中的知识点:")
    for kp_name, keywords in nlp_service.keyword_patterns.items():
        print(f"   • {kp_name}: {keywords[:5]}...")  # 只显示前5个关键词
    
    # 逐个测试关键词匹配
    print(f"\n🧪 逐个测试关键词匹配:")
    for kp_name in nlp_service.keyword_patterns.keys():
        score, matched = nlp_service._keyword_matching_score(test_question, kp_name)
        if score > 0 or matched:
            print(f"   ✅ {kp_name}: 分数={score:.3f}, 匹配词={matched}")
        else:
            print(f"   ❌ {kp_name}: 无匹配")
    
    # 测试数据库连接
    print(f"\n🗄️ 测试数据库知识点获取:")
    if neo4j_service.connect():
        db_kps = neo4j_service.search_knowledge_points("")
        print(f"   📊 数据库中有 {len(db_kps)} 个知识点")
        for kp in db_kps[:5]:
            print(f"   • {kp.get('name', '未知')}")
        neo4j_service.close()
    else:
        print("   ❌ 数据库连接失败")

def test_direct_matching():
    """直接测试匹配功能"""
    print(f"\n🎯 直接测试匹配功能:")
    
    test_cases = [
        ("She goes to school every day.", "一般现在时", ["every day", "goes"]),
        ("I have already finished my homework.", "现在完成时", ["already", "have", "finished"]),
        ("The book which is on the table belongs to me.", "定语从句", ["which"]),
        ("Yesterday I went to the park.", "一般过去时", ["yesterday", "went"])
    ]
    
    for question, expected_kp, expected_keywords in test_cases:
        print(f"\n📝 题目: {question[:40]}...")
        print(f"🎯 期望知识点: {expected_kp}")
        print(f"🔑 期望关键词: {expected_keywords}")
        
        if expected_kp in nlp_service.keyword_patterns:
            score, matched = nlp_service._keyword_matching_score(question, expected_kp)
            print(f"   📊 实际分数: {score:.3f}")
            print(f"   🔍 实际匹配: {matched}")
            
            # 检查期望关键词是否在模式库中
            patterns = nlp_service.keyword_patterns[expected_kp]
            missing_keywords = [k for k in expected_keywords if k not in patterns]
            if missing_keywords:
                print(f"   ⚠️ 缺失关键词: {missing_keywords}")
        else:
            print(f"   ❌ 关键词库中没有 {expected_kp}")

def fix_nlp_service():
    """修复NLP服务"""
    print(f"\n🔧 修复NLP服务...")
    
    # 确保数据库连接
    if not neo4j_service.connect():
        print("❌ 无法连接数据库")
        return False
    
    try:
        # 获取数据库中的实际知识点
        db_kps = neo4j_service.search_knowledge_points("")
        print(f"📚 数据库知识点: {[kp['name'] for kp in db_kps]}")
        
        # 更新NLP服务的知识点缓存
        nlp_service.knowledge_points_cache = db_kps
        
        print("✅ NLP服务知识点缓存已更新")
        return True
    finally:
        neo4j_service.close()

def test_complete_suggestion_process():
    """测试完整的建议过程"""
    print(f"\n🎪 测试完整建议过程:")
    
    test_question = "I have already finished my homework."
    question_type = "选择题"
    
    print(f"📝 题目: {test_question}")
    print(f"📋 类型: {question_type}")
    
    try:
        suggestions = nlp_service.suggest_knowledge_points(test_question, question_type)
        
        print(f"\n💡 建议结果 ({len(suggestions)}个):")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"   {i}. {suggestion['knowledge_point_name']}")
            print(f"      置信度: {suggestion['confidence']:.3f}")
            print(f"      匹配关键词: {suggestion.get('matched_keywords', [])}")
            print(f"      理由: {suggestion.get('reason', '无')}")
    
    except Exception as e:
        print(f"❌ 建议过程失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("🐛 NLP关键词匹配调试")
    
    # 调试关键词匹配
    debug_keyword_matching()
    
    # 直接测试匹配
    test_direct_matching()
    
    # 修复NLP服务
    if fix_nlp_service():
        # 测试完整过程
        test_complete_suggestion_process()

if __name__ == "__main__":
    main()
