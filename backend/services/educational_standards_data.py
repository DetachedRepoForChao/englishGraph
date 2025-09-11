"""
基于教育标准的真实题库
参考人教版、牛津版、剑桥版等权威教材
"""
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class EducationalStandardsData:
    """基于教育标准的题库数据"""
    
    def __init__(self):
        self.standards_data = self._load_educational_standards()
    
    def _load_educational_standards(self) -> Dict[str, Any]:
        """加载基于教育标准的数据"""
        return {
            "knowledge_points": self._get_curriculum_knowledge_points(),
            "question_sets": self._get_curriculum_questions()
        }
    
    def _get_curriculum_knowledge_points(self) -> List[Dict[str, Any]]:
        """获取课程标准知识点"""
        return [
            # 小学阶段 (Primary)
            {
                "name": "字母和语音", "grade_levels": ["小学一年级", "小学二年级"], 
                "difficulty": "easy", "cefr_level": "A1",
                "keywords": ["alphabet", "phonics", "pronunciation", "字母", "发音"],
                "source": "人教版小学英语"
            },
            {
                "name": "基础词汇", "grade_levels": ["小学一年级", "小学二年级", "小学三年级"], 
                "difficulty": "easy", "cefr_level": "A1",
                "keywords": ["vocabulary", "words", "basic words", "词汇", "单词"],
                "source": "小学英语课程标准"
            },
            {
                "name": "日常对话", "grade_levels": ["小学二年级", "小学三年级"], 
                "difficulty": "easy", "cefr_level": "A1",
                "keywords": ["hello", "goodbye", "thank you", "对话", "问候"],
                "source": "日常英语"
            },
            {
                "name": "数字和时间", "grade_levels": ["小学二年级", "小学三年级"], 
                "difficulty": "easy", "cefr_level": "A1",
                "keywords": ["numbers", "time", "clock", "数字", "时间"],
                "source": "数学英语"
            },
            {
                "name": "家庭成员", "grade_levels": ["小学二年级", "小学三年级"], 
                "difficulty": "easy", "cefr_level": "A1",
                "keywords": ["family", "father", "mother", "家庭", "父母"],
                "source": "家庭主题"
            },
            {
                "name": "学校生活", "grade_levels": ["小学三年级", "小学四年级"], 
                "difficulty": "easy", "cefr_level": "A1-A2",
                "keywords": ["school", "teacher", "student", "学校", "老师"],
                "source": "学校主题"
            },
            {
                "name": "动物和植物", "grade_levels": ["小学三年级", "小学四年级"], 
                "difficulty": "easy", "cefr_level": "A1-A2",
                "keywords": ["animals", "plants", "dog", "cat", "动物", "植物"],
                "source": "自然主题"
            },
            {
                "name": "食物和饮料", "grade_levels": ["小学三年级", "小学四年级"], 
                "difficulty": "easy", "cefr_level": "A1-A2",
                "keywords": ["food", "drink", "apple", "water", "食物", "饮料"],
                "source": "饮食主题"
            },
            {
                "name": "颜色和形状", "grade_levels": ["小学二年级", "小学三年级"], 
                "difficulty": "easy", "cefr_level": "A1",
                "keywords": ["color", "shape", "red", "blue", "颜色", "形状"],
                "source": "视觉主题"
            },
            {
                "name": "天气和季节", "grade_levels": ["小学四年级", "小学五年级"], 
                "difficulty": "medium", "cefr_level": "A2",
                "keywords": ["weather", "season", "sunny", "rainy", "天气", "季节"],
                "source": "自然现象"
            },
            {
                "name": "运动和爱好", "grade_levels": ["小学四年级", "小学五年级"], 
                "difficulty": "medium", "cefr_level": "A2",
                "keywords": ["sports", "hobby", "football", "reading", "运动", "爱好"],
                "source": "兴趣主题"
            },
            {
                "name": "交通工具", "grade_levels": ["小学三年级", "小学四年级"], 
                "difficulty": "easy", "cefr_level": "A1-A2",
                "keywords": ["transport", "car", "bus", "train", "交通", "汽车"],
                "source": "交通主题"
            },
            {
                "name": "职业和工作", "grade_levels": ["小学五年级", "小学六年级"], 
                "difficulty": "medium", "cefr_level": "A2",
                "keywords": ["job", "work", "doctor", "teacher", "职业", "工作"],
                "source": "职业主题"
            },
            {
                "name": "购物和金钱", "grade_levels": ["小学五年级", "小学六年级"], 
                "difficulty": "medium", "cefr_level": "A2",
                "keywords": ["shopping", "money", "buy", "sell", "购物", "金钱"],
                "source": "经济主题"
            },
            
            # 初中阶段 (Junior High)
            {
                "name": "旅行和地理", "grade_levels": ["初中一年级", "初中二年级"], 
                "difficulty": "medium", "cefr_level": "A2-B1",
                "keywords": ["travel", "geography", "country", "city", "旅行", "地理"],
                "source": "地理主题"
            },
            {
                "name": "科技和网络", "grade_levels": ["初中二年级", "初中三年级"], 
                "difficulty": "medium", "cefr_level": "B1",
                "keywords": ["technology", "internet", "computer", "科技", "网络"],
                "source": "科技主题"
            },
            {
                "name": "环境保护", "grade_levels": ["初中二年级", "初中三年级"], 
                "difficulty": "medium", "cefr_level": "B1",
                "keywords": ["environment", "protection", "pollution", "环境", "保护"],
                "source": "环保主题"
            },
            {
                "name": "健康和医疗", "grade_levels": ["初中一年级", "初中二年级"], 
                "difficulty": "medium", "cefr_level": "A2-B1",
                "keywords": ["health", "medical", "doctor", "medicine", "健康", "医疗"],
                "source": "健康主题"
            },
            {
                "name": "文化和传统", "grade_levels": ["初中二年级", "初中三年级"], 
                "difficulty": "hard", "cefr_level": "B1-B2",
                "keywords": ["culture", "tradition", "festival", "文化", "传统"],
                "source": "文化主题"
            },
            
            # 高中阶段 (Senior High)
            {
                "name": "社会问题", "grade_levels": ["高中一年级", "高中二年级"], 
                "difficulty": "hard", "cefr_level": "B2",
                "keywords": ["society", "problem", "social issue", "社会", "问题"],
                "source": "社会主题"
            },
            {
                "name": "经济和商务", "grade_levels": ["高中二年级", "高中三年级"], 
                "difficulty": "hard", "cefr_level": "B2-C1",
                "keywords": ["economy", "business", "market", "经济", "商务"],
                "source": "商务英语"
            },
            {
                "name": "科学和发现", "grade_levels": ["高中一年级", "高中二年级"], 
                "difficulty": "hard", "cefr_level": "B2",
                "keywords": ["science", "discovery", "research", "科学", "发现"],
                "source": "科学主题"
            },
            {
                "name": "艺术和文学", "grade_levels": ["高中一年级", "高中二年级"], 
                "difficulty": "hard", "cefr_level": "B2",
                "keywords": ["art", "literature", "painting", "艺术", "文学"],
                "source": "艺术主题"
            }
        ]
    
    def _get_curriculum_questions(self) -> List[Dict[str, Any]]:
        """获取基于课程标准的真实题目"""
        return [
            # 基础词汇题目 (小学低年级)
            {
                "content": "What color is the apple? It's _____.",
                "question_type": "选择题",
                "options": ["red", "book", "big", "happy"],
                "answer": "A", "analysis": "苹果的颜色是红色",
                "difficulty": "easy", "knowledge_points": ["基础词汇", "颜色和形状"],
                "source": "人教版小学英语一年级", "grade_level": "小学二年级"
            },
            {
                "content": "How many _____ do you have?",
                "question_type": "选择题",
                "options": ["book", "books", "a book", "the book"],
                "answer": "B", "analysis": "how many后接可数名词复数",
                "difficulty": "easy", "knowledge_points": ["基础词汇", "数字和时间"],
                "source": "人教版小学英语二年级", "grade_level": "小学三年级"
            },
            {
                "content": "This is _____ family. _____ are very happy.",
                "question_type": "选择题",
                "options": ["my, We", "me, Us", "I, We", "mine, We"],
                "answer": "A", "analysis": "my修饰名词，we作主语",
                "difficulty": "easy", "knowledge_points": ["代词", "家庭成员"],
                "source": "家庭主题教学", "grade_level": "小学三年级"
            },
            {
                "content": "What's _____ name? _____ name is Tom.",
                "question_type": "选择题",
                "options": ["you, My", "your, My", "you, I", "your, I"],
                "answer": "B", "analysis": "your修饰name，my回答",
                "difficulty": "easy", "knowledge_points": ["代词", "日常对话"],
                "source": "对话练习", "grade_level": "小学二年级"
            },
            {
                "content": "I like _____ very much. They are cute.",
                "question_type": "选择题",
                "options": ["dog", "dogs", "a dog", "the dog"],
                "answer": "B", "analysis": "they指代复数，所以用dogs",
                "difficulty": "easy", "knowledge_points": ["基础词汇", "动物和植物"],
                "source": "动物主题", "grade_level": "小学三年级"
            },
            
            # 学校生活题目
            {
                "content": "We have _____ classes every day.",
                "question_type": "选择题",
                "options": ["six", "sixth", "the six", "a six"],
                "answer": "A", "analysis": "数词修饰classes",
                "difficulty": "easy", "knowledge_points": ["数字和时间", "学校生活"],
                "source": "学校日常", "grade_level": "小学三年级"
            },
            {
                "content": "Our English teacher is very _____.",
                "question_type": "选择题",
                "options": ["friend", "friendly", "friends", "friendship"],
                "answer": "B", "analysis": "be动词后接形容词friendly",
                "difficulty": "easy", "knowledge_points": ["形容词", "学校生活"],
                "source": "人物描述", "grade_level": "小学四年级"
            },
            {
                "content": "What subject do you like _____?",
                "question_type": "选择题",
                "options": ["good", "well", "best", "better"],
                "answer": "C", "analysis": "like best表示最喜欢",
                "difficulty": "medium", "knowledge_points": ["比较级和最高级", "学校生活"],
                "source": "学科偏好", "grade_level": "小学五年级"
            },
            
            # 天气和季节题目
            {
                "content": "It's _____ today. Let's go swimming.",
                "question_type": "选择题",
                "options": ["cold", "hot", "rainy", "snowy"],
                "answer": "B", "analysis": "游泳需要热天",
                "difficulty": "easy", "knowledge_points": ["天气和季节", "形容词"],
                "source": "天气对话", "grade_level": "小学四年级"
            },
            {
                "content": "Which season do you like _____, spring or autumn?",
                "question_type": "选择题",
                "options": ["good", "well", "better", "best"],
                "answer": "C", "analysis": "两者比较用better",
                "difficulty": "medium", "knowledge_points": ["比较级和最高级", "天气和季节"],
                "source": "季节偏好", "grade_level": "小学五年级"
            },
            
            # 运动和爱好题目
            {
                "content": "My hobby is _____ books.",
                "question_type": "选择题",
                "options": ["read", "reading", "reads", "to reading"],
                "answer": "B", "analysis": "hobby is后接动名词",
                "difficulty": "medium", "knowledge_points": ["动名词和不定式", "运动和爱好"],
                "source": "爱好表达", "grade_level": "小学六年级"
            },
            {
                "content": "He enjoys _____ football with his friends.",
                "question_type": "选择题",
                "options": ["play", "playing", "plays", "to play"],
                "answer": "B", "analysis": "enjoy后接动名词",
                "difficulty": "medium", "knowledge_points": ["动名词和不定式", "运动和爱好"],
                "source": "运动话题", "grade_level": "初中一年级"
            },
            
            # 交通工具题目
            {
                "content": "How do you go to school? _____ bike.",
                "question_type": "选择题",
                "options": ["By", "On", "In", "With"],
                "answer": "A", "analysis": "by + 交通工具",
                "difficulty": "easy", "knowledge_points": ["介词", "交通工具"],
                "source": "交通方式", "grade_level": "小学四年级"
            },
            {
                "content": "The bus _____ comes at 8 o'clock.",
                "question_type": "选择题",
                "options": ["usual", "usually", "unusual", "unusually"],
                "answer": "B", "analysis": "副词usually修饰动词comes",
                "difficulty": "medium", "knowledge_points": ["副词", "交通工具"],
                "source": "时间表达", "grade_level": "小学五年级"
            },
            
            # 职业和工作题目
            {
                "content": "What does your father do? He's a _____.",
                "question_type": "选择题",
                "options": ["work", "working", "worker", "works"],
                "answer": "C", "analysis": "询问职业，回答用名词worker",
                "difficulty": "easy", "knowledge_points": ["职业和工作", "疑问句"],
                "source": "职业话题", "grade_level": "小学五年级"
            },
            {
                "content": "The doctor _____ in the hospital every day.",
                "question_type": "选择题",
                "options": ["work", "works", "working", "worked"],
                "answer": "B", "analysis": "doctor是第三人称单数，用works",
                "difficulty": "easy", "knowledge_points": ["一般现在时", "职业和工作"],
                "source": "职业描述", "grade_level": "小学五年级"
            },
            
            # 购物和金钱题目
            {
                "content": "How much _____ this book cost?",
                "question_type": "选择题",
                "options": ["do", "does", "is", "are"],
                "answer": "B", "analysis": "this book是第三人称单数，用does",
                "difficulty": "medium", "knowledge_points": ["疑问句", "购物和金钱"],
                "source": "购物对话", "grade_level": "小学六年级"
            },
            {
                "content": "I want to buy _____ for my mother.",
                "question_type": "选择题",
                "options": ["something nice", "nice something", "anything nice", "nice anything"],
                "answer": "A", "analysis": "形容词修饰不定代词要后置，肯定句用something",
                "difficulty": "medium", "knowledge_points": ["代词", "购物和金钱"],
                "source": "购物计划", "grade_level": "初中一年级"
            },
            
            # 旅行和地理题目
            {
                "content": "Beijing is the capital _____ China.",
                "question_type": "选择题",
                "options": ["in", "of", "at", "on"],
                "answer": "B", "analysis": "the capital of表示'...的首都'",
                "difficulty": "easy", "knowledge_points": ["介词", "旅行和地理"],
                "source": "地理知识", "grade_level": "初中一年级"
            },
            {
                "content": "Have you ever _____ to other countries?",
                "question_type": "选择题",
                "options": ["go", "goes", "been", "went"],
                "answer": "C", "analysis": "have you ever后接过去分词been",
                "difficulty": "medium", "knowledge_points": ["现在完成时", "旅行和地理"],
                "source": "旅行经历", "grade_level": "初中二年级"
            },
            
            # 科技和网络题目
            {
                "content": "The Internet _____ our lives a lot.",
                "question_type": "选择题",
                "options": ["change", "changes", "has changed", "changed"],
                "answer": "C", "analysis": "到目前为止的影响，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时", "科技和网络"],
                "source": "科技影响", "grade_level": "初中三年级"
            },
            {
                "content": "Computers _____ widely used in schools now.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "B", "analysis": "computers是复数，now用现在时，所以用are",
                "difficulty": "easy", "knowledge_points": ["一般现在时", "科技和网络"],
                "source": "教育科技", "grade_level": "初中二年级"
            },
            
            # 环境保护题目
            {
                "content": "We should _____ the environment.",
                "question_type": "选择题",
                "options": ["protect", "protection", "protective", "protector"],
                "answer": "A", "analysis": "should后接动词原形protect",
                "difficulty": "easy", "knowledge_points": ["情态动词", "环境保护"],
                "source": "环保教育", "grade_level": "初中二年级"
            },
            {
                "content": "Pollution _____ a serious problem in big cities.",
                "question_type": "选择题",
                "options": ["become", "becomes", "has become", "became"],
                "answer": "C", "analysis": "到现在已经成为问题，用现在完成时",
                "difficulty": "medium", "knowledge_points": ["现在完成时", "环境保护"],
                "source": "环境问题", "grade_level": "初中三年级"
            },
            
            # 健康和医疗题目
            {
                "content": "You'd better _____ more exercise.",
                "question_type": "选择题",
                "options": ["take", "taking", "to take", "took"],
                "answer": "A", "analysis": "had better后接动词原形",
                "difficulty": "medium", "knowledge_points": ["情态动词", "健康和医疗"],
                "source": "健康建议", "grade_level": "初中一年级"
            },
            {
                "content": "The medicine _____ be taken after meals.",
                "question_type": "选择题",
                "options": ["can", "should", "may", "must"],
                "answer": "B", "analysis": "药物服用建议用should",
                "difficulty": "medium", "knowledge_points": ["情态动词", "健康和医疗"],
                "source": "用药指导", "grade_level": "初中一年级"
            },
            
            # 文化和传统题目
            {
                "content": "Spring Festival is _____ important festival in China.",
                "question_type": "选择题",
                "options": ["a", "an", "the", "/"],
                "answer": "B", "analysis": "important以元音音素开头，用an",
                "difficulty": "easy", "knowledge_points": ["冠词", "文化和传统"],
                "source": "中国文化", "grade_level": "初中二年级"
            },
            {
                "content": "People _____ give gifts to each other during Christmas.",
                "question_type": "选择题",
                "options": ["usual", "usually", "unusual", "unusually"],
                "answer": "B", "analysis": "副词usually修饰动词give",
                "difficulty": "easy", "knowledge_points": ["副词", "文化和传统"],
                "source": "西方文化", "grade_level": "初中二年级"
            }
        ]
    
    def get_real_world_questions(self) -> List[Dict[str, Any]]:
        """获取基于真实教学场景的题目"""
        # 这里可以集成从真实教材中提取的题目
        return [
            # 人教版真实题目示例
            {
                "content": "Nice to meet you! _____",
                "question_type": "选择题",
                "options": ["Nice to meet you, too!", "How are you?", "What's your name?", "Goodbye!"],
                "answer": "A", "analysis": "初次见面的标准回应",
                "difficulty": "easy", "knowledge_points": ["日常对话"],
                "source": "人教版小学英语三年级", "grade_level": "小学三年级"
            },
            {
                "content": "What's this in English? It's _____ orange.",
                "question_type": "选择题",
                "options": ["a", "an", "the", "/"],
                "answer": "B", "analysis": "orange以元音音素开头，用an",
                "difficulty": "easy", "knowledge_points": ["冠词", "基础词汇"],
                "source": "人教版小学英语三年级", "grade_level": "小学三年级"
            },
            {
                "content": "Where _____ you from? I'm from China.",
                "question_type": "选择题",
                "options": ["is", "are", "am", "be"],
                "answer": "B", "analysis": "you用are",
                "difficulty": "easy", "knowledge_points": ["疑问句", "日常对话"],
                "source": "人教版小学英语四年级", "grade_level": "小学四年级"
            },
            {
                "content": "Can you _____ English?",
                "question_type": "选择题",
                "options": ["say", "speak", "talk", "tell"],
                "answer": "B", "analysis": "说某种语言用speak",
                "difficulty": "easy", "knowledge_points": ["情态动词", "基础词汇"],
                "source": "人教版小学英语四年级", "grade_level": "小学四年级"
            },
            {
                "content": "There _____ a book and two pens on the desk.",
                "question_type": "选择题",
                "options": ["is", "are", "am", "be"],
                "answer": "A", "analysis": "there be句型就近原则，a book是单数用is",
                "difficulty": "medium", "knowledge_points": ["there be句型"],
                "source": "人教版小学英语五年级", "grade_level": "小学五年级"
            },
            {
                "content": "Would you like _____ tea or coffee?",
                "question_type": "选择题",
                "options": ["some", "any", "a", "an"],
                "answer": "A", "analysis": "would you like表示邀请，用some",
                "difficulty": "medium", "knowledge_points": ["代词", "食物和饮料"],
                "source": "人教版小学英语五年级", "grade_level": "小学五年级"
            }
        ]
    
    def get_all_questions(self) -> List[Dict[str, Any]]:
        """获取所有题目"""
        curriculum_questions = self.standards_data["question_sets"]
        real_world_questions = self.get_real_world_questions()
        return curriculum_questions + real_world_questions
    
    def get_all_knowledge_points(self) -> List[Dict[str, Any]]:
        """获取所有知识点"""
        return self.standards_data["knowledge_points"]

# 全局实例
educational_standards_data = EducationalStandardsData()
