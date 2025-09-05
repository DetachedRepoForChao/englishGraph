#!/usr/bin/env python3
"""
测试前端显示问题
"""

import requests
import json

def test_api_response():
    """测试API响应"""
    url = "http://localhost:8000/api/annotation/suggest"
    
    test_cases = [
        {
            "question_content": "I have already finished my homework.",
            "question_type": "选择题"
        },
        {
            "question_content": "She goes to school every day.",
            "question_type": "选择题"
        },
        {
            "question_content": "The letter was written by Tom yesterday.",
            "question_type": "选择题"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"🧪 测试案例 {i}: {test_case['question_content']}")
        print('='*50)
        
        try:
            response = requests.post(url, json=test_case)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ API调用成功")
            print(f"📊 返回建议数量: {len(data['suggestions'])}")
            
            for j, suggestion in enumerate(data['suggestions'], 1):
                print(f"\n{j}. {suggestion['knowledge_point_name']}")
                print(f"   置信度: {suggestion['confidence']:.3f} ({suggestion['confidence']*100:.1f}%)")
                print(f"   匹配关键词: {suggestion['matched_keywords']}")
                print(f"   理由: {suggestion['reason']}")
                
        except Exception as e:
            print(f"❌ API调用失败: {e}")

def test_frontend_display():
    """测试前端显示逻辑"""
    print(f"\n{'='*50}")
    print("🎨 测试前端显示逻辑")
    print('='*50)
    
    # 模拟前端JavaScript的displayKnowledgeSuggestions函数
    suggestions = [
        {
            "knowledge_point_id": "kp_573225",
            "knowledge_point_name": "动词时态",
            "confidence": 0.16,
            "reason": "题目类型匹配",
            "matched_keywords": []
        },
        {
            "knowledge_point_id": "kp_441152",
            "knowledge_point_name": "现在完成时",
            "confidence": 0.149,
            "reason": "匹配关键词: already, have, finished",
            "matched_keywords": ["already", "have", "finished"]
        }
    ]
    
    print("模拟前端显示结果:")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion['knowledge_point_name']}")
        print(f"   置信度: {(suggestion['confidence'] * 100):.0f}%")
        print(f"   匹配关键词: {suggestion['matched_keywords']}")
        print(f"   理由: {suggestion['reason']}")
        
        # 模拟前端HTML生成
        if suggestion['matched_keywords'] and len(suggestion['matched_keywords']) > 0:
            keywords_html = f"匹配关键词: {', '.join(suggestion['matched_keywords'])}"
            print(f"   HTML显示: {keywords_html}")

if __name__ == "__main__":
    print("🔧 前端显示问题诊断工具")
    test_api_response()
    test_frontend_display()
    print(f"\n{'='*50}")
    print("✅ 诊断完成")
    print("💡 如果API返回正确但前端显示错误，可能是:")
    print("   1. 浏览器缓存问题 - 请强制刷新 (Ctrl+F5)")
    print("   2. JavaScript错误 - 请检查浏览器控制台")
    print("   3. 前端代码问题 - 请检查app.js")
    print('='*50)
