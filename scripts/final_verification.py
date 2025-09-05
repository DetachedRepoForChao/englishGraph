#!/usr/bin/env python3
"""
最终验证脚本
验证所有功能是否正常工作，包括数据分析显示
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_header(title):
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def verify_system_health():
    """验证系统健康状态"""
    print("🏥 验证系统健康状态...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ 系统状态: {health_data.get('status', 'unknown')}")
            print(f"📝 消息: {health_data.get('message', 'no message')}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def verify_web_pages():
    """验证网页是否可访问"""
    print("\n🌐 验证网页访问...")
    
    pages = [
        (f"{BASE_URL}/", "主页面"),
        (f"{BASE_URL}/analytics-test", "数据分析测试页"),
        (f"{BASE_URL}/debug", "调试页面"),
        (f"{BASE_URL}/docs", "API文档")
    ]
    
    for url, name in pages:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name}: 可访问")
            else:
                print(f"❌ {name}: 状态码 {response.status_code}")
        except Exception as e:
            print(f"❌ {name}: 访问失败 - {e}")

def verify_data_analysis_apis():
    """验证数据分析API"""
    print("\n📊 验证数据分析API...")
    
    api_tests = [
        (f"{API_BASE}/analytics/dashboard-stats", "仪表板统计"),
        (f"{API_BASE}/analytics/coverage", "知识点覆盖"),
        (f"{API_BASE}/analytics/difficulty-distribution", "难度分布"),
        (f"{API_BASE}/analytics/type-distribution", "类型分布"),
        (f"{API_BASE}/analytics/ai-agent-accuracy", "AI准确率"),
    ]
    
    all_passed = True
    
    for endpoint, name in api_tests:
        try:
            response = requests.get(endpoint, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {name}: API正常")
                
                # 验证数据结构
                if 'coverage_data' in data:
                    count = len(data['coverage_data'])
                    print(f"   📋 包含 {count} 个知识点数据")
                elif 'difficulty_distribution' in data:
                    count = len(data['difficulty_distribution'])
                    print(f"   📊 包含 {count} 个难度级别")
                elif 'type_distribution' in data:
                    count = len(data['type_distribution'])
                    print(f"   📈 包含 {count} 个题目类型")
                elif 'accuracy_analysis' in data:
                    rate = data['accuracy_analysis'].get('accuracy_rate', 0)
                    print(f"   🤖 AI准确率: {rate}%")
                else:
                    print(f"   📊 数据键: {list(data.keys())}")
            else:
                print(f"❌ {name}: 状态码 {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ {name}: 异常 - {e}")
            all_passed = False
    
    return all_passed

def verify_ai_agent_functionality():
    """验证AI Agent功能"""
    print("\n🤖 验证AI Agent功能...")
    
    test_question = {
        "content": "She has already finished her homework.",
        "question_type": "选择题",
        "answer": "already"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/ai-agent/auto-annotate",
            json={"question": test_question},
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            suggestions = result.get("suggestions", [])
            
            print(f"✅ AI Agent自动标注正常")
            print(f"📝 测试题目: {test_question['content'][:40]}...")
            print(f"💡 推荐数量: {len(suggestions)}")
            
            if suggestions:
                top_suggestion = suggestions[0]
                print(f"🏆 最佳推荐: {top_suggestion['knowledge_point_name']}")
                print(f"🎯 置信度: {top_suggestion['confidence']:.3f}")
            
            return True
        else:
            print(f"❌ AI Agent测试失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI Agent测试异常: {e}")
        return False

def generate_final_status_report():
    """生成最终状态报告"""
    print_header("最终系统状态报告")
    
    try:
        # 获取系统统计
        stats_response = requests.get(f"{API_BASE}/analytics/dashboard-stats")
        coverage_response = requests.get(f"{API_BASE}/analytics/coverage")
        accuracy_response = requests.get(f"{API_BASE}/analytics/ai-agent-accuracy")
        
        if all(r.status_code == 200 for r in [stats_response, coverage_response, accuracy_response]):
            stats = stats_response.json()
            coverage = coverage_response.json()
            accuracy = accuracy_response.json()
            
            print("📊 系统数据统计:")
            print(f"   🧠 知识点总数: {stats.get('total_knowledge_points', 0)}")
            print(f"   📝 题目总数: {stats.get('total_questions', 0)}")
            print(f"   🏷️  已标注题目: {stats.get('annotated_questions', 0)}")
            print(f"   📈 标注覆盖率: {stats.get('annotation_coverage', 0)}%")
            
            print(f"\n🤖 AI Agent性能:")
            ai_accuracy = accuracy.get('accuracy_analysis', {})
            print(f"   🎯 标注准确率: {ai_accuracy.get('accuracy_rate', 0)}%")
            print(f"   ✅ 正确标注: {ai_accuracy.get('correct_annotations', 0)}")
            print(f"   📊 总标注数: {ai_accuracy.get('total_annotations', 0)}")
            
            print(f"\n📋 知识点覆盖:")
            coverage_data = coverage.get('coverage_data', [])
            covered_kps = [kp for kp in coverage_data if kp.get('question_count', 0) > 0]
            uncovered_kps = [kp for kp in coverage_data if kp.get('question_count', 0) == 0]
            
            print(f"   ✅ 已覆盖: {len(covered_kps)} 个知识点")
            for kp in covered_kps[:5]:  # 显示前5个
                print(f"      • {kp['knowledge_point']}: {kp['question_count']} 题")
            
            print(f"   ❌ 未覆盖: {len(uncovered_kps)} 个知识点")
            for kp in uncovered_kps[:5]:  # 显示前5个
                print(f"      • {kp['knowledge_point']}: 0 题")
        else:
            print("❌ 无法获取完整统计数据")
    except Exception as e:
        print(f"❌ 生成状态报告失败: {e}")

def main():
    """主验证函数"""
    print("🚀 K12英语知识图谱系统 - 最终功能验证")
    print(f"⏰ 验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 执行各项验证
    health_ok = verify_system_health()
    
    if not health_ok:
        print("❌ 系统健康检查失败，终止验证")
        return
    
    verify_web_pages()
    api_ok = verify_data_analysis_apis()
    ai_ok = verify_ai_agent_functionality()
    
    # 生成最终报告
    generate_final_status_report()
    
    # 总结
    print_header("验证结果总结")
    
    if health_ok and api_ok and ai_ok:
        print("🎉 所有功能验证通过！")
        print("\n🌐 系统访问指南:")
        print(f"   主界面: {BASE_URL}")
        print(f"   数据分析: {BASE_URL}/analytics-test")
        print(f"   调试页面: {BASE_URL}/debug")
        print(f"   API文档: {BASE_URL}/docs")
        
        print("\n💡 使用建议:")
        print("1. 在主界面点击'数据分析'标签页查看分析结果")
        print("2. 如果数据分析页面空白，点击'刷新数据'或'加载数据分析'按钮")
        print("3. 使用F12开发者工具查看Console日志排查问题")
        print("4. 访问调试页面查看详细的API测试结果")
    else:
        print("⚠️  部分功能验证失败，需要进一步检查")
        print("🔧 建议:")
        print("1. 检查系统日志查看错误信息")
        print("2. 重启系统: kill -9 $(lsof -ti:8000) && python3 run.py")
        print("3. 查看浏览器开发者工具Console错误")

if __name__ == "__main__":
    main()
