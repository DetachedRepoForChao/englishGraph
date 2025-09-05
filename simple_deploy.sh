#!/bin/bash

echo "🚀 简化Vercel部署脚本"

# 确保所有文件都已提交
echo "📝 提交所有更改..."
git add .
git commit -m "Deploy to Vercel with fixed environment variables" || echo "No changes to commit"

# 推送到GitHub
echo "📤 推送到GitHub..."
git push origin main

echo "✅ 代码已推送到GitHub"
echo ""
echo "🔧 接下来请手动操作："
echo "1. 访问 https://vercel.com/dashboard"
echo "2. 找到您的项目"
echo "3. 进入 Settings → Environment Variables"
echo "4. 删除所有 NEO4J_* 变量"
echo "5. 添加以下环境变量（选择 Plain Text）："
echo "   NEO4J_URI = neo4j+s://4620a4e5.databases.neo4j.io"
echo "   NEO4J_USERNAME = neo4j"
echo "   NEO4J_PASSWORD = Bt-iEdlUwkUHukW4x4yiGbKM0t64n8_l0eWNeN_IwSE"
echo "6. 重新部署项目"
echo ""
echo "🎯 部署完成后，访问 /api/init-database 初始化数据库"
