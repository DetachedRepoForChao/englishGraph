#!/usr/bin/env python3
"""
AI Agent功能测试脚本
测试自动标注功能是否正常工作
"""
import sys
import os
import asyncio
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from backend.services.database import neo4j_service
from backend.services.ai_agent_service import ai_agent_service
from backend.models.schema import Question

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_single_auto_annotation():
    """测试单个题目自动标注"""
    logger.info("=== 测试单个题目自动标注 ===")
    
    # 创建测试题目
    test_question = Question(
        content="She _____ to school every day. A) go B) goes C) going D) gone",
        question_type="选择题",
        options=["go", "goes", "going", "gone"],
        answer="B",
        analysis="主语She是第三人称单数，动词需要用第三人称单数形式goes",
        source="AI Agent测试",
        difficulty="easy"
    )
    
    try:
        # 执行自动标注
        result = await ai_agent_service.auto_annotate_question(test_question)
        
        logger.info(f"标注结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("status") == "completed":
            suggestions = result.get("auto_annotations", [])
            applied = result.get("applied_annotations", [])
            
            logger.info(f"✅ 自动标注成功")
            logger.info(f"   - 知识点建议数: {len(suggestions)}")
            logger.info(f"   - 自动应用数: {len(applied)}")
            
            for i, suggestion in enumerate(suggestions[:3], 1):
                logger.info(f"   {i}. {suggestion['knowledge_point_name']} "
                          f"(置信度: {suggestion['confidence']:.3f}, "
                          f"决策分数: {suggestion['decision_score']:.3f})")
            
            return True
        else:
            logger.error("❌ 自动标注失败")
            return False
            
    except Exception as e:
        logger.error(f"❌ 测试过程出错: {e}")
        return False


async def test_batch_auto_annotation():
    """测试批量自动标注"""
    logger.info("\n=== 测试批量自动标注 ===")
    
    # 加载示例题目
    try:
        with open("data/sample_questions/import_example.json", "r", encoding="utf-8") as f:
            questions_data = json.load(f)
        
        test_questions = []
        for q_data in questions_data[:3]:  # 只测试前3道题
            question = Question(**q_data)
            test_questions.append(question)
        
        logger.info(f"准备批量标注 {len(test_questions)} 道题目")
        
        # 执行批量标注
        result = await ai_agent_service.batch_auto_annotate(test_questions)
        
        logger.info(f"批量标注结果:")
        logger.info(f"   - 总题目数: {result['total_questions']}")
        logger.info(f"   - 成功数: {result['success_count']}")
        logger.info(f"   - 失败数: {result['error_count']}")
        logger.info(f"   - 成功率: {result['success_rate']:.2%}")
        
        if result['success_rate'] > 0.5:
            logger.info("✅ 批量标注测试通过")
            return True
        else:
            logger.error("❌ 批量标注成功率过低")
            return False
            
    except Exception as e:
        logger.error(f"❌ 批量标注测试失败: {e}")
        return False


async def test_ai_agent_configuration():
    """测试AI Agent配置功能"""
    logger.info("\n=== 测试AI Agent配置 ===")
    
    try:
        # 获取当前配置
        current_config = ai_agent_service.get_configuration()
        logger.info(f"当前配置: {current_config}")
        
        # 更新配置
        new_config = {
            "confidence_threshold": 0.5,
            "max_auto_annotations": 3,
            "learning_enabled": True
        }
        
        ai_agent_service.update_configuration(new_config)
        
        # 验证配置更新
        updated_config = ai_agent_service.get_configuration()
        logger.info(f"更新后配置: {updated_config}")
        
        if updated_config["confidence_threshold"] == 0.5:
            logger.info("✅ 配置更新测试通过")
            
            # 恢复原始配置
            ai_agent_service.update_configuration(current_config)
            return True
        else:
            logger.error("❌ 配置更新失败")
            return False
            
    except Exception as e:
        logger.error(f"❌ 配置测试失败: {e}")
        return False


async def test_decision_scoring():
    """测试AI Agent决策评分机制"""
    logger.info("\n=== 测试决策评分机制 ===")
    
    try:
        # 创建不同类型的测试题目
        test_cases = [
            {
                "question": Question(
                    content="She is playing basketball now.",
                    question_type="选择题",
                    answer="现在进行时",
                    difficulty="medium"
                ),
                "expected_kp": "现在进行时"
            },
            {
                "question": Question(
                    content="I went to school yesterday.",
                    question_type="选择题", 
                    answer="一般过去时",
                    difficulty="easy"
                ),
                "expected_kp": "一般过去时"
            }
        ]
        
        correct_predictions = 0
        total_tests = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"测试案例 {i}: {test_case['question'].content}")
            
            result = await ai_agent_service.auto_annotate_question(test_case["question"])
            
            if result.get("status") == "completed":
                suggestions = result.get("auto_annotations", [])
                
                # 检查是否包含预期的知识点
                found_expected = any(
                    test_case["expected_kp"] in suggestion.get("knowledge_point_name", "")
                    for suggestion in suggestions
                )
                
                if found_expected:
                    correct_predictions += 1
                    logger.info(f"   ✅ 正确识别了预期知识点")
                else:
                    logger.info(f"   ❌ 未识别预期知识点: {test_case['expected_kp']}")
                    logger.info(f"   实际建议: {[s['knowledge_point_name'] for s in suggestions[:3]]}")
        
        accuracy = correct_predictions / total_tests
        logger.info(f"\n决策准确率: {accuracy:.2%} ({correct_predictions}/{total_tests})")
        
        if accuracy >= 0.5:
            logger.info("✅ 决策评分测试通过")
            return True
        else:
            logger.error("❌ 决策准确率过低")
            return False
            
    except Exception as e:
        logger.error(f"❌ 决策评分测试失败: {e}")
        return False


async def run_comprehensive_ai_agent_test():
    """运行AI Agent综合测试"""
    logger.info("🚀 开始AI Agent功能测试")
    
    # 确保数据库连接
    if not neo4j_service.connect():
        logger.error("❌ 无法连接到数据库，测试终止")
        return False
    
    try:
        test_results = {}
        
        # 执行各项测试
        test_results['single_annotation'] = await test_single_auto_annotation()
        test_results['batch_annotation'] = await test_batch_auto_annotation()
        test_results['configuration'] = await test_ai_agent_configuration()
        test_results['decision_scoring'] = await test_decision_scoring()
        
        # 汇总结果
        logger.info("\n" + "="*60)
        logger.info("🎯 AI Agent测试结果汇总")
        logger.info("="*60)
        
        passed = 0
        total = 0
        
        for test_name, result in test_results.items():
            total += 1
            if result:
                passed += 1
                logger.info(f"✅ {test_name.replace('_', ' ').title()}: 通过")
            else:
                logger.info(f"❌ {test_name.replace('_', ' ').title()}: 失败")
        
        success_rate = passed / total
        logger.info(f"\n🎉 AI Agent测试通过率: {success_rate:.1%} ({passed}/{total})")
        
        if success_rate >= 0.75:
            logger.info("🎊 AI Agent功能测试全面通过！")
        elif success_rate >= 0.5:
            logger.info("⚠️  AI Agent基本功能正常，部分功能需要优化")
        else:
            logger.info("❌ AI Agent功能存在较多问题，需要检查")
        
        return success_rate >= 0.5
        
    finally:
        neo4j_service.close()


if __name__ == "__main__":
    asyncio.run(run_comprehensive_ai_agent_test())
