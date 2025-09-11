# 🏗️ K12英语知识图谱系统架构图

## 📊 整体架构概览

```mermaid
graph TB
    subgraph "用户界面层 (Frontend)"
        A[知识点管理界面] 
        B[题目标注界面]
        C[数据分析界面]
        D[可视化界面]
    end
    
    subgraph "API网关层"
        E[FastAPI路由器]
    end
    
    subgraph "业务逻辑层 (Backend Services)"
        F[知识点服务]
        G[标注服务] 
        H[分析服务]
        I[可视化服务]
    end
    
    subgraph "AI模型层"
        J[AI Agent]
        K[NLP服务]
        L[协作智能服务]
        M[LabelLLM]
        N[MEGAnno]
    end
    
    subgraph "数据存储层"
        O[(Neo4j AuraDB)]
        P[知识点节点]
        Q[题目节点]
        R[关系边]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F
    E --> G
    E --> H
    E --> I
    
    F --> J
    G --> K
    G --> L
    H --> J
    I --> F
    
    L --> M
    L --> N
    K --> J
    
    F --> O
    G --> O
    H --> O
    I --> O
    
    O --> P
    O --> Q
    O --> R
```

## 🤖 AI模型架构详解

```mermaid
graph LR
    subgraph "输入层"
        A[题目文本输入]
    end
    
    subgraph "预处理层"
        B[文本清洗]
        C[题干提取]
        D[特征预处理]
    end
    
    subgraph "特征分析层"
        E[语言学特征分析<br/>LabelLLM]
        F[关键词匹配<br/>分析]
        G[题型识别<br/>分析]
    end
    
    subgraph "评分计算层"
        H[语言学权重<br/>40%]
        I[关键词权重<br/>35%]
        J[题型权重<br/>25%]
    end
    
    subgraph "协作验证层"
        K[MEGAnno<br/>多模态验证]
        L[协作融合<br/>算法]
    end
    
    subgraph "输出层"
        M[推荐结果<br/>置信度评分]
    end
    
    A --> B
    B --> C
    C --> D
    
    D --> E
    D --> F
    D --> G
    
    E --> H
    F --> I
    G --> J
    
    H --> L
    I --> L
    J --> L
    
    L --> K
    K --> M
```

## 📊 数据流程架构

```mermaid
sequenceDiagram
    participant U as 用户界面
    participant API as FastAPI
    participant AI as AI服务
    participant DB as Neo4j数据库
    participant Cache as 缓存层
    
    U->>API: 1. 提交题目标注请求
    API->>Cache: 2. 检查缓存
    
    alt 缓存命中
        Cache->>API: 3a. 返回缓存结果
    else 缓存未命中
        API->>AI: 3b. 调用AI推荐服务
        AI->>AI: 4. 语言学特征分析
        AI->>AI: 5. 关键词匹配分析
        AI->>AI: 6. 题型识别分析
        AI->>DB: 7. 查询知识点数据
        DB->>AI: 8. 返回知识点信息
        AI->>AI: 9. 综合评分计算
        AI->>API: 10. 返回推荐结果
        API->>Cache: 11. 更新缓存
    end
    
    API->>U: 12. 返回推荐结果
    U->>API: 13. 用户确认标注
    API->>DB: 14. 保存标注结果
    API->>U: 15. 确认保存成功
```

## 🗄️ 数据模型架构

```mermaid
erDiagram
    KNOWLEDGE_POINT {
        string id PK
        string name
        string level
        string difficulty
        string description
        array keywords
        datetime created_at
        datetime updated_at
    }
    
    QUESTION {
        string id PK
        text content
        array options
        string answer
        string difficulty
        string question_type
        string grade_level
        string source
        datetime created_at
    }
    
    ANNOTATION {
        string id PK
        string question_id FK
        string knowledge_point_id FK
        float confidence
        string method
        json reasoning
        string user_id
        datetime created_at
    }
    
    HIERARCHY {
        string parent_id FK
        string child_id FK
        float weight
        datetime created_at
    }
    
    KNOWLEDGE_POINT ||--o{ HIERARCHY : "parent"
    KNOWLEDGE_POINT ||--o{ HIERARCHY : "child"
    KNOWLEDGE_POINT ||--o{ ANNOTATION : "annotates"
    QUESTION ||--o{ ANNOTATION : "annotated_by"
    QUESTION }o--|| KNOWLEDGE_POINT : "TESTS"
```

## 🔧 部署架构

```mermaid
graph TB
    subgraph "开发环境"
        A[本地开发]
        B[Git仓库]
    end
    
    subgraph "CI/CD流水线"
        C[GitHub Actions]
        D[自动测试]
        E[代码检查]
    end
    
    subgraph "Vercel云平台"
        F[Serverless函数]
        G[静态资源CDN]
        H[环境变量管理]
    end
    
    subgraph "数据库服务"
        I[Neo4j AuraDB]
        J[自动备份]
        K[监控告警]
    end
    
    subgraph "监控运维"
        L[性能监控]
        M[错误追踪]
        N[日志分析]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    
    D --> F
    E --> F
    
    F --> G
    F --> H
    
    F --> I
    I --> J
    I --> K
    
    F --> L
    F --> M
    F --> N
```

