// 开源英语教育数据集成脚本
// 基于多个开源标准和题库整理

// 清空现有数据
MATCH (n) DETACH DELETE n;

// 创建约束
CREATE CONSTRAINT knowledge_point_id IF NOT EXISTS FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE;
CREATE CONSTRAINT question_id IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE;

// 创建知识点

CREATE (kp_001:KnowledgePoint {
    id: 'kp_opensource_001',
    name: '一般现在时',
    description: '表示经常性、习惯性的动作或状态',
    difficulty: 'easy',
    keywords: ["always", "usually", "often", "every day", "第三人称单数"],
    grade_levels: ["小学三年级", "小学四年级", "小学五年级"],
    source: 'Common Core State Standards',
    cefr_level: 'A1-A2'
});

CREATE (kp_002:KnowledgePoint {
    id: 'kp_opensource_002',
    name: '现在进行时',
    description: '表示现在正在进行的动作',
    difficulty: 'medium',
    keywords: ["now", "look!", "listen!", "be + ing"],
    grade_levels: ["小学四年级", "小学五年级", "小学六年级"],
    source: 'Cambridge English Standards',
    cefr_level: 'A2'
});

CREATE (kp_003:KnowledgePoint {
    id: 'kp_opensource_003',
    name: '定语从句',
    description: '用来修饰名词或代词的从句',
    difficulty: 'hard',
    keywords: ["who", "which", "that", "关系代词"],
    grade_levels: ["初中二年级", "初中三年级", "高中一年级"],
    source: 'Oxford Grammar Standards',
    cefr_level: 'B1-B2'
});

CREATE (kp_004:KnowledgePoint {
    id: 'kp_opensource_004',
    name: '情态动词',
    description: '表示说话人的情感、态度或语气',
    difficulty: 'medium',
    keywords: ["can", "could", "may", "might", "must", "should", "would"],
    grade_levels: ["小学六年级", "初中一年级", "初中二年级"],
    source: 'British Council Standards',
    cefr_level: 'A2-B1'
});

CREATE (kp_005:KnowledgePoint {
    id: 'kp_opensource_005',
    name: '条件句',
    description: '表示假设条件和可能结果的句子',
    difficulty: 'hard',
    keywords: ["if", "unless", "provided that", "假设", "条件"],
    grade_levels: ["初中三年级", "高中一年级", "高中二年级"],
    source: 'Cambridge Advanced Grammar',
    cefr_level: 'B2-C1'
});

CREATE (kp_006:KnowledgePoint {
    id: 'kp_opensource_006',
    name: '动名词和不定式',
    description: '动词的非谓语形式',
    difficulty: 'hard',
    keywords: ["to do", "doing", "enjoy doing", "want to do"],
    grade_levels: ["初中二年级", "初中三年级", "高中一年级"],
    source: 'Murphy's Grammar',
    cefr_level: 'B1-B2'
});

CREATE (kp_007:KnowledgePoint {
    id: 'kp_opensource_007',
    name: '冠词',
    description: '用于名词前的限定词',
    difficulty: 'easy',
    keywords: ["a", "an", "the", "零冠词"],
    grade_levels: ["小学二年级", "小学三年级", "小学四年级"],
    source: 'Elementary Grammar Standards',
    cefr_level: 'A1'
});

CREATE (kp_008:KnowledgePoint {
    id: 'kp_opensource_008',
    name: '疑问句',
    description: '用来提出问题的句子',
    difficulty: 'easy',
    keywords: ["what", "where", "when", "who", "how", "疑问词"],
    grade_levels: ["小学二年级", "小学三年级", "小学四年级"],
    source: 'Basic English Standards',
    cefr_level: 'A1-A2'
});

CREATE (kp_009:KnowledgePoint {
    id: 'kp_opensource_009',
    name: '感叹句',
    description: '表达强烈情感的句子',
    difficulty: 'easy',
    keywords: ["what", "how", "感叹"],
    grade_levels: ["小学四年级", "小学五年级"],
    source: 'Primary Grammar',
    cefr_level: 'A2'
});

CREATE (kp_010:KnowledgePoint {
    id: 'kp_opensource_010',
    name: '倒装句',
    description: '改变正常语序的句子结构',
    difficulty: 'hard',
    keywords: ["never", "seldom", "hardly", "倒装"],
    grade_levels: ["高中二年级", "高中三年级"],
    source: 'Advanced Grammar',
    cefr_level: 'C1'
});

