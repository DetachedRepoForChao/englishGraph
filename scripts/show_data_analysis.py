#!/usr/bin/env python3
"""
数据分析展示脚本
展示所有题目、AI Agent准确率分析等详细信息
"""
import requests
import json
import sys
from typing import Dict, Any, List

# API配置
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_header(title: str):
    """打印标题头"""
    print("\n" + "="*80)
    print(f"📊 {title}")
    print("="*80)

def print_section(title: str):
    """打印章节标题"""
    print(f"\n🔍 {title}")
    print("-" * 60)

def format_percentage(value: float) -> str:
    """格式化百分比"""
    return f"{value:.1f}%"

def get_system_overview():
    """获取系统概览"""
    print_header("K12英语知识图谱系统 - 数据分析报告")
    
    try:
        # 获取基础统计
        response = requests.get(f"{API_BASE}/analytics/dashboard-stats")
        if response.status_code == 200:
            stats = response.json()
            
            print_section("系统基础统计")
            print(f"📚 知识点总数: {stats.get('total_knowledge_points', 0)}")
            print(f"📝 题目总数: {stats.get('total_questions', 0)}")
            print(f"🏷️  已标注题目: {stats.get('annotated_questions', 0)}")
            print(f"📈 标注覆盖率: {format_percentage(stats.get('annotation_coverage', 0))}")
        else:
            print("❌ 无法获取系统统计信息")
    except Exception as e:
        print(f"❌ 获取系统概览失败: {e}")

def show_knowledge_points_analysis():
    """显示知识点分析"""
    print_section("知识点覆盖分析")
    
    try:
        response = requests.get(f"{API_BASE}/analytics/coverage")
        if response.status_code == 200:
            data = response.json()
            coverage_data = data.get('coverage_data', [])
            summary = data.get('summary', {})
            
            print(f"📊 覆盖率概览:")
            print(f"   总知识点数: {summary.get('total_knowledge_points', 0)}")
            print(f"   已覆盖知识点: {summary.get('covered_knowledge_points', 0)}")
            print(f"   覆盖率: {format_percentage(summary.get('coverage_rate', 0))}")
            print(f"   平均每知识点题目数: {summary.get('average_questions_per_kp', 0):.1f}")
            
            print(f"\n📋 各知识点详情:")
            print(f"{'知识点名称':<20} {'学段':<12} {'难度':<8} {'题目数':<8}")
            print("-" * 60)
            
            for kp in sorted(coverage_data, key=lambda x: x.get('question_count', 0), reverse=True):
                name = kp.get('knowledge_point', '未知')[:18]
                level = (kp.get('level', '未设置') or '未设置')[:10]
                difficulty = (kp.get('difficulty', '未设置') or '未设置')[:6]
                count = kp.get('question_count', 0)
                
                print(f"{name:<20} {level:<12} {difficulty:<8} {count:<8}")
        else:
            print("❌ 无法获取知识点覆盖数据")
    except Exception as e:
        print(f"❌ 知识点分析失败: {e}")

def show_ai_agent_accuracy():
    """显示AI Agent准确率分析"""
    print_section("AI Agent模型准确率分析")
    
    try:
        response = requests.get(f"{API_BASE}/analytics/ai-agent-accuracy")
        if response.status_code == 200:
            data = response.json()
            
            accuracy_analysis = data.get('accuracy_analysis', {})
            
            print(f"🤖 AI Agent性能指标:")
            print(f"   总标注题目数: {data.get('total_annotated', 0)}")
            print(f"   未标注题目数: {data.get('unannotated_count', 0)}")
            print(f"   标注覆盖率: {format_percentage(data.get('coverage_rate', 0))}")
            print(f"   标注准确率: {format_percentage(accuracy_analysis.get('accuracy_rate', 0))}")
            print(f"   正确标注数: {accuracy_analysis.get('correct_annotations', 0)}")
            print(f"   总标注数: {accuracy_analysis.get('total_annotations', 0)}")
            
            # 显示准确率详情
            details = accuracy_analysis.get('details', [])
            if details:
                print(f"\n📋 标注准确性详情:")
                print(f"{'题目内容':<35} {'标注知识点':<20} {'预期知识点':<20} {'准确性'}")
                print("-" * 95)
                
                for detail in details[:10]:  # 只显示前10个
                    content = detail['content'][:32]
                    annotated = ', '.join(detail['annotated_kps'])[:18]
                    expected = ', '.join(detail['expected_kps'])[:18]
                    accuracy = "✅ 正确" if detail['is_accurate'] else "❌ 错误"
                    
                    print(f"{content:<35} {annotated:<20} {expected:<20} {accuracy}")
                
                if len(details) > 10:
                    print(f"... 还有 {len(details) - 10} 个题目")
        else:
            print("❌ 无法获取AI Agent准确率数据")
    except Exception as e:
        print(f"❌ AI Agent准确率分析失败: {e}")

