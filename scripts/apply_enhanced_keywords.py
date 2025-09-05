#!/usr/bin/env python3
"""
将增强后的关键词库应用到NLP服务中
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def apply_enhanced_keywords():
    """应用增强后的关键词库"""
    print("🚀 开始应用增强后的关键词库...")
    
    # 加载增强后的关键词库
    try:
        with open("enhanced_keyword_patterns_simple.json", 'r', encoding='utf-8') as f:
            enhanced_patterns = json.load(f)
        print("✅ 增强后的关键词库加载成功")
    except FileNotFoundError:
        print("❌ 增强后的关键词库文件未找到，请先运行 enhance_keywords_simple.py")
        return False
    
    # 更新NLP服务的关键词模式
    nlp_service_file = "backend/services/nlp_service.py"
    
    try:
        # 读取当前NLP服务文件
        with open(nlp_service_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 生成新的关键词模式代码
        new_patterns_code = generate_patterns_code(enhanced_patterns)
        
        # 替换关键词模式部分
        updated_content = replace_patterns_in_content(content, new_patterns_code)
        
        # 写回文件
        with open(nlp_service_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ NLP服务关键词库更新成功")
        return True
        
    except Exception as e:
        print(f"❌ 更新NLP服务失败: {e}")
        return False

def generate_patterns_code(enhanced_patterns):
    """生成关键词模式代码"""
    code_lines = [
        "    def _build_keyword_patterns(self) -> Dict[str, List[str]]:",
        "        \"\"\"构建关键词模式库 - 增强版\"\"\"",
        "        return {"
    ]
    
    for kp, keywords in enhanced_patterns.items():
        code_lines.append(f'            "{kp}": [')
        
        # 每行最多5个关键词，便于阅读
        for i in range(0, len(keywords), 5):
            batch = keywords[i:i+5]
            quoted_keywords = [f'"{kw}"' for kw in batch]
            if i + 5 < len(keywords):
                code_lines.append(f"                {', '.join(quoted_keywords)},")
            else:
                code_lines.append(f"                {', '.join(quoted_keywords)}")
        
        code_lines.append("            ],")
    
    code_lines.append("        }")
    
    return "\n".join(code_lines)

def replace_patterns_in_content(content, new_patterns_code):
    """在内容中替换关键词模式"""
    # 找到_build_keyword_patterns方法的开始和结束
    start_marker = "    def _build_keyword_patterns(self) -> Dict[str, List[str]]:"
    end_marker = "        }"
    
    # 找到开始位置
    start_pos = content.find(start_marker)
    if start_pos == -1:
        print("❌ 未找到_build_keyword_patterns方法")
        return content
    
    # 找到结束位置（需要找到对应的}）
    brace_count = 0
    end_pos = start_pos
    in_method = False
    
    for i, char in enumerate(content[start_pos:], start_pos):
        if char == '{':
            brace_count += 1
            in_method = True
        elif char == '}':
            brace_count -= 1
            if in_method and brace_count == 0:
                end_pos = i + 1
                break
    
    if end_pos == start_pos:
        print("❌ 未找到方法结束位置")
        return content
    
    # 替换内容
    new_content = content[:start_pos] + new_patterns_code + content[end_pos:]
    return new_content

def test_enhanced_nlp_service():
    """测试增强后的NLP服务"""
    print("\n🧪 测试增强后的NLP服务...")
    
    try:
        # 导入NLP服务
        from backend.services.nlp_service import NLPService
        
        # 创建NLP服务实例
        nlp_service = NLPService()
        
        # 测试题目
        test_questions = [
            "Look! The children are playing in the playground.",
            "I have already finished my homework.",
            "She goes to school every day.",
            "The book which is on the table belongs to me.",
            "This is the most beautiful flower I have ever seen."
        ]
        
        print("测试题目:")
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. {question}")
            
            # 获取建议
            suggestions = nlp_service.suggest_knowledge_points(question, "选择题")
            
            if suggestions:
                print("   建议知识点:")
                for suggestion in suggestions[:3]:  # 只显示前3个
                    print(f"   - {suggestion['knowledge_point_name']}: {suggestion['confidence']:.3f}")
            else:
                print("   ❌ 无建议")
        
        print("\n✅ NLP服务测试完成")
        return True
        
    except Exception as e:
        print(f"❌ NLP服务测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        # 应用增强后的关键词库
        if apply_enhanced_keywords():
            print("\n🎉 关键词库应用成功！")
            
            # 测试增强后的效果
            test_enhanced_nlp_service()
            
            print("\n💡 下一步:")
            print("1. 重启服务器以应用新的关键词库")
            print("2. 测试标注准确率是否有提升")
            print("3. 监控系统性能")
        else:
            print("\n❌ 关键词库应用失败")
            
    except Exception as e:
        print(f"\n❌ 应用过程失败: {e}")
        import traceback
        traceback.print_exc()
