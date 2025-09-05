"""
知识图谱Schema定义
定义了K12英语知识图谱的实体类型和关系类型
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum


class DifficultyLevel(str, Enum):
    """难度等级"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GradeLevel(str, Enum):
    """学段等级"""
    PRIMARY_1 = "小学一年级"
    PRIMARY_2 = "小学二年级"
    PRIMARY_3 = "小学三年级"
    PRIMARY_4 = "小学四年级"
    PRIMARY_5 = "小学五年级"
    PRIMARY_6 = "小学六年级"
    JUNIOR_1 = "初中一年级"
    JUNIOR_2 = "初中二年级"
    JUNIOR_3 = "初中三年级"
    SENIOR_1 = "高中一年级"
    SENIOR_2 = "高中二年级"
    SENIOR_3 = "高中三年级"


class QuestionType(str, Enum):
    """题目类型"""
    MULTIPLE_CHOICE = "选择题"
    FILL_BLANK = "填空题"
    READING_COMPREHENSION = "阅读理解"
    TRANSLATION = "翻译题"
    WRITING = "写作题"
    LISTENING = "听力题"


# ===== 实体类型 (Node Models) =====

class KnowledgePoint(BaseModel):
    """知识点实体"""
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    level: Optional[GradeLevel] = None
    difficulty: Optional[DifficultyLevel] = None
    keywords: Optional[List[str]] = []
    
    class Config:
        use_enum_values = True


class Question(BaseModel):
    """题目实体"""
    id: Optional[str] = None
    content: str  # 题干
    question_type: QuestionType
    options: Optional[List[str]] = []  # 选项（选择题用）
    answer: str  # 答案
    analysis: Optional[str] = None  # 解析
    source: Optional[str] = None  # 来源
    difficulty: Optional[DifficultyLevel] = None
    
    class Config:
        use_enum_values = True


class Textbook(BaseModel):
    """教材实体"""
    id: Optional[str] = None
    name: str
    publisher: str  # 出版社
    grade: GradeLevel
    version: Optional[str] = None
    
    class Config:
        use_enum_values = True


class Chapter(BaseModel):
    """章节实体"""
    id: Optional[str] = None
    name: str
    chapter_number: int
    textbook_id: str
    description: Optional[str] = None


# ===== 关系类型 (Relationship Models) =====

class Relationship(BaseModel):
    """基础关系模型"""
    from_node: str
    to_node: str
    properties: Optional[Dict[str, Any]] = {}


class HasSubPoint(Relationship):
    """包含关系 - 知识点层级结构"""
    pass


class TestsKnowledge(Relationship):
    """考查关系 - 题目考查知识点"""
    weight: float = 1.0  # 考查权重 0-1


class BelongsTo(Relationship):
    """属于关系 - 知识点属于教材/章节"""
    pass


class Requires(Relationship):
    """前置要求关系 - 学习依赖"""
    strength: float = 1.0  # 依赖强度


# ===== Cypher查询辅助类 =====

class GraphSchema:
    """图数据库Schema管理"""
    
    # 节点标签
    NODE_LABELS = {
        "KnowledgePoint": "知识点",
        "Question": "题目", 
        "Textbook": "教材",
        "Chapter": "章节"
    }
    
    # 关系类型
    RELATIONSHIP_TYPES = {
        "HAS_SUB_POINT": "包含",
        "TESTS": "考查",
        "BELONGS_TO": "属于", 
        "REQUIRES": "前置要求"
    }
    
    @staticmethod
    def get_create_constraints_cypher() -> List[str]:
        """获取创建约束的Cypher语句"""
        return [
            "CREATE CONSTRAINT knowledge_point_id IF NOT EXISTS FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE",
            "CREATE CONSTRAINT question_id IF NOT EXISTS FOR (q:Question) REQUIRE q.id IS UNIQUE",
            "CREATE CONSTRAINT textbook_id IF NOT EXISTS FOR (t:Textbook) REQUIRE t.id IS UNIQUE", 
            "CREATE CONSTRAINT chapter_id IF NOT EXISTS FOR (c:Chapter) REQUIRE c.id IS UNIQUE"
        ]
    
    @staticmethod
    def get_create_indexes_cypher() -> List[str]:
        """获取创建索引的Cypher语句"""
        return [
            "CREATE INDEX knowledge_point_name IF NOT EXISTS FOR (kp:KnowledgePoint) ON (kp.name)",
            "CREATE INDEX question_type IF NOT EXISTS FOR (q:Question) ON (q.question_type)",
            "CREATE INDEX question_difficulty IF NOT EXISTS FOR (q:Question) ON (q.difficulty)"
        ]


# ===== 示例数据结构 =====

SAMPLE_KNOWLEDGE_POINTS = [
    {
        "name": "英语语法",
        "description": "英语语法基础知识",
        "level": "小学三年级",
        "difficulty": "medium",
        "keywords": ["语法", "grammar"]
    },
    {
        "name": "动词时态", 
        "description": "动词的各种时态形式",
        "level": "小学四年级",
        "difficulty": "medium",
        "keywords": ["动词", "时态", "tense"]
    },
    {
        "name": "一般现在时",
        "description": "表示经常性、习惯性的动作或状态",
        "level": "小学四年级", 
        "difficulty": "easy",
        "keywords": ["一般现在时", "present simple"]
    },
    {
        "name": "一般过去时",
        "description": "表示过去发生的动作或状态",
        "level": "小学五年级",
        "difficulty": "easy", 
        "keywords": ["一般过去时", "past simple"]
    },
    {
        "name": "现在进行时",
        "description": "表示现在正在进行的动作",
        "level": "小学五年级",
        "difficulty": "medium",
        "keywords": ["现在进行时", "present continuous"]
    }
]