def show_all_questions():
    """显示所有题目"""
    print_section("所有题目列表")
    
    try:
        # 获取所有知识点
        kp_response = requests.get(f"{API_BASE}/knowledge/search?keyword=")
        if kp_response.status_code != 200:
            print("❌ 无法获取知识点列表")
            return
            
        kp_data = kp_response.json()
        all_questions = {}
        
        # 从每个知识点获取关联的题目
        for kp in kp_data.get('results', []):
            try:
                response = requests.get(f"{API_BASE}/questions/by-knowledge/{kp['name']}")
                if response.status_code == 200:
                    data = response.json()
                    for item in data.get('questions', []):
                        question = item['question']
                        q_id = question['id']
                        
                        if q_id not in all_questions:
                            all_questions[q_id] = {
                                **question,
                                'knowledge_points': []
                            }
                        
                        all_questions[q_id]['knowledge_points'].append({
                            'name': kp['name'],
                            'weight': item['weight']
                        })
            except Exception as e:
                print(f"⚠️ 获取知识点 {kp['name']} 的题目失败: {e}")
        
        # 显示题目列表
        questions_list = list(all_questions.values())
        questions_list.sort(key=lambda x: x.get('id', ''))
        
        print(f"📝 共找到 {len(questions_list)} 道题目:")
        print()
        
        # 按类型统计
        type_stats = {}
        difficulty_stats = {}
        
        for i, question in enumerate(questions_list, 1):
            q_type = question.get('question_type', '未知')
            difficulty = question.get('difficulty', '未设置')
            
            type_stats[q_type] = type_stats.get(q_type, 0) + 1
            difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
            
            content = question.get('content', '')[:50]
            answer = question.get('answer', '')[:10]
            kps = [kp['name'] for kp in question.get('knowledge_points', [])]
            kp_str = ', '.join(kps) if kps else '未标注'
            
            print(f"{i:2d}. {content:<52} | {q_type:<8} | {difficulty:<8} | {answer:<12} | {kp_str}")
        
        # 显示统计信息
        print(f"\n📊 题目类型统计:")
        for q_type, count in sorted(type_stats.items()):
            percentage = (count / len(questions_list) * 100) if questions_list else 0
            print(f"   {q_type}: {count} 道 ({percentage:.1f}%)")
        
        print(f"\n📊 难度分布统计:")
        for difficulty, count in sorted(difficulty_stats.items()):
            percentage = (count / len(questions_list) * 100) if questions_list else 0
            print(f"   {difficulty}: {count} 道 ({percentage:.1f}%)")
            
    except Exception as e:
        print(f"❌ 获取题目列表失败: {e}")

