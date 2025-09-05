# Vercel Dashboard 部署指南

## 问题解决
由于项目名称包含中文字符，Vercel CLI 无法正常部署。请通过 Vercel Dashboard 手动部署。

## 部署步骤

### 1. 访问 Vercel Dashboard
- 打开 https://vercel.com/dashboard
- 点击 "New Project"

### 2. 连接 GitHub 仓库
- 选择 "Import Git Repository"
- 找到并选择 `DetachedRepoForChao/englishGraph`
- 点击 "Import"

### 3. 配置项目
- **Project Name**: `english-knowledge-graph`
- **Framework Preset**: `Other`
- **Root Directory**: 保持默认
- **Build Command**: 留空
- **Output Directory**: 留空

### 4. 设置环境变量
在部署前，先设置环境变量：

| 变量名 | 值 | 类型 |
|--------|-----|------|
| NEO4J_URI | neo4j+s://4620a4e5.databases.neo4j.io | Plain Text |
| NEO4J_USERNAME | neo4j | Plain Text |
| NEO4J_PASSWORD | Bt-iEdlUwkUHukW4x4yiGbKM0t64n8_l0eWNeN_IwSE | Plain Text |

**重要**: 必须选择 "Plain Text"，不要选择 "Secret"

### 5. 部署
- 点击 "Deploy"
- 等待部署完成

### 6. 初始化数据库
部署完成后，访问：
```
https://your-project-name.vercel.app/api/init-database
```

### 7. 测试应用
访问：
```
https://your-project-name.vercel.app
```

## 常见问题

### Q: 环境变量设置后还是报错？
A: 确保选择 "Plain Text" 而不是 "Secret"，然后重新部署。

### Q: 项目名称无效？
A: 只使用字母、数字和连字符，不要使用中文字符。

### Q: 部署失败？
A: 检查 vercel.json 配置是否正确，确保所有文件都已推送到 GitHub。

## 验证部署
1. 访问应用首页，应该能看到知识图谱界面
2. 测试题目标注功能
3. 检查数据库连接是否正常
