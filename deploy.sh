#!/bin/bash

echo "🚀 开始部署到Vercel..."

# 1. 安装Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "📦 安装Vercel CLI..."
    npm install -g vercel
fi

# 2. 登录Vercel
echo "🔐 登录Vercel..."
vercel login

# 3. 设置环境变量
echo "⚙️ 设置环境变量..."
echo "请确保在Vercel Dashboard中设置以下环境变量："
echo "- NEO4J_URI: 您的Neo4j AuraDB连接URI"
echo "- NEO4J_USERNAME: 您的Neo4j用户名"
echo "- NEO4J_PASSWORD: 您的Neo4j密码"

# 4. 部署
echo "🚀 开始部署..."
vercel --prod

echo "✅ 部署完成！"
echo "🌐 您的应用将在 https://your-app-name.vercel.app 上运行"
