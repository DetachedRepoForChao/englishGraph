#!/usr/bin/env python3
"""
测试用户提供的10个题目
验证所有语法识别功能
"""
import requests
import time

API_BASE = "https://english-knowledge-graph-hkxkycm1m-chao-wangs-projects-dfded257.vercel.app"

def test_user_questions():
    """测试用户提供的10个题目"""
    
    print("🧪 用户提供的10个题目识别测试")
    print("=" * 80)
    
    user_questions = [
        {
            "content": "He _____ TV every evening. A. watch B. watches C. watched D. watching",
            "expected": ["一般现在时", "第三人称单数"],
            "description": "第三人称单数/一般现在时"
        },
        {
            "content": "They _____ to the park last Sunday. A. go B. are going C. went D. gone",
            "expected": ["一般过去时"],
            "description": "一般过去时"
        },
        {
            "content": "There _____ three apples on the table. A. is B. are C. was D. be",
            "expected": ["There be句型", "be动词"],
            "description": "There be句型/be动词"
        },
        {
            "content": "Mary is taller _____ Jane. A. then B. than C. as D. like",
            "expected": ["比较级和最高级"],
            "description": "比较级"
        },
        {
            "content": "I have _____ idea about the answer. A. no B. a C. an D. the",
            "expected": ["冠词"],
            "description": "不定冠词"
        },
        {
            "content": "Which word is opposite of \"young\"? A. small B. old C. new D. short",
            "expected": ["词汇"],
            "description": "词汇/反义词"
        },
        {
            "content": "Choose the correct question: _____ your homework? A. Do you finish B. Did you finished C. Have you finished D. Are you finish",
            "expected": ["现在完成时"],
            "description": "现在完成时疑问句"
        },
        {
            "content": "The book is _____ the shelf. A. in B. on C. at D. under",
            "expected": ["介词"],
            "description": "地点介词"
        },
        {
            "content": "If it _____ tomorrow, we will stay at home. A. rain B. rains C. rained D. will rain",
            "expected": ["一般现在时", "条件句", "第三人称单数"],
            "description": "条件句/一般现在时"
        },
        {
            "content": "How many _____ are there? There are five. A. book B. books C. much D. many",
            "expected": ["数量表达"],
            "description": "数量表达/可数名词复数"
        }
    ]
    
    success_count = 0
    total_count = len(user_questions)
    
    for i, test_case in enumerate(user_questions, 1):
        print(f"\n🧪 测试 {i}: {test_case['description']}")
        print(f"   📄 题目: {test_case['content'][:60]}...")
        
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
                    top = suggestions[0]
                    name = top['knowledge_point_name']
                    confidence = top['confidence']
                    
                    print(f"   📊 结果: {name} (置信度: {confidence:.3f})")
                    
                    if name in test_case['expected']:
                        print(f"   ✅ 识别正确")
                        success_count += 1
                    else:
                        print(f"   ⚠️ 识别错误 (期望: {'/'.join(test_case['expected'])})")
                        # 显示前3个建议
                        print(f"   💡 所有建议:")
                        for j, sugg in enumerate(suggestions[:3], 1):
                            print(f"      {j}. {sugg['knowledge_point_name']} ({sugg['confidence']:.3f})")
                else:
                    print(f"   ❌ 无识别结果")
                    
            else:
                print(f"   ❌ API请求失败 (状态码: {response.status_code})")
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
        
        time.sleep(1.5)
    
    print("\n" + "=" * 80)
    print(f"📊 用户题目测试结果: {success_count}/{total_count} 通过")
    
    success_rate = success_count / total_count
    if success_rate >= 0.9:
        print("🎊 优秀！几乎所有题目都能正确识别！")
    elif success_rate >= 0.8:
        print("🎉 很好！大部分题目都能正确识别！")
    elif success_rate >= 0.7:
        print("✅ 良好！多数题目都能正确识别！")
    else:
        print("⚠️ 需要进一步优化识别算法")
    
    return success_count

def main():
    """主函数"""
    
    print("🚀 K12英语知识图谱 - 用户题目识别测试")
    print("=" * 80)
    print(f"🔗 API地址: {API_BASE}")
    print(f"⏰ 测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 健康检查
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            print("✅ 系统健康检查通过")
        else:
            print("⚠️ 系统健康检查异常")
    except:
        print("❌ 系统健康检查失败")
    
    # 测试用户题目
    success_count = test_user_questions()
    
    print("\n" + "=" * 80)
    print("🎯 最终结果:")
    
    if success_count >= 9:
        print("🎊 完美！用户的所有题目都能正确识别！")
        print("\n💡 系统现在支持的语法结构:")
        print("   📚 基础语法: 介词、冠词、代词、连词、be动词")
        print("   📖 时态语法: 一般现在时、一般过去时、现在进行时、现在完成时、第三人称单数")
        print("   🎯 高级语法: 情态动词、倒装句、虚拟语气、非谓语动词、比较级")
        print("   📝 句型结构: There be句型、定语从句、宾语从句")
        print("   🔤 词汇语法: 词汇、数量表达")
        
        print(f"\n🌐 完整系统访问:")
        print(f"   {API_BASE}")
        
    elif success_count >= 8:
        print("✅ 很好！大部分用户题目都能正确识别！")
    else:
        print("⚠️ 部分用户题目需要进一步优化")

if __name__ == "__main__":
    main()
