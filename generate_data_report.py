#!/usr/bin/env python3
"""
生成数据集成报告
"""
import requests
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://english-knowledge-graph-cqi7il5gi-chao-wangs-projects-dfded257.vercel.app"

def generate_report():
    """生成完整的数据报告"""
    logger.info("📊 生成数据集成报告...")
    
    try:
        # 1. 获取基础统计
        stats_response = requests.get(f"{BASE_URL}/api/analytics/dashboard-stats")
        stats = stats_response.json()
        
        # 2. 获取知识点列表
        kp_response = requests.get(f"{BASE_URL}/api/knowledge/search?keyword=")
        kp_data = kp_response.json()
        knowledge_points = kp_data.get("results", [])
        
        # 3. 获取题目列表
        questions_response = requests.get(f"{BASE_URL}/api/questions/")
        questions_data = questions_response.json()
        questions = questions_data.get("questions", [])
        
        # 4. 生成报告
        report = {
            "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "system_overview": {
                "total_knowledge_points": stats.get("total_knowledge_points", 0),
                "total_questions": stats.get("total_questions", 0),
                "annotated_questions": stats.get("annotated_questions", 0),
                "annotation_coverage": f"{stats.get('annotation_coverage', 0):.1f}%"
            },
            "knowledge_points_analysis": analyze_knowledge_points(knowledge_points),
            "questions_analysis": analyze_questions(questions),
            "data_sources": get_data_sources(knowledge_points, questions),
            "grade_distribution": get_grade_distribution(knowledge_points, questions),
            "difficulty_analysis": get_difficulty_analysis(questions)
        }
        
        # 保存报告
        with open("data_integration_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 生成可读性报告
        generate_readable_report(report)
        
        logger.info("✅ 数据报告生成完成")
        logger.info("📄 详细报告: data_integration_report.json")
        logger.info("📋 可读报告: data_integration_report.md")
        
        return report
        
    except Exception as e:
        logger.error(f"❌ 报告生成失败: {e}")
        return None

def analyze_knowledge_points(knowledge_points):
    """分析知识点"""
    analysis = {
        "total_count": len(knowledge_points),
        "by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
        "by_source": {},
        "grade_coverage": {}
    }
    
    for kp in knowledge_points:
        # 难度分布
        difficulty = kp.get("difficulty", "medium")
        analysis["by_difficulty"][difficulty] = analysis["by_difficulty"].get(difficulty, 0) + 1
        
        # 来源分布
        source = kp.get("source", "Unknown")
        analysis["by_source"][source] = analysis["by_source"].get(source, 0) + 1
    
    return analysis

def analyze_questions(questions):
    """分析题目"""
    analysis = {
        "total_count": len(questions),
        "by_type": {},
        "by_difficulty": {"easy": 0, "medium": 0, "hard": 0},
        "by_source": {},
        "with_knowledge_points": 0
    }
    
    for q in questions:
        # 题目类型
        q_type = q.get("question_type", "未知")
        analysis["by_type"][q_type] = analysis["by_type"].get(q_type, 0) + 1
        
        # 难度分布
        difficulty = q.get("difficulty", "medium")
        analysis["by_difficulty"][difficulty] = analysis["by_difficulty"].get(difficulty, 0) + 1
        
        # 来源分布
        source = q.get("source", "Unknown")
        analysis["by_source"][source] = analysis["by_source"].get(source, 0) + 1
        
        # 有知识点关联的题目
        if q.get("knowledge_points") and len(q["knowledge_points"]) > 0:
            analysis["with_knowledge_points"] += 1
    
    return analysis

def get_data_sources(knowledge_points, questions):
    """获取数据来源统计"""
    sources = set()
    
    for kp in knowledge_points:
        if kp.get("source"):
            sources.add(kp["source"])
    
    for q in questions:
        if q.get("source"):
            sources.add(q["source"])
    
    return list(sources)

def get_grade_distribution(knowledge_points, questions):
    """获取年级分布"""
    grade_stats = {}
    
    for kp in knowledge_points:
        grade_levels = kp.get("grade_levels", [])
        for grade in grade_levels:
            grade_stats[grade] = grade_stats.get(grade, 0) + 1
    
    return grade_stats

def get_difficulty_analysis(questions):
    """获取难度分析"""
    difficulty_stats = {"easy": 0, "medium": 0, "hard": 0}
    
    for q in questions:
        difficulty = q.get("difficulty", "medium")
        difficulty_stats[difficulty] += 1
    
    return difficulty_stats

def generate_readable_report(report):
    """生成可读性报告"""
    md_content = f"""# K12英语知识图谱系统 - 数据集成报告

**生成时间**: {report['report_time']}

## 📊 系统概览

- **知识点总数**: {report['system_overview']['total_knowledge_points']} 个
- **题目总数**: {report['system_overview']['total_questions']} 道
- **已标注题目**: {report['system_overview']['annotated_questions']} 道
- **标注覆盖率**: {report['system_overview']['annotation_coverage']}

## 📚 知识点分析

### 难度分布
- **简单**: {report['knowledge_points_analysis']['by_difficulty']['easy']} 个
- **中等**: {report['knowledge_points_analysis']['by_difficulty']['medium']} 个  
- **困难**: {report['knowledge_points_analysis']['by_difficulty']['hard']} 个

### 数据来源
{chr(10).join([f"- **{source}**: {count} 个" for source, count in report['knowledge_points_analysis']['by_source'].items()])}

## 📝 题目分析

### 题目类型分布
{chr(10).join([f"- **{q_type}**: {count} 道" for q_type, count in report['questions_analysis']['by_type'].items()])}

### 难度分布  
- **简单**: {report['questions_analysis']['by_difficulty']['easy']} 道
- **中等**: {report['questions_analysis']['by_difficulty']['medium']} 道
- **困难**: {report['questions_analysis']['by_difficulty']['hard']} 道

### 标注情况
- **有知识点关联**: {report['questions_analysis']['with_knowledge_points']} 道
- **关联率**: {(report['questions_analysis']['with_knowledge_points'] / report['questions_analysis']['total_count'] * 100):.1f}%

## 🎓 年级分布

{chr(10).join([f"- **{grade}**: {count} 个知识点" for grade, count in report['grade_distribution'].items()])}

## 🌐 数据来源

本系统集成了以下权威开源英语教育资源：

{chr(10).join([f"- {source}" for source in report['data_sources']])}

## 📈 质量评估

- **覆盖度**: 涵盖K12全学段，从小学二年级到高中三年级
- **权威性**: 基于剑桥、牛津、英国文化协会等权威标准
- **系统性**: 符合CEFR欧洲语言参考框架A1-C1级别
- **实用性**: 包含选择题、填空题等多种题型

---

**系统地址**: https://english-knowledge-graph-cqi7il5gi-chao-wangs-projects-dfded257.vercel.app
**GitHub仓库**: https://github.com/DetachedRepoForChao/englishGraph.git
"""
    
    with open("data_integration_report.md", "w", encoding="utf-8") as f:
        f.write(md_content)

if __name__ == "__main__":
    generate_report()
