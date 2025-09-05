#!/usr/bin/env python3
"""
前端API测试脚本
测试所有数据分析相关的API是否正常工作
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_api_endpoint(endpoint, description):
    """测试单个API端点"""
    print(f"\n🔍 测试 {description}")
    print(f"   URL: {endpoint}")
    
    try:
        start_time = time.time()
        response = requests.get(endpoint, timeout=10)
        end_time = time.time()
        
        print(f"   📡 状态码: {response.status_code}")
        print(f"   ⏱️  响应时间: {(end_time - start_time):.3f}s")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ JSON解析成功")
                print(f"   📊 数据键: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                
                # 检查数据结构
                if 'coverage_data' in data:
                    print(f"   📋 覆盖数据: {len(data['coverage_data'])} 个知识点")
                if 'difficulty_distribution' in data:
                    print(f"   📊 难度分布: {len(data['difficulty_distribution'])} 个级别")
                if 'type_distribution' in data:
                    print(f"   📈 类型分布: {len(data['type_distribution'])} 个类型")
                if 'accuracy_analysis' in data:
                    print(f"   🤖 准确率: {data['accuracy_analysis'].get('accuracy_rate', 0)}%")
                
                return True, data
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON解析失败: {e}")
                print(f"   📄 响应内容前100字符: {response.text[:100]}")
                return False, None
        else:
            print(f"   ❌ API调用失败: {response.status_code}")
            print(f"   📄 错误信息: {response.text[:200]}")
            return False, None
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ 请求超时")
        return False, None
    except requests.exceptions.ConnectionError:
        print(f"   🔌 连接错误")
        return False, None
    except Exception as e:
        print(f"   ❌ 未知错误: {e}")
        return False, None

def main():
    """主测试函数"""
    print("🧪 前端数据分析API测试")
    print("=" * 50)
    
    # 检查系统健康状态
    print("🏥 检查系统健康状态...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 系统运行正常")
        else:
            print("❌ 系统状态异常")
            return
    except Exception as e:
        print(f"❌ 无法连接系统: {e}")
        return
    
    # 测试各个API端点
    test_results = {}
    
    api_tests = [
        (f"{API_BASE}/analytics/dashboard-stats", "仪表板统计"),
        (f"{API_BASE}/analytics/coverage", "知识点覆盖分析"),
        (f"{API_BASE}/analytics/difficulty-distribution", "难度分布分析"),
        (f"{API_BASE}/analytics/type-distribution", "类型分布分析"),
        (f"{API_BASE}/analytics/ai-agent-accuracy", "AI Agent准确率分析"),
        (f"{API_BASE}/knowledge/search?keyword=", "知识点搜索"),
    ]
    
    for endpoint, description in api_tests:
        success, data = test_api_endpoint(endpoint, description)
        test_results[description] = {"success": success, "data": data}
    
    # 汇总测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    passed = sum(1 for result in test_results.values() if result["success"])
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result["success"] else "❌ 失败"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 测试通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 所有API测试通过！")
        print("💡 如果前端仍有问题，可能是JavaScript代码逻辑问题")
    else:
        print("⚠️  部分API测试失败，需要检查后端服务")
    
    # 提供调试建议
    print("\n🔧 调试建议:")
    print("1. 访问 http://localhost:8000/debug 查看详细API测试")
    print("2. 打开浏览器开发者工具查看Console错误")
    print("3. 检查Network标签页查看API请求状态")

if __name__ == "__main__":
    main()
