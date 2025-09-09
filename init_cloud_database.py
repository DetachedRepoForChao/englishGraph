#!/usr/bin/env python3
"""
初始化Neo4j云数据库脚本
"""
import sys
import os
import requests
import json

# 云数据库连接信息
NEO4J_URI = "neo4j+s://383b0a61.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI"

def init_via_api():
    """通过部署的API初始化数据库"""
    base_url = "https://english-knowledge-graph-bsfvthw7u-chao-wangs-projects-dfded257.vercel.app"
    
    print("🚀 开始初始化云数据库...")
    
    # 1. 初始化数据库结构
    print("📊 初始化数据库结构...")
    try:
        response = requests.post(f"{base_url}/api/init/database", timeout=30)
        if response.status_code == 200:
            print("✅ 数据库结构初始化成功")
        else:
            print(f"❌ 数据库结构初始化失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 初始化数据库结构失败: {e}")
    
    # 2. 加载示例数据
    print("📚 加载示例知识点...")
    try:
        response = requests.post(f"{base_url}/api/init/sample-data", timeout=30)
        if response.status_code == 200:
            print("✅ 示例数据加载成功")
        else:
            print(f"❌ 示例数据加载失败: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 加载示例数据失败: {e}")
    
    # 3. 验证数据
    print("🔍 验证数据...")
    try:
        response = requests.get(f"{base_url}/api/analytics/dashboard-stats", timeout=30)
        if response.status_code == 200:
            stats = response.json()
            print("✅ 数据验证成功")
            print(f"📊 知识点总数: {stats.get('knowledge_points_count', 0)}")
            print(f"📝 题目总数: {stats.get('questions_count', 0)}")
        else:
            print(f"❌ 数据验证失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 数据验证失败: {e}")
    
    print("\n🎉 云数据库初始化完成！")
    print(f"🌐 访问地址: {base_url}")

if __name__ == "__main__":
    init_via_api()
