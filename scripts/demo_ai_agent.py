#!/usr/bin/env python3
"""
AI Agent功能演示脚本
展示AI Agent自动标注的完整流程
"""
import asyncio
import json
import requests
import time
from typing import List, Dict, Any

# API基础配置
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_separator(title: str):
    """打印分隔线和标题"""
    print("\n" + "="*60)
    print(f"🤖 {title}")
    print("="*60)

def print_json(data: Any, title: str = ""):
    """格式化打印JSON数据"""
    if title:
        print(f"\n📊 {title}:")
    print(json.dumps(data, ensure_ascii=False, indent=2))

def test_ai_agent_single_annotation():
    """测试单个题目自动标注"""
    print_separator("AI Agent单个题目自动标注演示")
    
    # 测试题目
    test_questions = [
        {
            "content": "I have already finished my homework.",
            "question_type": "选择题",
            "answer": "already",
            "expected_knowledge": "现在完成时"
        },
        {
            "content": "The book which is on the table belongs to me.",
            "question_type": "选择题", 
            "answer": "which",
            "expected_knowledge": "定语从句"
        },
        {
            "content": "The windows were cleaned by the students yesterday.",
            "question_type": "选择题",
            "answer": "were cleaned",
            "expected_knowledge": "被动语态"
        },
        {
            "content": "This apple is sweeter than that one.",
            "question_type": "选择题",
            "answer": "sweeter", 
            "expected_knowledge": "比较级和最高级"
        }
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 测试题目 {i}: {question['content'][:50]}...")
        print(f"   预期知识点: {question['expected_knowledge']}")
        
        try:
            response = requests.post(
                f"{API_BASE}/ai-agent/auto-annotate",
                json={"question": question},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                suggestions = result.get("suggestions", [])
                auto_annotations = result.get("auto_annotations", [])
                applied_annotations = result.get("applied_annotations", [])
                
                print(f"   💡 AI推荐了 {len(suggestions)} 个知识点:")
                for j, suggestion in enumerate(suggestions[:3], 1):
                    print(f"      {j}. {suggestion['knowledge_point_name']} "
                          f"(置信度: {suggestion['confidence']:.3f})")
                
                print(f"   🎯 自动标注数: {len(auto_annotations)}")
                print(f"   ✅ 自动应用数: {len(applied_annotations)}")
                
                # 检查是否识别了预期的知识点
                found_expected = any(
                    question['expected_knowledge'] in s['knowledge_point_name'] 
                    for s in suggestions
                )
                
                if found_expected:
                    print(f"   ✅ 成功识别预期知识点: {question['expected_knowledge']}")
                else:
                    print(f"   ❌ 未识别预期知识点: {question['expected_knowledge']}")
                    
            else:
                print(f"   ❌ API调用失败: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
        
        time.sleep(0.5)  # 避免请求过快

def test_batch_import():
    """测试批量导入功能"""
    print_separator("AI Agent批量导入演示")
    
    # 创建测试题目
    batch_questions = [
        {
            "content": "If it rains tomorrow, we will stay at home.",
            "question_type": "选择题",
            "answer": "rains",
            "analysis": "if引导的条件句，从句用一般现在时",
            "difficulty": "hard"
        },
        {
            "content": "Could you tell me where the library is?",
            "question_type": "选择题", 
            "answer": "where",
            "analysis": "宾语从句询问地点，用where引导",
            "difficulty": "medium"
        },
        {
            "content": "She is more beautiful than her sister.",
            "question_type": "选择题",
            "answer": "more beautiful",
            "analysis": "多音节形容词用more构成比较级",
            "difficulty": "medium"
        }
    ]
    
    print(f"📥 准备批量导入 {len(batch_questions)} 道题目...")
    
    try:
        response = requests.post(
            f"{API_BASE}/ai-agent/smart-import",
            json=batch_questions,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 批量导入成功!")
            print(f"   📊 导入题目数: {result.get('imported_count', 0)}")
            print(f"   🎯 标注结果数: {len(result.get('annotation_results', []))}")
            
            # 分析标注结果
            annotation_results = result.get('annotation_results', [])
            success_count = sum(1 for r in annotation_results if r.get('status') == 'completed')
            
            print(f"   ✅ 成功标注: {success_count}/{len(annotation_results)}")
            
            # 显示前几个结果的详情
            for i, ann_result in enumerate(annotation_results[:2], 1):
                suggestions = ann_result.get('suggestions', [])
                print(f"\n   📝 题目 {i} 的标注结果:")
                for j, suggestion in enumerate(suggestions[:2], 1):
                    print(f"      {j}. {suggestion['knowledge_point_name']} "
                          f"(置信度: {suggestion['confidence']:.3f})")
        else:
            print(f"❌ 批量导入失败: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ 批量导入测试失败: {e}")

def test_ai_agent_config():
    """测试AI Agent配置功能"""
    print_separator("AI Agent配置演示")
    
    try:
        # 获取当前配置
        response = requests.get(f"{API_BASE}/ai-agent/config")
        if response.status_code == 200:
            current_config = response.json()
            print_json(current_config, "当前AI Agent配置")
        
        # 更新配置
        new_config = {
            "confidence_threshold": 0.15,  # 更低的阈值
            "max_auto_annotations": 4,
            "learning_enabled": True
        }
        
        print(f"\n🔧 更新AI Agent配置...")
        response = requests.put(
            f"{API_BASE}/ai-agent/config",
            json=new_config
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 配置更新成功!")
            print_json(result.get('new_config', {}), "新配置")
        else:
            print(f"❌ 配置更新失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")

def show_system_stats():
    """显示系统统计信息"""
    print_separator("系统统计信息")
    
    try:
        response = requests.get(f"{API_BASE}/analytics/dashboard-stats")
        if response.status_code == 200:
            stats = response.json()
            
            print("📊 系统概览:")
            print(f"   🧠 知识点总数: {stats.get('total_knowledge_points', 0)}")
            print(f"   📝 题目总数: {stats.get('total_questions', 0)}")
            print(f"   🏷️  已标注题目: {stats.get('annotated_questions', 0)}")
            print(f"   📈 标注覆盖率: {stats.get('annotation_coverage', 0)}%")
            
        # 获取知识点覆盖分析
        response = requests.get(f"{API_BASE}/analytics/coverage")
        if response.status_code == 200:
            coverage = response.json()
            
            print(f"\n📋 知识点覆盖详情:")
            coverage_data = coverage.get('coverage_data', [])[:5]  # 只显示前5个
            
            for kp in coverage_data:
                name = kp.get('knowledge_point', '未知')
                count = kp.get('question_count', 0)
                level = kp.get('level', '未设置')
                print(f"   • {name} ({level}): {count} 道题目")
                
    except Exception as e:
        print(f"❌ 统计信息获取失败: {e}")

def main():
    """主演示函数"""
    print("🚀 K12英语知识图谱系统 AI Agent 功能演示")
    print("=" * 60)
    
    # 检查系统状态
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ 系统未正常运行，请先启动系统")
            return
    except Exception:
        print("❌ 无法连接到系统，请确保系统已启动 (python run.py)")
        return
    
    print("✅ 系统连接正常")
    
    # 运行各项演示
    show_system_stats()
    test_ai_agent_config()
    test_ai_agent_single_annotation()
    test_batch_import()
    
    # 最终统计
    print_separator("演示完成")
    show_system_stats()
    
    print("\n🎉 AI Agent功能演示完成!")
    print("💡 您可以访问 http://localhost:8000 查看Web界面")
    print("📚 API文档: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
