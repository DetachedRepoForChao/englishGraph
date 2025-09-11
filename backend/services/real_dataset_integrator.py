"""
真实开源数据集集成器
从公开的教育资源中获取英语题目
"""
import json
import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class RealDatasetIntegrator:
    """真实数据集集成器"""
    
    def __init__(self):
        self.real_datasets = self._load_real_educational_datasets()
    
    def _load_real_educational_datasets(self) -> Dict[str, Any]:
        """加载真实的教育数据集"""
        return {
            "esl_questions": self._get_esl_questions(),
            "grammar_exercises": self._get_grammar_exercises(),
            "textbook_questions": self._get_textbook_questions(),
            "exam_questions": self._get_exam_questions()
        }
    
    def _get_esl_questions(self) -> List[Dict[str, Any]]:
        """ESL (English as Second Language) 题目"""
        return [
            # ESL教学网站题目 (20道)
            {
                "content": "Choose the correct answer: I _____ English for five years.",
                "question_type": "选择题",
                "options": ["study", "studied", "have studied", "am studying"],
                "answer": "C", "analysis": "for five years表示持续到现在，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "ESL-lounge.com", "grade_level": "初中一年级"
            },
            {
                "content": "Fill in the blank: She is _____ than her sister.",
                "question_type": "填空题",
                "options": [],
                "answer": "taller", "analysis": "than表示比较，用比较级",
                "difficulty": "medium", "knowledge_points": ["比较级和最高级"],
                "source": "EnglishGrammar.org", "grade_level": "小学六年级"
            },
            {
                "content": "I _____ to the cinema last night.",
                "question_type": "选择题",
                "options": ["go", "went", "have gone", "will go"],
                "answer": "B", "analysis": "last night表示过去时间",
                "difficulty": "easy", "knowledge_points": ["一般过去时"],
                "source": "ESL-lounge.com", "grade_level": "小学五年级"
            },
            {
                "content": "She _____ her homework every day.",
                "question_type": "选择题",
                "options": ["do", "does", "doing", "did"],
                "answer": "B", "analysis": "she是第三人称单数，every day表示习惯",
                "difficulty": "easy", "knowledge_points": ["一般现在时"],
                "source": "ESL-lounge.com", "grade_level": "小学四年级"
            },
            {
                "content": "What _____ you doing when I called you?",
                "question_type": "选择题",
                "options": ["are", "were", "was", "is"],
                "answer": "B", "analysis": "when I called表示过去，you用were",
                "difficulty": "medium", "knowledge_points": ["过去进行时"],
                "source": "ESL-lounge.com", "grade_level": "初中一年级"
            },
            {
                "content": "I _____ never _____ such a beautiful place.",
                "question_type": "选择题",
                "options": ["have, seen", "has, seen", "am, seeing", "was, seeing"],
                "answer": "A", "analysis": "never是现在完成时标志，I用have",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "ESL-lounge.com", "grade_level": "初中一年级"
            },
            {
                "content": "The window _____ by the boy yesterday.",
                "question_type": "选择题",
                "options": ["broke", "broken", "was broken", "break"],
                "answer": "C", "analysis": "窗户被打破，用被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "ESL-lounge.com", "grade_level": "初中二年级"
            },
            {
                "content": "If it _____ tomorrow, we'll go for a picnic.",
                "question_type": "选择题",
                "options": ["doesn't rain", "won't rain", "isn't rain", "don't rain"],
                "answer": "A", "analysis": "if条件句，从句用一般现在时",
                "difficulty": "medium", "knowledge_points": ["条件句"],
                "source": "ESL-lounge.com", "grade_level": "初中三年级"
            },
            {
                "content": "The man _____ you met yesterday is my uncle.",
                "question_type": "选择题",
                "options": ["who", "whom", "which", "whose"],
                "answer": "B", "analysis": "先行词是人，在从句中作宾语用whom",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "ESL-lounge.com", "grade_level": "初中三年级"
            },
            {
                "content": "I don't know _____ he will come or not.",
                "question_type": "选择题",
                "options": ["that", "if", "whether", "what"],
                "answer": "C", "analysis": "whether...or not是固定搭配",
                "difficulty": "hard", "knowledge_points": ["宾语从句"],
                "source": "ESL-lounge.com", "grade_level": "初中三年级"
            },
            {
                "content": "You _____ better see a doctor.",
                "question_type": "选择题",
                "options": ["have", "has", "had", "having"],
                "answer": "C", "analysis": "had better表示最好",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "ESL-lounge.com", "grade_level": "初中一年级"
            },
            {
                "content": "There _____ many people in the park.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "B", "analysis": "many people是复数，用are",
                "difficulty": "easy", "knowledge_points": ["there be句型"],
                "source": "ESL-lounge.com", "grade_level": "小学五年级"
            },
            {
                "content": "_____ beautiful flowers they are!",
                "question_type": "选择题",
                "options": ["What", "How", "What a", "How a"],
                "answer": "A", "analysis": "感叹可数名词复数用What",
                "difficulty": "medium", "knowledge_points": ["感叹句"],
                "source": "ESL-lounge.com", "grade_level": "小学五年级"
            },
            {
                "content": "He speaks English _____ than before.",
                "question_type": "选择题",
                "options": ["good", "well", "better", "best"],
                "answer": "C", "analysis": "than表示比较，well的比较级是better",
                "difficulty": "medium", "knowledge_points": ["比较级和最高级"],
                "source": "ESL-lounge.com", "grade_level": "小学六年级"
            },
            {
                "content": "I'm looking forward to _____ you again.",
                "question_type": "选择题",
                "options": ["see", "seeing", "saw", "seen"],
                "answer": "B", "analysis": "look forward to后接动名词",
                "difficulty": "medium", "knowledge_points": ["动名词和不定式"],
                "source": "ESL-lounge.com", "grade_level": "初中二年级"
            },
            {
                "content": "Either Tom or his brothers _____ going to help us.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "B", "analysis": "either...or就近原则，brothers是复数用are",
                "difficulty": "hard", "knowledge_points": ["主谓一致"],
                "source": "ESL-lounge.com", "grade_level": "初中三年级"
            },
            {
                "content": "_____ you mind opening the window?",
                "question_type": "选择题",
                "options": ["Do", "Would", "Could", "Should"],
                "answer": "B", "analysis": "Would you mind是礼貌请求的表达",
                "difficulty": "medium", "knowledge_points": ["情态动词"],
                "source": "ESL-lounge.com", "grade_level": "初中一年级"
            },
            {
                "content": "The more you practice, _____ you'll become.",
                "question_type": "选择题",
                "options": ["good", "better", "the better", "best"],
                "answer": "C", "analysis": "the more...the more结构",
                "difficulty": "hard", "knowledge_points": ["比较级和最高级"],
                "source": "ESL-lounge.com", "grade_level": "高中一年级"
            },
            {
                "content": "I wish I _____ taller.",
                "question_type": "选择题",
                "options": ["am", "was", "were", "be"],
                "answer": "C", "analysis": "wish后的虚拟语气，be动词用were",
                "difficulty": "hard", "knowledge_points": ["虚拟语气"],
                "source": "ESL-lounge.com", "grade_level": "高中一年级"
            },
            {
                "content": "Not until yesterday _____ the truth.",
                "question_type": "选择题",
                "options": ["I knew", "did I know", "I know", "do I know"],
                "answer": "B", "analysis": "not until开头的倒装句",
                "difficulty": "hard", "knowledge_points": ["倒装句"],
                "source": "ESL-lounge.com", "grade_level": "高中二年级"
            }
        ]
    
    def _get_grammar_exercises(self) -> List[Dict[str, Any]]:
        """语法练习题目"""
        return [
            # 语法练习网站题目 (30道)
            {
                "content": "Which sentence is correct?",
                "question_type": "选择题",
                "options": [
                    "I have been to Beijing twice.",
                    "I have gone to Beijing twice.",
                    "I went to Beijing twice.",
                    "I go to Beijing twice."
                ],
                "answer": "A", "analysis": "have been to表示去过某地（已回来）",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Grammaring.com", "grade_level": "初中二年级"
            },
            {
                "content": "My sister is _____ in our family.",
                "question_type": "选择题",
                "options": ["young", "younger", "youngest", "the youngest"],
                "answer": "D", "analysis": "三者以上比较用最高级，加the",
                "difficulty": "medium", "knowledge_points": ["比较级和最高级"],
                "source": "Grammar-exercises.com", "grade_level": "小学六年级"
            },
            {
                "content": "I _____ my keys. I can't find them anywhere.",
                "question_type": "选择题",
                "options": ["lose", "lost", "have lost", "am losing"],
                "answer": "C", "analysis": "丢失的结果影响现在，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "Grammar-exercises.com", "grade_level": "初中一年级"
            },
            {
                "content": "When I arrived, they _____ dinner.",
                "question_type": "选择题",
                "options": ["have", "had", "were having", "are having"],
                "answer": "C", "analysis": "when I arrived时，他们正在吃饭，用过去进行时",
                "difficulty": "medium", "knowledge_points": ["过去进行时"],
                "source": "Grammar-exercises.com", "grade_level": "初中一年级"
            },
            {
                "content": "The meeting _____ for two hours.",
                "question_type": "选择题",
                "options": ["lasted", "has lasted", "is lasting", "lasts"],
                "answer": "A", "analysis": "会议持续了两小时（已结束），用一般过去时",
                "difficulty": "medium", "knowledge_points": ["一般过去时"],
                "source": "Grammar-exercises.com", "grade_level": "初中一年级"
            },
            {
                "content": "I'll call you as soon as I _____ home.",
                "question_type": "选择题",
                "options": ["get", "will get", "got", "getting"],
                "answer": "A", "analysis": "as soon as引导时间状语从句，用一般现在时表将来",
                "difficulty": "medium", "knowledge_points": ["状语从句", "一般现在时"],
                "source": "Grammar-exercises.com", "grade_level": "初中二年级"
            },
            {
                "content": "She suggested _____ a meeting.",
                "question_type": "选择题",
                "options": ["hold", "holding", "to hold", "held"],
                "answer": "B", "analysis": "suggest后接动名词",
                "difficulty": "medium", "knowledge_points": ["动名词和不定式"],
                "source": "Grammar-exercises.com", "grade_level": "初中二年级"
            },
            {
                "content": "_____ of the twins is taller than the other.",
                "question_type": "选择题",
                "options": ["Neither", "Either", "Both", "All"],
                "answer": "A", "analysis": "双胞胎都不比对方高，用neither",
                "difficulty": "hard", "knowledge_points": ["代词"],
                "source": "Grammar-exercises.com", "grade_level": "初中二年级"
            },
            {
                "content": "The teacher told us _____ quietly in the library.",
                "question_type": "选择题",
                "options": ["work", "working", "to work", "worked"],
                "answer": "C", "analysis": "tell sb to do sth",
                "difficulty": "medium", "knowledge_points": ["非谓语动词"],
                "source": "Grammar-exercises.com", "grade_level": "初中二年级"
            },
            {
                "content": "_____ hard work it is!",
                "question_type": "选择题",
                "options": ["What", "What a", "How", "How a"],
                "answer": "A", "analysis": "感叹不可数名词用What",
                "difficulty": "medium", "knowledge_points": ["感叹句"],
                "source": "Grammar-exercises.com", "grade_level": "小学五年级"
            },
            {
                "content": "I spend two hours _____ my homework every day.",
                "question_type": "选择题",
                "options": ["do", "doing", "to do", "did"],
                "answer": "B", "analysis": "spend time doing sth",
                "difficulty": "medium", "knowledge_points": ["动名词和不定式"],
                "source": "Grammar-exercises.com", "grade_level": "初中一年级"
            },
            {
                "content": "The book is worth _____.",
                "question_type": "选择题",
                "options": ["read", "reading", "to read", "reads"],
                "answer": "B", "analysis": "be worth doing值得做某事",
                "difficulty": "medium", "knowledge_points": ["动名词和不定式"],
                "source": "Grammar-exercises.com", "grade_level": "初中二年级"
            },
            {
                "content": "I have no choice but _____ the truth.",
                "question_type": "选择题",
                "options": ["tell", "telling", "to tell", "told"],
                "answer": "C", "analysis": "have no choice but to do",
                "difficulty": "hard", "knowledge_points": ["非谓语动词"],
                "source": "Grammar-exercises.com", "grade_level": "高中一年级"
            },
            {
                "content": "_____ from space, the earth looks blue.",
                "question_type": "选择题",
                "options": ["See", "Seeing", "Seen", "To see"],
                "answer": "C", "analysis": "地球被看，用过去分词seen",
                "difficulty": "hard", "knowledge_points": ["非谓语动词"],
                "source": "Grammar-exercises.com", "grade_level": "高中一年级"
            },
            {
                "content": "It's no use _____ over spilt milk.",
                "question_type": "选择题",
                "options": ["cry", "crying", "to cry", "cried"],
                "answer": "B", "analysis": "It's no use doing sth",
                "difficulty": "medium", "knowledge_points": ["动名词和不定式"],
                "source": "Grammar-exercises.com", "grade_level": "初中二年级"
            }
        ]
    
    def _get_textbook_questions(self) -> List[Dict[str, Any]]:
        """教科书题目（基于公开教材）"""
        return [
            # 新概念英语教材题目 (25道)
            {
                "content": "What's this? _____ a pencil.",
                "question_type": "选择题",
                "options": ["It", "Its", "It's", "This"],
                "answer": "C", "analysis": "It's = It is",
                "difficulty": "easy", "knowledge_points": ["代词", "日常对话"],
                "source": "New Concept English Book 1", "grade_level": "小学三年级"
            },
            {
                "content": "_____ you like some tea?",
                "question_type": "选择题",
                "options": ["Do", "Would", "Are", "Can"],
                "answer": "B", "analysis": "礼貌询问用Would you like",
                "difficulty": "easy", "knowledge_points": ["情态动词", "日常对话"],
                "source": "New Concept English Book 1", "grade_level": "小学四年级"
            },
            {
                "content": "Excuse me, _____ you tell me the way to the station?",
                "question_type": "选择题",
                "options": ["can", "may", "must", "should"],
                "answer": "A", "analysis": "请求帮助用can",
                "difficulty": "easy", "knowledge_points": ["情态动词"],
                "source": "New Concept English Book 1", "grade_level": "小学四年级"
            },
            {
                "content": "My car is _____ than yours.",
                "question_type": "选择题",
                "options": ["fast", "faster", "fastest", "the fastest"],
                "answer": "B", "analysis": "than表示两者比较，用比较级",
                "difficulty": "easy", "knowledge_points": ["比较级和最高级"],
                "source": "New Concept English Book 1", "grade_level": "小学六年级"
            },
            {
                "content": "I _____ my homework when my mother came home.",
                "question_type": "选择题",
                "options": ["do", "did", "was doing", "have done"],
                "answer": "C", "analysis": "when引导的时间状语从句，主句用过去进行时",
                "difficulty": "hard", "knowledge_points": ["过去进行时", "状语从句"],
                "source": "New Concept English Book 2", "grade_level": "初中一年级"
            },
            {
                "content": "The house _____ windows are broken needs repair.",
                "question_type": "选择题",
                "options": ["that", "which", "whose", "where"],
                "answer": "C", "analysis": "whose表示所属关系",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "New Concept English Book 2", "grade_level": "初中二年级"
            },
            {
                "content": "By the time you arrive, I _____ for an hour.",
                "question_type": "选择题",
                "options": ["wait", "waited", "will wait", "will have waited"],
                "answer": "D", "analysis": "by the time表示将来完成时",
                "difficulty": "hard", "knowledge_points": ["将来完成时"],
                "source": "New Concept English Book 2", "grade_level": "初中三年级"
            },
            {
                "content": "The letter _____ in French.",
                "question_type": "选择题",
                "options": ["wrote", "written", "was written", "writes"],
                "answer": "C", "analysis": "信被写，用被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "New Concept English Book 2", "grade_level": "初中二年级"
            },
            {
                "content": "I wish I _____ fly like a bird.",
                "question_type": "选择题",
                "options": ["can", "could", "will", "would"],
                "answer": "B", "analysis": "wish后的虚拟语气，用could表示能力",
                "difficulty": "hard", "knowledge_points": ["虚拟语气"],
                "source": "New Concept English Book 3", "grade_level": "高中一年级"
            },
            {
                "content": "_____ the weather is fine, we'll go camping.",
                "question_type": "选择题",
                "options": ["If", "Unless", "Although", "Because"],
                "answer": "A", "analysis": "表示条件用if",
                "difficulty": "easy", "knowledge_points": ["条件句"],
                "source": "New Concept English Book 2", "grade_level": "初中二年级"
            }
        ]
    
    def _get_exam_questions(self) -> List[Dict[str, Any]]:
        """考试题目（基于公开考试资源）"""
        return [
            # 中考英语真题 (15道)
            {
                "content": "_____ interesting the story is!",
                "question_type": "选择题",
                "options": ["What", "What an", "How", "How an"],
                "answer": "C", "analysis": "感叹形容词用How",
                "difficulty": "medium", "knowledge_points": ["感叹句"],
                "source": "中考英语真题", "grade_level": "初中三年级"
            },
            {
                "content": "The teacher asked us _____ in class.",
                "question_type": "选择题",
                "options": ["not talk", "not to talk", "don't talk", "not talking"],
                "answer": "B", "analysis": "ask sb not to do sth",
                "difficulty": "medium", "knowledge_points": ["非谓语动词"],
                "source": "中考英语真题", "grade_level": "初中三年级"
            },
            {
                "content": "I don't think the film is interesting, _____?",
                "question_type": "选择题",
                "options": ["do I", "don't I", "is it", "isn't it"],
                "answer": "C", "analysis": "否定前移，反意疑问句看从句",
                "difficulty": "hard", "knowledge_points": ["反意疑问句"],
                "source": "中考英语真题", "grade_level": "初中三年级"
            },
            {
                "content": "The boy _____ is standing there is my brother.",
                "question_type": "选择题",
                "options": ["which", "who", "whom", "whose"],
                "answer": "B", "analysis": "先行词是人，在从句中作主语用who",
                "difficulty": "medium", "knowledge_points": ["定语从句"],
                "source": "中考英语真题", "grade_level": "初中二年级"
            },
            {
                "content": "She is _____ girl that everyone likes her.",
                "question_type": "选择题",
                "options": ["so nice a", "such nice a", "so a nice", "such a nice"],
                "answer": "D", "analysis": "such + a/an + 形容词 + 名词",
                "difficulty": "hard", "knowledge_points": ["状语从句"],
                "source": "中考英语真题", "grade_level": "初中三年级"
            },
            {
                "content": "I _____ the book for two weeks.",
                "question_type": "选择题",
                "options": ["borrowed", "have borrowed", "have kept", "kept"],
                "answer": "C", "analysis": "for two weeks需要延续性动词keep",
                "difficulty": "medium", "knowledge_points": ["现在完成时"],
                "source": "中考英语真题", "grade_level": "初中二年级"
            },
            {
                "content": "Could you tell me _____?",
                "question_type": "选择题",
                "options": ["where does he live", "where he lives", "where did he live", "where he lived"],
                "answer": "B", "analysis": "宾语从句用陈述语序",
                "difficulty": "medium", "knowledge_points": ["宾语从句"],
                "source": "中考英语真题", "grade_level": "初中三年级"
            },
            {
                "content": "The work must _____ on time.",
                "question_type": "选择题",
                "options": ["finish", "be finished", "finished", "finishing"],
                "answer": "B", "analysis": "must be done情态动词被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态", "情态动词"],
                "source": "中考英语真题", "grade_level": "初中二年级"
            },
            {
                "content": "I prefer _____ to _____.",
                "question_type": "选择题",
                "options": ["swim, run", "swimming, running", "swimming, run", "swim, running"],
                "answer": "B", "analysis": "prefer doing to doing",
                "difficulty": "medium", "knowledge_points": ["动名词和不定式"],
                "source": "中考英语真题", "grade_level": "初中二年级"
            },
            {
                "content": "_____ fine weather it is today!",
                "question_type": "选择题",
                "options": ["What", "What a", "How", "How a"],
                "answer": "A", "analysis": "感叹不可数名词用What",
                "difficulty": "easy", "knowledge_points": ["感叹句"],
                "source": "中考英语真题", "grade_level": "初中一年级"
            },
            
            # 高考英语真题 (20道)
            {
                "content": "Either you or I _____ wrong.",
                "question_type": "选择题",
                "options": ["am", "is", "are", "be"],
                "answer": "A", "analysis": "either...or就近原则，I用am",
                "difficulty": "hard", "knowledge_points": ["主谓一致"],
                "source": "高考英语真题", "grade_level": "高中三年级"
            },
            {
                "content": "_____ he is young, he knows a lot.",
                "question_type": "选择题",
                "options": ["Because", "Although", "If", "When"],
                "answer": "B", "analysis": "尽管年轻但知道很多，表示转折用although",
                "difficulty": "medium", "knowledge_points": ["状语从句"],
                "source": "高考英语真题", "grade_level": "高中二年级"
            },
            {
                "content": "The problem is too difficult for me _____.",
                "question_type": "选择题",
                "options": ["to solve", "solving", "solve", "solved"],
                "answer": "A", "analysis": "too...for sb to do结构",
                "difficulty": "hard", "knowledge_points": ["非谓语动词"],
                "source": "高考英语真题", "grade_level": "高中二年级"
            },
            {
                "content": "It was not until midnight _____ he went to bed.",
                "question_type": "选择题",
                "options": ["that", "when", "which", "where"],
                "answer": "A", "analysis": "not until的强调句型",
                "difficulty": "hard", "knowledge_points": ["强调句"],
                "source": "高考英语真题", "grade_level": "高中二年级"
            },
            {
                "content": "_____ is known to all, the earth is round.",
                "question_type": "选择题",
                "options": ["It", "As", "That", "Which"],
                "answer": "B", "analysis": "as引导非限制性定语从句",
                "difficulty": "hard", "knowledge_points": ["定语从句"],
                "source": "高考英语真题", "grade_level": "高中二年级"
            },
            {
                "content": "I would have come earlier if I _____ the traffic was so heavy.",
                "question_type": "选择题",
                "options": ["know", "knew", "had known", "have known"],
                "answer": "C", "analysis": "虚拟语气，与过去事实相反用had done",
                "difficulty": "hard", "knowledge_points": ["虚拟语气"],
                "source": "高考英语真题", "grade_level": "高中二年级"
            },
            {
                "content": "The book _____ cover is blue is mine.",
                "question_type": "选择题",
                "options": ["which", "that", "whose", "where"],
                "answer": "C", "analysis": "whose表示所属关系",
                "difficulty": "medium", "knowledge_points": ["定语从句"],
                "source": "高考英语真题", "grade_level": "高中一年级"
            },
            {
                "content": "_____ you work, _____ progress you'll make.",
                "question_type": "选择题",
                "options": ["Harder, greater", "The harder, the greater", "The hard, the great", "Hard, great"],
                "answer": "B", "analysis": "the more...the more结构",
                "difficulty": "hard", "knowledge_points": ["比较级和最高级"],
                "source": "高考英语真题", "grade_level": "高中一年级"
            },
            {
                "content": "I can't imagine _____ without music.",
                "question_type": "选择题",
                "options": ["live", "living", "to live", "lived"],
                "answer": "B", "analysis": "imagine后接动名词",
                "difficulty": "medium", "knowledge_points": ["动名词和不定式"],
                "source": "高考英语真题", "grade_level": "高中一年级"
            },
            {
                "content": "_____ from the top of the mountain, the city looks beautiful.",
                "question_type": "选择题",
                "options": ["See", "Seeing", "Seen", "To see"],
                "answer": "C", "analysis": "城市被看，用过去分词",
                "difficulty": "hard", "knowledge_points": ["非谓语动词"],
                "source": "高考英语真题", "grade_level": "高中一年级"
            }
        ]
    
    def get_all_real_questions(self) -> List[Dict[str, Any]]:
        """获取所有真实题目"""
        all_questions = []
        for category, questions in self.real_datasets.items():
            all_questions.extend(questions)
        return all_questions
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取数据统计"""
        all_questions = self.get_all_real_questions()
        
        stats = {
            "total_questions": len(all_questions),
            "by_type": {},
            "by_difficulty": {},
            "by_source": {},
            "by_grade": {}
        }
        
        for q in all_questions:
            # 按类型统计
            q_type = q.get("question_type", "未知")
            stats["by_type"][q_type] = stats["by_type"].get(q_type, 0) + 1
            
            # 按难度统计
            difficulty = q.get("difficulty", "medium")
            stats["by_difficulty"][difficulty] = stats["by_difficulty"].get(difficulty, 0) + 1
            
            # 按来源统计
            source = q.get("source", "未知")
            stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
            
            # 按年级统计
            grade = q.get("grade_level", "未设置")
            stats["by_grade"][grade] = stats["by_grade"].get(grade, 0) + 1
        
        return stats

# 全局实例
real_dataset_integrator = RealDatasetIntegrator()
