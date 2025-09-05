#!/bin/bash

echo "🚀 部署英文版K12英语知识图谱系统"

# 确保所有文件都已提交
echo "📝 提交所有更改..."
git add .
git commit -m "Deploy English version to Vercel" || echo "No changes to commit"

# 推送到GitHub
echo "📤 推送到GitHub..."
git push origin main

echo "✅ 代码已推送到GitHub"
echo ""
echo "🔧 接下来请通过Vercel Dashboard操作："
echo "1. 访问 https://vercel.com/dashboard"
echo "2. 点击 'New Project'"
echo "3. 选择 'Import Git Repository'"
echo "4. 选择 'DetachedRepoForChao/englishGraph'"
echo "5. 项目名称设置为: english-knowledge-graph"
echo "6. 框架选择: Other"
echo "7. 设置环境变量（Plain Text）："
echo "   NEO4J_URI = neo4j+s://4620a4e5.databases.neo4j.io"
echo "   NEO4J_USERNAME = neo4j"
echo "   NEO4J_PASSWORD = Bt-iEdlUwkUHukW4x4yiGbKM0t64n8_l0eWNeN_IwSE"
echo "8. 点击 'Deploy'"
echo ""
echo "🎯 部署完成后，访问 /api/init-database 初始化数据库"