def show_detailed_accuracy_analysis():
    """显示详细的准确率分析"""
    print_section("AI Agent详细准确率分析")
    
    try:
        response = requests.get(f"{API_BASE}/analytics/ai-agent-accuracy")
        if response.status_code == 200:
            data = response.json()
            accuracy_analysis = data.get('accuracy_analysis', {})
            details = accuracy_analysis.get('details', [])
            
            print(f"🎯 准确率统计:")
            print(f"   整体准确率: {format_percentage(accuracy_analysis.get('accuracy_rate', 0))}")
            print(f"   正确标注数: {accuracy_analysis.get('correct_annotations', 0)}")
            print(f"   总标注数: {accuracy_analysis.get('total_annotations', 0)}")
            
            if details:
                print(f"\n📋 标注准确性详细分析:")
                
                correct_count = 0
                incorrect_count = 0
                
                for detail in details:
                    is_accurate = detail.get('is_accurate', False)
                    if is_accurate:
                        correct_count += 1
                    else:
                        incorrect_count += 1
                    
                    status = "✅ 正确" if is_accurate else "❌ 错误"
                    content = detail.get('content', '')[:40]
                    annotated = ', '.join(detail.get('annotated_kps', []))[:20]
                    expected = ', '.join(detail.get('expected_kps', []))[:20]
                    matches = ', '.join(detail.get('matches', []))[:15]
                    
                    print(f"   {status} | {content:<42} | 标注: {annotated:<22} | 预期: {expected:<22} | 匹配: {matches}")
                
                print(f"\n📈 准确性汇总:")
                print(f"   ✅ 正确标注: {correct_count} 题")
                print(f"   ❌ 错误标注: {incorrect_count} 题")
                print(f"   🎯 准确率: {format_percentage(correct_count / len(details) * 100) if details else '0%'}")
        else:
            print("❌ 无法获取AI Agent准确率数据")
    except Exception as e:
        print(f"❌ 详细准确率分析失败: {e}")

def show_model_performance_recommendations():
    """显示模型性能改进建议"""
    print_section("AI Agent性能改进建议")
    
    try:
        # 获取准确率数据
        response = requests.get(f"{API_BASE}/analytics/ai-agent-accuracy")
        if response.status_code == 200:
            data = response.json()
            accuracy_rate = data.get('accuracy_analysis', {}).get('accuracy_rate', 0)
            coverage_rate = data.get('coverage_rate', 0)
            
            print("💡 性能评估:")
            if accuracy_rate >= 80:
                print("   🎉 准确率优秀 (≥80%)")
            elif accuracy_rate >= 60:
                print("   👍 准确率良好 (60-80%)")
            elif accuracy_rate >= 40:
                print("   ⚠️  准确率一般 (40-60%)")
            else:
                print("   ❌ 准确率较低 (<40%)")
            
            if coverage_rate >= 80:
                print("   🎉 覆盖率优秀 (≥80%)")
            elif coverage_rate >= 60:
                print("   👍 覆盖率良好 (60-80%)")
            else:
                print("   ⚠️  覆盖率需要提升")
            
            print("\n🔧 改进建议:")
            
            if accuracy_rate < 70:
                print("   1. 扩充关键词库 - 为每个知识点添加更多相关关键词")
                print("   2. 优化决策算法 - 调整各因子的权重")
                print("   3. 增加训练数据 - 收集更多已标注的高质量题目")
            
            if coverage_rate < 70:
                print("   4. 降低置信度阈值 - 让AI Agent更积极地进行标注")
                print("   5. 增加知识点数量 - 建立更完整的知识点体系")
            
            print("   6. 引入更先进的NLP模型 - 如BERT、GPT等")
            print("   7. 实现用户反馈学习机制 - 基于专家标注持续改进")
            
        else:
            print("❌ 无法获取性能数据")
    except Exception as e:
        print(f"❌ 性能分析失败: {e}")

def main():
    """主函数"""
    # 检查系统连接
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ 系统未正常运行，请先启动系统 (python run.py)")
            return
    except Exception:
        print("❌ 无法连接到系统，请确保系统已启动")
        return
    
    print("✅ 系统连接正常")
    
    # 执行各项分析
    get_system_overview()
    show_knowledge_points_analysis()
    show_ai_agent_accuracy()
    show_all_questions()
    show_detailed_accuracy_analysis()
    show_model_performance_recommendations()
    
    print_header("数据分析报告完成")
    print("💻 您可以访问 Web界面查看可视化数据:")
    print("   🌐 主界面: http://localhost:8000")
    print("   📊 数据分析: http://localhost:8000 (点击'数据分析'标签)")
    print("   📖 API文档: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