// 创建题目

CREATE (q_001:Question {
    id: 'q_opensource_001',
    content: 'She _____ to work by bus every morning.',
    question_type: '选择题',
    options: ["go", "goes", "going", "gone"],
    answer: 'B',
    analysis: '主语she是第三人称单数，动词用goes',
    difficulty: 'easy',
    source: 'Cambridge Primary English',
    grade_level: '小学四年级'
});

CREATE (q_002:Question {
    id: 'q_opensource_002',
    content: 'My brother _____ football every weekend.',
    question_type: '选择题',
    options: ["play", "plays", "playing", "played"],
    answer: 'B',
    analysis: 'every weekend表示习惯性动作，用一般现在时',
    difficulty: 'easy',
    source: 'Oxford Primary Grammar',
    grade_level: '小学四年级'
});

CREATE (q_003:Question {
    id: 'q_opensource_003',
    content: 'Listen! The birds _____ in the tree.',
    question_type: '选择题',
    options: ["sing", "sings", "are singing", "sang"],
    answer: 'C',
    analysis: 'Listen!表示现在正在发生，用现在进行时',
    difficulty: 'medium',
    source: 'Cambridge Elementary',
    grade_level: '小学五年级'
});

CREATE (q_004:Question {
    id: 'q_opensource_004',
    content: 'What _____ you _____ now?',
    question_type: '选择题',
    options: ["are, doing", "do, do", "did, do", "will, do"],
    answer: 'A',
    analysis: 'now表示现在，用现在进行时',
    difficulty: 'medium',
    source: 'British Council LearnEnglish',
    grade_level: '小学六年级'
});

CREATE (q_005:Question {
    id: 'q_opensource_005',
    content: 'The book _____ is on the table belongs to Mary.',
    question_type: '选择题',
    options: ["who", "which", "where", "when"],
    answer: 'B',
    analysis: '修饰物用which，the book which...',
    difficulty: 'hard',
    source: 'Oxford Advanced Grammar',
    grade_level: '初中二年级'
});

CREATE (q_006:Question {
    id: 'q_opensource_006',
    content: 'The girl _____ hair is long is my sister.',
    question_type: '选择题',
    options: ["who", "whose", "which", "that"],
    answer: 'B',
    analysis: '表示所属关系用whose',
    difficulty: 'hard',
    source: 'Murphy's Grammar in Use',
    grade_level: '初中三年级'
});

CREATE (q_007:Question {
    id: 'q_opensource_007',
    content: 'This house _____ by my grandfather in 1950.',
    question_type: '选择题',
    options: ["built", "was built", "is built", "builds"],
    answer: 'B',
    analysis: 'in 1950表示过去时间，用一般过去时的被动语态',
    difficulty: 'hard',
    source: 'Cambridge Grammar',
    grade_level: '初中二年级'
});

CREATE (q_008:Question {
    id: 'q_opensource_008',
    content: 'This book is _____ than that one.',
    question_type: '选择题',
    options: ["interesting", "more interesting", "most interesting", "interestinger"],
    answer: 'B',
    analysis: 'than表示比较，interesting是多音节词，用more + 原级',
    difficulty: 'medium',
    source: 'Essential Grammar in Use',
    grade_level: '小学六年级'
});

CREATE (q_009:Question {
    id: 'q_opensource_009',
    content: 'You _____ finish your homework before watching TV.',
    question_type: '选择题',
    options: ["can", "may", "must", "could"],
    answer: 'C',
    analysis: '表示必须、义务用must',
    difficulty: 'medium',
    source: 'Cambridge English Grammar',
    grade_level: '初中一年级'
});

CREATE (q_010:Question {
    id: 'q_opensource_010',
    content: 'I saw _____ elephant in _____ zoo yesterday.',
    question_type: '选择题',
    options: ["a, the", "an, the", "the, a", "an, a"],
    answer: 'B',
    analysis: 'elephant以元音开头用an，特指的zoo用the',
    difficulty: 'easy',
    source: 'Elementary English',
    grade_level: '小学三年级'
});

CREATE (q_011:Question {
    id: 'q_opensource_011',
    content: '_____ do you go to school? By bike.',
    question_type: '选择题',
    options: ["What", "Where", "How", "When"],
    answer: 'C',
    analysis: '回答是方式，用How提问',
    difficulty: 'easy',
    source: 'Primary English',
    grade_level: '小学三年级'
});

