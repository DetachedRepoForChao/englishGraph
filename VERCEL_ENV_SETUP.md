# Vercel环境变量设置指南

## 🚨 问题
```
Environment Variable "NEO4J_URI" references Secret "neo4j_uri", which does not exist.
```

## 🔧 解决方案

### 步骤1：访问Vercel项目设置
1. 打开 [vercel.com](https://vercel.com)
2. 登录您的账户
3. 选择您的项目：`englishGraph`
4. 点击 "Settings" 标签

### 步骤2：设置环境变量
1. 在左侧菜单中点击 "Environment Variables"
2. 点击 "Add New" 按钮
3. 添加以下三个环境变量：

#### 环境变量1：
- **Name**: `NEO4J_URI`
- **Value**: `neo4j+s://your-instance.databases.neo4j.io`
- **Environment**: 选择 "Production", "Preview", "Development"

#### 环境变量2：
- **Name**: `NEO4J_USERNAME`
- **Value**: `neo4j`
- **Environment**: 选择 "Production", "Preview", "Development"

#### 环境变量3：
- **Name**: `NEO4J_PASSWORD`
- **Value**: `Bt-iEdlUwkUHukW4x4yiGbKM0t64n8_l0eWNeN_IwSE`
- **Environment**: 选择 "Production", "Preview", "Development"

### 步骤3：重新部署
1. 点击 "Deployments" 标签
2. 找到最新的部署
3. 点击 "..." 菜单
4. 选择 "Redeploy"

### 步骤4：验证部署
1. 等待部署完成
2. 访问您的应用URL
3. 测试API端点：`https://your-app.vercel.app/api/health`

## 📝 重要提示

### 获取正确的Neo4j URI
1. 登录 [Neo4j AuraDB Console](https://console.neo4j.io/)
2. 选择您的数据库实例
3. 点击 "Connect" 按钮
4. 复制 "Connection URI"（应该类似：`neo4j+s://xxxxx.databases.neo4j.io`）

### 环境变量格式
确保环境变量值没有多余的空格或引号：
```
✅ 正确: neo4j+s://xxxxx.databases.neo4j.io
❌ 错误: "neo4j+s://xxxxx.databases.neo4j.io"
❌ 错误:  neo4j+s://xxxxx.databases.neo4j.io 
```

## 🎯 验证步骤

部署完成后，测试以下端点：
1. **健康检查**: `GET /api/health`
2. **初始化数据库**: `POST /api/init-database`
3. **知识点推荐**: `POST /api/annotation/suggest`

## 🆘 如果仍有问题

1. 检查环境变量是否正确设置
2. 确认Neo4j AuraDB实例正在运行
3. 查看Vercel函数日志排查问题
4. 确认网络连接正常
