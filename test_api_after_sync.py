#!/usr/bin/env python3
"""
同步后的API测试脚本
验证云端数据库同步是否成功
"""
import requests
import json
import time

API_BASE = "https://english-knowledge-graph-2ktxa4o24-chao-wangs-projects-dfded257.vercel.app"

def test_api_functionality():
    """测试API功能"""
    
    print("🧪 开始测试API功能...")
    print("=" * 60)
    
    # 测试用例
    test_cases = [
        {
            "name": "情态动词识别",
            "content": "You must finish your homework before going out.",
            "expected": "情态动词",
            "min_confidence": 0.8
        },
        {
            "name": "倒装句识别",
            "content": "Never have I seen such a beautiful sunset.",
            "expected": "倒装句",
            "min_confidence": 0.8
        },
        {
            "name": "现在进行时识别",
            "content": "Look! The children are playing in the playground.",
            "expected": "现在进行时",
            "min_confidence": 0.5
        },
        {
            "name": "非谓语动词识别",
            "content": "The manager, concerned about his company's performance, held a press conference.",
            "expected": "非谓语动词",
            "min_confidence": 0.4
        }
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 测试 {i}: {test_case['name']}")
        print(f"   📝 输入: {test_case['content'][:50]}...")
        
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
                    
                    # 检查是否符合预期
                    if name == test_case['expected'] and confidence >= test_case['min_confidence']:
                        print(f"   ✅ 测试通过")
                        success_count += 1
                    elif name == test_case['expected']:
                        print(f"   ⚠️  识别正确但置信度偏低 (期望: {test_case['min_confidence']:.1f})")
                        success_count += 0.5
                    else:
                        print(f"   ❌ 识别错误 (期望: {test_case['expected']})")
                        # 显示所有建议
                        print(f"   💡 所有建议:")
                        for j, sugg in enumerate(suggestions[:3], 1):
                            print(f"      {j}. {sugg['knowledge_point_name']} ({sugg['confidence']:.3f})")
                else:
                    print(f"   ❌ 无识别结果")
                    
            else:
                print(f"   ❌ API请求失败 (状态码: {response.status_code})")
                if response.text:
                    print(f"      错误信息: {response.text[:200]}")
                    
        except requests.exceptions.Timeout:
            print(f"   ❌ 请求超时")
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
        
        # 避免请求过快
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {success_count}/{total_count} 通过")
    
    if success_count == total_count:
        print("🎉 所有测试完全通过！")
        return True
    elif success_count >= total_count * 0.8:
        print("✅ 大部分测试通过，系统基本正常")
        return True
    else:
        print("⚠️  测试通过率较低，需要检查数据库同步")
        return False

def test_health_check():
    """测试健康检查"""
    print("🏥 测试系统健康状态...")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 系统状态: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"   ❌ 健康检查失败 (状态码: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ 健康检查异常: {e}")
        return False

def main():
    """主函数"""
    
    print("🚀 云端数据库同步后的功能测试")
    print("=" * 60)
    print(f"🔗 API地址: {API_BASE}")
    print(f"⏰ 测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 健康检查
    if not test_health_check():
        print("❌ 系统健康检查失败，退出测试")
        return
    
    print()
    
    # 功能测试
    if test_api_functionality():
        print("\n🎊 测试完成！系统工作正常")
        print("\n💡 如果某些测试未通过，请：")
        print("   1. 确认已在Neo4j Browser中执行所有Cypher语句")
        print("   2. 等待5-10分钟让缓存刷新")
        print("   3. 重新运行此测试脚本")
    else:
        print("\n⚠️  测试未完全通过，请检查：")
        print("   1. 云端数据库中的知识点是否创建成功")
        print("   2. 层级关系是否建立正确")
        print("   3. Vercel应用是否使用最新代码")

if __name__ == "__main__":
    main()