CREATE (q_012:Question {
    id: 'q_opensource_012',
    content: 'I _____ this movie three times.',
    question_type: '选择题',
    options: ["see", "saw", "have seen", "will see"],
    answer: 'C',
    analysis: 'three times表示到现在为止的次数，用现在完成时',
    difficulty: 'medium',
    source: 'Intermediate Grammar',
    grade_level: '初中一年级'
});

CREATE (q_013:Question {
    id: 'q_opensource_013',
    content: 'Last summer, we _____ to Beijing for vacation.',
    question_type: '选择题',
    options: ["go", "went", "goes", "going"],
    answer: 'B',
    analysis: 'Last summer表示过去时间，用一般过去时',
    difficulty: 'easy',
    source: 'Elementary Grammar',
    grade_level: '小学五年级'
});

CREATE (q_014:Question {
    id: 'q_opensource_014',
    content: 'The meeting is _____ 3 o\'clock _____ the afternoon.',
    question_type: '选择题',
    options: ["at, in", "on, at", "in, on", "at, on"],
    answer: 'A',
    analysis: '具体时刻用at，下午用in',
    difficulty: 'medium',
    source: 'Grammar in Use',
    grade_level: '小学六年级'
});

CREATE (q_015:Question {
    id: 'q_opensource_015',
    content: 'If it _____ tomorrow, we will stay at home.',
    question_type: '选择题',
    options: ["rain", "rains", "will rain", "rained"],
    answer: 'B',
    analysis: 'if条件句中，从句用一般现在时表将来',
    difficulty: 'hard',
    source: 'Advanced Grammar',
    grade_level: '初中三年级'
});

CREATE (q_016:Question {
    id: 'q_opensource_016',
    content: 'She enjoys _____ music in her free time.',
    question_type: '选择题',
    options: ["listen", "listening", "to listen", "listened"],
    answer: 'B',
    analysis: 'enjoy后面接动名词doing',
    difficulty: 'medium',
    source: 'Grammar Reference',
    grade_level: '初中二年级'
});

CREATE (q_017:Question {
    id: 'q_opensource_017',
    content: '_____ beautiful flowers they are!',
    question_type: '选择题',
    options: ["What", "How", "What a", "How a"],
    answer: 'A',
    analysis: '感叹可数名词复数用What',
    difficulty: 'easy',
    source: 'Primary Grammar',
    grade_level: '小学五年级'
});

CREATE (q_018:Question {
    id: 'q_opensource_018',
    content: 'I don\'t know _____ he will come tomorrow.',
    question_type: '选择题',
    options: ["that", "if", "what", "which"],
    answer: 'B',
    analysis: '表示是否用if或whether引导宾语从句',
    difficulty: 'hard',
    source: 'Grammar in Context',
    grade_level: '初中三年级'
});

CREATE (q_019:Question {
    id: 'q_opensource_019',
    content: 'If I _____ you, I would study harder.',
    question_type: '选择题',
    options: ["am", "was", "were", "be"],
    answer: 'C',
    analysis: '虚拟语气中，be动词统一用were',
    difficulty: 'hard',
    source: 'Advanced English Grammar',
    grade_level: '高中一年级'
});

CREATE (q_020:Question {
    id: 'q_opensource_020',
    content: 'Never _____ such a beautiful sunset before.',
    question_type: '选择题',
    options: ["I saw", "I have seen", "have I seen", "did I see"],
    answer: 'C',
    analysis: 'never开头的倒装句，助动词前置',
    difficulty: 'hard',
    source: 'Advanced Grammar Reference',
    grade_level: '高中二年级'
});

CREATE (q_021:Question {
    id: 'q_opensource_021',
    content: 'The boy _____ under the tree is reading a book.',
    question_type: '选择题',
    options: ["sit", "sitting", "sat", "to sit"],
    answer: 'B',
    analysis: '现在分词作定语，表示主动进行',
    difficulty: 'hard',
    source: 'Grammar Comprehensive',
    grade_level: '高中一年级'
});

