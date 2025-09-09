// K12英语知识图谱系统 - 完整数据同步脚本
// 从本地数据库导出，用于同步到Neo4j AuraDB
// 导出时间: 2025-09-09 15:45:07
// 数据统计: 11个知识点, 23道题目, 9个关系

// ===== 第1步: 清空数据库 =====
MATCH (n) DETACH DELETE n;

// ===== 第2步: 创建约束 =====
CREATE CONSTRAINT knowledge_point_id IF NOT EXISTS FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE;
CREATE CONSTRAINT question_id IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE;

// ===== 第3步: 创建知识点 =====

CREATE (kp_kp_588066:KnowledgePoint {
    id: 'kp_588066',
    name: '一般现在时',
    description: '表示经常性、习惯性的动作或状态',
    level: '小学四年级',
    difficulty: 'easy',
    keywords: ["一般现在时", "present simple"]
});

CREATE (kp_kp_2925:KnowledgePoint {
    id: 'kp_2925',
    name: '一般过去时',
    description: '表示过去发生的动作或状态',
    level: '小学五年级',
    difficulty: 'easy',
    keywords: ["一般过去时", "past simple"]
});

CREATE (kp_kp_472230:KnowledgePoint {
    id: 'kp_472230',
    name: '介词',
    description: '表示名词、代词等与句中其他词的关系的词',
    level: '初中一年级',
    difficulty: 'medium',
    keywords: ["in", "on", "at", "by", "for", "with", "from", "to", "of", "about", "under", "over", "above", "below", "between", "among", "through", "interested in", "good at", "afraid of", "proud of", "famous for", "介词", "前置词", "preposition", "介词短语", "固定搭配", "_____ in", "_____ on", "_____ at", "_____ by", "_____ for", "A) in B) on C) at D) by", "介词选择", "介词填空"]
});

CREATE (kp_kp_573225:KnowledgePoint {
    id: 'kp_573225',
    name: '动词时态',
    description: '动词的各种时态形式',
    level: '小学四年级',
    difficulty: 'medium',
    keywords: ["动词", "时态", "tense"]
});

CREATE (kp_kp_969701:KnowledgePoint {
    id: 'kp_969701',
    name: '定语从句',
    description: '用来修饰名词或代词的从句',
    level: '初中二年级',
    difficulty: 'hard',
    keywords: ["who", "which", "that", "whom", "whose", "where", "when", "关系代词", "先行词"]
});

CREATE (kp_kp_980608:KnowledgePoint {
    id: 'kp_980608',
    name: '宾语从句',
    description: '在句子中作宾语的从句',
    level: '初中二年级',
    difficulty: 'hard',
    keywords: ["that", "whether", "if", "what", "when", "where", "why", "how", "宾语从句", "引导词"]
});

CREATE (kp_kp_793115:KnowledgePoint {
    id: 'kp_793115',
    name: '比较级和最高级',
    description: '形容词和副词的比较形式',
    level: '小学五年级',
    difficulty: 'medium',
    keywords: ["than", "more", "most", "-er", "-est", "better", "best", "比较级", "最高级"]
});

CREATE (kp_kp_441152:KnowledgePoint {
    id: 'kp_441152',
    name: '现在完成时',
    description: '表示过去发生的动作对现在造成的影响或结果',
    level: '初中一年级',
    difficulty: 'medium',
    keywords: ["have", "has", "already", "yet", "just", "ever", "never", "since", "for"]
});

CREATE (kp_kp_605632:KnowledgePoint {
    id: 'kp_605632',
    name: '现在进行时',
    description: '表示现在正在进行的动作',
    level: '小学五年级',
    difficulty: 'medium',
    keywords: ["现在进行时", "present continuous"]
});

CREATE (kp_kp_115430:KnowledgePoint {
    id: 'kp_115430',
    name: '英语语法',
    description: '英语语法基础知识',
    level: '小学三年级',
    difficulty: 'medium',
    keywords: ["语法", "grammar"]
});

