# Vercel部署指南

## 🚀 快速部署

### 1. 准备工作

#### 1.1 设置Neo4j AuraDB
1. 访问 [Neo4j AuraDB](https://console.neo4j.io/)
2. 创建免费实例
3. 获取连接信息：
   - URI: `neo4j+s://xxxxx.databases.neo4j.io`
   - Username: `neo4j`
   - Password: `your-password`

#### 1.2 安装Vercel CLI
```bash
npm install -g vercel
```

### 2. 部署步骤

#### 2.1 克隆项目
```bash
git clone <your-repo-url>
cd 英语知识图库
```

#### 2.2 登录Vercel
```bash
vercel login
```

#### 2.3 设置环境变量
在Vercel Dashboard中设置以下环境变量：
- `NEO4J_URI`: 您的Neo4j AuraDB URI
- `NEO4J_USERNAME`: 您的Neo4j用户名
- `NEO4J_PASSWORD`: 您的Neo4j密码

#### 2.4 部署
```bash
./deploy.sh
```

或者手动部署：
```bash
vercel --prod
```

### 3. 初始化数据库

部署完成后，需要初始化数据库：

1. 访问您的Vercel应用URL
2. 访问 `/api/init-database` 端点来初始化数据库
3. 或者运行初始化脚本

### 4. 功能特性

✅ **已支持的功能**：
- 知识点管理
- 题目标注
- AI智能推荐
- 数据分析
- 前端界面

⚠️ **注意事项**：
- 使用Neo4j AuraDB云服务
- 无服务器函数有执行时间限制
- 静态文件通过CDN分发

### 5. 故障排除

#### 5.1 数据库连接问题
- 检查环境变量是否正确设置
- 确认Neo4j AuraDB实例正在运行
- 检查网络连接

#### 5.2 函数超时
- Vercel免费版函数执行时间限制为10秒
- 考虑升级到Pro版（60秒限制）

#### 5.3 静态文件问题
- 确保前端文件在 `frontend/` 目录下
- 检查 `vercel.json` 配置

### 6. 监控和维护

- 使用Vercel Dashboard监控应用状态
- 查看函数日志排查问题
- 定期备份Neo4j数据库

## 📞 支持

如有问题，请查看：
- [Vercel文档](https://vercel.com/docs)
- [Neo4j AuraDB文档](https://neo4j.com/docs/aura/)
- 项目GitHub Issues
