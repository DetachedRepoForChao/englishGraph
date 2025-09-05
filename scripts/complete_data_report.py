#!/usr/bin/env python3
"""
完整数据分析报告脚本
生成AI Agent准确率、所有题目列表等完整分析报告
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_header(title):
    print("\n" + "="*80)
    print(f"📊 {title}")
    print("="*80)

def print_section(title):
    print(f"\n🔍 {title}")
    print("-" * 60)

def check_system_health():
    """检查系统健康状态"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 系统运行正常")
            return True
        else:
            print("❌ 系统状态异常")
            return False
    except Exception as e:
        print(f"❌ 无法连接系统: {e}")
        print("💡 请确保系统已启动: python3 run.py")
        return False

def get_ai_agent_accuracy_report():
    """获取AI Agent准确率详细报告"""
    print_header("AI Agent模型准确率详细分析")
    
    try:
        response = requests.get(f"{API_BASE}/analytics/ai-agent-accuracy")
        if response.status_code == 200:
            data = response.json()
            
            # 基础统计
            accuracy_analysis = data.get('accuracy_analysis', {})
            print_section("模型性能指标")
            print(f"🎯 整体准确率: {accuracy_analysis.get('accuracy_rate', 0):.2f}%")
            print(f"✅ 正确标注数: {accuracy_analysis.get('correct_annotations', 0)}")
            print(f"📊 总标注数: {accuracy_analysis.get('total_annotations', 0)}")
            print(f"📈 标注覆盖率: {data.get('coverage_rate', 0):.2f}%")
            print(f"📝 未标注题目: {data.get('unannotated_count', 0)} 道")
            
            # 详细分析
            details = accuracy_analysis.get('details', [])
            if details:
                print_section("标注准确性详细分析")
                print(f"{'序号':<4} {'准确性':<8} {'题目内容':<40} {'AI标注':<20} {'期望标注':<20}")
                print("-" * 100)
                
                for i, detail in enumerate(details, 1):
                    accuracy = "✅ 正确" if detail.get('is_accurate') else "❌ 错误"
                    content = detail.get('content', '')[:38]
                    annotated = ', '.join(detail.get('annotated_kps', []))[:18]
                    expected = ', '.join(detail.get('expected_kps', []))[:18] or '无'
                    
                    print(f"{i:<4} {accuracy:<8} {content:<40} {annotated:<20} {expected:<20}")
                
                # 错误分析
                incorrect_items = [d for d in details if not d.get('is_accurate')]
                if incorrect_items:
                    print_section("错误标注分析")
                    for item in incorrect_items:
                        print(f"❌ 题目: {item.get('content', '')[:50]}")
                        print(f"   AI标注: {', '.join(item.get('annotated_kps', []))}")
                        print(f"   期望标注: {', '.join(item.get('expected_kps', [])) or '无明确期望'}")
                        print(f"   改进建议: 需要为相关知识点添加更多关键词")
                        print()
        else:
            print("❌ 无法获取AI Agent准确率数据")
    except Exception as e:
        print(f"❌ 准确率分析失败: {e}")

