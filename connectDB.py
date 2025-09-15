from neo4j import GraphDatabase

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j+ssc://383b0a61.databases.neo4j.io"
AUTH = ("neo4j", "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI")

print("🧪 测试数据库连接...")
try:
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        print("✅ 连接成功！")
        
        # 测试简单查询
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            test_value = result.single()["test"]
            print(f"✅ 查询测试成功，返回值: {test_value}")
            
except Exception as e:
    print(f"❌ 连接失败: {e}")
    import traceback
    print(f"详细错误: {traceback.format_exc()}")