CREATE (kp_kp_199751:KnowledgePoint {
    id: 'kp_199751',
    name: '被动语态',
    description: '表示主语是动作的承受者',
    level: '初中二年级',
    difficulty: 'hard',
    keywords: ["be动词", "过去分词", "by", "was", "were", "is", "are", "被动", "passive"]
});

// ===== 第4步: 创建题目 =====

CREATE (q_q_182690:Question {
    id: 'q_182690',
    content: 'I _____ to Beijing last summer vacation. A) go B) goes C) went D) will go',
    question_type: '选择题',
    options: ["go", "goes", "went", "will go"],
    answer: 'C',
    analysis: 'last summer vacation表示过去的时间，用一般过去时went',
    source: 'AI Agent测试题目',
    difficulty: 'easy'
});

CREATE (q_q_184500:Question {
    id: 'q_184500',
    content: 'This apple is _____ than that one. A) sweet B) sweeter C) sweetest D) the sweetest',
    question_type: '选择题',
    options: ["sweet", "sweeter", "sweetest", "the sweetest"],
    answer: 'B',
    analysis: '两者比较用比较级sweeter',
    source: 'AI Agent测试题目',
    difficulty: 'easy'
});

CREATE (q_q_2085:Question {
    id: 'q_2085',
    content: 'The windows _____ by the students yesterday. A) cleaned B) were cleaned C) are cleaned D) clean',
    question_type: '选择题',
    options: ["cleaned", "were cleaned", "are cleaned", "clean"],
    answer: 'B',
    analysis: '主语windows是动作的承受者，用被动语态，yesterday表示过去时间',
    source: 'AI Agent测试题目',
    difficulty: 'hard'
});

CREATE (q_q_293508:Question {
    id: 'q_293508',
    content: 'The book _____ is on the table belongs to me. A) who B) which C) where D) when',
    question_type: '选择题',
    options: ["who", "which", "where", "when"],
    answer: 'B',
    analysis: '先行词是物(book)，关系代词用which',
    source: '人教版初中英语',
    difficulty: 'hard'
});

CREATE (q_q_321432:Question {
    id: 'q_321432',
    content: 'Could you tell me _____ the library is? A) where B) what C) how D) why',
    question_type: '选择题',
    options: ["where", "what", "how", "why"],
    answer: 'A',
    analysis: '宾语从句询问地点，用where引导',
    source: 'AI Agent测试题目',
    difficulty: 'medium'
});

CREATE (q_q_354107:Question {
    id: 'q_354107',
    content: 'This book is _____ than that one. A) good B) better C) best D) the best',
    question_type: '选择题',
    options: ["good", "better", "best", "the best"],
    answer: 'B',
    analysis: '两者比较用比较级better',
    source: '人教版小学英语',
    difficulty: 'easy'
});

CREATE (q_q_381551:Question {
    id: 'q_381551',
    content: 'My sister _____ her homework every evening. A) do B) does C) doing D) did',
    question_type: '选择题',
    options: ["do", "does", "doing", "did"],
    answer: 'B',
    analysis: '主语My sister是第三人称单数，every evening表示经常性动作，用一般现在时does',
    source: 'AI Agent测试题目',
    difficulty: 'easy'
});

CREATE (q_q_403468:Question {
    id: 'q_403468',
    content: 'Can you tell me _____ the nearest hospital is? A) where B) what C) how D) why',
    question_type: '选择题',
    options: ["where", "what", "how", "why"],
    answer: 'A',
    analysis: '宾语从句询问地点，用where引导',
    source: '人教版初中英语',
    difficulty: 'medium'
});

CREATE (q_q_43661:Question {
    id: 'q_43661',
    content: 'She is more beautiful than her sister.',
    question_type: '选择题',
    options: [],
    answer: 'more beautiful',
    analysis: '多音节形容词用more构成比较级',
    source: '本地导入',
    difficulty: 'medium'
});

CREATE (q_q_554737:Question {
    id: 'q_554737',
    content: 'If it _____ tomorrow, we will stay at home. A) rain B) rains C) will rain D) rained',
    question_type: '选择题',
    options: ["rain", "rains", "will rain", "rained"],
    answer: 'B',
    analysis: 'if引导的条件句，从句用一般现在时，主句用将来时',
    source: 'AI Agent测试题目',
    difficulty: 'hard'
});

