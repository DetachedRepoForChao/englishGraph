# 🚨 Vercel环境变量快速修复指南

## 问题
```
Environment Variable "NEO4J_URI" references Secret "neo4j_uri", which does not exist.
```

## ⚡ 快速解决步骤

### 步骤1：获取Neo4j URI
1. 访问 [Neo4j AuraDB Console](https://console.neo4j.io/)
2. 登录您的账户
3. 选择您的数据库实例
4. 点击 "Connect" 按钮
5. 复制 "Connection URI"（类似：`neo4j+s://xxxxx.databases.neo4j.io`）

### 步骤2：修复Vercel环境变量
1. 访问 [vercel.com](https://vercel.com)
2. 选择您的项目
3. 进入 **Settings** → **Environment Variables**
4. **删除** 现有的 `NEO4J_URI` 环境变量
5. **添加** 新的环境变量：

| 名称 | 值 | 环境 |
|------|-----|------|
| `NEO4J_URI` | `neo4j+s://your-actual-uri.databases.neo4j.io` | Production, Preview, Development |
| `NEO4J_USERNAME` | `neo4j` | Production, Preview, Development |
| `NEO4J_PASSWORD` | `Bt-iEdlUwkUHukW4x4yiGbKM0t64n8_l0eWNeN_IwSE` | Production, Preview, Development |

### 步骤3：重新部署
1. 进入 **Deployments** 标签
2. 点击最新部署的 **"..."** 菜单
3. 选择 **"Redeploy"**

### 步骤4：验证
部署完成后，访问：
- 健康检查：`https://your-app.vercel.app/api/health`
- 初始化数据库：`https://your-app.vercel.app/api/init-database`

## ⚠️ 重要提示

1. **不要使用Secret引用**：直接输入值，不要选择 "Use Secret"
2. **确保URI正确**：必须是 `neo4j+s://` 开头的完整URI
3. **选择所有环境**：确保环境变量在所有环境中都可用

## 🆘 如果仍有问题

1. 检查环境变量值是否正确
2. 确认Neo4j AuraDB实例正在运行
3. 查看Vercel函数日志
4. 尝试删除所有环境变量后重新添加