## 🔄 AI模型训练流程

```mermaid
graph TD
    subgraph "数据准备阶段"
        A[原始题目数据]
        B[数据清洗]
        C[标注数据]
        D[特征工程]
    end
    
    subgraph "模型训练阶段"
        E[语言学特征提取]
        F[关键词模式学习]
        G[题型分类训练]
        H[权重优化]
    end
    
    subgraph "模型验证阶段"
        I[交叉验证]
        J[A/B测试]
        K[用户反馈收集]
        L[性能评估]
    end
    
    subgraph "模型部署阶段"
        M[模型打包]
        N[生产部署]
        O[监控反馈]
        P[持续优化]
    end
    
    A --> B
    B --> C
    C --> D
    
    D --> E
    D --> F
    D --> G
    E --> H
    F --> H
    G --> H
    
    H --> I
    I --> J
    J --> K
    K --> L
    
    L --> M
    M --> N
    N --> O
    O --> P
    
    P --> K
```

## 📊 系统性能监控架构

```mermaid
graph LR
    subgraph "数据采集层"
        A[API响应时间]
        B[数据库查询时间]
        C[AI模型推理时间]
        D[用户行为数据]
    end
    
    subgraph "数据处理层"
        E[实时流处理]
        F[批量数据处理]
        G[异常检测]
        H[趋势分析]
    end
    
    subgraph "存储层"
        I[时序数据库]
        J[日志存储]
        K[指标存储]
    end
    
    subgraph "可视化层"
        L[实时监控面板]
        M[性能报表]
        N[告警通知]
    end
    
    A --> E
    B --> E
    C --> E
    D --> F
    
    E --> G
    F --> H
    
    G --> I
    H --> J
    E --> K
    
    I --> L
    J --> M
    K --> L
    
    L --> N
    M --> N
```

## 🔐 安全架构

```mermaid
graph TB
    subgraph "网络安全层"
        A[HTTPS加密]
        B[API限流]
        C[CORS策略]
    end
    
    subgraph "应用安全层"
        D[输入验证]
        E[SQL注入防护]
        F[XSS防护]
        G[CSRF防护]
    end
    
    subgraph "数据安全层"
        H[数据加密]
        I[访问控制]
        J[审计日志]
    end
    
    subgraph "基础设施安全"
        K[环境变量保护]
        L[密钥管理]
        M[备份加密]
    end
    
    A --> D
    B --> D
    C --> D
    
    D --> H
    E --> H
    F --> H
    G --> H
    
    H --> K
    I --> K
    J --> L
    
    K --> M
    L --> M
```

## 📈 扩展性架构规划

```mermaid
graph TD
    subgraph "当前架构 v1.0"
        A[单体FastAPI应用]
        B[Neo4j单实例]
        C[Vercel Serverless]
    end
    
    subgraph "扩展架构 v2.0"
        D[微服务架构]
        E[Neo4j集群]
        F[容器化部署]
        G[API网关]
    end
    
    subgraph "未来架构 v3.0"
        H[云原生架构]
        I[多云部署]
        J[边缘计算]
        K[AI模型服务化]
    end
    
    A --> D
    B --> E
    C --> F
    
    D --> H
    E --> I
    F --> J
    G --> K
    
    style A fill:#e1f5fe
    style D fill:#f3e5f5
    style H fill:#e8f5e8
```

---

## 📝 架构说明

### 🎯 设计原则

1. **模块化设计**: 各层职责清晰，便于维护和扩展
2. **高可用性**: 云端部署，自动扩展和容错
3. **性能优化**: 多级缓存，数据库索引优化
4. **安全可靠**: 多层安全防护，数据加密存储
5. **易于扩展**: 微服务化，插件化架构

### 🔧 技术选型理由

| 技术组件 | 选型理由 |
|---------|----------|
| **FastAPI** | 高性能异步框架，自动API文档生成 |
| **Neo4j** | 图数据库，适合复杂关系查询 |
| **Vercel** | 无服务器部署，自动扩展 |
| **Bootstrap** | 快速响应式界面开发 |
| **Python** | 丰富的AI/ML生态系统 |

### 📊 性能指标

| 指标 | 目标值 | 当前值 |
|------|-------|-------|
| API响应时间 | < 500ms | ~200ms |
| 数据库查询 | < 100ms | ~50ms |
| AI推荐准确率 | > 80% | 85% |
| 系统可用性 | > 99% | 99.5% |

---

**💡 这个架构图展示了系统的完整技术栈和数据流，为开发者提供了清晰的技术路线图。**
