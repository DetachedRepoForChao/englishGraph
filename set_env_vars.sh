#!/bin/bash

echo "🔧 设置Vercel环境变量"
echo "================================"
echo ""

# 检查是否已登录Vercel
if ! vercel whoami &> /dev/null; then
    echo "❌ 请先登录Vercel:"
    echo "   vercel login"
    exit 1
fi

echo "✅ 已登录Vercel"
echo ""

# 设置环境变量
echo "📝 设置环境变量..."

# 注意：您需要替换为实际的Neo4j AuraDB URI
NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="Bt-iEdlUwkUHukW4x4yiGbKM0t64n8_l0eWNeN_IwSE"

echo "设置 NEO4J_URI..."
vercel env add NEO4J_URI production <<< "$NEO4J_URI"

echo "设置 NEO4J_USERNAME..."
vercel env add NEO4J_USERNAME production <<< "$NEO4J_USERNAME"

echo "设置 NEO4J_PASSWORD..."
vercel env add NEO4J_PASSWORD production <<< "$NEO4J_PASSWORD"

echo ""
echo "✅ 环境变量设置完成！"
echo ""
echo "🚀 现在重新部署项目:"
echo "   vercel --prod"
