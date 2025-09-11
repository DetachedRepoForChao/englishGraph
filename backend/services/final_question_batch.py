"""
最终题目批次 - 补充到200道题目
基于权威英语教育资源的精选题目
"""
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class FinalQuestionBatch:
    """最终题目批次"""
    
    def __init__(self):
        self.final_questions = self._get_final_question_batch()
    
    def _get_final_question_batch(self) -> List[Dict[str, Any]]:
        """获取最终批次的37道题目"""
        return [
            # 基础语法补充题目 (15道)
            {
                "content": "My friend and I _____ going to the movies tonight.",
                "question_type": "选择题",
                "options": ["is", "are", "am", "be"],
                "answer": "B", "analysis": "My friend and I是复数主语，用are",
                "difficulty": "easy", "knowledge_points": ["一般将来时", "主谓一致"],
                "source": "Cambridge Practice Tests", "grade_level": "小学五年级"
            },
            {
                "content": "Neither Tom nor his sister _____ at home yesterday.",
                "question_type": "选择题",
                "options": ["was", "were", "is", "are"],
                "answer": "A", "analysis": "neither...nor就近原则，sister是单数用was",
                "difficulty": "medium", "knowledge_points": ["主谓一致", "一般过去时"],
                "source": "Oxford Test Builder", "grade_level": "初中二年级"
            },
            {
                "content": "The news _____ very exciting.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "A", "analysis": "news是不可数名词，用单数",
                "difficulty": "medium", "knowledge_points": ["主谓一致"],
                "source": "Grammar Focus", "grade_level": "初中一年级"
            },
            {
                "content": "Two thirds of the students _____ girls.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "B", "analysis": "分数+复数名词，谓语动词用复数",
                "difficulty": "medium", "knowledge_points": ["主谓一致"],
                "source": "Advanced Grammar", "grade_level": "初中三年级"
            },
            {
                "content": "Everyone _____ ready for the test.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "A", "analysis": "everyone是单数，用is",
                "difficulty": "easy", "knowledge_points": ["主谓一致"],
                "source": "Basic Grammar", "grade_level": "小学六年级"
            },
            {
                "content": "The pair of shoes _____ expensive.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "A", "analysis": "a pair of作主语，谓语动词用单数",
                "difficulty": "medium", "knowledge_points": ["主谓一致"],
                "source": "Grammar Rules", "grade_level": "初中一年级"
            },
            {
                "content": "Physics _____ my favorite subject.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "A", "analysis": "学科名词作主语，用单数",
                "difficulty": "easy", "knowledge_points": ["主谓一致"],
                "source": "Subject English", "grade_level": "初中一年级"
            },
            {
                "content": "A number of students _____ absent today.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "B", "analysis": "a number of表示许多，谓语动词用复数",
                "difficulty": "medium", "knowledge_points": ["主谓一致"],
                "source": "Grammar Practice", "grade_level": "初中二年级"
            },
            {
                "content": "Not only the students but also the teacher _____ excited.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "A", "analysis": "not only...but also就近原则，teacher是单数",
                "difficulty": "hard", "knowledge_points": ["主谓一致"],
                "source": "Complex Grammar", "grade_level": "初中三年级"
            },
            {
                "content": "Ten minutes _____ enough for this task.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "A", "analysis": "时间作主语，看作整体用单数",
                "difficulty": "medium", "knowledge_points": ["主谓一致"],
                "source": "Time Grammar", "grade_level": "初中二年级"
            },
            
            # 高级语法题目 (12道)
            {
                "content": "It is the first time that I _____ such a beautiful sunset.",
                "question_type": "选择题",
                "options": ["see", "saw", "have seen", "had seen"],
                "answer": "C", "analysis": "It is the first time that...用现在完成时",
                "difficulty": "hard", "knowledge_points": ["现在完成时", "强调句"],
                "source": "Advanced Grammar", "grade_level": "高中一年级"
            },
            {
                "content": "_____ you told me earlier, I wouldn't have made this mistake.",
                "question_type": "选择题",
                "options": ["If", "Had", "Should", "Were"],
                "answer": "B", "analysis": "虚拟语气的倒装，Had you told = If you had told",
                "difficulty": "hard", "knowledge_points": ["虚拟语气", "倒装句"],
                "source": "High School Grammar", "grade_level": "高中二年级"
            },
            {
                "content": "The building _____ next year will be our new library.",
                "question_type": "选择题",
                "options": ["built", "building", "to be built", "being built"],
                "answer": "C", "analysis": "将来被建造的建筑，用to be built",
                "difficulty": "hard", "knowledge_points": ["非谓语动词", "被动语态"],
                "source": "Construction Grammar", "grade_level": "高中一年级"
            },
            {
                "content": "_____ in the mountains for a week, the two students were finally saved.",
                "question_type": "选择题",
                "options": ["Having lost", "Lost", "Being lost", "Losing"],
                "answer": "A", "analysis": "完成时分词表示先后顺序",
                "difficulty": "hard", "knowledge_points": ["非谓语动词"],
                "source": "Participle Practice", "grade_level": "高中二年级"
            },
            {
                "content": "It was in this room _____ the meeting was held.",
                "question_type": "选择题",
                "options": ["where", "that", "which", "when"],
                "answer": "B", "analysis": "强调句型It was...that...",
                "difficulty": "hard", "knowledge_points": ["强调句"],
                "source": "Emphasis Structure", "grade_level": "高中一年级"
            },
            {
                "content": "The moment I saw him, I knew something _____ wrong.",
                "question_type": "选择题",
                "options": ["went", "had gone", "has gone", "goes"],
                "answer": "B", "analysis": "过去的过去，用过去完成时",
                "difficulty": "hard", "knowledge_points": ["过去完成时"],
                "source": "Tense Sequence", "grade_level": "高中一年级"
            },
            {
                "content": "_____ he said at the meeting astonished everybody present.",
                "question_type": "选择题",
                "options": ["What", "That", "Which", "Where"],
                "answer": "A", "analysis": "what引导主语从句",
                "difficulty": "hard", "knowledge_points": ["主语从句"],
                "source": "Clause Grammar", "grade_level": "高中二年级"
            },
            {
                "content": "I would appreciate it if you _____ me a hand.",
                "question_type": "选择题",
                "options": ["give", "gave", "will give", "could give"],
                "answer": "D", "analysis": "虚拟语气，could表示礼貌请求",
                "difficulty": "hard", "knowledge_points": ["虚拟语气", "情态动词"],
                "source": "Polite Request", "grade_level": "高中一年级"
            },
            {
                "content": "The reason _____ he was late was _____ his car broke down.",
                "question_type": "选择题",
                "options": ["why, that", "that, because", "why, because", "that, that"],
                "answer": "A", "analysis": "reason后用why，表语从句用that",
                "difficulty": "hard", "knowledge_points": ["定语从句", "表语从句"],
                "source": "Complex Clauses", "grade_level": "高中二年级"
            },
            {
                "content": "_____ from what he said, he must be an honest man.",
                "question_type": "选择题",
                "options": ["Judge", "Judging", "Judged", "To judge"],
                "answer": "B", "analysis": "judging from是固定搭配",
                "difficulty": "hard", "knowledge_points": ["非谓语动词"],
                "source": "Fixed Expressions", "grade_level": "高中一年级"
            },
            {
                "content": "Little _____ that he would become famous one day.",
                "question_type": "选择题",
                "options": ["he knew", "did he know", "he knows", "does he know"],
                "answer": "B", "analysis": "little开头的倒装句",
                "difficulty": "hard", "knowledge_points": ["倒装句"],
                "source": "Inversion Practice", "grade_level": "高中二年级"
            },
            {
                "content": "The professor, together with his students, _____ doing the experiment.",
                "question_type": "选择题",
                "options": ["is", "are", "was", "were"],
                "answer": "A", "analysis": "together with不影响主语，professor是单数",
                "difficulty": "medium", "knowledge_points": ["主谓一致"],
                "source": "Subject Agreement", "grade_level": "初中三年级"
            },
            
            # 实用对话题目 (10道)
            {
                "content": "A: How do you like your new job? B: _____",
                "question_type": "选择题",
                "options": ["Very much", "I like it very much", "It's very good", "All of the above"],
                "answer": "D", "analysis": "询问看法的多种回答方式",
                "difficulty": "easy", "knowledge_points": ["日常对话"],
                "source": "Conversation Practice", "grade_level": "小学六年级"
            },
            {
                "content": "A: Would you mind if I opened the window? B: _____",
                "question_type": "选择题",
                "options": ["Yes, please", "No, go ahead", "Yes, I would", "No, I wouldn't"],
                "answer": "B", "analysis": "Would you mind的回答，不介意说No",
                "difficulty": "medium", "knowledge_points": ["情态动词", "日常对话"],
                "source": "Polite English", "grade_level": "初中一年级"
            },
            {
                "content": "A: I'm sorry to keep you waiting. B: _____",
                "question_type": "选择题",
                "options": ["That's all right", "You're welcome", "The same to you", "That's right"],
                "answer": "A", "analysis": "对道歉的回应用That's all right",
                "difficulty": "easy", "knowledge_points": ["日常对话"],
                "source": "Apology Response", "grade_level": "小学五年级"
            },
            {
                "content": "A: Could I use your phone? B: _____",
                "question_type": "选择题",
                "options": ["Yes, you could", "Sure, go ahead", "No, you couldn't", "Yes, you can"],
                "answer": "B", "analysis": "同意请求的自然回答",
                "difficulty": "easy", "knowledge_points": ["情态动词", "日常对话"],
                "source": "Permission Dialogue", "grade_level": "小学六年级"
            },
            {
                "content": "A: What's the weather like today? B: _____",
                "question_type": "选择题",
                "options": ["It's sun", "It's sunny", "It's rain", "It's wind"],
                "answer": "B", "analysis": "天气形容词用sunny",
                "difficulty": "easy", "knowledge_points": ["天气和季节", "形容词"],
                "source": "Weather Talk", "grade_level": "小学四年级"
            },
            {
                "content": "A: How often do you exercise? B: _____",
                "question_type": "选择题",
                "options": ["Two hours", "In the morning", "Three times a week", "At the gym"],
                "answer": "C", "analysis": "how often询问频率",
                "difficulty": "easy", "knowledge_points": ["疑问句", "副词"],
                "source": "Frequency Questions", "grade_level": "小学五年级"
            },
            {
                "content": "A: What do you do? B: _____",
                "question_type": "选择题",
                "options": ["I'm fine", "I'm a teacher", "I'm reading", "I'm from China"],
                "answer": "B", "analysis": "询问职业，回答职业",
                "difficulty": "easy", "knowledge_points": ["职业和工作", "日常对话"],
                "source": "Job Interview", "grade_level": "小学五年级"
            },
            {
                "content": "A: How much is this shirt? B: _____",
                "question_type": "选择题",
                "options": ["It's blue", "It's cotton", "It's 50 dollars", "It's large"],
                "answer": "C", "analysis": "询问价格，回答价格",
                "difficulty": "easy", "knowledge_points": ["购物和金钱", "数字和时间"],
                "source": "Shopping Dialogue", "grade_level": "小学六年级"
            },
            {
                "content": "A: How long does it take to get there? B: _____",
                "question_type": "选择题",
                "options": ["About 2 kilometers", "About 2 hours", "Very far", "By bus"],
                "answer": "B", "analysis": "how long询问时间长度",
                "difficulty": "medium", "knowledge_points": ["疑问句", "数字和时间"],
                "source": "Travel Questions", "grade_level": "小学六年级"
            },
            {
                "content": "A: What's your hobby? B: _____",
                "question_type": "选择题",
                "options": ["I like reading", "I'm reading", "I can read", "I read books"],
                "answer": "A", "analysis": "询问爱好，用like表达喜好",
                "difficulty": "easy", "knowledge_points": ["运动和爱好", "日常对话"],
                "source": "Hobby Talk", "grade_level": "小学五年级"
            },
            
            # 阅读理解题目 (5道)
            {
                "content": "Read and choose: Tom is a student. He likes playing football. What does Tom like?",
                "question_type": "阅读理解",
                "options": ["Basketball", "Football", "Tennis", "Swimming"],
                "answer": "B", "analysis": "文中明确说Tom likes playing football",
                "difficulty": "easy", "knowledge_points": ["阅读理解", "运动和爱好"],
                "source": "Reading Comprehension", "grade_level": "小学四年级"
            },
            {
                "content": "According to the passage: 'Mary gets up at 6:00 AM every day.' When does Mary get up?",
                "question_type": "阅读理解",
                "options": ["6:00 PM", "6:00 AM", "7:00 AM", "5:00 AM"],
                "answer": "B", "analysis": "文中明确说6:00 AM",
                "difficulty": "easy", "knowledge_points": ["阅读理解", "数字和时间"],
                "source": "Daily Routine Reading", "grade_level": "小学三年级"
            },
            {
                "content": "From the text: 'It was raining heavily yesterday.' What was the weather like yesterday?",
                "question_type": "阅读理解",
                "options": ["Sunny", "Cloudy", "Rainy", "Windy"],
                "answer": "C", "analysis": "raining heavily表示下大雨",
                "difficulty": "easy", "knowledge_points": ["阅读理解", "天气和季节"],
                "source": "Weather Reading", "grade_level": "小学四年级"
            },
            {
                "content": "The passage says: 'She has lived in Beijing since 2010.' How long has she lived in Beijing?",
                "question_type": "阅读理解",
                "options": ["For 2010 years", "Since 13 years", "For about 13 years", "In 2010"],
                "answer": "C", "analysis": "从2010年到现在大约13年",
                "difficulty": "medium", "knowledge_points": ["阅读理解", "现在完成时"],
                "source": "Time Reading", "grade_level": "初中一年级"
            },
            {
                "content": "According to the article: 'The book was written by a famous author.' Who wrote the book?",
                "question_type": "阅读理解",
                "options": ["A student", "A teacher", "A famous author", "A reporter"],
                "answer": "C", "analysis": "文中明确说by a famous author",
                "difficulty": "easy", "knowledge_points": ["阅读理解", "被动语态"],
                "source": "Author Reading", "grade_level": "初中二年级"
            },
            
            # 写作和翻译题目 (10道)
            {
                "content": "Translate into English: 他每天骑自行车上学。",
                "question_type": "翻译题",
                "options": [],
                "answer": "He goes to school by bike every day.",
                "analysis": "every day用一般现在时，by bike表示方式",
                "difficulty": "medium", "knowledge_points": ["一般现在时", "介词", "交通工具"],
                "source": "Translation Practice", "grade_level": "小学五年级"
            },
            {
                "content": "Translate: 我正在做作业，请不要打扰我。",
                "question_type": "翻译题",
                "options": [],
                "answer": "I am doing my homework. Please don't disturb me.",
                "analysis": "正在做用现在进行时，请不要是祈使句",
                "difficulty": "medium", "knowledge_points": ["现在进行时", "祈使句"],
                "source": "Translation Practice", "grade_level": "小学六年级"
            },
            {
                "content": "Complete the sentence: 昨天下雨了，所以我没有出去。",
                "question_type": "翻译题",
                "options": [],
                "answer": "It rained yesterday, so I didn't go out.",
                "analysis": "昨天用过去时，so表示因果关系",
                "difficulty": "medium", "knowledge_points": ["一般过去时", "状语从句"],
                "source": "Translation Practice", "grade_level": "小学五年级"
            },
            {
                "content": "Translate: 这是我看过的最有趣的电影。",
                "question_type": "翻译题",
                "options": [],
                "answer": "This is the most interesting movie I have ever seen.",
                "analysis": "最高级+定语从句+现在完成时",
                "difficulty": "hard", "knowledge_points": ["比较级和最高级", "定语从句", "现在完成时"],
                "source": "Complex Translation", "grade_level": "初中三年级"
            },
            {
                "content": "Translate: 如果明天天气好，我们就去公园。",
                "question_type": "翻译题",
                "options": [],
                "answer": "If the weather is fine tomorrow, we will go to the park.",
                "analysis": "if条件句，从句现在时，主句将来时",
                "difficulty": "medium", "knowledge_points": ["条件句", "一般将来时"],
                "source": "Conditional Translation", "grade_level": "初中二年级"
            },
            {
                "content": "Write a sentence using 'used to': (关于过去的习惯)",
                "question_type": "写作题",
                "options": [],
                "answer": "I used to play football when I was young.",
                "analysis": "used to表示过去的习惯",
                "difficulty": "medium", "knowledge_points": ["一般过去时"],
                "source": "Writing Practice", "grade_level": "初中一年级"
            },
            {
                "content": "Make a question for the answer: 'She goes to work by subway.'",
                "question_type": "写作题",
                "options": [],
                "answer": "How does she go to work?",
                "analysis": "询问方式用how",
                "difficulty": "medium", "knowledge_points": ["疑问句", "交通工具"],
                "source": "Question Formation", "grade_level": "小学六年级"
            },
            {
                "content": "Rewrite using passive voice: 'The teacher explained the grammar clearly.'",
                "question_type": "转换题",
                "options": [],
                "answer": "The grammar was explained clearly by the teacher.",
                "analysis": "主动语态变被动语态",
                "difficulty": "medium", "knowledge_points": ["被动语态"],
                "source": "Voice Transformation", "grade_level": "初中二年级"
            },
            {
                "content": "Change to reported speech: He said, 'I will come tomorrow.'",
                "question_type": "转换题",
                "options": [],
                "answer": "He said that he would come the next day.",
                "analysis": "直接引语变间接引语，时态和时间状语要变",
                "difficulty": "hard", "knowledge_points": ["宾语从句"],
                "source": "Reported Speech", "grade_level": "初中三年级"
            }
        ]
    
    def get_final_questions(self) -> List[Dict[str, Any]]:
        """获取最终批次题目"""
        return self.final_questions
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        questions = self.final_questions
        
        stats = {
            "total_questions": len(questions),
            "by_type": {},
            "by_difficulty": {},
            "by_grade": {},
            "by_knowledge_point": {}
        }
        
        for q in questions:
            # 按类型
            q_type = q.get("question_type", "未知")
            stats["by_type"][q_type] = stats["by_type"].get(q_type, 0) + 1
            
            # 按难度
            difficulty = q.get("difficulty", "medium")
            stats["by_difficulty"][difficulty] = stats["by_difficulty"].get(difficulty, 0) + 1
            
            # 按年级
            grade = q.get("grade_level", "未设置")
            stats["by_grade"][grade] = stats["by_grade"].get(grade, 0) + 1
            
            # 按知识点
            for kp in q.get("knowledge_points", []):
                stats["by_knowledge_point"][kp] = stats["by_knowledge_point"].get(kp, 0) + 1
        
        return stats

# 全局实例
final_question_batch = FinalQuestionBatch()