CREATE (q_q_674394:Question {
    id: 'q_674394',
    content: 'I have _____ finished my homework. A) already B) yet C) just D) ever',
    question_type: '选择题',
    options: ["already", "yet", "just", "ever"],
    answer: 'A',
    analysis: '现在完成时的肯定句中，already表示\'已经\'',
    source: '人教版初中英语',
    difficulty: 'medium'
});

CREATE (q_q_674976:Question {
    id: 'q_674976',
    content: 'She _____ to school every day. A) go B) goes C) going D) gone',
    question_type: '选择题',
    options: ["go", "goes", "going", "gone"],
    answer: 'B',
    analysis: '主语She是第三人称单数，动词需要用第三人称单数形式goes',
    source: '人教版小学英语',
    difficulty: 'easy'
});

CREATE (q_q_685858:Question {
    id: 'q_685858',
    content: 'If it rains tomorrow, we will stay at home.',
    question_type: '选择题',
    options: [],
    answer: 'rains',
    analysis: 'if引导的条件句，从句用一般现在时',
    source: '本地导入',
    difficulty: 'hard'
});

CREATE (q_q_692469:Question {
    id: 'q_692469',
    content: 'Look! The children _____ in the playground. A) play B) plays C) are playing D) played',
    question_type: '选择题',
    options: ["play", "plays", "are playing", "played"],
    answer: 'C',
    analysis: 'Look!表示现在正在发生的动作，用现在进行时are playing',
    source: '人教版小学英语',
    difficulty: 'medium'
});

CREATE (q_q_717843:Question {
    id: 'q_717843',
    content: 'Fill in the blank: I\'m good _____ playing basketball.',
    question_type: '填空题',
    options: [],
    answer: 'at',
    analysis: 'be good at是固定搭配，表示\'擅长于\'',
    source: 'AI Agent测试题目',
    difficulty: 'medium'
});

CREATE (q_q_776074:Question {
    id: 'q_776074',
    content: 'Translate: 如果我有时间，我会帮助你。',
    question_type: '翻译题',
    options: [],
    answer: 'If I have time, I will help you.',
    analysis: 'if引导的条件句，主句用将来时，从句用一般现在时',
    source: '人教版初中英语',
    difficulty: 'hard'
});

CREATE (q_q_83759:Question {
    id: 'q_83759',
    content: 'She has _____ lived in Shanghai for 5 years. A) already B) yet C) just D) never',
    question_type: '选择题',
    options: ["already", "yet", "just", "never"],
    answer: 'A',
    analysis: '现在完成时的肯定句中，already表示\'已经\'，强调动作已经完成',
    source: 'AI Agent测试题目',
    difficulty: 'medium'
});

CREATE (q_q_844018:Question {
    id: 'q_844018',
    content: 'The man _____ is wearing a blue shirt is my teacher. A) who B) which C) where D) when',
    question_type: '选择题',
    options: ["who", "which", "where", "when"],
    answer: 'A',
    analysis: '先行词是人(man)，关系代词用who引导定语从句',
    source: 'AI Agent测试题目',
    difficulty: 'hard'
});

CREATE (q_q_8457:Question {
    id: 'q_8457',
    content: 'Look! The birds _____ in the sky. A) fly B) flies C) are flying D) flew',
    question_type: '选择题',
    options: ["fly", "flies", "are flying", "flew"],
    answer: 'C',
    analysis: 'Look!提示现在正在发生的动作，用现在进行时are flying',
    source: 'AI Agent测试题目',
    difficulty: 'medium'
});

CREATE (q_q_894204:Question {
    id: 'q_894204',
    content: 'Yesterday I _____ to the park with my friends. A) go B) went C) going D) will go',
    question_type: '选择题',
    options: ["go", "went", "going", "will go"],
    answer: 'B',
    analysis: 'Yesterday表示过去的时间，需要用一般过去时went',
    source: '人教版小学英语',
    difficulty: 'easy'
});

