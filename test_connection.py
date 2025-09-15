#!/usr/bin/env python3
"""
测试数据库连接
"""
from neo4j import GraphDatabase
import traceback

# 使用与connectDB.py相同的连接信息
URI = "neo4j+s://383b0a61.databases.neo4j.io"
AUTH = ("neo4j", "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI")

def test_basic_connection():
    """测试基础连接"""
    print("🧪 测试基础连接...")
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            driver.verify_connectivity()
            print("✅ 基础连接成功")
            return True
    except Exception as e:
        print(f"❌ 基础连接失败: {e}")
        print(f"详细错误: {traceback.format_exc()}")
        return False

def test_simple_query():
    """测试简单查询"""
    print("\n🧪 测试简单查询...")
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                result = session.run("RETURN 1 as test")
                test_value = result.single()["test"]
                print(f"✅ 查询成功，返回值: {test_value}")
                return True
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return False

def test_knowledge_points():
    """测试知识点查询"""
    print("\n🧪 测试知识点查询...")
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                result = session.run("MATCH (kp:KnowledgePoint) RETURN count(kp) as count")
                count = result.single()["count"]
                print(f"✅ 当前知识点数量: {count}")
                
                # 查询具体知识点
                result = session.run("""
                    MATCH (kp:KnowledgePoint) 
                    RETURN kp.name as name, kp.id as id 
                    LIMIT 5
                """)
                
                print("📋 前5个知识点:")
                for record in result:
                    print(f"   - {record['name']} (ID: {record['id']})")
                
                return True
    except Exception as e:
        print(f"❌ 知识点查询失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 数据库连接测试工具")
    print(f"🔗 URI: {URI}")
    print(f"👤 用户名: {AUTH[0]}")
    print("=" * 50)
    
    # 测试连接
    if not test_basic_connection():
        print("\n❌ 基础连接失败，无法继续测试")
        return
    
    # 测试查询
    if not test_simple_query():
        print("\n❌ 简单查询失败")
        return
    
    # 测试知识点
    if test_knowledge_points():
        print("\n✅ 所有测试通过！数据库连接正常")
        
        # 检查关键知识点
        print("\n🔍 检查关键知识点是否存在...")
        try:
            with GraphDatabase.driver(URI, auth=AUTH) as driver:
                with driver.session() as session:
                    key_points = ['情态动词', '倒装句', '虚拟语气']
                    for kp_name in key_points:
                        result = session.run("""
                            MATCH (kp:KnowledgePoint {name: $name})
                            RETURN kp.id as id
                        """, {"name": kp_name})
                        
                        record = result.single()
                        if record:
                            print(f"   ✅ {kp_name} 存在 (ID: {record['id']})")
                        else:
                            print(f"   ❌ {kp_name} 不存在")
        except Exception as e:
            print(f"   ❌ 检查失败: {e}")
    else:
        print("\n❌ 知识点查询失败")

if __name__ == "__main__":
    main()
