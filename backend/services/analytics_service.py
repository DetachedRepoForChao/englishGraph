"""
数据分析服务
提供学情分析、知识图谱分析等功能
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict, Counter
import json

from backend.services.database import neo4j_service

logger = logging.getLogger(__name__)


class AnalyticsService:
    """数据分析服务类"""
    
    def __init__(self):
        pass
    
    def _ensure_db_connection(self):
        """确保数据库连接可用"""
        if not neo4j_service.driver:
            if not neo4j_service.connect():
                logger.error("无法连接到数据库")
                return False
        return True
    
    def get_knowledge_coverage_analysis(self) -> Dict[str, Any]:
        """获取知识点覆盖分析"""
        try:
            # 确保数据库连接
            if not self._ensure_db_connection():
                return {"coverage_data": [], "summary": {}}
            
            with neo4j_service.driver.session() as session:
                # 统计每个知识点对应的题目数量
                result = session.run("""
                    MATCH (kp:KnowledgePoint)
                    OPTIONAL MATCH (q:Question)-[:TESTS]->(kp)
                    RETURN kp.name as knowledge_point, 
                           kp.level as level,
                           kp.difficulty as difficulty,
                           count(q) as question_count
                    ORDER BY question_count DESC
                """)
                
                coverage_data = []
                total_questions = 0
                
                for record in result:
                    kp_data = {
                        "knowledge_point": record["knowledge_point"],
                        "level": record["level"],
                        "difficulty": record["difficulty"],
                        "question_count": record["question_count"]
                    }
                    coverage_data.append(kp_data)
                    total_questions += record["question_count"]
                
                # 计算覆盖率统计
                covered_kps = len([kp for kp in coverage_data if kp["question_count"] > 0])
                total_kps = len(coverage_data)
                coverage_rate = (covered_kps / total_kps * 100) if total_kps > 0 else 0
                
                return {
                    "coverage_data": coverage_data,
                    "summary": {
                        "total_knowledge_points": total_kps,
                        "covered_knowledge_points": covered_kps,
                        "coverage_rate": round(coverage_rate, 2),
                        "total_questions": total_questions,
                        "average_questions_per_kp": round(total_questions / total_kps, 2) if total_kps > 0 else 0
                    }
                }
        
        except Exception as e:
            logger.error(f"知识点覆盖分析失败: {e}")
            return {"coverage_data": [], "summary": {}}
    
    def get_difficulty_distribution(self) -> Dict[str, Any]:
        """获取题目难度分布"""
        try:
            # 确保数据库连接
            if not self._ensure_db_connection():
                return {"difficulty_distribution": [], "total_questions": 0}
            
            with neo4j_service.driver.session() as session:
                # 统计各难度级别的题目数量
                result = session.run("""
                    MATCH (q:Question)
                    RETURN q.difficulty as difficulty, count(q) as count
                """)
                
                difficulty_data = []
                total_questions = 0
                
                for record in result:
                    difficulty = record["difficulty"] or "未设置"
                    count = record["count"]
                    difficulty_data.append({
                        "difficulty": difficulty,
                        "count": count
                    })
                    total_questions += count
                
                # 计算百分比
                for item in difficulty_data:
                    item["percentage"] = round(item["count"] / total_questions * 100, 2) if total_questions > 0 else 0
                
                return {
                    "difficulty_distribution": difficulty_data,
                    "total_questions": total_questions
                }
        
        except Exception as e:
            logger.error(f"难度分布分析失败: {e}")
            return {"difficulty_distribution": [], "total_questions": 0}
    
    def get_question_type_distribution(self) -> Dict[str, Any]:
        """获取题目类型分布"""
        try:
            with neo4j_service.driver.session() as session:
                result = session.run("""
                    MATCH (q:Question)
                    RETURN q.question_type as question_type, count(q) as count
                    ORDER BY count DESC
                """)
                
                type_data = []
                total_questions = 0
                
                for record in result:
                    count = record["count"]
                    type_data.append({
                        "question_type": record["question_type"],
                        "count": count
                    })
                    total_questions += count
                
                # 计算百分比
                for item in type_data:
                    item["percentage"] = round(item["count"] / total_questions * 100, 2) if total_questions > 0 else 0
                
                return {
                    "type_distribution": type_data,
                    "total_questions": total_questions
                }
        
        except Exception as e:
            logger.error(f"题目类型分布分析失败: {e}")
            return {"type_distribution": [], "total_questions": 0}
    
    def get_knowledge_hierarchy_analysis(self) -> Dict[str, Any]:
        """获取知识点层级结构分析"""
        try:
            with neo4j_service.driver.session() as session:
                # 获取层级关系
                result = session.run("""
                    MATCH (parent:KnowledgePoint)-[:HAS_SUB_POINT]->(child:KnowledgePoint)
                    RETURN parent.name as parent_name, 
                           child.name as child_name,
                           parent.id as parent_id,
                           child.id as child_id
                """)
                
                hierarchy_relations = []
                nodes = set()
                
                for record in result:
                    relation = {
                        "parent": record["parent_name"],
                        "child": record["child_name"],
                        "parent_id": record["parent_id"],
                        "child_id": record["child_id"]
                    }
                    hierarchy_relations.append(relation)
                    nodes.add(record["parent_name"])
                    nodes.add(record["child_name"])
                
                # 找出根节点（没有父节点的节点）
                children = {rel["child"] for rel in hierarchy_relations}
                parents = {rel["parent"] for rel in hierarchy_relations}
                root_nodes = parents - children
                
                # 计算每个节点的层级深度
                def calculate_depth(node_name, relations, visited=None):
                    if visited is None:
                        visited = set()
                    
                    if node_name in visited:
                        return 0  # 避免循环
                    
                    visited.add(node_name)
                    
                    # 找到所有子节点
                    child_relations = [rel for rel in relations if rel["parent"] == node_name]
                    if not child_relations:
                        return 1  # 叶子节点
                    
                    max_child_depth = max(calculate_depth(rel["child"], relations, visited.copy()) 
                                        for rel in child_relations)
                    return max_child_depth + 1
                
                depth_analysis = {}
                for root in root_nodes:
                    depth_analysis[root] = calculate_depth(root, hierarchy_relations)
                
                return {
                    "hierarchy_relations": hierarchy_relations,
                    "root_nodes": list(root_nodes),
                    "total_nodes": len(nodes),
                    "total_relations": len(hierarchy_relations),
                    "depth_analysis": depth_analysis,
                    "max_depth": max(depth_analysis.values()) if depth_analysis else 0
                }
        
        except Exception as e:
            logger.error(f"知识点层级分析失败: {e}")
            return {
                "hierarchy_relations": [],
                "root_nodes": [],
                "total_nodes": 0,
                "total_relations": 0,
                "depth_analysis": {},
                "max_depth": 0
            }
    
    def get_ai_agent_accuracy_analysis(self) -> Dict[str, Any]:
        """分析AI Agent标注准确率"""
        try:
            with neo4j_service.driver.session() as session:
                # 获取所有已标注的题目
                result = session.run("""
                    MATCH (q:Question)-[r:TESTS]->(kp:KnowledgePoint)
                    RETURN q.id as question_id,
                           q.content as content,
                           q.question_type as question_type,
                           q.difficulty as difficulty,
                           collect({name: kp.name, weight: r.weight}) as knowledge_points
                """)
                
                questions_with_annotations = []
                for record in result:
                    questions_with_annotations.append({
                        "question_id": record["question_id"],
                        "content": record["content"],
                        "question_type": record["question_type"],
                        "difficulty": record["difficulty"],
                        "knowledge_points": record["knowledge_points"]
                    })
                
                # 分析准确率
                accuracy_analysis = self._analyze_annotation_accuracy(questions_with_annotations)
                
                # 获取未标注题目
                result = session.run("""
                    MATCH (q:Question)
                    WHERE NOT (q)-[:TESTS]->()
                    RETURN count(q) as unannotated_count
                """)
                unannotated_count = result.single()["unannotated_count"]
                
                return {
                    "annotated_questions": questions_with_annotations,
                    "accuracy_analysis": accuracy_analysis,
                    "total_annotated": len(questions_with_annotations),
                    "unannotated_count": unannotated_count,
                    "coverage_rate": len(questions_with_annotations) / (len(questions_with_annotations) + unannotated_count) * 100 if (len(questions_with_annotations) + unannotated_count) > 0 else 0
                }
        
        except Exception as e:
            logger.error(f"AI Agent准确率分析失败: {e}")
            return {
                "annotated_questions": [],
                "accuracy_analysis": {},
                "total_annotated": 0,
                "unannotated_count": 0,
                "coverage_rate": 0
            }
    
    def _analyze_annotation_accuracy(self, questions_with_annotations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析标注准确率"""
        if not questions_with_annotations:
            return {"accuracy_rate": 0, "details": []}
        
        correct_annotations = 0
        total_annotations = len(questions_with_annotations)
        accuracy_details = []
        
        for question in questions_with_annotations:
            content = question["content"].lower()
            knowledge_points = [kp["name"] for kp in question["knowledge_points"]]
            
            # 基于关键词和语法特征的准确性评估
            expected_kps = self._get_expected_knowledge_points(content)
            
            # 计算匹配度
            matches = []
            for expected_kp in expected_kps:
                if any(expected_kp in kp for kp in knowledge_points):
                    matches.append(expected_kp)
            
            is_accurate = len(matches) > 0
            if is_accurate:
                correct_annotations += 1
            
            accuracy_details.append({
                "question_id": question["question_id"],
                "content": question["content"][:50] + "..." if len(question["content"]) > 50 else question["content"],
                "annotated_kps": knowledge_points,
                "expected_kps": expected_kps,
                "matches": matches,
                "is_accurate": is_accurate
            })
        
        accuracy_rate = (correct_annotations / total_annotations * 100) if total_annotations > 0 else 0
        
        return {
            "accuracy_rate": round(accuracy_rate, 2),
            "correct_annotations": correct_annotations,
            "total_annotations": total_annotations,
            "details": accuracy_details
        }
    
    def _get_expected_knowledge_points(self, content: str) -> List[str]:
        """基于题目内容推断期望的知识点"""
        expected = []
        
        # 时态识别规则
        if any(word in content for word in ["every day", "every week", "always", "usually", "often"]):
            expected.append("一般现在时")
        
        if any(word in content for word in ["yesterday", "last week", "last month", "ago"]):
            expected.append("一般过去时")
        
        if any(word in content for word in ["now", "at the moment", "look!", "listen!"]):
            expected.append("现在进行时")
        
        if any(word in content for word in ["already", "yet", "just", "ever", "never", "since", "for"]):
            expected.append("现在完成时")
        
        # 语法结构识别
        if any(word in content for word in ["who", "which", "that", "whom", "whose"]):
            expected.append("定语从句")
        
        if "tell me" in content and any(word in content for word in ["where", "what", "when", "how", "why"]):
            expected.append("宾语从句")
        
        if any(word in content for word in ["by", "was", "were"]) and any(word in content for word in ["cleaned", "written", "made"]):
            expected.append("被动语态")
        
        if "than" in content or any(word in content for word in ["more", "most", "-er", "-est"]):
            expected.append("比较级和最高级")
        
        return expected

    def get_knowledge_correlation_analysis(self) -> Dict[str, Any]:
        """获取知识点关联分析"""
        try:
            with neo4j_service.driver.session() as session:
                # 找出经常一起出现的知识点对
                result = session.run("""
                    MATCH (q:Question)-[:TESTS]->(kp1:KnowledgePoint)
                    MATCH (q)-[:TESTS]->(kp2:KnowledgePoint)
                    WHERE kp1.id < kp2.id  // 避免重复和自关联
                    RETURN kp1.name as kp1_name, 
                           kp2.name as kp2_name,
                           count(q) as co_occurrence_count
                    ORDER BY co_occurrence_count DESC
                    LIMIT 20
                """)
                
                correlations = []
                for record in result:
                    correlations.append({
                        "knowledge_point_1": record["kp1_name"],
                        "knowledge_point_2": record["kp2_name"],
                        "co_occurrence_count": record["co_occurrence_count"]
                    })
                
                # 获取前置关系
                result = session.run("""
                    MATCH (target:KnowledgePoint)-[r:REQUIRES]->(prereq:KnowledgePoint)
                    RETURN target.name as target_name,
                           prereq.name as prereq_name,
                           r.strength as strength
                """)
                
                prerequisites = []
                for record in result:
                    prerequisites.append({
                        "target": record["target_name"],
                        "prerequisite": record["prereq_name"],
                        "strength": record["strength"]
                    })
                
                return {
                    "correlations": correlations,
                    "prerequisites": prerequisites
                }
        
        except Exception as e:
            logger.error(f"知识点关联分析失败: {e}")
            return {"correlations": [], "prerequisites": []}
    
    def generate_learning_path_recommendation(self, target_knowledge_points: List[str]) -> Dict[str, Any]:
        """生成学习路径推荐"""
        try:
            if not target_knowledge_points:
                return {"learning_path": [], "total_steps": 0}
            
            with neo4j_service.driver.session() as session:
                learning_paths = {}
                
                for target_kp in target_knowledge_points:
                    # 找到到达目标知识点的所有前置路径
                    result = session.run("""
                        MATCH path = (start:KnowledgePoint)-[:REQUIRES*0..5]->(target:KnowledgePoint {name: $target})
                        WHERE NOT (start)-[:REQUIRES]->()  // 起始节点没有前置要求
                        RETURN [node in nodes(path) | {name: node.name, id: node.id, difficulty: node.difficulty}] as path_nodes,
                               length(path) as path_length
                        ORDER BY path_length
                        LIMIT 5
                    """, {"target": target_kp})
                    
                    paths = []
                    for record in result:
                        paths.append({
                            "nodes": record["path_nodes"],
                            "length": record["path_length"]
                        })
                    
                    learning_paths[target_kp] = paths
                
                # 为每个目标知识点推荐最优路径
                recommendations = []
                for target_kp, paths in learning_paths.items():
                    if paths:
                        best_path = paths[0]  # 选择最短路径
                        recommendations.append({
                            "target_knowledge_point": target_kp,
                            "recommended_path": best_path["nodes"],
                            "path_length": best_path["length"],
                            "alternative_paths": paths[1:3]  # 提供备选路径
                        })
                    else:
                        recommendations.append({
                            "target_knowledge_point": target_kp,
                            "recommended_path": [{"name": target_kp}],
                            "path_length": 0,
                            "alternative_paths": []
                        })
                
                return {
                    "learning_path_recommendations": recommendations,
                    "total_targets": len(target_knowledge_points)
                }
        
        except Exception as e:
            logger.error(f"学习路径推荐生成失败: {e}")
            return {"learning_path_recommendations": [], "total_targets": 0}
    
    def analyze_student_weak_points(self, student_answers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析学生薄弱知识点
        
        Args:
            student_answers: 学生答题记录，格式: [{"question_id": "q1", "is_correct": False}, ...]
        """
        try:
            if not student_answers:
                return {"weak_points": [], "recommendations": []}
            
            # 获取错题对应的知识点
            wrong_questions = [ans["question_id"] for ans in student_answers if not ans["is_correct"]]
            
            if not wrong_questions:
                return {
                    "weak_points": [],
                    "recommendations": [],
                    "message": "学生答题全部正确，无薄弱知识点"
                }
            
            with neo4j_service.driver.session() as session:
                # 统计错题涉及的知识点
                result = session.run("""
                    MATCH (q:Question)-[r:TESTS]->(kp:KnowledgePoint)
                    WHERE q.id IN $wrong_question_ids
                    RETURN kp.name as knowledge_point,
                           kp.id as kp_id,
                           kp.difficulty as difficulty,
                           count(q) as error_count,
                           sum(r.weight) as total_weight
                    ORDER BY error_count DESC, total_weight DESC
                """, {"wrong_question_ids": wrong_questions})
                
                weak_points = []
                for record in result:
                    weak_points.append({
                        "knowledge_point": record["knowledge_point"],
                        "knowledge_point_id": record["kp_id"],
                        "difficulty": record["difficulty"],
                        "error_count": record["error_count"],
                        "weight_score": record["total_weight"],
                        "weakness_level": self._calculate_weakness_level(
                            record["error_count"], 
                            len(wrong_questions)
                        )
                    })
                
                # 为薄弱知识点生成学习建议
                recommendations = []
                for wp in weak_points[:5]:  # 只为前5个薄弱点生成建议
                    # 找到相关的练习题
                    practice_result = session.run("""
                        MATCH (q:Question)-[:TESTS]->(kp:KnowledgePoint {id: $kp_id})
                        WHERE q.id NOT IN $wrong_question_ids
                        RETURN q.id as question_id, q.content as content, q.difficulty as difficulty
                        ORDER BY q.difficulty
                        LIMIT 5
                    """, {
                        "kp_id": wp["knowledge_point_id"],
                        "wrong_question_ids": wrong_questions
                    })
                    
                    practice_questions = []
                    for q_record in practice_result:
                        practice_questions.append({
                            "question_id": q_record["question_id"],
                            "content": q_record["content"][:100] + "..." if len(q_record["content"]) > 100 else q_record["content"],
                            "difficulty": q_record["difficulty"]
                        })
                    
                    # 找到前置知识点
                    prereq_result = session.run("""
                        MATCH (kp:KnowledgePoint {id: $kp_id})-[:REQUIRES]->(prereq:KnowledgePoint)
                        RETURN prereq.name as prereq_name, prereq.id as prereq_id
                    """, {"kp_id": wp["knowledge_point_id"]})
                    
                    prerequisites = []
                    for prereq_record in prereq_result:
                        prerequisites.append({
                            "name": prereq_record["prereq_name"],
                            "id": prereq_record["prereq_id"]
                        })
                    
                    recommendations.append({
                        "knowledge_point": wp["knowledge_point"],
                        "weakness_level": wp["weakness_level"],
                        "recommended_actions": [
                            "重新学习基础概念",
                            "完成相关练习题",
                            "复习前置知识点" if prerequisites else "加强理解和记忆"
                        ],
                        "practice_questions": practice_questions,
                        "prerequisites": prerequisites
                    })
                
                return {
                    "weak_points": weak_points,
                    "recommendations": recommendations,
                    "total_errors": len(wrong_questions),
                    "total_weak_points": len(weak_points)
                }
        
        except Exception as e:
            logger.error(f"学生薄弱点分析失败: {e}")
            return {"weak_points": [], "recommendations": [], "error": str(e)}
    
    def _calculate_weakness_level(self, error_count: int, total_errors: int) -> str:
        """计算薄弱程度"""
        if total_errors == 0:
            return "无"
        
        ratio = error_count / total_errors
        if ratio >= 0.6:
            return "严重"
        elif ratio >= 0.3:
            return "中等"
        elif ratio >= 0.1:
            return "轻微"
        else:
            return "较轻"
    
    def get_comprehensive_report(self) -> Dict[str, Any]:
        """获取综合分析报告"""
        try:
            # 汇总各种分析结果
            coverage_analysis = self.get_knowledge_coverage_analysis()
            difficulty_distribution = self.get_difficulty_distribution()
            type_distribution = self.get_question_type_distribution()
            hierarchy_analysis = self.get_knowledge_hierarchy_analysis()
            correlation_analysis = self.get_knowledge_correlation_analysis()
            
            return {
                "timestamp": "2024-01-01T00:00:00Z",  # 实际应用中使用当前时间
                "coverage_analysis": coverage_analysis,
                "difficulty_distribution": difficulty_distribution,
                "type_distribution": type_distribution,
                "hierarchy_analysis": hierarchy_analysis,
                "correlation_analysis": correlation_analysis,
                "summary": {
                    "total_knowledge_points": coverage_analysis["summary"].get("total_knowledge_points", 0),
                    "total_questions": difficulty_distribution.get("total_questions", 0),
                    "coverage_rate": coverage_analysis["summary"].get("coverage_rate", 0),
                    "hierarchy_depth": hierarchy_analysis.get("max_depth", 0),
                    "strong_correlations": len(correlation_analysis.get("correlations", [])),
                    "prerequisite_relations": len(correlation_analysis.get("prerequisites", []))
                }
            }
        
        except Exception as e:
            logger.error(f"综合报告生成失败: {e}")
            return {"error": str(e)}


# 全局分析服务实例
analytics_service = AnalyticsService()
