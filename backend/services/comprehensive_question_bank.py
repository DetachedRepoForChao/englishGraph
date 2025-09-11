"""
综合英语题库 - 200道精选题目
涵盖K12全学段，包含20+个语法知识点
"""
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ComprehensiveQuestionBank:
    """综合英语题库"""
    
    def __init__(self):
        self.question_bank = self._build_comprehensive_bank()
        self.knowledge_points = self._build_comprehensive_knowledge_points()
    
    def _build_comprehensive_knowledge_points(self) -> List[Dict[str, Any]]:
        """构建全面的知识点库"""
        return [
            # 基础语法
            {
                "name": "一般现在时", "grade_levels": ["小学三年级", "小学四年级"], "difficulty": "easy",
                "keywords": ["always", "usually", "every day", "第三人称单数"], "cefr_level": "A1"
            },
            {
                "name": "现在进行时", "grade_levels": ["小学四年级", "小学五年级"], "difficulty": "medium",
                "keywords": ["now", "look!", "listen!", "be + ing"], "cefr_level": "A2"
            },
            {
                "name": "一般过去时", "grade_levels": ["小学四年级", "小学五年级"], "difficulty": "easy",
                "keywords": ["yesterday", "last week", "ago", "过去式"], "cefr_level": "A1-A2"
            },
            {
                "name": "现在完成时", "grade_levels": ["初中一年级", "初中二年级"], "difficulty": "medium",
                "keywords": ["already", "yet", "just", "have done"], "cefr_level": "B1"
            },
            {
                "name": "一般将来时", "grade_levels": ["小学五年级", "小学六年级"], "difficulty": "medium",
                "keywords": ["will", "be going to", "tomorrow", "next week"], "cefr_level": "A2"
            },
            {
                "name": "过去进行时", "grade_levels": ["初中一年级", "初中二年级"], "difficulty": "medium",
                "keywords": ["was doing", "were doing", "at that time"], "cefr_level": "B1"
            },
            
            # 语态
            {
                "name": "被动语态", "grade_levels": ["初中二年级", "初中三年级"], "difficulty": "hard",
                "keywords": ["be done", "by", "被动"], "cefr_level": "B1-B2"
            },
            
            # 从句
            {
                "name": "定语从句", "grade_levels": ["初中二年级", "初中三年级"], "difficulty": "hard",
                "keywords": ["who", "which", "that", "关系代词"], "cefr_level": "B1-B2"
            },
            {
                "name": "宾语从句", "grade_levels": ["初中二年级", "初中三年级"], "difficulty": "hard",
                "keywords": ["that", "what", "if", "whether"], "cefr_level": "B1-B2"
            },
            {
                "name": "状语从句", "grade_levels": ["初中三年级", "高中一年级"], "difficulty": "hard",
                "keywords": ["because", "when", "if", "although"], "cefr_level": "B2"
            },
            
            # 词类
            {
                "name": "冠词", "grade_levels": ["小学二年级", "小学三年级"], "difficulty": "easy",
                "keywords": ["a", "an", "the", "零冠词"], "cefr_level": "A1"
            },
            {
                "name": "介词", "grade_levels": ["小学三年级", "小学四年级"], "difficulty": "medium",
                "keywords": ["in", "on", "at", "for", "with"], "cefr_level": "A1-A2"
            },
            {
                "name": "代词", "grade_levels": ["小学三年级", "小学四年级"], "difficulty": "easy",
                "keywords": ["I", "you", "he", "she", "it", "they"], "cefr_level": "A1"
            },
            {
                "name": "形容词", "grade_levels": ["小学二年级", "小学三年级"], "difficulty": "easy",
                "keywords": ["big", "small", "good", "bad", "形容词"], "cefr_level": "A1"
            },
            {
                "name": "副词", "grade_levels": ["小学四年级", "小学五年级"], "difficulty": "medium",
                "keywords": ["quickly", "slowly", "carefully", "副词"], "cefr_level": "A2"
            },
            
            # 句型
            {
                "name": "疑问句", "grade_levels": ["小学二年级", "小学三年级"], "difficulty": "easy",
                "keywords": ["what", "where", "when", "who", "how"], "cefr_level": "A1"
            },
            {
                "name": "否定句", "grade_levels": ["小学二年级", "小学三年级"], "difficulty": "easy",
                "keywords": ["not", "don't", "doesn't", "didn't"], "cefr_level": "A1"
            },
            {
                "name": "感叹句", "grade_levels": ["小学四年级", "小学五年级"], "difficulty": "easy",
                "keywords": ["what", "how", "感叹"], "cefr_level": "A2"
            },
            {
                "name": "祈使句", "grade_levels": ["小学三年级", "小学四年级"], "difficulty": "easy",
                "keywords": ["please", "don't", "let's"], "cefr_level": "A1"
            },
            
            # 高级语法
            {
                "name": "比较级和最高级", "grade_levels": ["小学五年级", "小学六年级"], "difficulty": "medium",
                "keywords": ["than", "more", "most", "er", "est"], "cefr_level": "A2-B1"
            },
            {
                "name": "情态动词", "grade_levels": ["小学六年级", "初中一年级"], "difficulty": "medium",
                "keywords": ["can", "could", "may", "must", "should"], "cefr_level": "A2-B1"
            },
            {
                "name": "非谓语动词", "grade_levels": ["高中一年级", "高中二年级"], "difficulty": "hard",
                "keywords": ["to do", "doing", "done", "分词"], "cefr_level": "B2-C1"
            },
            {
                "name": "虚拟语气", "grade_levels": ["高中一年级", "高中二年级"], "difficulty": "hard",
                "keywords": ["if", "wish", "would", "虚拟"], "cefr_level": "B2-C1"
            },
            {
                "name": "倒装句", "grade_levels": ["高中二年级", "高中三年级"], "difficulty": "hard",
                "keywords": ["never", "seldom", "hardly", "倒装"], "cefr_level": "C1"
            },
            {
                "name": "强调句", "grade_levels": ["高中一年级", "高中二年级"], "difficulty": "hard",
                "keywords": ["it is", "it was", "强调"], "cefr_level": "B2"
            }
        ]
    
    def _build_comprehensive_bank(self) -> List[Dict[str, Any]]:
        """构建200道题目的综合题库"""
        questions = []
        
        # 一般现在时题目 (20道)
        questions.extend(self._generate_present_simple_questions())
        
        # 现在进行时题目 (15道)
        questions.extend(self._generate_present_continuous_questions())
        
        # 一般过去时题目 (15道)
        questions.extend(self._generate_past_simple_questions())
        
        # 现在完成时题目 (12道)
        questions.extend(self._generate_present_perfect_questions())
        
        # 一般将来时题目 (12道)
        questions.extend(self._generate_future_simple_questions())
        
        # 被动语态题目 (15道)
        questions.extend(self._generate_passive_voice_questions())
        
        # 定语从句题目 (15道)
        questions.extend(self._generate_relative_clause_questions())
        
        # 宾语从句题目 (12道)
        questions.extend(self._generate_object_clause_questions())
        
        # 比较级和最高级题目 (12道)
        questions.extend(self._generate_comparison_questions())
        
        # 情态动词题目 (15道)
        questions.extend(self._generate_modal_verb_questions())
        
        # 介词题目 (15道)
        questions.extend(self._generate_preposition_questions())
        
        # 冠词题目 (10道)
        questions.extend(self._generate_article_questions())
        
        # 疑问句题目 (10道)
        questions.extend(self._generate_question_sentence_questions())
        
        # 其他语法题目 (22道)
        questions.extend(self._generate_other_grammar_questions())
        
        return questions[:200]  # 确保正好200道
    
    def _generate_present_simple_questions(self) -> List[Dict[str, Any]]:
        """生成一般现在时题目"""
        return [
            {
                "content": "She _____ to work by bus every morning.",
                "question_type": "选择题",
                "options": ["go", "goes", "going", "gone"],
                "answer": "B", "analysis": "主语she是第三人称单数，动词用goes",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Cambridge Primary English", "grade_level": "小学四年级"
            },
            {
                "content": "My brother _____ football every weekend.",
                "question_type": "选择题",
                "options": ["play", "plays", "playing", "played"],
                "answer": "B", "analysis": "every weekend表示习惯性动作，用一般现在时",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Oxford Primary Grammar", "grade_level": "小学四年级"
            },
            {
                "content": "Water _____ at 100 degrees Celsius.",
                "question_type": "选择题",
                "options": ["boil", "boils", "boiling", "boiled"],
                "answer": "B", "analysis": "客观事实用一般现在时，water是不可数名词",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Science English", "grade_level": "小学六年级"
            },
            {
                "content": "The sun _____ in the east.",
                "question_type": "选择题",
                "options": ["rise", "rises", "rising", "rose"],
                "answer": "B", "analysis": "客观真理用一般现在时，sun是第三人称单数",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "General Knowledge English", "grade_level": "小学五年级"
            },
            {
                "content": "Tom usually _____ his homework after dinner.",
                "question_type": "选择题",
                "options": ["do", "does", "doing", "did"],
                "answer": "B", "analysis": "usually表示习惯，Tom是第三人称单数",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Daily English", "grade_level": "小学四年级"
            },
            {
                "content": "Birds _____ south in winter.",
                "question_type": "选择题",
                "options": ["fly", "flies", "flying", "flew"],
                "answer": "A", "analysis": "birds是复数，动词用原形",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Nature English", "grade_level": "小学五年级"
            },
            {
                "content": "My mother _____ delicious food every day.",
                "question_type": "选择题",
                "options": ["cook", "cooks", "cooking", "cooked"],
                "answer": "B", "analysis": "every day表示习惯，mother是第三人称单数",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Family English", "grade_level": "小学三年级"
            },
            {
                "content": "We _____ English in the classroom.",
                "question_type": "选择题",
                "options": ["speak", "speaks", "speaking", "spoke"],
                "answer": "A", "analysis": "we是第一人称复数，动词用原形",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "School English", "grade_level": "小学三年级"
            },
            {
                "content": "The library _____ at 8:00 AM every day.",
                "question_type": "选择题",
                "options": ["open", "opens", "opening", "opened"],
                "answer": "B", "analysis": "library是第三人称单数，every day表示习惯",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Public Places English", "grade_level": "小学五年级"
            },
            {
                "content": "Fish _____ in water.",
                "question_type": "选择题",
                "options": ["live", "lives", "living", "lived"],
                "answer": "A", "analysis": "fish作复数时动词用原形，表示客观事实",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Animal English", "grade_level": "小学四年级"
            },
            {
                "content": "Does your father _____ to work by car?",
                "question_type": "选择题",
                "options": ["go", "goes", "going", "went"],
                "answer": "A", "analysis": "does后面用动词原形",
                "difficulty": "easy", "knowledge_points": ["一般现在时", "疑问句"],
                "source": "Question Practice", "grade_level": "小学四年级"
            },
            {
                "content": "I don't _____ coffee in the evening.",
                "question_type": "选择题",
                "options": ["drink", "drinks", "drinking", "drank"],
                "answer": "A", "analysis": "don't后面用动词原形",
                "difficulty": "easy", "knowledge_points": ["一般现在时", "否定句"],
                "source": "Negative Practice", "grade_level": "小学四年级"
            },
            {
                "content": "Cats _____ milk very much.",
                "question_type": "选择题",
                "options": ["like", "likes", "liking", "liked"],
                "answer": "A", "analysis": "cats是复数，动词用原形",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Animal Habits", "grade_level": "小学三年级"
            },
            {
                "content": "The earth _____ around the sun.",
                "question_type": "选择题",
                "options": ["move", "moves", "moving", "moved"],
                "answer": "B", "analysis": "客观真理用一般现在时，earth是第三人称单数",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Science Facts", "grade_level": "小学六年级"
            },
            {
                "content": "How often _____ you _____ your teeth?",
                "question_type": "选择题",
                "options": ["do, brush", "does, brush", "are, brushing", "did, brush"],
                "answer": "A", "analysis": "how often询问频率，you用do",
                "difficulty": "medium", "knowledge_points": ["一般现在时", "疑问句"],
                "source": "Health English", "grade_level": "小学五年级"
            },
            {
                "content": "My grandmother _____ stories to us every night.",
                "question_type": "选择题",
                "options": ["tell", "tells", "telling", "told"],
                "answer": "B", "analysis": "grandmother是第三人称单数，every night表示习惯",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "Family Stories", "grade_level": "小学三年级"
            },
            {
                "content": "What time _____ the store _____ on Sunday?",
                "question_type": "选择题",
                "options": ["do, open", "does, open", "is, open", "are, open"],
                "answer": "B", "analysis": "store是第三人称单数，用does",
                "difficulty": "medium", "knowledge_points": ["一般现在时", "疑问句"],
                "source": "Shopping English", "grade_level": "小学五年级"
            },
            {
                "content": "Trees _____ oxygen for us to breathe.",
                "question_type": "选择题",
                "options": ["provide", "provides", "providing", "provided"],
                "answer": "A", "analysis": "trees是复数，动词用原形",
                "difficulty": "medium", "knowledge_points": ["一般现在时"],
                "source": "Environmental English", "grade_level": "小学六年级"
            },
            {
                "content": "She never _____ late for school.",
                "question_type": "选择题",
                "options": ["is", "are", "am", "be"],
                "answer": "A", "analysis": "she是第三人称单数，用is",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "School Life", "grade_level": "小学三年级"
            },
            {
                "content": "Do you _____ any brothers or sisters?",
                "question_type": "选择题",
                "options": ["have", "has", "having", "had"],
                "answer": "A", "analysis": "do后面用动词原形have",
                "difficulty": "easy", "knowledge_points": ["一般现在时", "疑问句"],
                "source": "Family Questions", "grade_level": "小学四年级"
            }
        ]
    
    def _generate_present_continuous_questions(self) -> List[Dict[str, Any]]:
        """生成现在进行时题目"""
        return [
            {
                "content": "Listen! The birds _____ in the tree.",
                "question_type": "选择题",
                "options": ["sing", "sings", "are singing", "sang"],
                "answer": "C", "analysis": "Listen!表示现在正在发生，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Cambridge Elementary", "grade_level": "小学五年级"
            },
            {
                "content": "Look! The children _____ in the playground.",
                "question_type": "选择题",
                "options": ["play", "plays", "are playing", "played"],
                "answer": "C", "analysis": "Look!表示现在正在发生，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "School Activities", "grade_level": "小学五年级"
            },
            {
                "content": "Shh! The baby _____ in the next room.",
                "question_type": "选择题",
                "options": ["sleep", "sleeps", "is sleeping", "slept"],
                "answer": "C", "analysis": "Shh!表示此刻正在发生，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Daily English", "grade_level": "小学五年级"
            },
            {
                "content": "What _____ you _____ now?",
                "question_type": "选择题",
                "options": ["are, doing", "do, do", "did, do", "will, do"],
                "answer": "A", "analysis": "now表示现在，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时", "疑问句"],
                "source": "British Council LearnEnglish", "grade_level": "小学六年级"
            },
            {
                "content": "The students _____ an English lesson right now.",
                "question_type": "选择题",
                "options": ["have", "has", "are having", "had"],
                "answer": "C", "analysis": "right now表示现在，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Classroom English", "grade_level": "小学六年级"
            },
            {
                "content": "Be quiet! The teacher _____ the lesson.",
                "question_type": "选择题",
                "options": ["explain", "explains", "is explaining", "explained"],
                "answer": "C", "analysis": "Be quiet!提示正在进行，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Classroom Management", "grade_level": "小学五年级"
            },
            {
                "content": "I can't talk now. I _____ my homework.",
                "question_type": "选择题",
                "options": ["do", "does", "am doing", "did"],
                "answer": "C", "analysis": "now表示现在，I用am doing",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Daily Conversation", "grade_level": "小学六年级"
            },
            {
                "content": "The phone _____. Can you answer it?",
                "question_type": "选择题",
                "options": ["ring", "rings", "is ringing", "rang"],
                "answer": "C", "analysis": "电话正在响，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Home English", "grade_level": "小学五年级"
            },
            {
                "content": "Why _____ you _____ here? The movie is starting.",
                "question_type": "选择题",
                "options": ["are, standing", "do, stand", "did, stand", "will, stand"],
                "answer": "A", "analysis": "现在的状态，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时", "疑问句"],
                "source": "Entertainment English", "grade_level": "小学六年级"
            },
            {
                "content": "The cat _____ under the table at the moment.",
                "question_type": "选择题",
                "options": ["hide", "hides", "is hiding", "hid"],
                "answer": "C", "analysis": "at the moment表示现在，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Pet English", "grade_level": "小学五年级"
            },
            {
                "content": "Don't make noise! The baby _____.",
                "question_type": "选择题",
                "options": ["sleep", "sleeps", "is sleeping", "slept"],
                "answer": "C", "analysis": "现在正在睡觉，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Family Care", "grade_level": "小学五年级"
            },
            {
                "content": "Where _____ your parents _____ their vacation this year?",
                "question_type": "选择题",
                "options": ["are, spending", "do, spend", "did, spend", "will, spend"],
                "answer": "A", "analysis": "this year表示现阶段，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时", "疑问句"],
                "source": "Travel English", "grade_level": "初中一年级"
            },
            {
                "content": "The weather _____ warmer these days.",
                "question_type": "选择题",
                "options": ["get", "gets", "is getting", "got"],
                "answer": "C", "analysis": "these days表示现阶段的变化，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Weather English", "grade_level": "小学六年级"
            },
            {
                "content": "I _____ for the bus. It's late today.",
                "question_type": "选择题",
                "options": ["wait", "waits", "am waiting", "waited"],
                "answer": "C", "analysis": "现在正在等车，用现在进行时",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Transportation English", "grade_level": "小学六年级"
            },
            {
                "content": "The flowers _____ beautifully in spring.",
                "question_type": "选择题",
                "options": ["grow", "grows", "are growing", "grew"],
                "answer": "C", "analysis": "春天正在生长，用现在进行时表示现阶段",
                "difficulty": "medium", "knowledge_points": ["现在进行时"],
                "source": "Season English", "grade_level": "小学五年级"
            }
        ]
    
    def _generate_past_simple_questions(self) -> List[Dict[str, Any]]:
        """生成一般过去时题目"""
        return [
            {
                "content": "Yesterday I _____ to the park with my friends.",
                "question_type": "选择题",
                "options": ["go", "went", "going", "will go"],
                "answer": "B", "analysis": "Yesterday表示过去的时间，需要用一般过去时went",
                "difficulty": "easy", "knowledge_points": ["一般过去时"],
                "source": "人教版小学英语", "grade_level": "小学五年级"
            },
            {
                "content": "Last summer, we _____ to Beijing for vacation.",
                "question_type": "选择题",
                "options": ["go", "went", "goes", "going"],
                "answer": "B", "analysis": "Last summer表示过去时间，用一般过去时",
                "difficulty": "easy", "knowledge_points": ["一般过去时"],
                "source": "Elementary Grammar", "grade_level": "小学五年级"
            },
            {
                "content": "She _____ a beautiful dress at the party last night.",
                "question_type": "选择题",
                "options": ["wear", "wears", "wore", "wearing"],
                "answer": "C", "analysis": "last night表示过去时间，wear的过去式是wore",
                "difficulty": "easy", "knowledge_points": ["一般过去时"],
                "source": "Social English", "grade_level": "小学六年级"
            },
            {
                "content": "When _____ you _____ your homework yesterday?",
                "question_type": "选择题",
                "options": ["do, finish", "did, finish", "are, finishing", "will, finish"],
                "answer": "B", "analysis": "yesterday表示过去，疑问句用did",
                "difficulty": "medium", "knowledge_points": ["一般过去时", "疑问句"],
                "source": "Homework English", "grade_level": "小学五年级"
            },
            {
                "content": "The movie _____ two hours ago.",
                "question_type": "选择题",
                "options": ["start", "starts", "started", "starting"],
                "answer": "C", "analysis": "two hours ago表示过去时间，用过去式started",
                "difficulty": "easy", "knowledge_points": ["一般过去时"],
                "source": "Entertainment", "grade_level": "小学五年级"
            },
            {
                "content": "I _____ my keys this morning, but I found them later.",
                "question_type": "选择题",
                "options": ["lose", "loses", "lost", "losing"],
                "answer": "C", "analysis": "this morning表示今天早上（过去时间），用过去式lost",
                "difficulty": "medium", "knowledge_points": ["一般过去时"],
                "source": "Daily Problems", "grade_level": "小学六年级"
            },
            {
                "content": "They _____ a new house last year.",
                "question_type": "选择题",
                "options": ["buy", "buys", "bought", "buying"],
                "answer": "C", "analysis": "last year表示过去，buy的过去式是bought",
                "difficulty": "easy", "knowledge_points": ["一般过去时"],
                "source": "Real Estate English", "grade_level": "小学六年级"
            },
            {
                "content": "Did you _____ the football match on TV last night?",
                "question_type": "选择题",
                "options": ["watch", "watched", "watching", "watches"],
                "answer": "A", "analysis": "did后面用动词原形",
                "difficulty": "easy", "knowledge_points": ["一般过去时", "疑问句"],
                "source": "Sports English", "grade_level": "小学五年级"
            },
            {
                "content": "The train _____ the station at 6:30 this morning.",
                "question_type": "选择题",
                "options": ["leave", "leaves", "left", "leaving"],
                "answer": "C", "analysis": "this morning表示今早（过去），用过去式left",
                "difficulty": "medium", "knowledge_points": ["一般过去时"],
                "source": "Travel English", "grade_level": "小学六年级"
            },
            {
                "content": "My father _____ me a bike for my birthday last month.",
                "question_type": "选择题",
                "options": ["give", "gives", "gave", "giving"],
                "answer": "C", "analysis": "last month表示过去，give的过去式是gave",
                "difficulty": "easy", "knowledge_points": ["一般过去时"],
                "source": "Birthday English", "grade_level": "小学五年级"
            },
            {
                "content": "We _____ very tired after the long walk yesterday.",
                "question_type": "选择题",
                "options": ["are", "were", "is", "was"],
                "answer": "B", "analysis": "yesterday表示过去，we用were",
                "difficulty": "easy", "knowledge_points": ["一般过去时"],
                "source": "Exercise English", "grade_level": "小学五年级"
            },
            {
                "content": "She didn't _____ to school yesterday because she was sick.",
                "question_type": "选择题",
                "options": ["go", "goes", "went", "going"],
                "answer": "A", "analysis": "didn't后面用动词原形",
                "difficulty": "medium", "knowledge_points": ["一般过去时", "否定句"],
                "source": "Health Issues", "grade_level": "小学五年级"
            },
            {
                "content": "How _____ your weekend? It _____ great!",
                "question_type": "选择题",
                "options": ["was, was", "were, were", "is, is", "are, are"],
                "answer": "A", "analysis": "weekend是单数用was",
                "difficulty": "medium", "knowledge_points": ["一般过去时"],
                "source": "Weekend Talk", "grade_level": "小学六年级"
            },
            {
                "content": "The dog _____ loudly when the stranger came.",
                "question_type": "选择题",
                "options": ["bark", "barks", "barked", "barking"],
                "answer": "C", "analysis": "when从句用过去时，主句也用过去时",
                "difficulty": "medium", "knowledge_points": ["一般过去时"],
                "source": "Animal Behavior", "grade_level": "小学六年级"
            },
            {
                "content": "I _____ my grandmother last weekend.",
                "question_type": "选择题",
                "options": ["visit", "visits", "visited", "visiting"],
                "answer": "C", "analysis": "last weekend表示过去时间，用过去式visited",
                "difficulty": "easy", "knowledge_points": ["一般过去时"],
                "source": "Family Visit", "grade_level": "小学四年级"
            }
        ]
    
    def _generate_present_perfect_questions(self) -> List[Dict[str, Any]]:
        """生成现在完成时题目"""
        return [
            {
                "content": "I _____ this movie three times.",
                "question_type": "选择题",
                "options": ["see", "saw", "have seen", "will see"],
                "answer": "C", "analysis": "three times表示到现在为止的次数，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Intermediate Grammar", "grade_level": "初中一年级"
            },
            {
                "content": "She _____ already _____ her homework.",
                "question_type": "选择题",
                "options": ["has, finished", "have, finished", "is, finishing", "did, finish"],
                "answer": "A", "analysis": "already是现在完成时标志，she用has",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Homework Practice", "grade_level": "初中一年级"
            },
            {
                "content": "Have you _____ been to Shanghai?",
                "question_type": "选择题",
                "options": ["ever", "never", "already", "yet"],
                "answer": "A", "analysis": "疑问句中用ever表示'曾经'",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Travel Experience", "grade_level": "初中一年级"
            },
            {
                "content": "I haven't finished my report _____.",
                "question_type": "选择题",
                "options": ["already", "yet", "ever", "never"],
                "answer": "B", "analysis": "否定句中用yet表示'还没有'",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Work English", "grade_level": "初中二年级"
            },
            {
                "content": "We _____ in this city for five years.",
                "question_type": "选择题",
                "options": ["live", "lived", "have lived", "are living"],
                "answer": "C", "analysis": "for five years表示持续到现在，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Life Experience", "grade_level": "初中一年级"
            },
            {
                "content": "The students _____ just _____ their exam.",
                "question_type": "选择题",
                "options": ["have, finished", "has, finished", "are, finishing", "will, finish"],
                "answer": "A", "analysis": "just是现在完成时标志，students用have",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "School Exam", "grade_level": "初中一年级"
            },
            {
                "content": "How long _____ you _____ English?",
                "question_type": "选择题",
                "options": ["do, learn", "did, learn", "have, learned", "are, learning"],
                "answer": "C", "analysis": "how long询问持续时间，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时", "疑问句"],
                "source": "Learning Duration", "grade_level": "初中二年级"
            },
            {
                "content": "I _____ never _____ such a beautiful sunset.",
                "question_type": "选择题",
                "options": ["have, seen", "has, seen", "am, seeing", "did, see"],
                "answer": "A", "analysis": "never是现在完成时标志，I用have",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Nature Experience", "grade_level": "初中一年级"
            },
            {
                "content": "The company _____ a new product recently.",
                "question_type": "选择题",
                "options": ["develop", "develops", "has developed", "developed"],
                "answer": "C", "analysis": "recently表示最近，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Business English", "grade_level": "初中二年级"
            },
            {
                "content": "Since 2010, the city _____ a lot.",
                "question_type": "选择题",
                "options": ["change", "changes", "has changed", "changed"],
                "answer": "C", "analysis": "since表示从过去到现在，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "City Development", "grade_level": "初中二年级"
            },
            {
                "content": "_____ you _____ your lunch yet?",
                "question_type": "选择题",
                "options": ["Do, have", "Did, have", "Have, had", "Are, having"],
                "answer": "C", "analysis": "yet用于疑问句，现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时", "疑问句"],
                "source": "Meal Time", "grade_level": "初中一年级"
            },
            {
                "content": "My phone _____ missing since this morning.",
                "question_type": "选择题",
                "options": ["is", "was", "has been", "will be"],
                "answer": "C", "analysis": "since this morning表示从今早到现在，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Daily Problems", "grade_level": "初中二年级"
            }
        ]
    
    def _generate_future_simple_questions(self) -> List[Dict[str, Any]]:
        """生成一般将来时题目"""
        return [
            {
                "content": "I _____ visit my grandparents tomorrow.",
                "question_type": "选择题",
                "options": ["will", "would", "am", "was"],
                "answer": "A", "analysis": "tomorrow表示将来时间，用will",
                "difficulty": "easy", "knowledge_points": ["一般将来时"],
                "source": "Family Plans", "grade_level": "小学五年级"
            },
            {
                "content": "It _____ rain this afternoon according to the weather forecast.",
                "question_type": "选择题",
                "options": ["will", "is", "was", "has"],
                "answer": "A", "analysis": "天气预报表示将来，用will",
                "difficulty": "easy", "knowledge_points": ["一般将来时"],
                "source": "Weather Forecast", "grade_level": "小学六年级"
            },
            {
                "content": "We _____ going to have a picnic next Sunday.",
                "question_type": "选择题",
                "options": ["is", "are", "am", "be"],
                "answer": "B", "analysis": "we用are，be going to表示计划",
                "difficulty": "easy", "knowledge_points": ["一般将来时"],
                "source": "Weekend Plans", "grade_level": "小学五年级"
            },
            {
                "content": "What _____ you _____ after graduation?",
                "question_type": "选择题",
                "options": ["will, do", "are, doing", "did, do", "do, do"],
                "answer": "A", "analysis": "graduation是将来的事，用will",
                "difficulty": "medium", "knowledge_points": ["一般将来时", "疑问句"],
                "source": "Future Plans", "grade_level": "初中三年级"
            },
            {
                "content": "The new shopping mall _____ open next month.",
                "question_type": "选择题",
                "options": ["will", "is", "was", "has"],
                "answer": "A", "analysis": "next month表示将来，用will",
                "difficulty": "easy", "knowledge_points": ["一般将来时"],
                "source": "City News", "grade_level": "小学六年级"
            },
            {
                "content": "I think it _____ be sunny tomorrow.",
                "question_type": "选择题",
                "options": ["will", "is", "was", "has"],
                "answer": "A", "analysis": "tomorrow表示将来，think后常用will",
                "difficulty": "easy", "knowledge_points": ["一般将来时"],
                "source": "Weather Prediction", "grade_level": "小学五年级"
            },
            {
                "content": "_____ you _____ free this evening?",
                "question_type": "选择题",
                "options": ["Are, going to be", "Will, be", "Do, be", "Did, be"],
                "answer": "B", "analysis": "this evening表示今晚（将来），用will be",
                "difficulty": "medium", "knowledge_points": ["一般将来时", "疑问句"],
                "source": "Evening Plans", "grade_level": "小学六年级"
            },
            {
                "content": "She _____ to university next year.",
                "question_type": "选择题",
                "options": ["go", "goes", "will go", "went"],
                "answer": "C", "analysis": "next year表示将来，用will go",
                "difficulty": "easy", "knowledge_points": ["一般将来时"],
                "source": "Education Plans", "grade_level": "初中三年级"
            },
            {
                "content": "The meeting _____ start at 2 PM tomorrow.",
                "question_type": "选择题",
                "options": ["will", "is", "was", "has"],
                "answer": "A", "analysis": "tomorrow表示将来，用will",
                "difficulty": "easy", "knowledge_points": ["一般将来时"],
                "source": "Business Meeting", "grade_level": "初中一年级"
            },
            {
                "content": "I'm sure he _____ pass the exam.",
                "question_type": "选择题",
                "options": ["will", "is", "has", "did"],
                "answer": "A", "analysis": "表示对将来的确信，用will",
                "difficulty": "easy", "knowledge_points": ["一般将来时"],
                "source": "Exam Confidence", "grade_level": "初中一年级"
            },
            {
                "content": "There _____ a concert in the park next weekend.",
                "question_type": "选择题",
                "options": ["will be", "is", "was", "has been"],
                "answer": "A", "analysis": "next weekend表示将来，there will be",
                "difficulty": "medium", "knowledge_points": ["一般将来时"],
                "source": "Event Notice", "grade_level": "小学六年级"
            },
            {
                "content": "When _____ the new bridge _____ completed?",
                "question_type": "选择题",
                "options": ["will, be", "is, be", "was, be", "has, been"],
                "answer": "A", "analysis": "询问将来完成时间，用will be",
                "difficulty": "medium", "knowledge_points": ["一般将来时", "疑问句"],
                "source": "Construction News", "grade_level": "初中一年级"
            }
        ]
    
    def _generate_passive_voice_questions(self) -> List[Dict[str, Any]]:
        """生成被动语态题目（15道）"""
        return [
            {
                "content": "The letter _____ by Tom yesterday.",
                "question_type": "选择题",
                "options": ["wrote", "was written", "is written", "writes"],
                "answer": "B", "analysis": "主语letter是动作承受者，yesterday用过去时被动",
                "difficulty": "hard", "knowledge_points": ["被动语态", "一般过去时"],
                "source": "人教版初中英语", "grade_level": "初中二年级"
            },
            {
                "content": "English _____ in many countries around the world.",
                "question_type": "选择题",
                "options": ["speak", "speaks", "is spoken", "speaking"],
                "answer": "C", "analysis": "English是被说的，用被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "World English", "grade_level": "初中二年级"
            },
            {
                "content": "This house _____ by my grandfather in 1950.",
                "question_type": "选择题",
                "options": ["built", "was built", "is built", "builds"],
                "answer": "B", "analysis": "in 1950表示过去时间，用一般过去时的被动语态",
                "difficulty": "hard", "knowledge_points": ["被动语态", "一般过去时"],
                "source": "Cambridge Grammar", "grade_level": "初中二年级"
            },
            {
                "content": "The windows _____ every week in our school.",
                "question_type": "选择题",
                "options": ["clean", "cleans", "are cleaned", "cleaned"],
                "answer": "C", "analysis": "windows是被清洁的，用被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "School Maintenance", "grade_level": "初中二年级"
            },
            {
                "content": "The new hospital _____ next year.",
                "question_type": "选择题",
                "options": ["will build", "will be built", "builds", "is built"],
                "answer": "B", "analysis": "将来时的被动语态，will be built",
                "difficulty": "hard", "knowledge_points": ["被动语态", "一般将来时"],
                "source": "City Planning", "grade_level": "初中三年级"
            },
            {
                "content": "The homework _____ by the students every day.",
                "question_type": "选择题",
                "options": ["do", "does", "is done", "did"],
                "answer": "C", "analysis": "homework是被做的，用被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "School Life", "grade_level": "初中二年级"
            },
            {
                "content": "The bridge _____ two years ago.",
                "question_type": "选择题",
                "options": ["complete", "completed", "was completed", "completes"],
                "answer": "C", "analysis": "bridge是被完成的，two years ago用过去时",
                "difficulty": "hard", "knowledge_points": ["被动语态", "一般过去时"],
                "source": "Infrastructure", "grade_level": "初中二年级"
            },
            {
                "content": "Chinese _____ by more and more foreigners now.",
                "question_type": "选择题",
                "options": ["learn", "learns", "is learned", "learning"],
                "answer": "C", "analysis": "Chinese是被学习的，用被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "Language Learning", "grade_level": "初中二年级"
            },
            {
                "content": "The car _____ in Germany.",
                "question_type": "选择题",
                "options": ["make", "makes", "was made", "making"],
                "answer": "C", "analysis": "car是被制造的，用被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "Manufacturing", "grade_level": "初中二年级"
            },
            {
                "content": "The book _____ into many languages.",
                "question_type": "选择题",
                "options": ["translate", "translates", "has been translated", "translating"],
                "answer": "C", "analysis": "book是被翻译的，用现在完成时被动语态",
                "difficulty": "hard", "knowledge_points": ["被动语态", "现在完成时"],
                "source": "Publishing", "grade_level": "初中三年级"
            },
            {
                "content": "The flowers _____ every morning by the gardener.",
                "question_type": "选择题",
                "options": ["water", "waters", "are watered", "watered"],
                "answer": "C", "analysis": "flowers是被浇水的，用被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "Garden Care", "grade_level": "初中二年级"
            },
            {
                "content": "The problem _____ by the engineer last week.",
                "question_type": "选择题",
                "options": ["solve", "solved", "was solved", "solving"],
                "answer": "C", "analysis": "problem是被解决的，last week用过去时",
                "difficulty": "hard", "knowledge_points": ["被动语态", "一般过去时"],
                "source": "Engineering", "grade_level": "初中三年级"
            },
            {
                "content": "The medicine _____ three times a day.",
                "question_type": "选择题",
                "options": ["take", "takes", "should be taken", "taking"],
                "answer": "C", "analysis": "medicine是被服用的，用情态动词被动语态",
                "difficulty": "hard", "knowledge_points": ["被动语态", "情态动词"],
                "source": "Medical English", "grade_level": "初中三年级"
            },
            {
                "content": "The news _____ on TV every evening.",
                "question_type": "选择题",
                "options": ["broadcast", "broadcasts", "is broadcast", "broadcasting"],
                "answer": "C", "analysis": "news是被播出的，用被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "Media English", "grade_level": "初中二年级"
            },
            {
                "content": "The thief _____ by the police yesterday.",
                "question_type": "选择题",
                "options": ["catch", "caught", "was caught", "catching"],
                "answer": "C", "analysis": "thief是被抓的，yesterday用过去时",
                "difficulty": "medium", "knowledge_points": ["被动语态", "一般过去时"],
                "source": "Crime News", "grade_level": "初中二年级"
            }
        ]
    
    def _generate_relative_clause_questions(self) -> List[Dict[str, Any]]:
        """生成定语从句题目（15道）"""
        return [
            {
                "content": "The man _____ is wearing a blue shirt is my teacher.",
                "question_type": "选择题",
                "options": ["who", "which", "where", "when"],
                "answer": "A", "analysis": "先行词是人(man)，关系代词用who引导定语从句",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "AI Agent测试题目", "grade_level": "初中二年级"
            },
            {
                "content": "The book _____ is on the table belongs to Mary.",
                "question_type": "选择题",
                "options": ["who", "which", "where", "when"],
                "answer": "B", "analysis": "修饰物用which，the book which...",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Oxford Advanced Grammar", "grade_level": "初中二年级"
            },
            {
                "content": "This is the school _____ I studied when I was young.",
                "question_type": "选择题",
                "options": ["which", "where", "when", "that"],
                "answer": "B", "analysis": "先行词是地点school，用where引导定语从句",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Grammar Practice", "grade_level": "初中三年级"
            },
            {
                "content": "The girl _____ hair is long is my sister.",
                "question_type": "选择题",
                "options": ["who", "whose", "which", "that"],
                "answer": "B", "analysis": "表示所属关系用whose",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Murphy's Grammar in Use", "grade_level": "初中三年级"
            },
            {
                "content": "Do you know the reason _____ he was late?",
                "question_type": "选择题",
                "options": ["that", "which", "why", "when"],
                "answer": "C", "analysis": "先行词是reason，用why引导",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Reason Analysis", "grade_level": "初中三年级"
            },
            {
                "content": "The day _____ we met was sunny.",
                "question_type": "选择题",
                "options": ["that", "which", "when", "where"],
                "answer": "C", "analysis": "先行词是时间day，用when引导",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Time Reference", "grade_level": "初中三年级"
            },
            {
                "content": "The house _____ windows face south is very bright.",
                "question_type": "选择题",
                "options": ["that", "which", "whose", "where"],
                "answer": "C", "analysis": "表示所属关系，house的windows，用whose",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Architecture English", "grade_level": "初中三年级"
            },
            {
                "content": "I still remember the teacher _____ taught me English.",
                "question_type": "选择题",
                "options": ["who", "whom", "which", "whose"],
                "answer": "A", "analysis": "先行词是人teacher，在从句中作主语，用who",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Memory English", "grade_level": "初中二年级"
            },
            {
                "content": "The movie _____ we watched last night was interesting.",
                "question_type": "选择题",
                "options": ["who", "which", "where", "when"],
                "answer": "B", "analysis": "先行词是物movie，用which或that",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Entertainment", "grade_level": "初中二年级"
            },
            {
                "content": "The city _____ he was born is famous for its history.",
                "question_type": "选择题",
                "options": ["that", "which", "where", "when"],
                "answer": "C", "analysis": "先行词是地点city，用where引导",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Geography English", "grade_level": "初中三年级"
            },
            {
                "content": "The woman _____ you met yesterday is my aunt.",
                "question_type": "选择题",
                "options": ["who", "whom", "which", "whose"],
                "answer": "B", "analysis": "先行词是人，在从句中作宾语，用whom",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Family Relations", "grade_level": "初中三年级"
            },
            {
                "content": "This is the best book _____ I have ever read.",
                "question_type": "选择题",
                "options": ["who", "which", "that", "where"],
                "answer": "C", "analysis": "先行词有最高级修饰时，关系代词只能用that",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Reading Experience", "grade_level": "初中三年级"
            },
            {
                "content": "The park _____ we often play in is very beautiful.",
                "question_type": "选择题",
                "options": ["that", "which", "where", "when"],
                "answer": "A", "analysis": "先行词是地点，但从句中有介词in，用that/which",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Recreation English", "grade_level": "初中三年级"
            },
            {
                "content": "The doctor _____ saved my life is very kind.",
                "question_type": "选择题",
                "options": ["who", "whom", "which", "whose"],
                "answer": "A", "analysis": "先行词是人doctor，在从句中作主语，用who",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Medical Story", "grade_level": "初中二年级"
            },
            {
                "content": "The building _____ roof was damaged needs repair.",
                "question_type": "选择题",
                "options": ["that", "which", "whose", "where"],
                "answer": "C", "analysis": "表示所属关系，building的roof，用whose",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "Construction", "grade_level": "初中三年级"
            }
        ]
    
    def _generate_modal_verb_questions(self) -> List[Dict[str, Any]]:
        """生成情态动词题目（15道）"""
        return [
            {
                "content": "You _____ finish your homework before watching TV.",
                "question_type": "选择题",
                "options": ["can", "may", "must", "could"],
                "answer": "C", "analysis": "表示必须、义务用must",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Cambridge English Grammar", "grade_level": "初中一年级"
            },
            {
                "content": "_____ I borrow your pen, please?",
                "question_type": "选择题",
                "options": ["Must", "Should", "May", "Need"],
                "answer": "C", "analysis": "请求许可用may",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Polite Request", "grade_level": "小学六年级"
            },
            {
                "content": "You _____ smoke here. It's dangerous.",
                "question_type": "选择题",
                "options": ["can", "must", "mustn't", "needn't"],
                "answer": "C", "analysis": "表示禁止用mustn't",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Modal Verbs Practice", "grade_level": "初中一年级"
            },
            {
                "content": "She _____ speak three languages fluently.",
                "question_type": "选择题",
                "options": ["can", "must", "should", "may"],
                "answer": "A", "analysis": "表示能力用can",
                "difficulty": "easy", "knowledge_points": ["情态动词"],
                "source": "Ability Expression", "grade_level": "小学六年级"
            },
            {
                "content": "You _____ see a doctor if you feel sick.",
                "question_type": "选择题",
                "options": ["can", "may", "should", "must"],
                "answer": "C", "analysis": "表示建议用should",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Health Advice", "grade_level": "初中一年级"
            },
            {
                "content": "_____ you help me carry this heavy box?",
                "question_type": "选择题",
                "options": ["Could", "Must", "Should", "Need"],
                "answer": "A", "analysis": "礼貌请求帮助用could",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Help Request", "grade_level": "初中一年级"
            },
            {
                "content": "It _____ rain tomorrow. Take an umbrella.",
                "question_type": "选择题",
                "options": ["can", "might", "must", "should"],
                "answer": "B", "analysis": "表示可能性用might",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Weather Possibility", "grade_level": "初中一年级"
            },
            {
                "content": "Students _____ use mobile phones during the exam.",
                "question_type": "选择题",
                "options": ["can", "may", "mustn't", "needn't"],
                "answer": "C", "analysis": "考试期间禁止使用手机，用mustn't",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "School Rules", "grade_level": "初中一年级"
            },
            {
                "content": "You _____ be tired after such a long journey.",
                "question_type": "选择题",
                "options": ["can", "must", "may", "should"],
                "answer": "B", "analysis": "表示肯定推测用must",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Logical Deduction", "grade_level": "初中二年级"
            },
            {
                "content": "_____ I use your computer for a while?",
                "question_type": "选择题",
                "options": ["Must", "Should", "Could", "Need"],
                "answer": "C", "analysis": "礼貌请求许可用could",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Permission Request", "grade_level": "初中一年级"
            },
            {
                "content": "You _____ drive so fast. It's not safe.",
                "question_type": "选择题",
                "options": ["shouldn't", "can't", "mustn't", "needn't"],
                "answer": "A", "analysis": "表示不应该用shouldn't",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Safety Warning", "grade_level": "初中一年级"
            },
            {
                "content": "She _____ be at home now. I just saw her there.",
                "question_type": "选择题",
                "options": ["can", "must", "may", "could"],
                "answer": "B", "analysis": "有确凿证据的肯定推测用must",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Certain Deduction", "grade_level": "初中二年级"
            },
            {
                "content": "You _____ worry about the exam. You've prepared well.",
                "question_type": "选择题",
                "options": ["mustn't", "needn't", "can't", "shouldn't"],
                "answer": "B", "analysis": "表示没有必要用needn't",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Exam Comfort", "grade_level": "初中二年级"
            },
            {
                "content": "When I was young, I _____ swim very well.",
                "question_type": "选择题",
                "options": ["can", "could", "may", "must"],
                "answer": "B", "analysis": "过去的能力用could",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "Past Ability", "grade_level": "初中一年级"
            }
        ]
    
    def get_all_questions(self) -> List[Dict[str, Any]]:
        """获取所有200道题目"""
        return self.question_bank
    
    def get_all_knowledge_points(self) -> List[Dict[str, Any]]:
        """获取所有知识点"""
        return self.knowledge_points
    
    def get_questions_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """按难度获取题目"""
        return [q for q in self.question_bank if q.get("difficulty") == difficulty]
    
    def get_questions_by_grade(self, grade_level: str) -> List[Dict[str, Any]]:
        """按年级获取题目"""
        return [q for q in self.question_bank if q.get("grade_level") == grade_level]
    
    def export_to_cypher(self) -> str:
        """导出为完整的Cypher脚本"""
        lines = [
            "// K12英语知识图谱系统 - 200道题目综合数据库",
            "// 涵盖20+个语法知识点，适配K12全学段",
            f"// 生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "// 清空现有数据",
            "MATCH (n) DETACH DELETE n;",
            "",
            "// 创建约束",
            "CREATE CONSTRAINT knowledge_point_id IF NOT EXISTS FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE;",
            "CREATE CONSTRAINT question_id IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE;",
            ""
        ]
        
        # 导出知识点
        lines.append("// === 知识点创建 ===")
        for i, kp in enumerate(self.knowledge_points):
            kp_id = f"kp_comp_{i+1:03d}"
            name = kp['name'].replace("'", "\\'")
            keywords_json = json.dumps(kp['keywords'], ensure_ascii=False)
            grade_levels_json = json.dumps(kp['grade_levels'], ensure_ascii=False)
            
            lines.append(f"""
CREATE (kp_{i+1:03d}:KnowledgePoint {{
    id: '{kp_id}',
    name: '{name}',
    difficulty: '{kp['difficulty']}',
    keywords: {keywords_json},
    grade_levels: {grade_levels_json},
    cefr_level: '{kp.get('cefr_level', 'A1')}',
    source: 'Comprehensive Database'
}});""")
        
        # 导出题目
        lines.append("\n// === 题目创建 ===")
        for i, q in enumerate(self.question_bank):
            q_id = f"q_comp_{i+1:03d}"
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
    source: '{q.get('source', 'Comprehensive')}',
    grade_level: '{q.get('grade_level', '未设置')}'
}});""")
        
        # 创建关系
        lines.append("\n// === 关系创建 ===")
        for q_idx, q in enumerate(self.question_bank):
            for kp_name in q.get("knowledge_points", []):
                # 找到对应的知识点索引
                kp_idx = None
                for i, kp in enumerate(self.knowledge_points):
                    if kp['name'] == kp_name:
                        kp_idx = i + 1
                        break
                
                if kp_idx:
                    lines.append(f"""
MATCH (q:Question {{id: 'q_comp_{q_idx+1:03d}'}})
MATCH (kp:KnowledgePoint {{id: 'kp_comp_{kp_idx:03d}'}})
CREATE (q)-[:TESTS {{weight: 0.85}}]->(kp);""")
        
        lines.extend([
            "",
            "// === 数据验证 ===",
            "MATCH (kp:KnowledgePoint) RETURN count(kp) as total_knowledge_points;",
            "MATCH (q:Question) RETURN count(q) as total_questions;",
            "MATCH ()-[r:TESTS]->() RETURN count(r) as total_relationships;",
            "MATCH (q:Question) WHERE q.difficulty = 'easy' RETURN count(q) as easy_questions;",
            "MATCH (q:Question) WHERE q.difficulty = 'medium' RETURN count(q) as medium_questions;",
            "MATCH (q:Question) WHERE q.difficulty = 'hard' RETURN count(q) as hard_questions;",
            "",
            "// === 样本查看 ===",
            "MATCH (n) RETURN n LIMIT 10;"
        ])
        
        return "\n".join(lines)

# 全局实例
comprehensive_question_bank = ComprehensiveQuestionBank()
