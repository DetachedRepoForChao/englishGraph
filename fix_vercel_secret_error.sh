#!/bin/bash

echo "🔧 修复Vercel环境变量Secret引用错误"

# 确保登录到Vercel
echo "📝 检查Vercel登录状态..."
vercel whoami

if [ $? -ne 0 ]; then
    echo "❌ 请先登录Vercel: vercel login"
    exit 1
fi

echo "🗑️ 删除所有现有的NEO4J环境变量..."
vercel env rm NEO4J_URI production preview development --yes 2>/dev/null || echo "NEO4J_URI 不存在，跳过"
vercel env rm NEO4J_USERNAME production preview development --yes 2>/dev/null || echo "NEO4J_USERNAME 不存在，跳过"
vercel env rm NEO4J_PASSWORD production preview development --yes 2>/dev/null || echo "NEO4J_PASSWORD 不存在，跳过"

echo "➕ 添加正确的环境变量（Plain Text）..."

# 添加NEO4J_URI
echo "添加 NEO4J_URI..."
echo "neo4j+s://4620a4e5.databases.neo4j.io" | vercel env add NEO4J_URI production preview development

# 添加NEO4J_USERNAME
echo "添加 NEO4J_USERNAME..."
echo "neo4j" | vercel env add NEO4J_USERNAME production preview development

# 添加NEO4J_PASSWORD
echo "添加 NEO4J_PASSWORD..."
echo "Bt-iEdlUwkUHukW4x4yiGbKM0t64n8_l0eWNeN_IwSE" | vercel env add NEO4J_PASSWORD production preview development

echo "✅ 环境变量设置完成！"
echo ""
echo "🚀 重新部署项目..."
vercel --prod

echo "✅ 修复完成！"
echo "🔗 部署完成后，访问 /api/init-database 初始化数据库"
