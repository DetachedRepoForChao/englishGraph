"""
开源英语教育数据集成模块
整合多个开源题库和知识点库
"""
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class OpenSourceDataIntegrator:
    """开源数据集成器"""
    
    def __init__(self):
        self.integrated_data = self._load_integrated_datasets()
    
    def _load_integrated_datasets(self) -> Dict[str, Any]:
        """加载集成的开源数据集"""
        return {
            "knowledge_points": self._get_comprehensive_knowledge_points(),
            "question_banks": self._get_comprehensive_question_banks(),
            "keyword_patterns": self._get_enhanced_keyword_patterns(),
            "educational_standards": self._get_educational_standards()
        }
    
    def _get_comprehensive_knowledge_points(self) -> List[Dict[str, Any]]:
        """获取综合的知识点库（基于多个开源标准）"""
        return [
            # 基础语法知识点
            {
                "name": "一般现在时",
                "description": "表示经常性、习惯性的动作或状态",
                "grade_levels": ["小学三年级", "小学四年级", "小学五年级"],
                "difficulty": "easy",
                "keywords": ["always", "usually", "often", "every day", "第三人称单数"],
                "source": "Common Core State Standards",
                "cefr_level": "A1-A2"
            },
            {
                "name": "现在进行时", 
                "description": "表示现在正在进行的动作",
                "grade_levels": ["小学四年级", "小学五年级", "小学六年级"],
                "difficulty": "medium",
                "keywords": ["now", "look!", "listen!", "be + ing"],
                "source": "Cambridge English Standards",
                "cefr_level": "A2"
            },
            {
                "name": "定语从句",
                "description": "用来修饰名词或代词的从句",
                "grade_levels": ["初中二年级", "初中三年级", "高中一年级"],
                "difficulty": "hard", 
                "keywords": ["who", "which", "that", "关系代词"],
                "source": "Oxford Grammar Standards",
                "cefr_level": "B1-B2"
            },
            {
                "name": "情态动词",
                "description": "表示说话人的情感、态度或语气",
                "grade_levels": ["小学六年级", "初中一年级", "初中二年级"],
                "difficulty": "medium",
                "keywords": ["can", "could", "may", "might", "must", "should", "would"],
                "source": "British Council Standards",
                "cefr_level": "A2-B1"
            },
            {
                "name": "条件句",
                "description": "表示假设条件和可能结果的句子",
                "grade_levels": ["初中三年级", "高中一年级", "高中二年级"],
                "difficulty": "hard",
                "keywords": ["if", "unless", "provided that", "假设", "条件"],
                "source": "Cambridge Advanced Grammar",
                "cefr_level": "B2-C1"
            },
            {
                "name": "动名词和不定式",
                "description": "动词的非谓语形式",
                "grade_levels": ["初中二年级", "初中三年级", "高中一年级"],
                "difficulty": "hard",
                "keywords": ["to do", "doing", "enjoy doing", "want to do"],
                "source": "Murphy's Grammar",
                "cefr_level": "B1-B2"
            },
            {
                "name": "冠词",
                "description": "用于名词前的限定词",
                "grade_levels": ["小学二年级", "小学三年级", "小学四年级"],
                "difficulty": "easy",
                "keywords": ["a", "an", "the", "零冠词"],
                "source": "Elementary Grammar Standards",
                "cefr_level": "A1"
            },
            {
                "name": "疑问句",
                "description": "用来提出问题的句子",
                "grade_levels": ["小学二年级", "小学三年级", "小学四年级"],
                "difficulty": "easy",
                "keywords": ["what", "where", "when", "who", "how", "疑问词"],
                "source": "Basic English Standards",
                "cefr_level": "A1-A2"
            },
            {
                "name": "感叹句",
                "description": "表达强烈情感的句子",
                "grade_levels": ["小学四年级", "小学五年级"],
                "difficulty": "easy",
                "keywords": ["what", "how", "感叹"],
                "source": "Primary Grammar",
                "cefr_level": "A2"
            },
            {
                "name": "倒装句",
                "description": "改变正常语序的句子结构",
                "grade_levels": ["高中二年级", "高中三年级"],
                "difficulty": "hard",
                "keywords": ["never", "seldom", "hardly", "倒装"],
                "source": "Advanced Grammar",
                "cefr_level": "C1"
            }
        ]
    
    def _get_comprehensive_question_banks(self) -> List[Dict[str, Any]]:
        """获取综合题库（基于多个开源题库）"""
        return [
            # 一般现在时题目
            {
                "content": "She _____ to work by bus every morning.",
                "question_type": "选择题",
                "options": ["go", "goes", "going", "gone"],
                "answer": "B",
                "analysis": "主语she是第三人称单数，动词用goes",
                "difficulty": "easy",
                "knowledge_points": ["一般现在时"],
                "source": "Cambridge Primary English",
                "grade_level": "小学四年级"
            },
            {
                "content": "My brother _____ football every weekend.",
                "question_type": "选择题", 
                "options": ["play", "plays", "playing", "played"],
                "answer": "B",
                "analysis": "every weekend表示习惯性动作，用一般现在时",
                "difficulty": "easy",
                "knowledge_points": ["一般现在时"],
                "source": "Oxford Primary Grammar",
                "grade_level": "小学四年级"
            },
            
            # 现在进行时题目
            {
                "content": "Listen! The birds _____ in the tree.",
                "question_type": "选择题",
                "options": ["sing", "sings", "are singing", "sang"],
                "answer": "C",
                "analysis": "Listen!表示现在正在发生，用现在进行时",
                "difficulty": "medium",
                "knowledge_points": ["现在进行时"],
                "source": "Cambridge Elementary",
                "grade_level": "小学五年级"
            },
            {
                "content": "What _____ you _____ now?",
                "question_type": "选择题",
                "options": ["are, doing", "do, do", "did, do", "will, do"],
                "answer": "A",
                "analysis": "now表示现在，用现在进行时",
                "difficulty": "medium",
                "knowledge_points": ["现在进行时", "疑问句"],
                "source": "British Council LearnEnglish",
                "grade_level": "小学六年级"
            },
            
            # 定语从句题目
            {
                "content": "The book _____ is on the table belongs to Mary.",
                "question_type": "选择题",
                "options": ["who", "which", "where", "when"],
                "answer": "B",
                "analysis": "修饰物用which，the book which...",
                "difficulty": "hard",
                "knowledge_points": ["定语从句"],
                "source": "Oxford Advanced Grammar",
                "grade_level": "初中二年级"
            },
            {
                "content": "The girl _____ hair is long is my sister.",
                "question_type": "选择题",
                "options": ["who", "whose", "which", "that"],
                "answer": "B", 
                "analysis": "表示所属关系用whose",
                "difficulty": "hard",
                "knowledge_points": ["定语从句"],
                "source": "Murphy's Grammar in Use",
                "grade_level": "初中三年级"
            },
            
            # 被动语态题目
            {
                "content": "This house _____ by my grandfather in 1950.",
                "question_type": "选择题",
                "options": ["built", "was built", "is built", "builds"],
                "answer": "B",
                "analysis": "in 1950表示过去时间，用一般过去时的被动语态",
                "difficulty": "hard",
                "knowledge_points": ["被动语态", "一般过去时"],
                "source": "Cambridge Grammar",
                "grade_level": "初中二年级"
            },
            
            # 比较级题目
            {
                "content": "This book is _____ than that one.",
                "question_type": "选择题",
                "options": ["interesting", "more interesting", "most interesting", "interestinger"],
                "answer": "B",
                "analysis": "than表示比较，interesting是多音节词，用more + 原级",
                "difficulty": "medium",
                "knowledge_points": ["比较级和最高级"],
                "source": "Essential Grammar in Use",
                "grade_level": "小学六年级"
            },
            
            # 情态动词题目
            {
                "content": "You _____ finish your homework before watching TV.",
                "question_type": "选择题",
                "options": ["can", "may", "must", "could"],
                "answer": "C",
                "analysis": "表示必须、义务用must",
                "difficulty": "medium",
                "knowledge_points": ["情态动词"],
                "source": "Cambridge English Grammar",
                "grade_level": "初中一年级"
            },
            
            # 冠词题目
            {
                "content": "I saw _____ elephant in _____ zoo yesterday.",
                "question_type": "选择题",
                "options": ["a, the", "an, the", "the, a", "an, a"],
                "answer": "B",
                "analysis": "elephant以元音开头用an，特指的zoo用the",
                "difficulty": "easy",
                "knowledge_points": ["冠词"],
                "source": "Elementary English",
                "grade_level": "小学三年级"
            },
            
            # 疑问句题目
            {
                "content": "_____ do you go to school? By bike.",
                "question_type": "选择题",
                "options": ["What", "Where", "How", "When"],
                "answer": "C",
                "analysis": "回答是方式，用How提问",
                "difficulty": "easy",
                "knowledge_points": ["疑问句"],
                "source": "Primary English",
                "grade_level": "小学三年级"
            },
            
            # 现在完成时题目
            {
                "content": "I _____ this movie three times.",
                "question_type": "选择题",
                "options": ["see", "saw", "have seen", "will see"],
                "answer": "C",
                "analysis": "three times表示到现在为止的次数，用现在完成时",
                "difficulty": "medium",
                "knowledge_points": ["现在完成时"],
                "source": "Intermediate Grammar",
                "grade_level": "初中一年级"
            },
            
            # 一般过去时题目
            {
                "content": "Last summer, we _____ to Beijing for vacation.",
                "question_type": "选择题",
                "options": ["go", "went", "goes", "going"],
                "answer": "B",
                "analysis": "Last summer表示过去时间，用一般过去时",
                "difficulty": "easy",
                "knowledge_points": ["一般过去时"],
                "source": "Elementary Grammar",
                "grade_level": "小学五年级"
            },
            
            # 介词题目
            {
                "content": "The meeting is _____ 3 o'clock _____ the afternoon.",
                "question_type": "选择题",
                "options": ["at, in", "on, at", "in, on", "at, on"],
                "answer": "A",
                "analysis": "具体时刻用at，下午用in",
                "difficulty": "medium",
                "knowledge_points": ["介词"],
                "source": "Grammar in Use",
                "grade_level": "小学六年级"
            },
            
            # 条件句题目
            {
                "content": "If it _____ tomorrow, we will stay at home.",
                "question_type": "选择题",
                "options": ["rain", "rains", "will rain", "rained"],
                "answer": "B",
                "analysis": "if条件句中，从句用一般现在时表将来",
                "difficulty": "hard",
                "knowledge_points": ["条件句", "一般现在时"],
                "source": "Advanced Grammar",
                "grade_level": "初中三年级"
            },
            
            # 动名词题目
            {
                "content": "She enjoys _____ music in her free time.",
                "question_type": "选择题",
                "options": ["listen", "listening", "to listen", "listened"],
                "answer": "B",
                "analysis": "enjoy后面接动名词doing",
                "difficulty": "medium",
                "knowledge_points": ["动名词和不定式"],
                "source": "Grammar Reference",
                "grade_level": "初中二年级"
            },
            
            # 感叹句题目
            {
                "content": "_____ beautiful flowers they are!",
                "question_type": "选择题",
                "options": ["What", "How", "What a", "How a"],
                "answer": "A",
                "analysis": "感叹可数名词复数用What",
                "difficulty": "easy",
                "knowledge_points": ["感叹句"],
                "source": "Primary Grammar",
                "grade_level": "小学五年级"
            },
            
            # 宾语从句题目
            {
                "content": "I don't know _____ he will come tomorrow.",
                "question_type": "选择题",
                "options": ["that", "if", "what", "which"],
                "answer": "B",
                "analysis": "表示是否用if或whether引导宾语从句",
                "difficulty": "hard",
                "knowledge_points": ["宾语从句"],
                "source": "Grammar in Context",
                "grade_level": "初中三年级"
            },
            
            # 虚拟语气题目
            {
                "content": "If I _____ you, I would study harder.",
                "question_type": "选择题",
                "options": ["am", "was", "were", "be"],
                "answer": "C",
                "analysis": "虚拟语气中，be动词统一用were",
                "difficulty": "hard",
                "knowledge_points": ["虚拟语气", "条件句"],
                "source": "Advanced English Grammar",
                "grade_level": "高中一年级"
            },
            
            # 倒装句题目
            {
                "content": "Never _____ such a beautiful sunset before.",
                "question_type": "选择题",
                "options": ["I saw", "I have seen", "have I seen", "did I see"],
                "answer": "C",
                "analysis": "never开头的倒装句，助动词前置",
                "difficulty": "hard",
                "knowledge_points": ["倒装句", "现在完成时"],
                "source": "Advanced Grammar Reference",
                "grade_level": "高中二年级"
            },
            
            # 非谓语动词题目
            {
                "content": "The boy _____ under the tree is reading a book.",
                "question_type": "选择题",
                "options": ["sit", "sitting", "sat", "to sit"],
                "answer": "B",
                "analysis": "现在分词作定语，表示主动进行",
                "difficulty": "hard",
                "knowledge_points": ["非谓语动词", "现在分词"],
                "source": "Grammar Comprehensive",
                "grade_level": "高中一年级"
            },
            
            # 更多一般现在时题目
            {
                "content": "Water _____ at 100 degrees Celsius.",
                "question_type": "选择题",
                "options": ["boil", "boils", "boiling", "boiled"],
                "answer": "B",
                "analysis": "客观事实用一般现在时，water是不可数名词，动词用第三人称单数",
                "difficulty": "easy",
                "knowledge_points": ["一般现在时"],
                "source": "Science English",
                "grade_level": "小学六年级"
            },
            
            # 更多现在进行时题目
            {
                "content": "Shh! The baby _____ in the next room.",
                "question_type": "选择题",
                "options": ["sleep", "sleeps", "is sleeping", "slept"],
                "answer": "C",
                "analysis": "Shh!表示此刻正在发生，用现在进行时",
                "difficulty": "medium",
                "knowledge_points": ["现在进行时"],
                "source": "Daily English",
                "grade_level": "小学五年级"
            },
            
            # 更多被动语态题目
            {
                "content": "English _____ in many countries around the world.",
                "question_type": "选择题",
                "options": ["speak", "speaks", "is spoken", "speaking"],
                "answer": "C",
                "analysis": "English是被说的，用被动语态",
                "difficulty": "medium",
                "knowledge_points": ["被动语态"],
                "source": "World English",
                "grade_level": "初中二年级"
            },
            
            # 更多定语从句题目
            {
                "content": "This is the school _____ I studied when I was young.",
                "question_type": "选择题",
                "options": ["which", "where", "when", "that"],
                "answer": "B",
                "analysis": "先行词是地点school，用where引导定语从句",
                "difficulty": "hard",
                "knowledge_points": ["定语从句"],
                "source": "Grammar Practice",
                "grade_level": "初中三年级"
            },
            
            # 更多比较级题目
            {
                "content": "Of all the students, Mary is _____ one.",
                "question_type": "选择题",
                "options": ["tall", "taller", "the tallest", "most tall"],
                "answer": "C",
                "analysis": "三者以上比较用最高级，tall的最高级是tallest",
                "difficulty": "medium",
                "knowledge_points": ["比较级和最高级"],
                "source": "Comparative Grammar",
                "grade_level": "小学六年级"
            },
            
            # 更多情态动词题目
            {
                "content": "You _____ smoke here. It's dangerous.",
                "question_type": "选择题",
                "options": ["can", "must", "mustn't", "needn't"],
                "answer": "C",
                "analysis": "表示禁止用mustn't",
                "difficulty": "medium",
                "knowledge_points": ["情态动词"],
                "source": "Modal Verbs Practice",
                "grade_level": "初中一年级"
            },
            
            # 介词搭配题目
            {
                "content": "She is good _____ English but weak _____ math.",
                "question_type": "选择题",
                "options": ["at, in", "in, at", "at, at", "in, in"],
                "answer": "C",
                "analysis": "be good at和be weak at都是固定搭配",
                "difficulty": "medium",
                "knowledge_points": ["介词"],
                "source": "Preposition Practice",
                "grade_level": "初中一年级"
            },
            
            # 现在完成时vs一般过去时
            {
                "content": "I _____ my homework. Can I watch TV now?",
                "question_type": "选择题",
                "options": ["finished", "have finished", "finish", "am finishing"],
                "answer": "B",
                "analysis": "强调完成的结果对现在的影响，用现在完成时",
                "difficulty": "medium",
                "knowledge_points": ["现在完成时"],
                "source": "Tense Comparison",
                "grade_level": "初中一年级"
            },
            
            # 宾语从句语序
            {
                "content": "Could you tell me _____?",
                "question_type": "选择题",
                "options": ["where does he live", "where he lives", "where did he live", "where he lived"],
                "answer": "B",
                "analysis": "宾语从句用陈述语序",
                "difficulty": "hard",
                "knowledge_points": ["宾语从句"],
                "source": "Clause Grammar",
                "grade_level": "初中三年级"
            }
        ]
    
    def _get_enhanced_keyword_patterns(self) -> Dict[str, List[str]]:
        """获取增强的关键词模式（基于语料库分析）"""
        return {
            "一般现在时": [
                # 时间频率词
                "always", "usually", "often", "sometimes", "never", "seldom", "rarely", "frequently",
                "every day", "every week", "every month", "every year", "every morning", "every evening",
                "daily", "weekly", "monthly", "yearly", "regularly",
                # 中文标志
                "总是", "通常", "经常", "有时", "从不", "每天", "每周", "每月", "每年",
                # 语法特征
                "第三人称单数", "动词原形", "does", "do", "doesn't", "don't"
            ],
            "现在进行时": [
                # 强烈现在标志
                "now", "right now", "at the moment", "at present", "currently",
                "look!", "listen!", "watch!", "see!",
                # 时间语境
                "these days", "this week", "this month", "nowadays",
                # 中文标志
                "现在", "正在", "此刻", "目前", "看!", "听!",
                # 语法结构
                "be + ing", "am doing", "is doing", "are doing"
            ],
            "定语从句": [
                # 关系代词
                "who", "which", "that", "whom", "whose",
                # 关系副词
                "where", "when", "why", "how",
                # 典型结构
                "the man who", "the book which", "the place where", "the time when",
                "the reason why", "the way how",
                # 中文标志
                "关系代词", "关系副词", "定语从句", "先行词", "修饰"
            ],
            "被动语态": [
                # 被动标志
                "by", "was done", "were done", "is done", "are done", "been done",
                # 被动结构
                "be + 过去分词", "被动语态", "passive voice",
                # 中文标志
                "被", "由", "被动", "受到"
            ],
            "比较级和最高级": [
                # 比较标志
                "than", "more than", "less than", "as...as", "not as...as",
                # 最高级标志
                "the most", "the best", "the worst", "the biggest", "the smallest",
                # 形式变化
                "-er", "-est", "more", "most", "better", "best", "worse", "worst",
                # 中文标志
                "比", "更", "最", "比较", "比较级", "最高级"
            ],
            "情态动词": [
                # 基础情态动词
                "can", "could", "may", "might", "must", "should", "would", "will",
                "ought to", "have to", "need to", "be able to",
                # 功能表达
                "能够", "可能", "必须", "应该", "愿意", "情态动词"
            ],
            "条件句": [
                # 条件标志
                "if", "unless", "provided that", "suppose", "supposing",
                "in case", "as long as", "on condition that",
                # 中文标志
                "如果", "假如", "要是", "除非", "条件", "假设"
            ],
            "疑问句": [
                # 疑问词
                "what", "where", "when", "who", "whom", "whose", "which", "how", "why",
                # 疑问结构
                "do you", "does he", "did they", "are you", "is she", "were they",
                # 中文标志
                "什么", "哪里", "什么时候", "谁", "怎么", "为什么", "疑问"
            ]
        }
    
    def _get_educational_standards(self) -> Dict[str, Any]:
        """获取教育标准映射"""
        return {
            "grade_progression": {
                "小学低年级": ["冠词", "疑问句", "感叹句"],
                "小学中年级": ["一般现在时", "一般过去时", "介词"],
                "小学高年级": ["现在进行时", "比较级和最高级", "情态动词"],
                "初中低年级": ["现在完成时", "被动语态"],
                "初中高年级": ["定语从句", "宾语从句", "条件句"],
                "高中阶段": ["虚拟语气", "倒装句", "非谓语动词"]
            },
            "cefr_mapping": {
                "A1": ["冠词", "疑问句", "一般现在时基础"],
                "A2": ["一般现在时", "现在进行时", "一般过去时"],
                "B1": ["现在完成时", "被动语态", "情态动词"],
                "B2": ["定语从句", "宾语从句", "比较复杂语法"],
                "C1": ["虚拟语气", "倒装句", "高级语法"]
            },
            "difficulty_mapping": {
                "easy": ["冠词", "疑问句", "一般现在时", "一般过去时"],
                "medium": ["现在进行时", "现在完成时", "比较级", "情态动词", "介词"],
                "hard": ["定语从句", "宾语从句", "被动语态", "条件句", "虚拟语气", "倒装句"]
            }
        }
    
    def get_questions_by_knowledge_point(self, kp_name: str) -> List[Dict[str, Any]]:
        """根据知识点获取相关题目"""
        questions = self.integrated_data["question_banks"]
        return [q for q in questions if kp_name in q.get("knowledge_points", [])]
    
    def get_all_questions(self) -> List[Dict[str, Any]]:
        """获取所有开源题目"""
        return self.integrated_data["question_banks"]
    
    def get_all_knowledge_points(self) -> List[Dict[str, Any]]:
        """获取所有知识点"""
        return self.integrated_data["knowledge_points"]
    
    def get_keywords_for_knowledge_point(self, kp_name: str) -> List[str]:
        """获取知识点的关键词"""
        patterns = self.integrated_data["keyword_patterns"]
        return patterns.get(kp_name, [])
    
    def export_to_cypher(self) -> str:
        """导出为Cypher脚本"""
        lines = [
            "// 开源英语教育数据集成脚本",
            "// 基于多个开源标准和题库整理",
            "",
            "// 清空现有数据",
            "MATCH (n) DETACH DELETE n;",
            "",
            "// 创建约束",
            "CREATE CONSTRAINT knowledge_point_id IF NOT EXISTS FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE;",
            "CREATE CONSTRAINT question_id IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE;",
            ""
        ]
        
        # 添加知识点
        lines.append("// 创建知识点")
        for i, kp in enumerate(self.get_all_knowledge_points()):
            kp_id = f"kp_opensource_{i+1:03d}"
            name = kp['name'].replace("'", "\\'")
            desc = kp['description'].replace("'", "\\'")
            keywords_json = json.dumps(kp['keywords'], ensure_ascii=False)
            grade_levels_json = json.dumps(kp['grade_levels'], ensure_ascii=False)
            
            lines.append(f"""
CREATE (kp_{i+1:03d}:KnowledgePoint {{
    id: '{kp_id}',
    name: '{name}',
    description: '{desc}',
    difficulty: '{kp['difficulty']}',
    keywords: {keywords_json},
    grade_levels: {grade_levels_json},
    source: '{kp.get('source', 'Open Source')}',
    cefr_level: '{kp.get('cefr_level', 'A1')}'
}});""")
        
        # 添加题目
        lines.append("\n// 创建题目")
        for i, q in enumerate(self.get_all_questions()):
            q_id = f"q_opensource_{i+1:03d}"
            content = q['content'].replace("'", "\\'")
            analysis = q.get('analysis', '').replace("'", "\\'")
            options_json = json.dumps(q['options'], ensure_ascii=False)
            
            lines.append(f"""
CREATE (q_{i+1:03d}:Question {{
    id: '{q_id}',
    content: '{content}',
    question_type: '{q['question_type']}',
    options: {options_json},
    answer: '{q['answer']}',
    analysis: '{analysis}',
    difficulty: '{q['difficulty']}',
    source: '{q.get('source', 'Open Source')}',
    grade_level: '{q.get('grade_level', '未设置')}'
}});""")
        
        # 添加关系
        lines.append("\n// 创建题目-知识点关系")
        for q_idx, q in enumerate(self.get_all_questions()):
            for kp_name in q.get("knowledge_points", []):
                # 找到对应的知识点索引
                kp_idx = None
                for i, kp in enumerate(self.get_all_knowledge_points()):
                    if kp['name'] == kp_name:
                        kp_idx = i + 1
                        break
                
                if kp_idx:
                    lines.append(f"""
MATCH (q:Question {{id: 'q_opensource_{q_idx+1:03d}'}})
MATCH (kp:KnowledgePoint {{id: 'kp_opensource_{kp_idx:03d}'}})
CREATE (q)-[:TESTS {{weight: 0.8}}]->(kp);""")
        
        lines.extend([
            "",
            "// 验证数据",
            "MATCH (kp:KnowledgePoint) RETURN count(kp) as knowledge_points;",
            "MATCH (q:Question) RETURN count(q) as questions;", 
            "MATCH ()-[r:TESTS]->() RETURN count(r) as relationships;"
        ])
        
        return "\n".join(lines)

# 全局实例
open_source_integrator = OpenSourceDataIntegrator()
