#!/usr/bin/env python3
"""
通过Vercel部署的API初始化云数据库
"""
import requests
import json
import logging
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vercel部署的API地址
BASE_URL = "https://english-knowledge-graph-bsfvthw7u-chao-wangs-projects-dfded257.vercel.app"

def create_knowledge_point(kp_data: Dict[str, Any]) -> bool:
    """创建知识点"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/knowledge/",
            json=kp_data,
            timeout=30
        )
        if response.status_code == 200:
            logger.info(f"✅ 创建知识点成功: {kp_data['name']}")
            return True
        else:
            logger.error(f"❌ 创建知识点失败: {kp_data['name']} - {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ 创建知识点异常: {kp_data['name']} - {e}")
        return False

def create_question(q_data: Dict[str, Any]) -> str:
    """创建题目"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/questions/",
            json=q_data,
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            question_id = result.get("id")
            logger.info(f"✅ 创建题目成功: {question_id}")
            return question_id
        else:
            logger.error(f"❌ 创建题目失败: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"❌ 创建题目异常: {e}")
        return None

def link_question_to_knowledge(question_id: str, kp_name: str, weight: float = 0.8) -> bool:
    """关联题目和知识点"""
    try:
        # 先搜索知识点获取ID
        search_response = requests.get(
            f"{BASE_URL}/api/knowledge/search",
            params={"keyword": kp_name},
            timeout=30
        )
        
        if search_response.status_code != 200:
            logger.error(f"❌ 搜索知识点失败: {kp_name}")
            return False
        
        knowledge_points = search_response.json()
        kp_id = None
        for kp in knowledge_points:
            if kp["name"] == kp_name:
                kp_id = kp["id"]
                break
        
        if not kp_id:
            logger.error(f"❌ 未找到知识点: {kp_name}")
            return False
        
        # 创建关联
        response = requests.post(
            f"{BASE_URL}/api/questions/{question_id}/knowledge/{kp_id}",
            params={"weight": weight},
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"✅ 关联成功: {question_id} -> {kp_name}")
            return True
        else:
            logger.error(f"❌ 关联失败: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 关联异常: {e}")
        return False

def init_sample_data():
    """初始化示例数据"""
    logger.info("🚀 开始通过API初始化数据...")
    
    # 示例知识点
    knowledge_points = [
        {
            "name": "一般现在时",
            "description": "表示经常性、习惯性的动作或状态",
            "level": "小学四年级",
            "difficulty": "easy",
            "keywords": ["always", "usually", "every day", "第三人称单数"]
        },
        {
            "name": "一般过去时",
            "description": "表示过去发生的动作或状态",
            "level": "小学五年级",
            "difficulty": "easy",
            "keywords": ["yesterday", "last week", "ago", "过去式"]
        },
        {
            "name": "现在进行时",
            "description": "表示现在正在进行的动作",
            "level": "小学六年级",
            "difficulty": "medium",
            "keywords": ["now", "at present", "be doing", "正在"]
        },
        {
            "name": "现在完成时",
            "description": "表示过去发生的动作对现在造成的影响",
            "level": "初中一年级",
            "difficulty": "medium",
            "keywords": ["have done", "already", "yet", "since"]
        },
        {
            "name": "被动语态",
            "description": "表示动作的承受者作为主语",
            "level": "初中二年级",
            "difficulty": "hard",
            "keywords": ["be done", "by", "被动", "过去分词"]
        },
        {
            "name": "定语从句",
            "description": "修饰名词或代词的从句",
            "level": "初中三年级",
            "difficulty": "hard",
            "keywords": ["who", "which", "that", "关系代词"]
        },
        {
            "name": "宾语从句",
            "description": "作宾语的从句",
            "level": "初中三年级",
            "difficulty": "hard",
            "keywords": ["that", "what", "if", "whether"]
        },
        {
            "name": "比较级和最高级",
            "description": "形容词和副词的比较形式",
            "level": "小学六年级",
            "difficulty": "medium",
            "keywords": ["than", "more", "most", "er", "est"]
        },
        {
            "name": "介词",
            "description": "表示名词、代词等与其他词的关系",
            "level": "小学三年级",
            "difficulty": "easy",
            "keywords": ["in", "on", "at", "for", "with"]
        },
        {
            "name": "动词时态",
            "description": "动词的时间和状态变化",
            "level": "小学四年级",
            "difficulty": "medium",
            "keywords": ["时态", "tense", "动词变化"]
        }
    ]
    
    # 创建知识点
    logger.info("📚 创建知识点...")
    for kp in knowledge_points:
        create_knowledge_point(kp)
    
    # 示例题目
    questions = [
        {
            "content": "She _____ to school every day.",
            "question_type": "选择题",
            "options": ["go", "goes", "going", "gone"],
            "answer": "B",
            "analysis": "主语是第三人称单数，动词用goes",
            "difficulty": "easy",
            "knowledge_points": ["一般现在时"]
        },
        {
            "content": "Yesterday I _____ to the park.",
            "question_type": "选择题",
            "options": ["go", "goes", "went", "going"],
            "answer": "C",
            "analysis": "yesterday表示过去时间，用过去式went",
            "difficulty": "easy",
            "knowledge_points": ["一般过去时"]
        },
        {
            "content": "Look! The children _____ in the playground.",
            "question_type": "选择题",
            "options": ["play", "plays", "are playing", "played"],
            "answer": "C",
            "analysis": "Look!表示正在发生，用现在进行时",
            "difficulty": "medium",
            "knowledge_points": ["现在进行时"]
        },
        {
            "content": "I _____ already _____ my homework.",
            "question_type": "选择题",
            "options": ["have, finished", "has, finished", "had, finished", "will, finish"],
            "answer": "A",
            "analysis": "already是现在完成时的标志词",
            "difficulty": "medium",
            "knowledge_points": ["现在完成时"]
        },
        {
            "content": "The letter _____ by Tom yesterday.",
            "question_type": "选择题",
            "options": ["wrote", "was written", "is written", "writes"],
            "answer": "B",
            "analysis": "by表示被动语态，yesterday表示过去时",
            "difficulty": "hard",
            "knowledge_points": ["被动语态"]
        },
        {
            "content": "This apple is _____ than that one.",
            "question_type": "选择题",
            "options": ["sweet", "sweeter", "sweetest", "more sweet"],
            "answer": "B",
            "analysis": "than表示比较，用比较级sweeter",
            "difficulty": "medium",
            "knowledge_points": ["比较级和最高级"]
        }
    ]
    
    # 创建题目
    logger.info("📝 创建题目...")
    for q in questions:
        # 分离知识点信息
        knowledge_points = q.pop("knowledge_points", [])
        
        # 创建题目
        question_id = create_question(q)
        
        # 关联知识点
        if question_id:
            for kp_name in knowledge_points:
                link_question_to_knowledge(question_id, kp_name)
    
    logger.info("🎉 数据初始化完成！")

if __name__ == "__main__":
    init_sample_data()
