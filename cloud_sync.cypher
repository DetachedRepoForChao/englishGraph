// Neo4j云端数据库同步脚本
// 数据库URI: neo4j+s://383b0a61.databases.neo4j.io
// 用户名: neo4j
// 密码: AYD98-e0kiI3v_sshk3yLWSEkXg-bzL5E3SW0DnrYCI

// ============================================
// 第一部分：创建核心知识点
// ============================================

// 1. 创建英语语法根节点
MERGE (kp:KnowledgePoint {name: '英语语法'})
SET kp.id = 'kp_115430',
    kp.description = '英语语法知识点的根节点',
    kp.difficulty = 'medium',
    kp.grade_levels = ['小学', '初中', '高中'],
    kp.learning_objectives = ['掌握英语语法基础', '理解语法规则'],
    kp.source = 'system';

// 2. 创建动词时态节点
MERGE (kp:KnowledgePoint {name: '动词时态'})
SET kp.id = 'kp_573225',
    kp.description = '动词时态相关知识点',
    kp.difficulty = 'medium',
    kp.grade_levels = ['小学四年级', '小学五年级', '小学六年级', '初中'],
    kp.learning_objectives = ['掌握各种时态的用法', '理解时态的语法规则'],
    kp.source = 'system';

// 3. 创建句型结构节点
MERGE (kp:KnowledgePoint {name: '句型结构'})
SET kp.id = 'kp_222812',
    kp.description = '句型结构相关知识点',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中', '高中'],
    kp.learning_objectives = ['掌握各种句型结构', '理解句法规则'],
    kp.source = 'system';

// 4. 创建词类语法节点
MERGE (kp:KnowledgePoint {name: '词类语法'})
SET kp.id = 'kp_390008',
    kp.description = '词类语法相关知识点',
    kp.difficulty = 'medium',
    kp.grade_levels = ['小学', '初中', '高中'],
    kp.learning_objectives = ['掌握各种词类的用法', '理解词法规则'],
    kp.source = 'system';

// ============================================
// 第二部分：创建具体时态知识点
// ============================================

// 5. 一般现在时
MERGE (kp:KnowledgePoint {name: '一般现在时'})
SET kp.id = 'kp_588066',
    kp.description = '表示经常性、习惯性的动作或状态',
    kp.difficulty = 'easy',
    kp.grade_levels = ['小学三年级', '小学四年级', '小学五年级'],
    kp.learning_objectives = ['掌握一般现在时的基本用法', '理解第三人称单数变化规则'],
    kp.keywords = ['always', 'usually', 'often', 'sometimes', 'never', 'every day'],
    kp.source = 'system';

// 6. 现在进行时
MERGE (kp:KnowledgePoint {name: '现在进行时'})
SET kp.id = 'kp_605632',
    kp.description = '表示现在正在进行的动作',
    kp.difficulty = 'medium',
    kp.grade_levels = ['小学四年级', '小学五年级', '小学六年级'],
    kp.learning_objectives = ['掌握现在进行时的构成', '理解现在进行时的使用场景'],
    kp.keywords = ['look', 'listen', 'now', 'right now', 'at the moment'],
    kp.source = 'system';

// 7. 现在完成时
MERGE (kp:KnowledgePoint {name: '现在完成时'})
SET kp.id = 'kp_441152',
    kp.description = '表示过去发生的动作对现在造成的影响',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中一年级', '初中二年级', '初中三年级'],
    kp.learning_objectives = ['理解现在完成时的含义', '掌握过去分词的变化规则'],
    kp.keywords = ['already', 'yet', 'just', 'ever', 'never', 'since', 'for'],
    kp.source = 'system';

// 8. 一般过去时
MERGE (kp:KnowledgePoint {name: '一般过去时'})
SET kp.id = 'kp_2925',
    kp.description = '表示过去发生的动作或状态',
    kp.difficulty = 'easy',
    kp.grade_levels = ['小学四年级', '小学五年级', '小学六年级'],
    kp.learning_objectives = ['掌握一般过去时的用法', '理解动词过去式变化规则'],
    kp.keywords = ['yesterday', 'last week', 'last month', 'ago'],
    kp.source = 'system';

// ============================================
// 第三部分：创建重要语法结构
// ============================================

// 9. 情态动词 (关键)
MERGE (kp:KnowledgePoint {name: '情态动词'})
SET kp.id = 'kp_modal_verbs',
    kp.description = '情态动词表示说话人的态度、推测、能力、必要性等',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中二年级', '初中三年级', '高中一年级'],
    kp.learning_objectives = ['掌握情态动词的基本用法', '理解情态动词的推测用法'],
    kp.keywords = ['can', 'could', 'may', 'might', 'must', 'should', 'would', 'will', 'shall'],
    kp.source = 'enhanced';

