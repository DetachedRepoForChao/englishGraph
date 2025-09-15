
// 手动同步脚本 - 在Neo4j Browser中执行

// 1. 创建情态动词知识点
MERGE (kp:KnowledgePoint {name: '情态动词'})
SET kp.id = 'kp_modal_verbs',
    kp.description = '情态动词表示说话人的态度、推测、能力、必要性等',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中二年级', '初中三年级', '高中一年级'],
    kp.learning_objectives = ['掌握情态动词的基本用法', '理解情态动词的推测用法'],
    kp.keywords = ['can', 'could', 'may', 'might', 'must', 'should', 'would', 'will', 'shall'];

// 2. 创建倒装句知识点
MERGE (kp:KnowledgePoint {name: '倒装句'})
SET kp.id = 'kp_inversion',
    kp.description = '倒装句是指将谓语动词或助动词提到主语之前的句子结构',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握部分倒装的结构', '理解完全倒装的使用场景'],
    kp.keywords = ['never', 'seldom', 'rarely', 'hardly', 'scarcely', 'barely', 'no sooner', 'not only'];

// 3. 创建虚拟语气知识点
MERGE (kp:KnowledgePoint {name: '虚拟语气'})
SET kp.id = 'kp_subjunctive',
    kp.description = '虚拟语气表示假设、愿望、建议等非真实的情况',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握虚拟语气的基本形式', '理解虚拟语气的使用场景'],
    kp.keywords = ['if', 'wish', 'would', 'could', 'should', 'were', 'had'];

// 4. 建立层级关系 - 情态动词
MATCH (parent:KnowledgePoint {name: '词类语法'})
MATCH (child:KnowledgePoint {name: '情态动词'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

// 5. 建立层级关系 - 倒装句
MATCH (parent:KnowledgePoint {name: '句型结构'})
MATCH (child:KnowledgePoint {name: '倒装句'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

// 6. 建立层级关系 - 虚拟语气
MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '虚拟语气'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

// 7. 验证创建结果
MATCH (kp:KnowledgePoint) 
WHERE kp.name IN ['情态动词', '倒装句', '虚拟语气']
RETURN kp.name as name, kp.id as id
ORDER BY kp.name;