def get_all_questions_report():
    """获取所有题目详细报告"""
    print_header("所有题目详细列表")
    
    try:
        # 获取所有知识点
        kp_response = requests.get(f"{API_BASE}/knowledge/search?keyword=")
        if kp_response.status_code != 200:
            print("❌ 无法获取知识点列表")
            return
        
        kp_data = kp_response.json()
        all_questions = {}
        
        print_section("数据收集进度")
        print("📥 正在从各知识点收集题目...")
        
        # 从每个知识点获取题目
        for i, kp in enumerate(kp_data.get('results', []), 1):
            kp_name = kp['name']
            print(f"   {i:2d}. 正在获取 '{kp_name}' 的题目...", end=' ')
            
            try:
                response = requests.get(f"{API_BASE}/questions/by-knowledge/{kp_name}")
                if response.status_code == 200:
                    data = response.json()
                    question_count = len(data.get('questions', []))
                    print(f"✅ {question_count} 道题目")
                    
                    for item in data.get('questions', []):
                        question = item['question']
                        q_id = question['id']
                        
                        if q_id not in all_questions:
                            all_questions[q_id] = {
                                **question,
                                'knowledge_points': []
                            }
                        
                        all_questions[q_id]['knowledge_points'].append({
                            'name': kp_name,
                            'weight': item['weight']
                        })
                else:
                    print(f"❌ 获取失败")
            except Exception as e:
                print(f"❌ 错误: {e}")
        
        # 显示题目列表
        questions_list = list(all_questions.values())
        questions_list.sort(key=lambda x: x.get('id', ''))
        
        print_section(f"题目详细列表 (共 {len(questions_list)} 道)")
        
        if not questions_list:
            print("📝 暂无题目数据")
            return
        
        # 统计信息
        type_stats = {}
        difficulty_stats = {}
        annotated_count = 0
        
        print(f"{'序号':<4} {'题目内容':<45} {'类型':<8} {'难度':<8} {'答案':<15} {'知识点'}")
        print("-" * 120)
        
        for i, question in enumerate(questions_list, 1):
            q_type = question.get('question_type', '未知')
            difficulty = question.get('difficulty', '未设置')
            content = question.get('content', '')[:43]
            answer = question.get('answer', '')[:13]
            
            # 统计
            type_stats[q_type] = type_stats.get(q_type, 0) + 1
            difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
            
            kps = question.get('knowledge_points', [])
            if kps:
                annotated_count += 1
                kp_names = ', '.join([kp['name'] for kp in kps])[:25]
            else:
                kp_names = '未标注'
            
            print(f"{i:<4} {content:<45} {q_type:<8} {difficulty:<8} {answer:<15} {kp_names}")
        
        # 显示统计信息
        print_section("题目统计汇总")
        print(f"📊 总题目数: {len(questions_list)}")
        print(f"🏷️  已标注: {annotated_count} 道 ({annotated_count/len(questions_list)*100:.1f}%)")
        print(f"❌ 未标注: {len(questions_list) - annotated_count} 道")
        
        print(f"\n📋 类型分布:")
        for q_type, count in sorted(type_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = count / len(questions_list) * 100
            print(f"   {q_type}: {count} 道 ({percentage:.1f}%)")
        
        print(f"\n📊 难度分布:")
        for difficulty, count in sorted(difficulty_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = count / len(questions_list) * 100
            print(f"   {difficulty}: {count} 道 ({percentage:.1f}%)")
        
        return questions_list
        
    except Exception as e:
        print(f"❌ 获取题目列表失败: {e}")
        return []

def get_knowledge_points_report():
    """获取知识点详细报告"""
    print_header("知识点详细分析")
    
    try:
        response = requests.get(f"{API_BASE}/analytics/coverage")
        if response.status_code == 200:
            data = response.json()
            coverage_data = data.get('coverage_data', [])
            summary = data.get('summary', {})
            
            print_section("知识点覆盖概览")
            print(f"📚 总知识点数: {summary.get('total_knowledge_points', 0)}")
            print(f"✅ 已覆盖知识点: {summary.get('covered_knowledge_points', 0)}")
            print(f"📈 覆盖率: {summary.get('coverage_rate', 0):.1f}%")
            print(f"📊 平均每知识点题目数: {summary.get('average_questions_per_kp', 0):.1f}")
            
            print_section("各知识点详情")
            print(f"{'知识点名称':<18} {'学段':<12} {'难度':<8} {'题目数':<8} {'状态'}")
            print("-" * 65)
            
            # 按题目数量排序
            sorted_kps = sorted(coverage_data, key=lambda x: x.get('question_count', 0), reverse=True)
            
            for kp in sorted_kps:
                name = kp.get('knowledge_point', '未知')[:16]
                level = (kp.get('level', '未设置') or '未设置')[:10]
                difficulty = (kp.get('difficulty', '未设置') or '未设置')[:6]
                count = kp.get('question_count', 0)
                status = "✅ 已覆盖" if count > 0 else "❌ 未覆盖"
                
                print(f"{name:<18} {level:<12} {difficulty:<8} {count:<8} {status}")
        else:
            print("❌ 无法获取知识点覆盖数据")
    except Exception as e:
        print(f"❌ 知识点分析失败: {e}")

def generate_improvement_suggestions(questions_list):
    """生成改进建议"""
    print_header("AI Agent性能改进建议")
    
    if not questions_list:
        print("❌ 无题目数据，无法生成建议")
        return
    
    annotated_questions = [q for q in questions_list if q.get('knowledge_points')]
    unannotated_questions = [q for q in questions_list if not q.get('knowledge_points')]
    
    coverage_rate = len(annotated_questions) / len(questions_list) * 100
    
    print_section("当前状态评估")
    if coverage_rate >= 80:
        print("🎉 标注覆盖率优秀 (≥80%)")
    elif coverage_rate >= 60:
        print("👍 标注覆盖率良好 (60-80%)")
    elif coverage_rate >= 40:
        print("⚠️  标注覆盖率一般 (40-60%)")
    else:
        print("❌ 标注覆盖率较低 (<40%)")
    
    print_section("具体改进建议")
    
    suggestions = []
    
    if coverage_rate < 70:
        suggestions.append("1. 降低AI Agent置信度阈值，提高自动标注覆盖率")
        suggestions.append("2. 扩充关键词库，提高知识点识别准确性")
    
    if len(unannotated_questions) > 5:
        suggestions.append("3. 为未标注题目手动添加标注，丰富训练数据")
    
    # 分析未标注题目的特点
    if unannotated_questions:
        print(f"\n📋 未标注题目分析 (共 {len(unannotated_questions)} 道):")
        for i, q in enumerate(unannotated_questions[:5], 1):
            content = q.get('content', '')[:50]
            q_type = q.get('question_type', '未知')
            print(f"   {i}. {content}... ({q_type})")
        
        if len(unannotated_questions) > 5:
            print(f"   ... 还有 {len(unannotated_questions) - 5} 道题目")
        
        suggestions.append("4. 分析未标注题目的共同特征，优化识别算法")
    
    suggestions.extend([
        "5. 集成更先进的NLP模型 (如BERT、GPT)",
        "6. 实现用户反馈学习机制",
        "7. 建立更完整的知识点层级体系",
        "8. 增加多语言支持和语义理解能力"
    ])
    
    print("💡 推荐的改进措施:")
    for suggestion in suggestions:
        print(f"   {suggestion}")
    
    print_section("优先级建议")
    print("🥇 高优先级: 扩充关键词库、降低置信度阈值")
    print("🥈 中优先级: 手动标注未覆盖题目、优化算法权重")
    print("🥉 低优先级: 集成先进模型、多语言支持")

def test_specific_questions():
    """测试特定题目的标注效果"""
    print_header("特定题目AI标注测试")
    
    test_cases = [
        {
            "content": "I have already finished my homework.",
            "expected": "现在完成时",
            "description": "现在完成时测试"
        },
        {
            "content": "The book which is on the table belongs to me.",
            "expected": "定语从句",
            "description": "定语从句测试"
        },
        {
            "content": "The letter was written by Tom yesterday.",
            "expected": "被动语态",
            "description": "被动语态测试"
        },
        {
            "content": "This apple is sweeter than that one.",
            "expected": "比较级和最高级",
            "description": "比较级测试"
        },
        {
            "content": "Could you tell me where the library is?",
            "expected": "宾语从句",
            "description": "宾语从句测试"
        }
    ]
    
    print_section("实时AI标注测试")
    correct_predictions = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 测试 {i}: {test_case['description']}")
        print(f"   题目: {test_case['content']}")
        print(f"   期望: {test_case['expected']}")
        
        try:
            response = requests.post(
                f"{API_BASE}/ai-agent/auto-annotate",
                json={
                    "question": {
                        "content": test_case["content"],
                        "question_type": "选择题",
                        "answer": "test"
                    }
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                suggestions = result.get("suggestions", [])
                
                if suggestions:
                    print(f"   💡 AI推荐:")
                    for j, suggestion in enumerate(suggestions[:3], 1):
                        kp_name = suggestion['knowledge_point_name']
                        confidence = suggestion['confidence']
                        print(f"      {j}. {kp_name} (置信度: {confidence:.3f})")
                    
                    # 检查是否正确识别
                    top_suggestion = suggestions[0]['knowledge_point_name']
                    if test_case['expected'] in top_suggestion or any(test_case['expected'] in s['knowledge_point_name'] for s in suggestions[:2]):
                        print(f"   ✅ 正确识别了目标知识点")
                        correct_predictions += 1
                    else:
                        print(f"   ❌ 未正确识别目标知识点")
                else:
                    print(f"   ❌ 无推荐结果")
            else:
                print(f"   ❌ API调用失败: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
    
    accuracy = correct_predictions / len(test_cases) * 100
    print(f"\n🎯 实时测试准确率: {accuracy:.1f}% ({correct_predictions}/{len(test_cases)})")

def generate_comprehensive_report():
    """生成综合报告"""
    print_header("K12英语知识图谱系统 - 综合数据分析报告")
    print(f"📅 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 系统健康检查
    if not check_system_health():
        return
    
    # AI Agent准确率分析
    get_ai_agent_accuracy_report()
    
    # 所有题目报告
    questions_list = get_all_questions_report()
    
    # 知识点分析
    get_knowledge_points_report()
    
    # 特定题目测试
    test_specific_questions()
    
    # 改进建议
    generate_improvement_suggestions(questions_list)
    
    print_header("报告总结")
    print("📊 数据分析报告生成完成")
    print("💻 您可以访问以下链接查看可视化界面:")
    print(f"   🌐 主系统: {BASE_URL}")
    print(f"   📊 数据分析测试页: {BASE_URL}/analytics-test")
    print(f"   📖 API文档: {BASE_URL}/docs")

if __name__ == "__main__":
    try:
        generate_comprehensive_report()
    except KeyboardInterrupt:
        print("\n\n⚠️  报告生成被用户中断")
    except Exception as e:
        print(f"\n❌ 报告生成失败: {e}")
        sys.exit(1)
