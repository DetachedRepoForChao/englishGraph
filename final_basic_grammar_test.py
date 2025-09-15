#!/usr/bin/env python3
"""
最终基础语法测试
验证所有基础语法题目的识别功能
"""
import requests
import time

API_BASE = "https://english-knowledge-graph-5s6qq3y2c-chao-wangs-projects-dfded257.vercel.app"

def test_basic_grammar():
    """测试基础语法识别"""
    
    print("🧪 基础语法识别测试")
    print("=" * 60)
    
    test_cases = [
        {
            "name": "介词识别",
            "content": "The cat is sitting ___ the table. A. in B. on C. at D. under",
            "expected": "介词",
            "description": "地点介词填空"
        },
        {
            "name": "冠词识别", 
            "content": "I saw ___ elephant at the zoo. A. a B. an C. the D. Ø",
            "expected": "冠词",
            "description": "不定冠词a/an选择"
        },
        {
            "name": "代词识别",
            "content": "Tom and Jerry are friends. ___ play together. A. He B. They C. It D. She", 
            "expected": "代词",
            "description": "人称代词指代"
        },
        {
            "name": "连词识别",
            "content": "I like apples ___ oranges. A. and B. but C. because D. or",
            "expected": "连词", 
            "description": "并列连词选择"
        }
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 测试 {i}: {test_case['name']}")
        print(f"   📝 描述: {test_case['description']}")
        print(f"   📄 题目: {test_case['content'][:50]}...")
        
        try:
            response = requests.post(
                f"{API_BASE}/api/annotation/suggest",
                json={
                    "question_content": test_case["content"],
                    "question_type": "选择题"
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                suggestions = data.get('suggestions', [])
                
                if suggestions:
                    top_suggestion = suggestions[0]
                    name = top_suggestion['knowledge_point_name']
                    confidence = top_suggestion['confidence']
                    
                    print(f"   📊 结果: {name} (置信度: {confidence:.3f})")
                    
                    if name == test_case['expected']:
                        print(f"   ✅ 识别正确")
                        success_count += 1
                    else:
                        print(f"   ⚠️ 识别错误 (期望: {test_case['expected']})")
                        # 显示前3个建议
                        print(f"   💡 所有建议:")
                        for j, sugg in enumerate(suggestions[:3], 1):
                            print(f"      {j}. {sugg['knowledge_point_name']} ({sugg['confidence']:.3f})")
                else:
                    print(f"   ❌ 无识别结果")
                    
            else:
                print(f"   ❌ API请求失败 (状态码: {response.status_code})")
                print(f"      响应: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
        
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {success_count}/{total_count} 通过")
    
    if success_count == total_count:
        print("🎉 所有基础语法识别完全正常！")
    elif success_count >= total_count * 0.75:
        print("✅ 大部分基础语法识别正常")
    else:
        print("⚠️ 基础语法识别需要进一步优化")
    
    return success_count >= total_count * 0.75

def test_advanced_grammar():
    """测试高级语法识别"""
    
    print("\n🧪 高级语法识别验证")
    print("=" * 60)
    
    advanced_cases = [
        {
            "content": "You must finish your homework before going out.",
            "expected": "情态动词"
        },
        {
            "content": "Never have I seen such a beautiful sunset.",
            "expected": "倒装句"
        },
        {
            "content": "Look! The children are playing in the playground.",
            "expected": "现在进行时"
        }
    ]
    
    success_count = 0
    
    for i, test_case in enumerate(advanced_cases, 1):
        print(f"\n🧪 验证 {i}: {test_case['content'][:40]}...")
        
        try:
            response = requests.post(
                f"{API_BASE}/api/annotation/suggest",
                json={
                    "question_content": test_case["content"],
                    "question_type": "选择题"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                suggestions = response.json().get('suggestions', [])
                if suggestions and suggestions[0]['knowledge_point_name'] == test_case['expected']:
                    print(f"   ✅ {test_case['expected']} (置信度: {suggestions[0]['confidence']:.3f})")
                    success_count += 1
                else:
                    print(f"   ⚠️ 识别异常")
            else:
                print(f"   ❌ 请求失败")
                
        except Exception as e:
            print(f"   ❌ 异常: {e}")
        
        time.sleep(1)
    
    print(f"\n📊 高级语法验证: {success_count}/{len(advanced_cases)} 通过")
    return success_count >= len(advanced_cases) * 0.8

def main():
    """主函数"""
    
    print("🚀 K12英语知识图谱 - 语法识别功能测试")
    print("=" * 60)
    print(f"🔗 API地址: {API_BASE}")
    print(f"⏰ 测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 测试基础语法
    basic_success = test_basic_grammar()
    
    # 测试高级语法
    advanced_success = test_advanced_grammar()
    
    print("\n" + "=" * 60)
    print("🎯 最终测试总结:")
    print(f"   📚 基础语法: {'✅ 正常' if basic_success else '⚠️ 需优化'}")
    print(f"   🎓 高级语法: {'✅ 正常' if advanced_success else '⚠️ 需优化'}")
    
    if basic_success and advanced_success:
        print("\n🎊 恭喜！所有语法识别功能完全正常！")
        print("\n📱 您现在可以访问:")
        print(f"   {API_BASE}")
        print("   查看完整的知识图谱系统")
    else:
        print("\n💡 部分功能需要进一步优化")

if __name__ == "__main__":
    main()
