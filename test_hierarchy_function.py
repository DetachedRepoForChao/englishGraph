#!/usr/bin/env python3
"""
测试知识层级显示功能
验证前端是否能正确显示知识层级结构
"""
import requests
import json

API_BASE = "https://english-knowledge-graph-2ktxa4o24-chao-wangs-projects-dfded257.vercel.app"

def test_hierarchy_api():
    """测试知识层级API"""
    
    print("🧪 测试知识层级API...")
    
    try:
        response = requests.get(f"{API_BASE}/api/knowledge/hierarchy/tree", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            hierarchy = data.get('hierarchy', [])
            
            print(f"   ✅ API响应成功")
            print(f"   📊 层级关系数量: {len(hierarchy)}")
            
            if hierarchy:
                # 分析层级结构
                parents = set()
                children = set()
                
                for item in hierarchy:
                    parents.add(item['parent_name'])
                    children.add(item['child_name'])
                
                root_nodes = parents - children
                
                print(f"   📊 父节点数量: {len(parents)}")
                print(f"   📊 子节点数量: {len(children)}")
                print(f"   📊 根节点数量: {len(root_nodes)}")
                print(f"   🌳 根节点: {list(root_nodes)[:5]}")
                
                # 检查关键知识点
                key_points = ['情态动词', '倒装句', '虚拟语气', '英语语法']
                found_points = []
                
                for item in hierarchy:
                    if item['parent_name'] in key_points or item['child_name'] in key_points:
                        found_points.append(f"{item['parent_name']} → {item['child_name']}")
                
                print(f"   🔍 找到关键知识点关系:")
                for point in found_points:
                    print(f"      - {point}")
                
                return True
            else:
                print("   ⚠️ 层级数据为空")
                return False
                
        else:
            print(f"   ❌ API请求失败 (状态码: {response.status_code})")
            print(f"   📄 响应内容: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ API测试异常: {e}")
        return False

def test_frontend_access():
    """测试前端页面访问"""
    
    print("\n🌐 测试前端页面访问...")
    
    try:
        response = requests.get(API_BASE, timeout=10)
        
        if response.status_code == 200:
            print(f"   ✅ 前端页面访问成功")
            
            # 检查HTML内容
            html_content = response.text
            
            # 检查知识层级相关元素
            if 'knowledge-hierarchy' in html_content:
                print(f"   ✅ 找到知识层级容器")
            else:
                print(f"   ⚠️ 未找到知识层级容器")
            
            if 'loadKnowledgeHierarchy' in html_content:
                print(f"   ✅ 找到加载函数")
            else:
                print(f"   ⚠️ 未找到加载函数")
            
            return True
        else:
            print(f"   ❌ 前端页面访问失败 (状态码: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"   ❌ 前端访问异常: {e}")
        return False

def generate_test_instructions():
    """生成测试说明"""
    
    print("\n📋 前端测试说明:")
    print("=" * 50)
    print("1. 打开浏览器访问:")
    print(f"   {API_BASE}")
    print()
    print("2. 在浏览器中:")
    print("   - 打开开发者工具 (F12)")
    print("   - 切换到 Console 标签页")
    print("   - 查看是否有错误信息")
    print()
    print("3. 在页面中找到 '知识点层级结构' 部分:")
    print("   - 应该显示层级树结构")
    print("   - 包含统计信息 (总节点、关系、根节点)")
    print("   - 树形展示各个知识点")
    print()
    print("4. 如果显示有问题:")
    print("   - 检查控制台是否有JavaScript错误")
    print("   - 点击 '重新加载' 按钮")
    print("   - 刷新页面重试")
    print()
    print("5. 测试页面 (独立测试):")
    print("   打开: test_hierarchy_display.html")

def main():
    """主函数"""
    
    print("🚀 知识层级显示功能测试")
    print("=" * 60)
    print(f"🔗 API地址: {API_BASE}")
    print("=" * 60)
    
    # 测试API
    api_success = test_hierarchy_api()
    
    # 测试前端
    frontend_success = test_frontend_access()
    
    # 生成说明
    generate_test_instructions()
    
    print("\n" + "=" * 60)
    if api_success and frontend_success:
        print("✅ 所有基础测试通过！")
        print("💡 请按照上述说明在浏览器中验证前端显示")
    elif api_success:
        print("✅ API测试通过，前端可能需要检查")
        print("💡 请检查前端页面和JavaScript控制台")
    else:
        print("❌ API测试失败，请检查后端服务")

if __name__ == "__main__":
    main()
