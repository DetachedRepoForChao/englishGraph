# 手动Cypher同步指南

由于网络连接问题，请您手动在Neo4j AuraDB控制台中执行以下Cypher语句。

## 连接信息
- **URI**: `neo4j+s://383b0a61.databases.neo4j.io`
- **用户名**: `neo4j`
- **密码**: `AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI`

## 操作步骤

### 1. 登录Neo4j AuraDB控制台
1. 访问 [https://console.neo4j.io/](https://console.neo4j.io/)
2. 登录您的账号
3. 找到对应的数据库实例
4. 点击 "Open" 进入Neo4j Browser

### 2. 依次执行以下Cypher语句

#### 步骤1：创建情态动词知识点
```cypher
MERGE (kp:KnowledgePoint {name: '情态动词'})
SET kp.id = 'kp_modal_verbs',
    kp.description = '情态动词表示说话人的态度、推测、能力、必要性等',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中二年级', '初中三年级', '高中一年级'],
    kp.learning_objectives = ['掌握情态动词的基本用法', '理解情态动词的推测用法'],
    kp.keywords = ['can', 'could', 'may', 'might', 'must', 'should', 'would', 'will', 'shall'],
    kp.source = 'enhanced';
```

#### 步骤2：创建倒装句知识点
```cypher
MERGE (kp:KnowledgePoint {name: '倒装句'})
SET kp.id = 'kp_inversion',
    kp.description = '倒装句是指将谓语动词或助动词提到主语之前的句子结构',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握部分倒装的结构', '理解完全倒装的使用场景'],
    kp.keywords = ['never', 'seldom', 'rarely', 'hardly', 'scarcely', 'barely', 'no sooner', 'not only'],
    kp.source = 'enhanced';
```

#### 步骤3：创建虚拟语气知识点
```cypher
MERGE (kp:KnowledgePoint {name: '虚拟语气'})
SET kp.id = 'kp_subjunctive',
    kp.description = '虚拟语气表示假设、愿望、建议等非真实的情况',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握虚拟语气的基本形式', '理解虚拟语气的使用场景'],
    kp.keywords = ['if', 'wish', 'would', 'could', 'should', 'were', 'had'],
    kp.source = 'enhanced';
```

#### 步骤4：创建基础知识点
```cypher
MERGE (kp:KnowledgePoint {name: '英语语法'})
SET kp.id = 'kp_115430',
    kp.description = '英语语法知识点的根节点',
    kp.difficulty = 'medium',
    kp.source = 'system';
```

```cypher
MERGE (kp:KnowledgePoint {name: '词类语法'})
SET kp.id = 'kp_390008',
    kp.description = '词类语法相关知识点',
    kp.difficulty = 'medium',
    kp.source = 'system';
```

```cypher
MERGE (kp:KnowledgePoint {name: '句型结构'})
SET kp.id = 'kp_222812',
    kp.description = '句型结构相关知识点',
    kp.difficulty = 'medium',
    kp.source = 'system';
```

```cypher
MERGE (kp:KnowledgePoint {name: '动词时态'})
SET kp.id = 'kp_573225',
    kp.description = '动词时态相关知识点',
    kp.difficulty = 'medium',
    kp.source = 'system';
```

#### 步骤5：建立层级关系
```cypher
MATCH (parent:KnowledgePoint {name: '英语语法'})
MATCH (child:KnowledgePoint {name: '词类语法'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

```cypher
MATCH (parent:KnowledgePoint {name: '英语语法'})
MATCH (child:KnowledgePoint {name: '句型结构'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

```cypher
MATCH (parent:KnowledgePoint {name: '英语语法'})
MATCH (child:KnowledgePoint {name: '动词时态'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

```cypher
MATCH (parent:KnowledgePoint {name: '词类语法'})
MATCH (child:KnowledgePoint {name: '情态动词'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

```cypher
MATCH (parent:KnowledgePoint {name: '句型结构'})
MATCH (child:KnowledgePoint {name: '倒装句'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

```cypher
MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '虚拟语气'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

### 3. 验证同步结果

#### 验证关键知识点
```cypher
MATCH (kp:KnowledgePoint) 
WHERE kp.name IN ['情态动词', '倒装句', '虚拟语气']
RETURN kp.name as name, kp.id as id, kp.difficulty as difficulty
ORDER BY kp.name;
```

**预期结果**：
- 情态动词 (kp_modal_verbs, medium)
- 倒装句 (kp_inversion, hard)  
- 虚拟语气 (kp_subjunctive, hard)

#### 统计知识点总数
```cypher
MATCH (kp:KnowledgePoint) 
RETURN count(kp) as total_knowledge_points;
```

#### 统计关系总数
```cypher
MATCH ()-[:HAS_SUB_POINT]->() 
RETURN count(*) as total_relationships;
```

### 4. 测试API功能

同步完成后，在终端中测试：

```bash
# 测试情态动词识别
curl -X POST "https://english-knowledge-graph-75dzfwqux-chao-wangs-projects-dfded257.vercel.app/api/annotation/suggest" \
  -H "Content-Type: application/json" \
  -d '{
    "question_content": "You must finish your homework before going out.",
    "question_type": "选择题"
  }' | jq '.suggestions[0] | {name: .knowledge_point_name, confidence: .confidence}'
```

**预期结果**：情态动词 (置信度 > 0.8)

```bash
# 测试倒装句识别
curl -X POST "https://english-knowledge-graph-75dzfwqux-chao-wangs-projects-dfded257.vercel.app/api/annotation/suggest" \
  -H "Content-Type: application/json" \
  -d '{
    "question_content": "Never have I seen such a beautiful sunset.",
    "question_type": "选择题"
  }' | jq '.suggestions[0] | {name: .knowledge_point_name, confidence: .confidence}'
```

**预期结果**：倒装句 (置信度 > 0.8, 排第一位)

### 5. 使用测试脚本验证

执行完所有Cypher语句后，运行：

```bash
python3 test_api_after_sync.py
```

**预期结果**：所有4个测试都应该通过 ✅

## 完成标志

当您看到以下结果时，说明同步成功：

1. ✅ 所有Cypher语句执行无错误
2. ✅ 验证查询显示3个关键知识点
3. ✅ API测试显示情态动词识别正常
4. ✅ API测试显示倒装句优先级最高
5. ✅ 基础语法识别功能正常

## 故障排除

如果API测试失败：

1. **等待5-10分钟** - 数据库和API之间可能有缓存延迟
2. **重新运行测试脚本** - `python3 test_api_after_sync.py`
3. **检查知识点创建** - 重新执行验证查询
4. **重新部署应用** - `vercel --prod`

完成这些步骤后，您的K12英语知识图谱系统应该能够完美识别情态动词、倒装句等复杂语法结构！
