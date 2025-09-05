#!/usr/bin/env python3
"""
系统功能测试脚本
用于验证各个模块是否正常工作
"""
import sys
import os
import asyncio
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from backend.services.database import neo4j_service
from backend.services.nlp_service import nlp_service
from backend.services.analytics_service import analytics_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_database_connection():
    """测试数据库连接"""
    logger.info("=== 测试数据库连接 ===")
    try:
        if neo4j_service.connect():
            logger.info("✅ 数据库连接成功")
            
            # 测试基本查询
            with neo4j_service.driver.session() as session:
                result = session.run("MATCH (kp:KnowledgePoint) RETURN count(kp) as count")
                kp_count = result.single()["count"]
                logger.info(f"✅ 知识点数量: {kp_count}")
                
                result = session.run("MATCH (q:Question) RETURN count(q) as count")
                q_count = result.single()["count"]
                logger.info(f"✅ 题目数量: {q_count}")
            
            neo4j_service.close()
            return True
        else:
            logger.error("❌ 数据库连接失败")
            return False
    except Exception as e:
        logger.error(f"❌ 数据库测试失败: {e}")
        return False


async def test_nlp_service():
    """测试NLP服务"""
    logger.info("\n=== 测试NLP服务 ===")
    try:
        # 测试知识点推荐
        test_question = "She _____ to school every day. A) go B) goes C) going D) gone"
        suggestions = nlp_service.suggest_knowledge_points(test_question, "选择题")
        
        if suggestions:
            logger.info("✅ NLP推荐功能正常")
            for i, suggestion in enumerate(suggestions[:3], 1):
                logger.info(f"  {i}. {suggestion['knowledge_point_name']} (置信度: {suggestion['confidence']:.2f})")
        else:
            logger.warning("⚠️  NLP推荐返回空结果")
        
        return True
    except Exception as e:
        logger.error(f"❌ NLP服务测试失败: {e}")
        return False


async def test_analytics_service():
    """测试分析服务"""
    logger.info("\n=== 测试分析服务 ===")
    try:
        # 测试知识点覆盖分析
        coverage = analytics_service.get_knowledge_coverage_analysis()
        if coverage and "summary" in coverage:
            logger.info("✅ 知识点覆盖分析正常")
            summary = coverage["summary"]
            logger.info(f"  总知识点: {summary.get('total_knowledge_points', 0)}")
            logger.info(f"  覆盖率: {summary.get('coverage_rate', 0)}%")
        
        # 测试难度分布分析
        difficulty = analytics_service.get_difficulty_distribution()
        if difficulty:
            logger.info("✅ 难度分布分析正常")
            logger.info(f"  总题目数: {difficulty.get('total_questions', 0)}")
        
        # 测试学习路径推荐
        path_rec = analytics_service.generate_learning_path_recommendation(["一般现在时"])
        if path_rec:
            logger.info("✅ 学习路径推荐正常")
            logger.info(f"  推荐数量: {len(path_rec.get('learning_path_recommendations', []))}")
        
        return True
    except Exception as e:
        logger.error(f"❌ 分析服务测试失败: {e}")
        return False


async def test_api_endpoints():
    """测试API端点（需要服务器运行）"""
    logger.info("\n=== 测试API端点 ===")
    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            # 测试健康检查
            async with session.get('http://localhost:8000/health') as resp:
                if resp.status == 200:
                    logger.info("✅ 健康检查API正常")
                else:
                    logger.warning("⚠️  健康检查API异常")
            
            # 测试知识点搜索
            async with session.get('http://localhost:8000/api/knowledge/search?keyword=时态') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"✅ 知识点搜索API正常，返回{len(data.get('results', []))}个结果")
                else:
                    logger.warning("⚠️  知识点搜索API异常")
        
        return True
    except Exception as e:
        logger.warning(f"⚠️  API测试需要服务器运行: {e}")
        return False


async def run_comprehensive_test():
    """运行综合测试"""
    logger.info("🚀 开始系统功能测试")
    
    test_results = {}
    
    # 测试数据库连接
    test_results['database'] = await test_database_connection()
    
    # 测试NLP服务
    test_results['nlp'] = await test_nlp_service()
    
    # 测试分析服务
    test_results['analytics'] = await test_analytics_service()
    
    # 测试API端点
    test_results['api'] = await test_api_endpoints()
    
    # 汇总测试结果
    logger.info("\n" + "="*50)
    logger.info("📊 测试结果汇总")
    logger.info("="*50)
    
    passed = 0
    total = 0
    
    for test_name, result in test_results.items():
        total += 1
        if result:
            passed += 1
            logger.info(f"✅ {test_name.upper()}: 通过")
        else:
            logger.info(f"❌ {test_name.upper()}: 失败")
    
    logger.info(f"\n🎯 测试通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        logger.info("🎉 所有测试通过！系统运行正常")
    elif passed >= total * 0.7:
        logger.info("⚠️  大部分测试通过，系统基本正常")
    else:
        logger.info("❌ 多项测试失败，请检查系统配置")
    
    return passed / total


if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())