// 10. 倒装句 (关键)
MERGE (kp:KnowledgePoint {name: '倒装句'})
SET kp.id = 'kp_inversion',
    kp.description = '倒装句是指将谓语动词或助动词提到主语之前的句子结构',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握部分倒装的结构', '理解完全倒装的使用场景'],
    kp.keywords = ['never', 'seldom', 'rarely', 'hardly', 'scarcely', 'barely', 'no sooner', 'not only'],
    kp.source = 'enhanced';

// 11. 虚拟语气 (关键)
MERGE (kp:KnowledgePoint {name: '虚拟语气'})
SET kp.id = 'kp_subjunctive',
    kp.description = '虚拟语气表示假设、愿望、建议等非真实的情况',
    kp.difficulty = 'hard',
    kp.grade_levels = ['高中一年级', '高中二年级', '高中三年级'],
    kp.learning_objectives = ['掌握虚拟语气的基本形式', '理解虚拟语气的使用场景'],
    kp.keywords = ['if', 'wish', 'would', 'could', 'should', 'were', 'had'],
    kp.source = 'enhanced';

// ============================================
// 第四部分：创建其他重要知识点
// ============================================

// 12. 被动语态
MERGE (kp:KnowledgePoint {name: '被动语态'})
SET kp.id = 'kp_199751',
    kp.description = '被动语态表示动作的承受者',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中二年级', '初中三年级'],
    kp.learning_objectives = ['掌握被动语态的构成', '理解被动语态的使用场景'],
    kp.keywords = ['by', 'be done', 'was done', 'were done'],
    kp.source = 'system';

// 13. 定语从句
MERGE (kp:KnowledgePoint {name: '定语从句'})
SET kp.id = 'kp_969701',
    kp.description = '定语从句用来修饰名词或代词',
    kp.difficulty = 'hard',
    kp.grade_levels = ['初中三年级', '高中一年级', '高中二年级'],
    kp.learning_objectives = ['掌握关系代词的用法', '理解定语从句的结构'],
    kp.keywords = ['who', 'which', 'that', 'whom', 'whose', 'where', 'when'],
    kp.source = 'system';

// 14. 宾语从句
MERGE (kp:KnowledgePoint {name: '宾语从句'})
SET kp.id = 'kp_980608',
    kp.description = '宾语从句在句中作宾语',
    kp.difficulty = 'medium',
    kp.grade_levels = ['初中二年级', '初中三年级'],
    kp.learning_objectives = ['掌握宾语从句的引导词', '理解宾语从句的语序'],
    kp.keywords = ['that', 'what', 'when', 'where', 'why', 'how', 'if', 'whether'],
    kp.source = 'system';

// ============================================
// 第五部分：建立层级关系
// ============================================

// 建立主要层级关系
MATCH (parent:KnowledgePoint {name: '英语语法'})
MATCH (child:KnowledgePoint {name: '动词时态'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '英语语法'})
MATCH (child:KnowledgePoint {name: '句型结构'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '英语语法'})
MATCH (child:KnowledgePoint {name: '词类语法'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

// 建立时态子关系
MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '一般现在时'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '现在进行时'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '现在完成时'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '一般过去时'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '虚拟语气'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

// 建立语法结构关系
MATCH (parent:KnowledgePoint {name: '词类语法'})
MATCH (child:KnowledgePoint {name: '情态动词'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '句型结构'})
MATCH (child:KnowledgePoint {name: '倒装句'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '句型结构'})
MATCH (child:KnowledgePoint {name: '定语从句'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '句型结构'})
MATCH (child:KnowledgePoint {name: '宾语从句'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {name: '动词时态'})
MATCH (child:KnowledgePoint {name: '被动语态'})
MERGE (parent)-[:HAS_SUB_POINT]->(child);

// ============================================
// 第六部分：验证同步结果
// ============================================

// 验证关键知识点是否创建成功
MATCH (kp:KnowledgePoint) 
WHERE kp.name IN ['情态动词', '倒装句', '虚拟语气', '现在进行时', '现在完成时']
RETURN kp.name as name, kp.id as id, kp.difficulty as difficulty
ORDER BY kp.name;

// 统计知识点总数
MATCH (kp:KnowledgePoint) 
RETURN count(kp) as total_knowledge_points;

// 统计层级关系总数
MATCH ()-[:HAS_SUB_POINT]->() 
RETURN count(*) as total_relationships;
