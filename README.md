# K12 English Knowledge Graph System

基于Neo4j图数据库的K12英语题库智能标注与分析系统，实现了从基础知识图谱构建到智能应用的完整流程。

## 🎯 系统特性

### 四层架构设计
1. **知识图谱构建层** - 定义Schema、知识抽取、图数据存储
2. **智能标注层** - NLP辅助标注、人工审核标注
3. **数据分析层** - 学情分析、知识关联分析、可视化展示
4. **智能应用层** - 精准检索、个性化推荐、学习路径规划

### 核心功能
- ✅ **知识点管理** - 支持知识点的增删改查、层级关系管理
- ✅ **智能标注** - NLP辅助推荐知识点，提高标注效率
- ✅ **题库管理** - 支持多种题型的录入和管理
- ✅ **数据分析** - 知识点覆盖分析、难度分布、关联分析
- ✅ **学情诊断** - 基于答题记录分析薄弱知识点
- ✅ **学习路径推荐** - 基于知识图谱的个性化学习路径

## 🏗️ 技术架构

### 后端技术栈
- **Web框架**: FastAPI
- **图数据库**: Neo4j
- **NLP处理**: jieba, scikit-learn
- **数据处理**: pandas, numpy

### 前端技术栈
- **基础技术**: HTML5, CSS3, JavaScript
- **UI框架**: Bootstrap 5
- **图标库**: Font Awesome

### 数据模型
```
实体类型:
- KnowledgePoint (知识点)
- Question (题目)
- Textbook (教材)
- Chapter (章节)

关系类型:
- HAS_SUB_POINT (包含关系)
- TESTS (考查关系)
- BELONGS_TO (归属关系)
- REQUIRES (前置要求关系)
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Neo4j 4.0+
- 8GB+ 内存推荐

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd english-knowledge-graph
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置Neo4j数据库**
```bash
# 安装Neo4j Desktop或Docker版本
# 创建数据库实例，设置用户名密码

# 复制配置文件
cp config.env.example config.env

# 编辑配置文件
vim config.env
```

配置示例：
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

4. **初始化数据库**
```bash
python scripts/init_database.py
```

5. **加载示例数据**
```bash
python scripts/load_sample_data.py
```

6. **启动系统**
```bash
python run.py
```

7. **访问系统**
- 主界面: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📖 使用指南

### 1. 知识点管理
- 在"知识点管理"标签页中添加新的知识点
- 支持设置知识点的学段、难度等属性
- 可以建立知识点之间的层级关系

### 2. 智能标注
- 在"智能标注"标签页中录入题目
- 点击"AI智能推荐"获取知识点建议
- 手动调整权重并提交标注结果

### 3. 数据分析
- 在"数据分析"标签页查看各种统计图表
- 支持知识点覆盖率、题目分布等分析
- 可视化知识图谱结构

## 🔧 高级配置

### 自定义知识点体系
编辑 `backend/models/schema.py` 中的 `SAMPLE_KNOWLEDGE_POINTS` 来定义你的知识点体系。

### NLP模型优化
在 `backend/services/nlp_service.py` 中调整关键词匹配规则和权重计算方法。

### 数据库优化
```cypher
// 创建额外的索引提升查询性能
CREATE INDEX question_content IF NOT EXISTS FOR (q:Question) ON (q.content)
CREATE INDEX knowledge_point_level IF NOT EXISTS FOR (kp:KnowledgePoint) ON (kp.level)
```

## 📊 API接口

### 知识点相关
- `GET /api/knowledge/search?keyword={keyword}` - 搜索知识点
- `POST /api/knowledge/` - 创建知识点
- `GET /api/knowledge/{id}` - 获取知识点详情

### 题目相关
- `POST /api/questions/` - 创建题目
- `POST /api/questions/{id}/knowledge/{kp_id}` - 关联知识点

### 标注相关
- `POST /api/annotation/suggest` - 获取知识点推荐
- `POST /api/annotation/submit` - 提交标注结果

### 分析相关
- `GET /api/analytics/coverage` - 知识点覆盖分析
- `GET /api/analytics/difficulty-distribution` - 难度分布
- `POST /api/analytics/weak-points` - 薄弱点分析

详细API文档请访问: http://localhost:8000/docs

## 🗂️ 项目结构

```
english-knowledge-graph/
├── backend/                 # 后端代码
│   ├── api/                # API路由
│   │   ├── routes/         # 具体路由实现
│   │   └── main.py         # FastAPI主应用
│   ├── models/             # 数据模型
│   │   └── schema.py       # 图数据库Schema
│   └── services/           # 业务逻辑服务
│       ├── database.py     # 数据库操作
│       ├── nlp_service.py  # NLP处理
│       └── analytics_service.py # 数据分析
├── frontend/               # 前端代码
│   ├── static/            # 静态资源
│   │   ├── css/          # 样式文件
│   │   └── js/           # JavaScript文件
│   └── templates/         # HTML模板
├── data/                  # 数据文件
│   └── sample_questions/  # 示例题目
├── scripts/               # 工具脚本
│   ├── init_database.py   # 数据库初始化
│   └── load_sample_data.py # 示例数据加载
├── requirements.txt       # Python依赖
├── run.py                # 启动脚本
└── README.md             # 项目说明
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 开发计划

- [ ] 支持更多NLP模型（BERT、GPT等）
- [ ] 增加知识图谱可视化组件
- [ ] 支持多用户和权限管理
- [ ] 增加题目自动生成功能
- [ ] 支持更多题型和格式
- [ ] 移动端适配

## 🐛 常见问题

### Q: Neo4j连接失败怎么办？
A: 请检查Neo4j服务是否启动，配置文件中的连接信息是否正确。

### Q: 如何添加自定义知识点？
A: 可以通过前端界面添加，或者修改示例数据文件重新导入。

### Q: 系统性能如何优化？
A: 建议为常用查询字段创建索引，适当调整Neo4j内存配置。

## 📄 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 邮箱: your-email@example.com
- 项目Issues: [GitHub Issues](https://github.com/your-repo/issues)

---

⭐ 如果这个项目对你有帮助，请给一个Star！
