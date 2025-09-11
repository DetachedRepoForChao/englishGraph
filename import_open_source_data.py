#!/usr/bin/env python3
"""
导入开源英语教育数据
"""
import sys
import os
import logging

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.open_source_data import open_source_integrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    logger.info("🚀 开始导入开源英语教育数据...")
    
    try:
        # 获取数据统计
        kp_count = len(open_source_integrator.get_all_knowledge_points())
        q_count = len(open_source_integrator.get_all_questions())
        
        logger.info(f"📊 数据统计:")
        logger.info(f"   知识点: {kp_count} 个")
        logger.info(f"   题目: {q_count} 道")
        
        # 生成Cypher脚本
        cypher_script = open_source_integrator.export_to_cypher()
        
        # 保存脚本
        output_file = "open_source_data.cypher"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cypher_script)
        
        logger.info(f"📄 开源数据脚本已保存到: {output_file}")
        
        # 显示部分知识点信息
        logger.info("📚 包含的知识点:")
        for kp in open_source_integrator.get_all_knowledge_points():
            grade_str = ", ".join(kp['grade_levels'])
            logger.info(f"   - {kp['name']} ({kp['difficulty']}) - {grade_str}")
        
        logger.info("")
        logger.info("🎯 使用方法:")
        logger.info("1. 打开 Neo4j AuraDB Browser")
        logger.info("2. 执行生成的 open_source_data.cypher 脚本")
        logger.info("3. 验证数据导入成功")
        logger.info("4. 在Vercel应用中查看丰富的题库")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 导入过程出错: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
