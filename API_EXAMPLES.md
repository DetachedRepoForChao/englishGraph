# 🔌 API使用示例和集成指南

> 完整的API接口使用示例，帮助开发者快速集成K12英语知识图谱系统

## 📋 目录

1. [基础配置](#基础配置)
2. [知识点管理API](#知识点管理api)
3. [智能推荐API](#智能推荐api)
4. [题目管理API](#题目管理api)
5. [数据分析API](#数据分析api)
6. [可视化API](#可视化api)
7. [批量操作示例](#批量操作示例)
8. [错误处理](#错误处理)
9. [SDK集成](#sdk集成)

---

## ⚙️ 基础配置

### API基础信息

```javascript
const API_CONFIG = {
    baseURL: 'https://english-knowledge-graph-h2yu6gw2a-chao-wangs-projects-dfded257.vercel.app/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
};
```

### 通用请求封装

```javascript
class KnowledgeGraphAPI {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }
    
    async request(method, endpoint, data = null, params = null) {
        const url = new URL(endpoint, this.baseURL);
        
        if (params) {
            Object.keys(params).forEach(key => 
                url.searchParams.append(key, params[key])
            );
        }
        
        const options = {
            method: method.toUpperCase(),
            headers: API_CONFIG.headers
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, options);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            throw error;
        }
    }
    
    // GET请求
    async get(endpoint, params = null) {
        return this.request('GET', endpoint, null, params);
    }
    
    // POST请求
    async post(endpoint, data) {
        return this.request('POST', endpoint, data);
    }
    
    // PUT请求
    async put(endpoint, data) {
        return this.request('PUT', endpoint, data);
    }
    
    // DELETE请求
    async delete(endpoint) {
        return this.request('DELETE', endpoint);
    }
}

// 初始化API客户端
const api = new KnowledgeGraphAPI(API_CONFIG.baseURL);
```

---

## 📚 知识点管理API

### 1. 创建知识点

```javascript
async function createKnowledgePoint() {
    const knowledgePoint = {
        name: "一般现在时",
        level: "小学四年级",
        difficulty: "easy",
        description: "描述经常发生的动作或状态的时态",
        keywords: ["present", "simple", "一般现在时", "do", "does", "习惯性动作"]
    };
    
    try {
        const result = await api.post('/knowledge/', knowledgePoint);
        console.log('知识点创建成功:', result);
        // 输出: { id: "kp_123456", message: "知识点创建成功" }
        return result;
    } catch (error) {
        console.error('创建失败:', error);
    }
}
```

### 2. 搜索知识点

```javascript
async function searchKnowledgePoints(keyword = '') {
    try {
        const results = await api.get('/knowledge/search', { keyword });
        console.log(`找到 ${results.total} 个知识点:`, results.results);
        
        // 处理结果
        results.results.forEach(kp => {
            console.log(`- ${kp.name} (${kp.level}, ${kp.difficulty})`);
        });
        
        return results;
    } catch (error) {
        console.error('搜索失败:', error);
    }
}

// 使用示例
searchKnowledgePoints('时态');  // 搜索包含"时态"的知识点
searchKnowledgePoints();        // 获取所有知识点
```

### 3. 获取知识点详情

```javascript
async function getKnowledgePointDetail(kpId) {
    try {
        const kp = await api.get(`/knowledge/${kpId}`);
        console.log('知识点详情:', kp);
        
        // 显示详细信息
        console.log(`名称: ${kp.name}`);
        console.log(`年级: ${kp.level}`);
        console.log(`难度: ${kp.difficulty}`);
        console.log(`关键词: ${kp.keywords.join(', ')}`);
        
        return kp;
    } catch (error) {
        console.error('获取详情失败:', error);
    }
}
```

### 4. 建立层级关系

```javascript
async function createHierarchy(parentId, childId) {
    try {
        const result = await api.post(`/knowledge/${parentId}/children/${childId}`);
        console.log('层级关系创建成功:', result);
        return result;
    } catch (error) {
        console.error('创建层级关系失败:', error);
    }
}

// 示例：建立"英语语法" -> "动词时态"的层级关系
createHierarchy('kp_115430', 'kp_573225');
```

### 5. 获取完整层级结构

```javascript
async function getHierarchyTree() {
    try {
        const hierarchy = await api.get('/knowledge/hierarchy/tree');
        console.log('层级结构统计:', hierarchy.stats);
        console.log('树形结构:', hierarchy.tree_structure);
        
        // 递归显示树形结构
        function displayTree(nodes, indent = 0) {
            nodes.forEach(node => {
                console.log('  '.repeat(indent) + `- ${node.name} (L${node.level})`);
                if (node.children && node.children.length > 0) {
                    displayTree(node.children, indent + 1);
                }
            });
        }
        
        displayTree(hierarchy.tree_structure);
        return hierarchy;
    } catch (error) {
        console.error('获取层级结构失败:', error);
    }
}
```

---

## 🤖 智能推荐API

### 1. AI基础推荐

```javascript
async function getAISuggestions(questionContent) {
    const request = {
        question_content: questionContent
    };
    
    try {
        const result = await api.post('/annotation/suggest', request);
        console.log('AI推荐结果:', result.suggestions);
        
        // 显示推荐详情
        result.suggestions.forEach((suggestion, index) => {
            console.log(`推荐 ${index + 1}:`);
            console.log(`  知识点: ${suggestion.knowledge_point_name}`);
            console.log(`  置信度: ${(suggestion.confidence * 100).toFixed(1)}%`);
            console.log(`  推荐理由: ${suggestion.reason}`);
            
            if (suggestion.matched_keywords) {
                console.log(`  匹配关键词: ${suggestion.matched_keywords.join(', ')}`);
            }
            
            if (suggestion.feature_analysis) {
                console.log('  特征分析:');
                Object.entries(suggestion.feature_analysis).forEach(([feature, info]) => {
                    console.log(`    ${feature}: ${info.words.join(', ')} (${(info.score * 100).toFixed(1)}%)`);
                });
            }
        });
        
        return result;
    } catch (error) {
        console.error('AI推荐失败:', error);
    }
}

// 使用示例
const question = "Look! The children _____ in the playground. A) play B) plays C) are playing D) played";
getAISuggestions(question);
```

### 2. 协作智能推荐

```javascript
async function getCollaborativeSuggestions(questionContent) {
    const request = {
        question_content: questionContent
    };
    
    try {
        const result = await api.post('/annotation/collaborative-suggest', request);
        console.log('协作推荐结果:', result.suggestions);
        
        // 显示协作推荐的详细信息
        result.suggestions.forEach((suggestion, index) => {
            console.log(`协作推荐 ${index + 1}:`);
            console.log(`  知识点: ${suggestion.knowledge_point_name}`);
            console.log(`  综合置信度: ${(suggestion.confidence * 100).toFixed(1)}%`);
            console.log(`  AI Agent评分: ${(suggestion.ai_score * 100).toFixed(1)}%`);
            console.log(`  LabelLLM评分: ${(suggestion.labelllm_score * 100).toFixed(1)}%`);
            console.log(`  MEGAnno评分: ${(suggestion.meganno_score * 100).toFixed(1)}%`);
            console.log(`  协作推理: ${suggestion.reasoning}`);
            
            if (suggestion.isCollaborative) {
                console.log('  ✅ 多模型一致推荐');
            }
        });
        
        return result;
    } catch (error) {
        console.error('协作推荐失败:', error);
    }
}
```

### 3. 批量推荐处理

```javascript
async function batchProcessQuestions(questions) {
    const results = [];
    
    for (let i = 0; i < questions.length; i++) {
        const question = questions[i];
        console.log(`处理题目 ${i + 1}/${questions.length}: ${question.substring(0, 50)}...`);
        
        try {
            const suggestion = await getAISuggestions(question);
            results.push({
                question: question,
                suggestions: suggestion.suggestions,
                processed_at: new Date().toISOString()
            });
            
            // 添加延迟避免API限流
            if (i < questions.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        } catch (error) {
            console.error(`处理题目 ${i + 1} 失败:`, error);
            results.push({
                question: question,
                error: error.message,
                processed_at: new Date().toISOString()
            });
        }
    }
    
    return results;
}
```

---

## 📝 题目管理API

### 1. 获取题目列表

```javascript
async function getQuestions(options = {}) {
    const params = {
        page: options.page || 1,
        page_size: options.pageSize || 20,
        difficulty: options.difficulty,
        question_type: options.questionType,
        grade_level: options.gradeLevel,
        source: options.source
    };
    
    // 移除undefined的参数
    Object.keys(params).forEach(key => {
        if (params[key] === undefined) {
            delete params[key];
        }
    });
    
    try {
        const result = await api.get('/questions/', params);
        console.log(`获取到 ${result.questions.length} 道题目 (共 ${result.pagination.total_count} 道)`);
        
        // 显示题目信息
        result.questions.forEach((q, index) => {
            console.log(`${index + 1}. ${q.content}`);
            if (q.options && q.options.length > 0) {
                q.options.forEach((option, i) => {
                    const letter = String.fromCharCode(65 + i);
                    console.log(`   ${letter}) ${option}`);
                });
            }
            console.log(`   答案: ${q.answer}`);
            console.log(`   难度: ${q.difficulty} | 知识点: ${q.knowledge_points.join(', ')}`);
            console.log('');
        });
        
        return result;
    } catch (error) {
        console.error('获取题目失败:', error);
    }
}

// 使用示例
getQuestions({ difficulty: 'easy', page: 1, pageSize: 10 });
getQuestions({ questionType: 'multiple_choice', gradeLevel: '小学四年级' });
```

### 2. 分页浏览题目

```javascript
class QuestionBrowser {
    constructor() {
        this.currentPage = 1;
        this.pageSize = 20;
        this.totalPages = 0;
        this.filters = {};
    }
    
    async loadPage(page = 1) {
        this.currentPage = page;
        const options = {
            page: this.currentPage,
            pageSize: this.pageSize,
            ...this.filters
        };
        
        const result = await getQuestions(options);
        if (result) {
            this.totalPages = result.pagination.total_pages;
            console.log(`第 ${this.currentPage} 页，共 ${this.totalPages} 页`);
        }
        return result;
    }
    
    async nextPage() {
        if (this.currentPage < this.totalPages) {
            return await this.loadPage(this.currentPage + 1);
        } else {
            console.log('已是最后一页');
            return null;
        }
    }
    
    async prevPage() {
        if (this.currentPage > 1) {
            return await this.loadPage(this.currentPage - 1);
        } else {
            console.log('已是第一页');
            return null;
        }
    }
    
    setFilters(filters) {
        this.filters = filters;
        this.currentPage = 1;  // 重置到第一页
    }
}

// 使用示例
const browser = new QuestionBrowser();
browser.setFilters({ difficulty: 'easy' });
browser.loadPage(1);
browser.nextPage();
```

---

## 📊 数据分析API

### 1. 获取仪表板统计

```javascript
async function getDashboardStats() {
    try {
        const stats = await api.get('/analytics/dashboard-stats');
        console.log('系统统计数据:');
        console.log(`总题目数: ${stats.total_questions}`);
        console.log(`总知识点数: ${stats.total_knowledge_points}`);
        console.log(`已标注题目: ${stats.annotated_questions}`);
        console.log(`标注完成率: ${(stats.annotation_rate * 100).toFixed(1)}%`);
        console.log(`AI平均置信度: ${(stats.avg_ai_confidence * 100).toFixed(1)}%`);
        
        return stats;
    } catch (error) {
        console.error('获取统计数据失败:', error);
    }
}
```

### 2. AI准确率分析

```javascript
async function getAIAccuracyAnalysis(options = {}) {
    const params = {
        page: options.page || 1,
        page_size: options.pageSize || 10,
        difficulty: options.difficulty,
        question_type: options.questionType
    };
    
    // 移除undefined参数
    Object.keys(params).forEach(key => {
        if (params[key] === undefined) {
            delete params[key];
        }
    });
    
    try {
        const result = await api.get('/analytics/ai-agent-accuracy', params);
        console.log('AI准确率分析:');
        console.log(`整体准确率: ${(result.summary.overall_accuracy * 100).toFixed(1)}%`);
        console.log(`高置信度准确率: ${(result.summary.high_confidence_accuracy * 100).toFixed(1)}%`);
        console.log(`低置信度准确率: ${(result.summary.low_confidence_accuracy * 100).toFixed(1)}%`);
        
        // 显示具体分析数据
        result.analysis.forEach((item, index) => {
            console.log(`\n分析 ${index + 1}:`);
            console.log(`题目: ${item.question_content.substring(0, 50)}...`);
            console.log(`AI推荐: ${item.ai_suggestions.join(', ')}`);
            console.log(`用户确认: ${item.user_confirmed.join(', ')}`);
            console.log(`准确率: ${(item.accuracy * 100).toFixed(1)}%`);
            console.log(`置信度: ${(item.confidence * 100).toFixed(1)}%`);
        });
        
        return result;
    } catch (error) {
        console.error('获取准确率分析失败:', error);
    }
}
```

### 3. 知识点覆盖分析

```javascript
async function getKnowledgeCoverageAnalysis() {
    try {
        const result = await api.get('/analytics/knowledge-coverage');
        console.log('知识点覆盖分析:');
        
        // 按题目数量排序
        const sortedCoverage = result.coverage.sort((a, b) => b.question_count - a.question_count);
        
        console.log('\n题目数量排名:');
        sortedCoverage.slice(0, 10).forEach((item, index) => {
            console.log(`${index + 1}. ${item.knowledge_point}: ${item.question_count}道题目`);
        });
        
        // 找出覆盖不足的知识点
        const lowCoverage = sortedCoverage.filter(item => item.question_count < 3);
        if (lowCoverage.length > 0) {
            console.log('\n⚠️ 题目覆盖不足的知识点:');
            lowCoverage.forEach(item => {
                console.log(`- ${item.knowledge_point}: 仅${item.question_count}道题目`);
            });
        }
        
        return result;
    } catch (error) {
        console.error('获取覆盖分析失败:', error);
    }
}
```

---

## 🎨 可视化API

### 1. 获取层级结构可视化数据

```javascript
async function getVisualizationData() {
    try {
        const data = await api.get('/knowledge/hierarchy/visualization');
        console.log('可视化数据统计:');
        console.log(`节点数: ${data.metadata.total_nodes}`);
        console.log(`边数: ${data.metadata.total_edges}`);
        console.log(`分组: ${data.metadata.groups.join(', ')}`);
        
        // 分析节点分布
        const groupCounts = {};
        data.nodes.forEach(node => {
            groupCounts[node.group] = (groupCounts[node.group] || 0) + 1;
        });
        
        console.log('\n各分组节点数量:');
        Object.entries(groupCounts).forEach(([group, count]) => {
            console.log(`- ${group}: ${count}个节点`);
        });
        
        // 分析难度分布
        const difficultyCounts = {};
        data.nodes.forEach(node => {
            difficultyCounts[node.difficulty] = (difficultyCounts[node.difficulty] || 0) + 1;
        });
        
        console.log('\n难度分布:');
        Object.entries(difficultyCounts).forEach(([difficulty, count]) => {
            console.log(`- ${difficulty}: ${count}个节点`);
        });
        
        return data;
    } catch (error) {
        console.error('获取可视化数据失败:', error);
    }
}
```

### 2. 生成网络图数据

```javascript
function generateNetworkGraph(visualizationData) {
    // 转换为网络图库(如vis.js, d3.js等)可用的格式
    const networkData = {
        nodes: visualizationData.nodes.map(node => ({
            id: node.id,
            label: node.label,
            color: node.color,
            group: node.group,
            title: `${node.label}\n难度: ${node.difficulty}\n分组: ${node.group}`,
            shape: 'dot',
            size: 20
        })),
        edges: visualizationData.edges.map(edge => ({
            from: edge.from,
            to: edge.to,
            label: edge.label,
            arrows: edge.arrows,
            color: { color: '#848484' },
            width: 2
        }))
    };
    
    console.log('网络图数据已生成');
    return networkData;
}
```

---

## 🔄 批量操作示例

### 1. 批量导入知识点

```javascript
async function batchImportKnowledgePoints(knowledgePointsData) {
    const results = {
        success: [],
        failed: []
    };
    
    console.log(`开始批量导入 ${knowledgePointsData.length} 个知识点...`);
    
    for (let i = 0; i < knowledgePointsData.length; i++) {
        const kp = knowledgePointsData[i];
        console.log(`导入进度: ${i + 1}/${knowledgePointsData.length} - ${kp.name}`);
        
        try {
            const result = await api.post('/knowledge/', kp);
            results.success.push({
                name: kp.name,
                id: result.id
            });
            
            // 添加延迟避免API限流
            await new Promise(resolve => setTimeout(resolve, 500));
        } catch (error) {
            results.failed.push({
                name: kp.name,
                error: error.message
            });
        }
    }
    
    console.log(`\n导入完成! 成功: ${results.success.length}, 失败: ${results.failed.length}`);
    
    if (results.failed.length > 0) {
        console.log('\n失败的知识点:');
        results.failed.forEach(item => {
            console.log(`- ${item.name}: ${item.error}`);
        });
    }
    
    return results;
}

// 示例数据
const sampleKnowledgePoints = [
    {
        name: "一般将来时",
        level: "小学六年级",
        difficulty: "medium",
        description: "表示将来某个时间要发生的动作或状态",
        keywords: ["will", "be going to", "future", "tomorrow", "next"]
    },
    {
        name: "现在完成进行时",
        level: "初中二年级", 
        difficulty: "hard",
        description: "表示从过去某时开始一直持续到现在的动作",
        keywords: ["have been", "has been", "doing", "continuous"]
    }
];

// batchImportKnowledgePoints(sampleKnowledgePoints);
```

### 2. 批量建立层级关系

```javascript
async function batchCreateHierarchy(hierarchyData) {
    const results = {
        success: [],
        failed: []
    };
    
    console.log(`开始批量创建 ${hierarchyData.length} 个层级关系...`);
    
    for (let i = 0; i < hierarchyData.length; i++) {
        const relation = hierarchyData[i];
        console.log(`创建关系 ${i + 1}/${hierarchyData.length}: ${relation.parent} -> ${relation.child}`);
        
        try {
            await api.post(`/knowledge/${relation.parentId}/children/${relation.childId}`);
            results.success.push(relation);
            
            // 添加延迟
            await new Promise(resolve => setTimeout(resolve, 300));
        } catch (error) {
            results.failed.push({
                ...relation,
                error: error.message
            });
        }
    }
    
    console.log(`\n创建完成! 成功: ${results.success.length}, 失败: ${results.failed.length}`);
    return results;
}
```

---

## ⚠️ 错误处理

### 1. 常见错误类型

```javascript
class APIError extends Error {
    constructor(message, status, code) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.code = code;
    }
}

function handleAPIError(error) {
    if (error instanceof APIError) {
        switch (error.status) {
            case 400:
                console.error('请求参数错误:', error.message);
                break;
            case 401:
                console.error('未授权访问:', error.message);
                break;
            case 403:
                console.error('禁止访问:', error.message);
                break;
            case 404:
                console.error('资源不存在:', error.message);
                break;
            case 429:
                console.error('请求过于频繁:', error.message);
                // 可以实现重试机制
                break;
            case 500:
                console.error('服务器内部错误:', error.message);
                break;
            default:
                console.error('未知错误:', error.message);
        }
    } else {
        console.error('网络错误:', error.message);
    }
}
```

### 2. 重试机制

```javascript
async function requestWithRetry(requestFunc, maxRetries = 3, delay = 1000) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await requestFunc();
        } catch (error) {
            console.log(`请求失败 (第${attempt}次尝试):`, error.message);
            
            if (attempt === maxRetries) {
                throw error;
            }
            
            // 指数退避延迟
            const backoffDelay = delay * Math.pow(2, attempt - 1);
            console.log(`等待 ${backoffDelay}ms 后重试...`);
            await new Promise(resolve => setTimeout(resolve, backoffDelay));
        }
    }
}

// 使用示例
async function robustGetKnowledgePoints() {
    return await requestWithRetry(async () => {
        return await api.get('/knowledge/search');
    }, 3, 1000);
}
```

---

## 📦 SDK集成

### 1. JavaScript SDK

```javascript
class EnglishKnowledgeGraphSDK {
    constructor(baseURL, options = {}) {
        this.api = new KnowledgeGraphAPI(baseURL);
        this.options = {
            timeout: 30000,
            retries: 3,
            ...options
        };
    }
    
    // 知识点管理
    async createKnowledgePoint(data) {
        return await this.api.post('/knowledge/', data);
    }
    
    async searchKnowledgePoints(keyword = '') {
        return await this.api.get('/knowledge/search', { keyword });
    }
    
    async getHierarchy() {
        return await this.api.get('/knowledge/hierarchy/tree');
    }
    
    // AI推荐
    async getSuggestions(questionContent, collaborative = false) {
        const endpoint = collaborative ? 
            '/annotation/collaborative-suggest' : 
            '/annotation/suggest';
        return await this.api.post(endpoint, { question_content: questionContent });
    }
    
    // 数据分析
    async getDashboardStats() {
        return await this.api.get('/analytics/dashboard-stats');
    }
    
    async getAccuracyAnalysis(options = {}) {
        return await this.api.get('/analytics/ai-agent-accuracy', options);
    }
    
    // 可视化
    async getVisualizationData() {
        return await this.api.get('/knowledge/hierarchy/visualization');
    }
    
    // 题目管理
    async getQuestions(options = {}) {
        return await this.api.get('/questions/', options);
    }
}

// 使用SDK
const sdk = new EnglishKnowledgeGraphSDK(API_CONFIG.baseURL);

// 简化的API调用
const suggestions = await sdk.getSuggestions("Look! The children _____ in the playground.");
const hierarchy = await sdk.getHierarchy();
const stats = await sdk.getDashboardStats();
```

### 2. Python SDK

```python
import requests
import json
from typing import Optional, Dict, List, Any

class EnglishKnowledgeGraphSDK:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _request(self, method: str, endpoint: str, 
                 data: Optional[Dict] = None, 
                 params: Optional[Dict] = None) -> Dict[str, Any]:
        """统一的请求方法"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API请求失败: {e}")
            raise
    
    # 知识点管理
    def create_knowledge_point(self, knowledge_point: Dict[str, Any]) -> Dict[str, Any]:
        """创建知识点"""
        return self._request('POST', '/api/knowledge/', data=knowledge_point)
    
    def search_knowledge_points(self, keyword: str = '') -> Dict[str, Any]:
        """搜索知识点"""
        return self._request('GET', '/api/knowledge/search', params={'keyword': keyword})
    
    def get_hierarchy(self) -> Dict[str, Any]:
        """获取知识点层级结构"""
        return self._request('GET', '/api/knowledge/hierarchy/tree')
    
    # AI推荐
    def get_suggestions(self, question_content: str, collaborative: bool = False) -> Dict[str, Any]:
        """获取AI推荐"""
        endpoint = '/api/annotation/collaborative-suggest' if collaborative else '/api/annotation/suggest'
        return self._request('POST', endpoint, data={'question_content': question_content})
    
    # 数据分析
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """获取仪表板统计"""
        return self._request('GET', '/api/analytics/dashboard-stats')
    
    # 可视化
    def get_visualization_data(self) -> Dict[str, Any]:
        """获取可视化数据"""
        return self._request('GET', '/api/knowledge/hierarchy/visualization')

# 使用示例
if __name__ == "__main__":
    sdk = EnglishKnowledgeGraphSDK('https://your-api-url.vercel.app')
    
    # 获取AI推荐
    question = "Look! The children _____ in the playground."
    suggestions = sdk.get_suggestions(question)
    print(f"AI推荐结果: {suggestions}")
    
    # 获取系统统计
    stats = sdk.get_dashboard_stats()
    print(f"系统统计: {stats}")
```

---

## 📝 使用最佳实践

### 1. API调用频率控制

```javascript
class RateLimiter {
    constructor(maxRequests = 60, timeWindow = 60000) { // 每分钟最多60次请求
        this.maxRequests = maxRequests;
        this.timeWindow = timeWindow;
        this.requests = [];
    }
    
    async waitForPermission() {
        const now = Date.now();
        
        // 清理过期的请求记录
        this.requests = this.requests.filter(time => now - time < this.timeWindow);
        
        if (this.requests.length >= this.maxRequests) {
            const oldestRequest = Math.min(...this.requests);
            const waitTime = this.timeWindow - (now - oldestRequest);
            console.log(`API限流: 等待 ${waitTime}ms`);
            await new Promise(resolve => setTimeout(resolve, waitTime));
        }
        
        this.requests.push(now);
    }
}

const rateLimiter = new RateLimiter();

// 在API调用前使用
async function callAPIWithRateLimit(apiCall) {
    await rateLimiter.waitForPermission();
    return await apiCall();
}
```

### 2. 数据缓存策略

```javascript
class APICache {
    constructor(ttl = 300000) { // 默认5分钟过期
        this.cache = new Map();
        this.ttl = ttl;
    }
    
    set(key, value) {
        this.cache.set(key, {
            value,
            timestamp: Date.now()
        });
    }
    
    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;
        
        if (Date.now() - item.timestamp > this.ttl) {
            this.cache.delete(key);
            return null;
        }
        
        return item.value;
    }
    
    clear() {
        this.cache.clear();
    }
}

const cache = new APICache();

// 带缓存的API调用
async function getCachedKnowledgePoints() {
    const cacheKey = 'knowledge_points_all';
    let result = cache.get(cacheKey);
    
    if (!result) {
        console.log('缓存未命中，从API获取数据');
        result = await api.get('/knowledge/search');
        cache.set(cacheKey, result);
    } else {
        console.log('使用缓存数据');
    }
    
    return result;
}
```

### 3. 错误监控和日志

```javascript
class APILogger {
    constructor() {
        this.logs = [];
    }
    
    log(level, message, data = null) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            level,
            message,
            data
        };
        
        this.logs.push(logEntry);
        console.log(`[${level.toUpperCase()}] ${message}`, data || '');
        
        // 可以发送到远程日志服务
        this.sendToLogService(logEntry);
    }
    
    info(message, data) {
        this.log('info', message, data);
    }
    
    error(message, data) {
        this.log('error', message, data);
    }
    
    warn(message, data) {
        this.log('warn', message, data);
    }
    
    sendToLogService(logEntry) {
        // 实现发送到远程日志服务的逻辑
        // 例如发送到 LogRocket, Sentry 等
    }
    
    getLogs(level = null) {
        if (level) {
            return this.logs.filter(log => log.level === level);
        }
        return this.logs;
    }
}

const logger = new APILogger();

// 在API调用中使用日志
async function loggedAPICall(apiCall, description) {
    logger.info(`开始API调用: ${description}`);
    
    try {
        const result = await apiCall();
        logger.info(`API调用成功: ${description}`, { result });
        return result;
    } catch (error) {
        logger.error(`API调用失败: ${description}`, { error: error.message });
        throw error;
    }
}
```

---

**🎯 这份API使用示例文档提供了完整的集成指南，帮助开发者快速上手K12英语知识图谱系统的所有功能！**
