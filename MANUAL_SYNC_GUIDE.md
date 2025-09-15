# Neo4j云端数据库手动同步指南

## 连接信息
- **数据库URI**: `neo4j+s://383b0a61.databases.neo4j.io`
- **用户名**: `neo4j`
- **密码**: `AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI`

## 操作步骤

### 1. 登录Neo4j AuraDB控制台
1. 访问 [https://console.neo4j.io/](https://console.neo4j.io/)
2. 使用您的Neo4j账号登录
3. 找到您的数据库实例并点击"Open"
4. 进入Neo4j Browser

### 2. 执行同步脚本

#### 方法一：直接复制粘贴Cypher语句

在Neo4j Browser中依次执行以下Cypher语句：

```cypher
// 1. 创建英语语法根节点
MERGE (kp:KnowledgePoint {name: '英语语法'})
SET kp.id = 'kp_115430',
    kp.description = '英语语法知识点的根节点',
    kp.difficulty = 'medium',
    kp.grade_levels = ['小学', '初中', '高中'],
    kp.learning_objectives = ['掌握英语语法基础', '理解语法规则'],
    kp.source = 'system';
```

```cypher
// 2. 创建情态动词知识点 (关键)
MERGE (kp:KnowledgePoint {name: '情态动词'})
SET kp.id = 'kp_modal_verbs',
    kp.description = '情态动词表示说话人的态度、推测、能力、必要性等',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中二年级', '初中三年级', '高中一年级'],
    kp.learning_objectives = ['掌握情态动词的基本用法', '理解情态动词的推测用法'],
    kp.keywords = ['can', 'could', 'may', 'might', 'must', 'should', 'would', 'will', 'shall'],
    kp.source = 'enhanced';
```

```cypher
// 3. 创建倒装句知识点 (关键)
MERGE (kp:KnowledgePoint {name: '倒装句'})
SET kp.id = 'kp_inversion',
    kp.description = '倒装句是指将谓语动词或助动词提到主语之前的句子结构',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握部分倒装的结构', '理解完全倒装的使用场景'],
    kp.keywords = ['never', 'seldom', 'rarely', 'hardly', 'scarcely', 'barely', 'no sooner', 'not only'],
    kp.source = 'enhanced';
```

```cypher
// 4. 创建虚拟语气知识点 (关键)
MERGE (kp:KnowledgePoint {name: '虚拟语气'})
SET kp.id = 'kp_subjunctive',
    kp.description = '虚拟语气表示假设、愿望、建议等非真实的情况',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握虚拟语气的基本形式', '理解虚拟语气的使用场景'],
    kp.keywords = ['if', 'wish', 'would', 'could', 'should', 'were', 'had'],
    kp.source = 'enhanced';
```

```cypher
// 5. 创建现在进行时
MERGE (kp:KnowledgePoint {name: '现在进行时'})
SET kp.id = 'kp_605632',
    kp.description = '表示现在正在进行的动作',
    kp.difficulty = 'medium',
    kp.grade_levels = ['小学四年级', '小学五年级', '小学六年级'],
    kp.learning_objectives = ['掌握现在进行时的构成', '理解现在进行时的使用场景'],
    kp.keywords = ['look', 'listen', 'now', 'right now', 'at the moment'],
    kp.source = 'system';
```

```cypher
// 6. 创建现在完成时
MERGE (kp:KnowledgePoint {name: '现在完成时'})
SET kp.id = 'kp_441152',
    kp.description = '表示过去发生的动作对现在造成的影响',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中一年级', '初中二年级', '初中三年级'],
    kp.learning_objectives = ['理解现在完成时的含义', '掌握过去分词的变化规则'],
    kp.keywords = ['already', 'yet', 'just', 'ever', 'never', 'since', 'for'],
    kp.source = 'system';
```

```cypher
// 7. 创建一般现在时
MERGE (kp:KnowledgePoint {name: '一般现在时'})
SET kp.id = 'kp_588066',
    kp.description = '表示经常性、习惯性的动作或状态',
    kp.difficulty = 'easy',
    kp.grade_levels = ['小学三年级', '小学四年级', '小学五年级'],
    kp.learning_objectives = ['掌握一般现在时的基本用法', '理解第三人称单数变化规则'],
    kp.keywords = ['always', 'usually', 'often', 'sometimes', 'never', 'every day'],
    kp.source = 'system';
```

```cypher
// 8. 创建词类语法节点
MERGE (kp:KnowledgePoint {name: '词类语法'})
SET kp.id = 'kp_390008',
    kp.description = '词类语法相关知识点',
    kp.difficulty = 'medium',
    kp.grade_levels = ['小学', '初中', '高中'],
    kp.learning_objectives = ['掌握各种词类的用法', '理解词法规则'],
    kp.source = 'system';
```

```cypher
// 9. 创建句型结构节点
MERGE (kp:KnowledgePoint {name: '句型结构'})
SET kp.id = 'kp_222812',
    kp.description = '句型结构相关知识点',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中', '高中'],
    kp.learning_objectives = ['掌握各种句型结构', '理解句法规则'],
    kp.source = 'system';
```

```cypher
// 10. 创建动词时态节点
MERGE (kp:KnowledgePoint {name: '动词时态'})
SET kp.id = 'kp_573225',
    kp.description = '动词时态相关知识点',
    kp.difficulty = 'medium',
    kp.grade_levels = ['小学四年级', '小学五年级', '小学六年级', '初中'],
    kp.learning_objectives = ['掌握各种时态的用法', '理解时态的语法规则'],
    kp.source = 'system';
```

```cypher
// 11. 建立层级关系 - 情态动词
MATCH (parent:KnowledgePoint {name: '词类语法'})
MATCH (child:KnowledgePoint {name: '情态动词'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

```cypher
// 12. 建立层级关系 - 倒装句
MATCH (parent:KnowledgePoint {name: '句型结构'})
MATCH (child:KnowledgePoint {name: '倒装句'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

```cypher
// 13. 建立层级关系 - 虚拟语气
MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '虚拟语气'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

```cypher
// 14. 建立层级关系 - 主要节点
MATCH (parent:KnowledgePoint {name: '英语语法'})
MATCH (child:KnowledgePoint {name: '词类语法'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '英语语法'})
MATCH (child:KnowledgePoint {name: '句型结构'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '英语语法'})
MATCH (child:KnowledgePoint {name: '动词时态'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

```cypher
// 15. 建立时态子关系
MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '现在进行时'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '现在完成时'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '一般现在时'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);
```

### 3. 验证同步结果

```cypher
// 验证关键知识点是否创建成功
MATCH (kp:KnowledgePoint) 
WHERE kp.name IN ['情态动词', '倒装句', '虚拟语气', '现在进行时', '现在完成时']
RETURN kp.name as name, kp.id as id, kp.difficulty as difficulty
ORDER BY kp.name;
```

预期结果应该显示：
- 情态动词 (kp_modal_verbs)
- 倒装句 (kp_inversion)  
- 虚拟语气 (kp_subjunctive)
- 现在进行时 (kp_605632)
- 现在完成时 (kp_441152)

```cypher
// 统计知识点总数
MATCH (kp:KnowledgePoint) 
RETURN count(kp) as total_knowledge_points;
```

```cypher
// 统计层级关系总数
MATCH ()-[:HAS_SUB_POINT]->() 
RETURN count(*) as total_relationships;
```

### 4. 测试API功能

同步完成后，测试以下API调用：

```bash
# 测试情态动词识别
curl -X POST "https://english-knowledge-graph-75dzfwqux-chao-wangs-projects-dfded257.vercel.app/api/annotation/suggest" \
  -H "Content-Type: application/json" \
  -d '{
    "question_content": "You must finish your homework before going out.",
    "question_type": "选择题"
  }'
```

```bash
# 测试倒装句识别
curl -X POST "https://english-knowledge-graph-75dzfwqux-chao-wangs-projects-dfded257.vercel.app/api/annotation/suggest" \
  -H "Content-Type: application/json" \
  -d '{
    "question_content": "Never have I seen such a beautiful sunset.",
    "question_type": "选择题"
  }'
```

```bash
# 测试基础语法识别
curl -X POST "https://english-knowledge-graph-75dzfwqux-chao-wangs-projects-dfded257.vercel.app/api/annotation/suggest" \
  -H "Content-Type: application/json" \
  -d '{
    "question_content": "Look! The children are playing in the playground.",
    "question_type": "选择题"
  }'
```

### 5. 预期结果

同步成功后，应该看到：

1. **情态动词识别** ✅
   - 输入: "You must finish your homework before going out."
   - 预期输出: 情态动词 (置信度 > 0.8)

2. **倒装句识别** ✅  
   - 输入: "Never have I seen such a beautiful sunset."
   - 预期输出: 倒装句 (置信度 > 0.8, 排第一位)

3. **基础语法识别** ✅
   - 输入: "Look! The children are playing in the playground."
   - 预期输出: 现在进行时 (置信度 > 0.5)

## 故障排除

如果测试失败：

1. **检查知识点是否创建成功**
   ```cypher
   MATCH (kp:KnowledgePoint {name: '情态动词'}) RETURN kp;
   MATCH (kp:KnowledgePoint {name: '倒装句'}) RETURN kp;
   ```

2. **检查层级关系**
   ```cypher
   MATCH (p)-[:HAS_SUB_POINT]->(c) 
   WHERE c.name IN ['情态动词', '倒装句', '虚拟语气']
   RETURN p.name as parent, c.name as child;
   ```

3. **重新部署Vercel应用**
   ```bash
   vercel --prod
   ```

4. **等待缓存刷新**
   - 等待5-10分钟后重新测试
   - 云端数据库和API之间可能有缓存延迟

## 完成标志

当所有测试都通过时，您应该看到：
- ✅ 情态动词正确识别
- ✅ 倒装句优先级最高
- ✅ 基础语法功能正常
- ✅ 云端数据库包含所有必要知识点
