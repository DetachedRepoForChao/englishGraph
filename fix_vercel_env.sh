#!/bin/bash

echo "🔧 修复Vercel环境变量配置"
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

# 获取项目信息
echo "📋 获取项目信息..."
PROJECT_NAME=$(vercel ls --json | jq -r '.[0].name' 2>/dev/null || echo "englishGraph")
echo "项目名称: $PROJECT_NAME"
echo ""

# 删除错误的环境变量
echo "🗑️ 删除错误的环境变量..."
vercel env rm NEO4J_URI production --yes 2>/dev/null || echo "NEO4J_URI 不存在，跳过删除"
vercel env rm NEO4J_USERNAME production --yes 2>/dev/null || echo "NEO4J_USERNAME 不存在，跳过删除"
vercel env rm NEO4J_PASSWORD production --yes 2>/dev/null || echo "NEO4J_PASSWORD 不存在，跳过删除"

echo ""
echo "📝 添加正确的环境变量..."

# 提示用户输入Neo4j URI
echo "请输入您的Neo4j AuraDB URI（格式：neo4j+s://xxxxx.databases.neo4j.io）:"
read -r NEO4J_URI

if [ -z "$NEO4J_URI" ]; then
    echo "❌ 未输入Neo4j URI，使用默认值"
    NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
fi

# 添加环境变量
echo "添加 NEO4J_URI..."
echo "$NEO4J_URI" | vercel env add NEO4J_URI production

echo "添加 NEO4J_USERNAME..."
echo "neo4j" | vercel env add NEO4J_USERNAME production

echo "添加 NEO4J_PASSWORD..."
echo "Bt-iEdlUwkUHukW4x4yiGbKM0t64n8_l0eWNeN_IwSE" | vercel env add NEO4J_PASSWORD production

echo ""
echo "✅ 环境变量修复完成！"
echo ""
echo "🚀 现在重新部署项目:"
echo "   vercel --prod"
echo ""
echo "📋 验证环境变量:"
echo "   vercel env ls"