CREATE (q_q_898687:Question {
    id: 'q_898687',
    content: 'Could you tell me where the library is?',
    question_type: '选择题',
    options: [],
    answer: 'where',
    analysis: '宾语从句询问地点，用where引导',
    source: '本地导入',
    difficulty: 'medium'
});

CREATE (q_q_909157:Question {
    id: 'q_909157',
    content: 'The letter _____ by Tom yesterday. A) wrote B) was written C) is written D) writes',
    question_type: '选择题',
    options: ["wrote", "was written", "is written", "writes"],
    answer: 'B',
    analysis: '主语letter是动作的承受者，用被动语态，时间是yesterday用过去时',
    source: '人教版初中英语',
    difficulty: 'hard'
});

CREATE (q_q_992293:Question {
    id: 'q_992293',
    content: 'Fill in the blank: I am interested _____ learning English.',
    question_type: '填空题',
    options: [],
    answer: 'in',
    analysis: 'be interested in是固定搭配，表示\'对...感兴趣\'',
    source: '人教版初中英语',
    difficulty: 'medium'
});

// ===== 第5步: 创建题目-知识点关系 =====

MATCH (q:Question {id: 'q_674394'})
MATCH (kp:KnowledgePoint {id: 'kp_573225'})
CREATE (q)-[:TESTS {weight: 1.0}]->(kp);

MATCH (q:Question {id: 'q_692469'})
MATCH (kp:KnowledgePoint {id: 'kp_573225'})
CREATE (q)-[:TESTS {weight: 1.0}]->(kp);

MATCH (q:Question {id: 'q_894204'})
MATCH (kp:KnowledgePoint {id: 'kp_573225'})
CREATE (q)-[:TESTS {weight: 1.0}]->(kp);

MATCH (q:Question {id: 'q_674976'})
MATCH (kp:KnowledgePoint {id: 'kp_573225'})
CREATE (q)-[:TESTS {weight: 1.0}]->(kp);

MATCH (q:Question {id: 'q_776074'})
MATCH (kp:KnowledgePoint {id: 'kp_588066'})
CREATE (q)-[:TESTS {weight: 1.0}]->(kp);

MATCH (q:Question {id: 'q_674976'})
MATCH (kp:KnowledgePoint {id: 'kp_588066'})
CREATE (q)-[:TESTS {weight: 1.0}]->(kp);

MATCH (q:Question {id: 'q_909157'})
MATCH (kp:KnowledgePoint {id: 'kp_2925'})
CREATE (q)-[:TESTS {weight: 1.0}]->(kp);

MATCH (q:Question {id: 'q_894204'})
MATCH (kp:KnowledgePoint {id: 'kp_2925'})
CREATE (q)-[:TESTS {weight: 1.0}]->(kp);

MATCH (q:Question {id: 'q_692469'})
MATCH (kp:KnowledgePoint {id: 'kp_605632'})
CREATE (q)-[:TESTS {weight: 1.0}]->(kp);

// ===== 第6步: 创建知识点层级关系 =====

MATCH (parent:KnowledgePoint {id: 'kp_115430'})
MATCH (child:KnowledgePoint {id: 'kp_573225'})
CREATE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {id: 'kp_573225'})
MATCH (child:KnowledgePoint {id: 'kp_588066'})
CREATE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {id: 'kp_573225'})
MATCH (child:KnowledgePoint {id: 'kp_2925'})
CREATE (parent)-[:HAS_SUB_POINT]->(child);

MATCH (parent:KnowledgePoint {id: 'kp_573225'})
MATCH (child:KnowledgePoint {id: 'kp_605632'})
CREATE (parent)-[:HAS_SUB_POINT]->(child);

// ===== 第7步: 验证数据 =====
MATCH (kp:KnowledgePoint) RETURN count(kp) as knowledge_points_count;
MATCH (q:Question) RETURN count(q) as questions_count;
MATCH ()-[r:TESTS]->() RETURN count(r) as tests_relationships_count;
MATCH ()-[r:HAS_SUB_POINT]->() RETURN count(r) as hierarchy_relationships_count;

// ===== 第8步: 查看数据样本 =====
MATCH (n) RETURN n LIMIT 10;