CREATE (q_022:Question {
    id: 'q_opensource_022',
    content: 'Water _____ at 100 degrees Celsius.',
    question_type: '选择题',
    options: ["boil", "boils", "boiling", "boiled"],
    answer: 'B',
    analysis: '客观事实用一般现在时，water是不可数名词，动词用第三人称单数',
    difficulty: 'easy',
    source: 'Science English',
    grade_level: '小学六年级'
});

CREATE (q_023:Question {
    id: 'q_opensource_023',
    content: 'Shh! The baby _____ in the next room.',
    question_type: '选择题',
    options: ["sleep", "sleeps", "is sleeping", "slept"],
    answer: 'C',
    analysis: 'Shh!表示此刻正在发生，用现在进行时',
    difficulty: 'medium',
    source: 'Daily English',
    grade_level: '小学五年级'
});

CREATE (q_024:Question {
    id: 'q_opensource_024',
    content: 'English _____ in many countries around the world.',
    question_type: '选择题',
    options: ["speak", "speaks", "is spoken", "speaking"],
    answer: 'C',
    analysis: 'English是被说的，用被动语态',
    difficulty: 'medium',
    source: 'World English',
    grade_level: '初中二年级'
});

CREATE (q_025:Question {
    id: 'q_opensource_025',
    content: 'This is the school _____ I studied when I was young.',
    question_type: '选择题',
    options: ["which", "where", "when", "that"],
    answer: 'B',
    analysis: '先行词是地点school，用where引导定语从句',
    difficulty: 'hard',
    source: 'Grammar Practice',
    grade_level: '初中三年级'
});

CREATE (q_026:Question {
    id: 'q_opensource_026',
    content: 'Of all the students, Mary is _____ one.',
    question_type: '选择题',
    options: ["tall", "taller", "the tallest", "most tall"],
    answer: 'C',
    analysis: '三者以上比较用最高级，tall的最高级是tallest',
    difficulty: 'medium',
    source: 'Comparative Grammar',
    grade_level: '小学六年级'
});

CREATE (q_027:Question {
    id: 'q_opensource_027',
    content: 'You _____ smoke here. It\'s dangerous.',
    question_type: '选择题',
    options: ["can", "must", "mustn't", "needn't"],
    answer: 'C',
    analysis: '表示禁止用mustn\'t',
    difficulty: 'medium',
    source: 'Modal Verbs Practice',
    grade_level: '初中一年级'
});

CREATE (q_028:Question {
    id: 'q_opensource_028',
    content: 'She is good _____ English but weak _____ math.',
    question_type: '选择题',
    options: ["at, in", "in, at", "at, at", "in, in"],
    answer: 'C',
    analysis: 'be good at和be weak at都是固定搭配',
    difficulty: 'medium',
    source: 'Preposition Practice',
    grade_level: '初中一年级'
});

CREATE (q_029:Question {
    id: 'q_opensource_029',
    content: 'I _____ my homework. Can I watch TV now?',
    question_type: '选择题',
    options: ["finished", "have finished", "finish", "am finishing"],
    answer: 'B',
    analysis: '强调完成的结果对现在的影响，用现在完成时',
    difficulty: 'medium',
    source: 'Tense Comparison',
    grade_level: '初中一年级'
});

CREATE (q_030:Question {
    id: 'q_opensource_030',
    content: 'Could you tell me _____?',
    question_type: '选择题',
    options: ["where does he live", "where he lives", "where did he live", "where he lived"],
    answer: 'B',
    analysis: '宾语从句用陈述语序',
    difficulty: 'hard',
    source: 'Clause Grammar',
    grade_level: '初中三年级'
});

// 创建题目-知识点关系

MATCH (q:Question {id: 'q_opensource_001'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_001'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_002'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_001'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_003'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_002'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_004'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_002'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_004'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_008'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_005'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_003'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_006'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_003'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_009'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_004'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_010'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_007'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_011'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_008'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_015'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_005'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_015'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_001'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_016'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_006'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_017'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_009'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_019'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_005'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_020'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_010'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_022'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_001'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_023'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_002'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_025'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_003'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

MATCH (q:Question {id: 'q_opensource_027'})
MATCH (kp:KnowledgePoint {id: 'kp_opensource_004'})
CREATE (q)-[:TESTS {weight: 0.8}]->(kp);

// 验证数据
MATCH (kp:KnowledgePoint) RETURN count(kp) as knowledge_points;
MATCH (q:Question) RETURN count(q) as questions;
MATCH ()-[r:TESTS]->() RETURN count(r) as relationships;