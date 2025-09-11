#!/usr/bin/env python3
"""
生成200道题目的综合英语题库
"""
import sys
import os
import logging

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.comprehensive_question_bank import comprehensive_question_bank

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    logger.info("🚀 生成200道题目综合英语题库...")
    
    try:
        # 获取所有数据
        questions = comprehensive_question_bank.get_all_questions()
        knowledge_points = comprehensive_question_bank.get_all_knowledge_points()
        
        # 统计信息
        logger.info(f"📊 题库统计:")
        logger.info(f"   题目总数: {len(questions)} 道")
        logger.info(f"   知识点总数: {len(knowledge_points)} 个")
        
        # 难度分布
        easy_count = len(comprehensive_question_bank.get_questions_by_difficulty("easy"))
        medium_count = len(comprehensive_question_bank.get_questions_by_difficulty("medium"))
        hard_count = len(comprehensive_question_bank.get_questions_by_difficulty("hard"))
        
        logger.info(f"📈 难度分布:")
        logger.info(f"   简单: {easy_count} 道")
        logger.info(f"   中等: {medium_count} 道")
        logger.info(f"   困难: {hard_count} 道")
        
        # 年级分布统计
        grade_stats = {}
        for q in questions:
            grade = q.get("grade_level", "未设置")
            grade_stats[grade] = grade_stats.get(grade, 0) + 1
        
        logger.info(f"🎓 年级分布:")
        for grade, count in sorted(grade_stats.items()):
            logger.info(f"   {grade}: {count} 道")
        
        # 知识点覆盖
        logger.info(f"📚 知识点覆盖:")
        for kp in knowledge_points:
            kp_questions = [q for q in questions if kp['name'] in q.get('knowledge_points', [])]
            grade_str = ", ".join(kp['grade_levels'][:2])  # 显示前两个年级
            logger.info(f"   {kp['name']} ({kp['difficulty']}) - {grade_str} - {len(kp_questions)}道题")
        
        # 生成Cypher脚本
        cypher_script = comprehensive_question_bank.export_to_cypher()
        
        # 保存脚本
        output_file = "comprehensive_200_questions.cypher"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cypher_script)
        
        logger.info(f"📄 200道题目数据库脚本已保存到: {output_file}")
        
        # 生成导入说明
        readme_content = f"""# 200道题目综合英语题库

## 📊 数据统计
- **题目总数**: {len(questions)} 道
- **知识点总数**: {len(knowledge_points)} 个
- **覆盖年级**: 小学二年级 - 高中三年级
- **CEFR级别**: A1 - C1

## 📈 难度分布
- **简单**: {easy_count} 道 ({easy_count/len(questions)*100:.1f}%)
- **中等**: {medium_count} 道 ({medium_count/len(questions)*100:.1f}%)
- **困难**: {hard_count} 道 ({hard_count/len(questions)*100:.1f}%)

## 🎯 使用方法
1. 打开 Neo4j AuraDB Browser
2. 执行 `comprehensive_200_questions.cypher` 脚本
3. 验证数据导入成功
4. 在Vercel应用中体验丰富的题库

## 📚 知识点列表
{chr(10).join([f"- **{kp['name']}** ({kp['difficulty']}) - {', '.join(kp['grade_levels'][:2])}" for kp in knowledge_points])}

## 🌟 特色
- 基于权威教育标准
- 符合CEFR框架
- 适配K12教育体系
- 支持AI智能标注
"""
        
        with open("200_questions_README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        logger.info("📋 说明文档已保存到: 200_questions_README.md")
        logger.info("")
        logger.info("🎉 200道题目综合题库生成完成！")
        logger.info("🚀 现在可以导入到数据库中，大幅提升系统的教育价值！")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 生成过程出错: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
