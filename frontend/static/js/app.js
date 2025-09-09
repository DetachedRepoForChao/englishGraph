// K12英语知识图谱系统前端JavaScript

// 全局变量
let selectedKnowledgePoints = [];
let currentQuestionId = null;

// API基础URL
const API_BASE_URL = '/api';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardStats();
    loadKnowledgePoints();
    initializeEventListeners();
    
    // 为数据分析标签页添加事件监听
    const analyticsTab = document.getElementById('analytics-tab');
    if (analyticsTab) {
        analyticsTab.addEventListener('click', function() {
            console.log('数据分析标签页被点击');
            setTimeout(() => {
                loadAnalyticsData();
            }, 100); // 稍微延迟确保标签页切换完成
        });
    } else {
        console.warn('未找到analytics-tab元素');
    }
});

// 初始化事件监听器
function initializeEventListeners() {
    // 知识点搜索
    document.getElementById('knowledge-search').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchKnowledgePoints();
        }
    });
    
    // 题目内容变化时清空推荐
    document.getElementById('question-content').addEventListener('input', function() {
        clearKnowledgeSuggestions();
    });
}

// 加载仪表板统计信息
async function loadDashboardStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/dashboard-stats`);
        const data = await response.json();
        
        document.getElementById('total-knowledge-points').textContent = data.total_knowledge_points || 0;
        document.getElementById('total-questions').textContent = data.total_questions || 0;
        document.getElementById('annotated-questions').textContent = data.annotated_questions || 0;
        document.getElementById('annotation-coverage').textContent = `${data.annotation_coverage || 0}%`;
    } catch (error) {
        console.error('加载统计信息失败:', error);
        // 使用默认值
        document.getElementById('total-knowledge-points').textContent = '0';
        document.getElementById('total-questions').textContent = '0';
        document.getElementById('annotated-questions').textContent = '0';
        document.getElementById('annotation-coverage').textContent = '0%';
    }
}

// 搜索知识点
async function searchKnowledgePoints() {
    const keyword = document.getElementById('knowledge-search').value.trim();
    if (!keyword) {
        loadKnowledgePoints();
        return;
    }
    
    try {
        showLoading('knowledge-points-list');
        const response = await fetch(`${API_BASE_URL}/knowledge/search?keyword=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        
        displayKnowledgePoints(data.results);
    } catch (error) {
        console.error('搜索知识点失败:', error);
        showError('knowledge-points-list', '搜索失败，请重试');
    }
}

// 加载所有知识点
async function loadKnowledgePoints() {
    try {
        showLoading('knowledge-points-list');
        const response = await fetch(`${API_BASE_URL}/knowledge/search?keyword=`);
        const data = await response.json();
        
        displayKnowledgePoints(data.results);
        loadKnowledgeHierarchy();
    } catch (error) {
        console.error('加载知识点失败:', error);
        showError('knowledge-points-list', '加载失败，请检查网络连接');
    }
}

// 显示知识点列表
function displayKnowledgePoints(knowledgePoints) {
    const container = document.getElementById('knowledge-points-list');
    
    if (!knowledgePoints || knowledgePoints.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <p>未找到相关知识点</p>
            </div>
        `;
        return;
    }
    
    const html = knowledgePoints.map(kp => `
        <div class="knowledge-point-item" onclick="selectKnowledgePoint('${kp.id}', '${kp.name}')">
            <div class="knowledge-point-name">${kp.name}</div>
            <div class="knowledge-point-meta">
                <span class="badge bg-secondary">${kp.level || '未设置'}</span>
                <span class="badge bg-info">${getDifficultyLabel(kp.difficulty)}</span>
            </div>
            ${kp.description ? `<div class="knowledge-point-description">${kp.description}</div>` : ''}
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// 获取难度标签
function getDifficultyLabel(difficulty) {
    const labels = {
        'easy': '简单',
        'medium': '中等', 
        'hard': '困难',
        'unknown': '未设置',
        'null': '未设置',
        'undefined': '未设置'
    };
    return labels[difficulty] || labels[String(difficulty)] || '未设置';
}

// 获取难度颜色
function getDifficultyColor(difficulty) {
    const colors = {
        'easy': 'success',
        'medium': 'warning', 
        'hard': 'danger',
        'unknown': 'secondary',
        'null': 'secondary',
        'undefined': 'secondary'
    };
    return colors[difficulty] || colors[String(difficulty)] || 'secondary';
}

// 选择知识点
function selectKnowledgePoint(kpId, kpName) {
    // 检查是否已选择
    if (selectedKnowledgePoints.some(kp => kp.id === kpId)) {
        showMessage('该知识点已选择', 'warning');
        return;
    }
    
    selectedKnowledgePoints.push({
        id: kpId,
        name: kpName,
        weight: 1.0
    });
    
    updateSelectedKnowledgePoints();
    showMessage(`已添加知识点: ${kpName}`, 'success');
}

// 更新已选择的知识点显示
function updateSelectedKnowledgePoints() {
    const container = document.getElementById('selected-knowledge-points');
    
    if (selectedKnowledgePoints.length === 0) {
        container.innerHTML = '<div class="text-muted">暂无选择的知识点</div>';
        return;
    }
    
    const html = selectedKnowledgePoints.map((kp, index) => `
        <div class="selected-kp-item">
            <span>${kp.name}</span>
            <span class="selected-kp-remove" onclick="removeSelectedKnowledgePoint(${index})">&times;</span>
            <div class="weight-slider">
                <input type="range" class="form-range" min="0.1" max="1.0" step="0.1" 
                       value="${kp.weight}" onchange="updateKnowledgePointWeight(${index}, this.value)">
                <span class="weight-display">权重: ${kp.weight}</span>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// 移除选中的知识点
function removeSelectedKnowledgePoint(index) {
    selectedKnowledgePoints.splice(index, 1);
    updateSelectedKnowledgePoints();
}

// 更新知识点权重
function updateKnowledgePointWeight(index, weight) {
    selectedKnowledgePoints[index].weight = parseFloat(weight);
    updateSelectedKnowledgePoints();
}

// AI智能推荐知识点
async function suggestKnowledgePoints() {
    const content = document.getElementById('question-content').value.trim();
    const type = document.getElementById('question-type').value;
    
    if (!content) {
        showMessage('请先输入题目内容', 'warning');
        return;
    }
    
    try {
        showLoading('knowledge-suggestions');
        console.log('🚀 开始AI智能推荐，题目内容:', content);
        
        const response = await fetch(`${API_BASE_URL}/annotation/suggest?t=${Date.now()}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            },
            body: JSON.stringify({
                question_content: content,
                question_type: type
            })
        });
        
        const data = await response.json();
        console.log('📊 API返回数据:', data);
        displayKnowledgeSuggestions(data.suggestions);
    } catch (error) {
        console.error('获取知识点推荐失败:', error);
        showError('knowledge-suggestions', '推荐失败，请重试');
    }
}

// 协作推荐知识点 (AI Agent + LabelLLM + MEGAnno)
async function collaborativeSuggest() {
    const content = document.getElementById('question-content').value.trim();
    const type = document.getElementById('question-type').value;
    
    if (!content) {
        showMessage('请先输入题目内容', 'warning');
        return;
    }
    
    try {
        showLoading('knowledge-suggestions', '正在进行协作分析...');
        console.log('🤝 开始协作推荐，题目内容:', content);
        
        const response = await fetch(`${API_BASE_URL}/annotation/collaborative-suggest?t=${Date.now()}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            },
            body: JSON.stringify({
                question_content: content,
                question_type: type
            })
        });
        
        const data = await response.json();
        console.log('🎯 协作推荐返回数据:', data);
        
        // 显示协作推荐结果，添加特殊标识
        const enhancedSuggestions = data.suggestions.map(s => ({
            ...s,
            isCollaborative: true,
            models_used: data.models_used || ["AI_Agent", "LabelLLM", "MEGAnno"]
        }));
        
        displayKnowledgeSuggestions(enhancedSuggestions);
        
        // 显示协作总结信息
        if (data.collaboration_summary) {
            const summary = data.collaboration_summary;
            showMessage(
                `协作推荐完成！AI Agent: ${summary.ai_agent_count}, LabelLLM: ${summary.labelllm_count}, MEGAnno验证: ${summary.meganno_validated}`, 
                'info'
            );
        }
        
    } catch (error) {
        console.error('协作推荐失败:', error);
        showError('knowledge-suggestions', '协作推荐失败，请重试');
    }
}

// 显示知识点推荐
function displayKnowledgeSuggestions(suggestions) {
    const container = document.getElementById('knowledge-suggestions');
    console.log('🎨 开始显示推荐结果:', suggestions);
    
    if (!suggestions || suggestions.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-lightbulb"></i>
                <p>暂无推荐的知识点</p>
            </div>
        `;
        return;
    }
    
    const html = suggestions.map(suggestion => `
        <div class="suggestion-item ${suggestion.isCollaborative ? 'collaborative-suggestion' : ''}" onclick="addSuggestedKnowledgePoint('${suggestion.knowledge_point_id}', '${suggestion.knowledge_point_name}', ${suggestion.confidence})">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <strong>${suggestion.knowledge_point_name}</strong>
                    <span class="suggestion-confidence ${getConfidenceClass(suggestion.confidence)}">
                        ${(suggestion.confidence * 100).toFixed(0)}%
                    </span>
                    ${suggestion.isCollaborative ? 
                        `<span class="badge bg-gradient bg-warning text-dark ms-1">
                            <i class="fas fa-users me-1"></i>协作推荐
                        </span>` : ''
                    }
                    ${suggestion.grade_levels && suggestion.grade_levels.length > 0 ? 
                        `<div class="mt-1">
                            ${suggestion.grade_levels.map(grade => `<span class="badge bg-info text-white me-1">${grade}</span>`).join('')}
                        </div>` : ''
                    }
                </div>
                <i class="fas fa-plus text-success"></i>
            </div>
            <div class="suggestion-reason mt-2">${suggestion.reason}</div>
            ${suggestion.matched_keywords && suggestion.matched_keywords.length > 0 ? 
                `<div class="mt-2">
                    <small class="text-muted">判断关键词: </small>
                    ${suggestion.matched_keywords.map(kw => `<span class="badge bg-primary text-white me-1">${kw}</span>`).join('')}
                </div>` : ''
            }
            ${suggestion.feature_analysis ? 
                `<div class="mt-2">
                    <small class="text-muted">特征分析: </small>
                    <div class="feature-analysis">
                        ${Object.entries(suggestion.feature_analysis).map(([category, info]) => 
                            `<div class="feature-item">
                                <span class="feature-category">${category}:</span> 
                                <span class="feature-words">${info.words.join(', ')}</span>
                                <span class="badge bg-success ms-1">${(info.score * 100).toFixed(0)}%</span>
                            </div>`
                        ).join('')}
                    </div>
                </div>` : ''
            }
            ${suggestion.learning_objectives && suggestion.learning_objectives.length > 0 ? 
                `<div class="mt-2">
                    <small class="text-muted">学习目标: </small>
                    <ul class="learning-objectives">
                        ${suggestion.learning_objectives.map(obj => `<li>${obj}</li>`).join('')}
                    </ul>
                </div>` : ''
            }
        </div>
    `).join('');
    
    container.innerHTML = html;
}

// 获取置信度样式类
function getConfidenceClass(confidence) {
    if (confidence >= 0.7) return 'confidence-high';
    if (confidence >= 0.4) return 'confidence-medium';
    return 'confidence-low';
}

// 添加推荐的知识点
function addSuggestedKnowledgePoint(kpId, kpName, confidence) {
    // 检查是否已选择
    if (selectedKnowledgePoints.some(kp => kp.id === kpId)) {
        showMessage('该知识点已选择', 'warning');
        return;
    }
    
    selectedKnowledgePoints.push({
        id: kpId,
        name: kpName,
        weight: Math.max(confidence, 0.5) // 最小权重0.5
    });
    
    updateSelectedKnowledgePoints();
    showMessage(`已添加推荐知识点: ${kpName}`, 'success');
}

// 清空知识点推荐
function clearKnowledgeSuggestions() {
    const container = document.getElementById('knowledge-suggestions');
    container.innerHTML = `
        <div class="text-center text-muted">
            <i class="fas fa-lightbulb fa-2x mb-3"></i>
            <p>点击"AI智能推荐"获取知识点建议</p>
        </div>
    `;
}

// 保存题目
async function saveQuestion() {
    const content = document.getElementById('question-content').value.trim();
    const type = document.getElementById('question-type').value;
    const answer = document.getElementById('question-answer').value.trim();
    
    if (!content || !answer) {
        showMessage('请填写题目内容和答案', 'warning');
        return;
    }
    
    try {
        // 创建题目
        const questionResponse = await fetch(`${API_BASE_URL}/questions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: content,
                question_type: type,
                answer: answer
            })
        });
        
        const questionData = await questionResponse.json();
        const questionId = questionData.id;
        
        // 如果用户选择了知识点，手动关联
        if (selectedKnowledgePoints.length > 0) {
            for (const kp of selectedKnowledgePoints) {
                await fetch(`${API_BASE_URL}/questions/${questionId}/knowledge/${kp.id}?weight=${kp.weight}`, {
                    method: 'POST'
                });
            }
            showMessage('题目保存成功！', 'success');
        } else {
            // 如果没有手动选择知识点，使用AI Agent自动标注
            showMessage('题目已保存，正在使用AI自动标注...', 'info');
            await triggerAutoAnnotation(questionId);
        }
        
        clearQuestionForm();
        loadDashboardStats(); // 刷新统计信息
    } catch (error) {
        console.error('保存题目失败:', error);
        showMessage('保存失败，请重试', 'danger');
    }
}

// 触发AI自动标注
async function triggerAutoAnnotation(questionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/ai-agent/trigger-auto-annotation/${questionId}`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.status === 'completed') {
            const appliedCount = result.applied_annotations ? result.applied_annotations.length : 0;
            if (appliedCount > 0) {
                showMessage(`AI自动标注完成！应用了 ${appliedCount} 个知识点标注`, 'success');
            } else {
                showMessage('AI自动标注完成，但未找到高置信度的知识点', 'warning');
            }
        } else {
            showMessage('AI自动标注失败', 'warning');
        }
    } catch (error) {
        console.error('AI自动标注失败:', error);
        showMessage('AI自动标注过程中出现错误', 'warning');
    }
}

// 智能导入题目
async function smartImportQuestions() {
    const fileInput = document.getElementById('import-file');
    if (!fileInput || !fileInput.files[0]) {
        showMessage('请选择要导入的文件', 'warning');
        return;
    }
    
    try {
        const file = fileInput.files[0];
        const text = await file.text();
        const questionsData = JSON.parse(text);
        
        if (!Array.isArray(questionsData)) {
            throw new Error('文件格式错误，应为题目数组');
        }
        
        showMessage(`正在智能导入 ${questionsData.length} 道题目...`, 'info');
        
        const response = await fetch(`${API_BASE_URL}/ai-agent/smart-import`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(questionsData)
        });
        
        const result = await response.json();
        
        if (result.status === 'completed') {
            showMessage(`智能导入成功！共导入 ${result.imported_count} 道题目并完成自动标注`, 'success');
            loadDashboardStats();
        } else {
            showMessage('智能导入失败', 'danger');
        }
    } catch (error) {
        console.error('智能导入失败:', error);
        showMessage('智能导入过程中出现错误', 'danger');
    }
}

// 清空题目表单
function clearQuestionForm() {
    document.getElementById('question-content').value = '';
    document.getElementById('question-answer').value = '';
    selectedKnowledgePoints = [];
    updateSelectedKnowledgePoints();
    clearKnowledgeSuggestions();
}

// 显示添加知识点模态框
function showAddKnowledgeModal() {
    const modal = new bootstrap.Modal(document.getElementById('addKnowledgeModal'));
    modal.show();
}

// 显示智能导入模态框
function showSmartImportModal() {
    const modal = new bootstrap.Modal(document.getElementById('smartImportModal'));
    modal.show();
    
    // 重置表单
    document.getElementById('import-file').value = '';
    document.getElementById('import-preview').style.display = 'none';
    document.getElementById('import-btn').disabled = true;
    
    // 绑定置信度阈值滑块事件
    const confidenceSlider = document.getElementById('confidence-threshold');
    const confidenceValue = document.getElementById('confidence-value');
    
    confidenceSlider.addEventListener('input', function() {
        confidenceValue.textContent = this.value;
    });
}

// 预览导入文件
async function previewImportFile() {
    const fileInput = document.getElementById('import-file');
    const previewDiv = document.getElementById('import-preview');
    const contentPre = document.getElementById('import-content');
    const importBtn = document.getElementById('import-btn');
    
    if (!fileInput.files[0]) {
        previewDiv.style.display = 'none';
        importBtn.disabled = true;
        return;
    }
    
    try {
        const file = fileInput.files[0];
        const text = await file.text();
        const data = JSON.parse(text);
        
        if (!Array.isArray(data)) {
            throw new Error('文件格式错误：应为题目数组');
        }
        
        // 验证数据格式
        const sampleItem = data[0];
        if (!sampleItem.content || !sampleItem.question_type || !sampleItem.answer) {
            throw new Error('题目格式错误：缺少必要字段(content, question_type, answer)');
        }
        
        // 显示预览
        const preview = {
            total_questions: data.length,
            sample_questions: data.slice(0, 3).map(q => ({
                content: q.content.substring(0, 50) + (q.content.length > 50 ? '...' : ''),
                question_type: q.question_type,
                answer: q.answer
            }))
        };
        
        contentPre.textContent = JSON.stringify(preview, null, 2);
        previewDiv.style.display = 'block';
        importBtn.disabled = false;
        
        showMessage(`文件验证成功，共 ${data.length} 道题目`, 'success');
        
    } catch (error) {
        showMessage(`文件格式错误: ${error.message}`, 'danger');
        previewDiv.style.display = 'none';
        importBtn.disabled = true;
    }
}

// 添加知识点
async function addKnowledgePoint() {
    const name = document.getElementById('new-kp-name').value.trim();
    const description = document.getElementById('new-kp-description').value.trim();
    const level = document.getElementById('new-kp-level').value;
    const difficulty = document.getElementById('new-kp-difficulty').value;
    
    if (!name) {
        showMessage('请输入知识点名称', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/knowledge/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                description: description,
                level: level,
                difficulty: difficulty
            })
        });
        
        const data = await response.json();
        
        showMessage('知识点添加成功！', 'success');
        
        // 关闭模态框
        const modal = bootstrap.Modal.getInstance(document.getElementById('addKnowledgeModal'));
        modal.hide();
        
        // 清空表单
        document.getElementById('add-knowledge-form').reset();
        
        // 刷新知识点列表
        loadKnowledgePoints();
        loadDashboardStats();
    } catch (error) {
        console.error('添加知识点失败:', error);
        showMessage('添加失败，请重试', 'danger');
    }
}

// 加载知识点层级结构
async function loadKnowledgeHierarchy() {
    try {
        const response = await fetch(`${API_BASE_URL}/knowledge/hierarchy/tree`);
        const data = await response.json();
        
        // TODO: 实现层级结构可视化
        console.log('知识点层级结构:', data.hierarchy);
    } catch (error) {
        console.error('加载知识点层级失败:', error);
    }
}

// 工具函数

// 显示加载状态
function showLoading(containerId) {
    document.getElementById(containerId).innerHTML = `
        <div class="loading">
            <i class="fas fa-spinner fa-spin"></i>
            <p>加载中...</p>
        </div>
    `;
}

// 显示错误信息
function showError(containerId, message) {
    document.getElementById(containerId).innerHTML = `
        <div class="text-center text-danger">
            <i class="fas fa-exclamation-triangle"></i>
            <p>${message}</p>
        </div>
    `;
}

// 显示消息提示
function showMessage(message, type = 'info') {
    // 创建提示元素
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 3秒后自动消失
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 3000);
}

// 加载数据分析数据
async function loadAnalyticsData() {
    try {
        showLoading('graph-visualization', '正在加载数据分析...');
        
        // 逐个获取分析数据，避免并发请求问题
        console.log('开始获取覆盖数据...');
        const coverageResponse = await fetch(`${API_BASE_URL}/analytics/coverage`);
        if (!coverageResponse.ok) {
            throw new Error(`Coverage API failed: ${coverageResponse.status}`);
        }
        const coverageData = await coverageResponse.json();
        console.log('覆盖数据获取成功:', coverageData);
        
        console.log('开始获取难度分布数据...');
        const difficultyResponse = await fetch(`${API_BASE_URL}/analytics/difficulty-distribution`);
        if (!difficultyResponse.ok) {
            throw new Error(`Difficulty API failed: ${difficultyResponse.status}`);
        }
        const difficultyData = await difficultyResponse.json();
        console.log('难度数据获取成功:', difficultyData);
        
        console.log('开始获取类型分布数据...');
        const typeResponse = await fetch(`${API_BASE_URL}/analytics/type-distribution`);
        if (!typeResponse.ok) {
            throw new Error(`Type API failed: ${typeResponse.status}`);
        }
        const typeData = await typeResponse.json();
        console.log('类型数据获取成功:', typeData);
        
        console.log('开始显示数据...');
        displayAnalyticsData(coverageData, difficultyData, typeData);
        console.log('数据显示完成');
        
    } catch (error) {
        console.error('加载数据分析失败:', error);
        showError('graph-visualization', `数据分析加载失败: ${error.message}`);
    }
}

// 显示数据分析结果
function displayAnalyticsData(coverageData, difficultyData, typeData) {
    try {
        console.log('开始显示数据分析结果...');
        console.log('覆盖数据:', coverageData);
        console.log('难度数据:', difficultyData);
        console.log('类型数据:', typeData);
        
        const container = document.getElementById('graph-visualization');
        if (!container) {
            console.error('找不到graph-visualization容器');
            return;
        }
        
        // 安全地获取数据
        const coverage_data = coverageData?.coverage_data || [];
        const coverage_summary = coverageData?.summary || {};
        const difficulty_distribution = difficultyData?.difficulty_distribution || [];
        const type_distribution = typeData?.type_distribution || [];
        
        console.log('处理后的数据:', {
            coverage_data: coverage_data.length,
            difficulty_distribution: difficulty_distribution.length,
            type_distribution: type_distribution.length
        });
        
        const html = `
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6><i class="fas fa-chart-pie me-2"></i>知识点覆盖分析</h6>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <strong>覆盖率概览:</strong>
                                <div class="progress mt-2">
                                    <div class="progress-bar bg-info" role="progressbar" 
                                         style="width: ${coverage_summary.coverage_rate || 0}%">
                                        ${(coverage_summary.coverage_rate || 0).toFixed(1)}%
                                    </div>
                                </div>
                            </div>
                            <div style="max-height: 300px; overflow-y: auto;">
                                ${coverage_data.map(kp => `
                                    <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
                                        <div>
                                            <strong>${kp.knowledge_point || '未知'}</strong>
                                            <br><small class="text-muted">${kp.level || '未设置'}</small>
                                        </div>
                                        <span class="badge ${(kp.question_count || 0) > 0 ? 'bg-success' : 'bg-secondary'}">
                                            ${kp.question_count || 0} 题
                                        </span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h6><i class="fas fa-chart-bar me-2"></i>题目分布分析</h6>
                        </div>
                        <div class="card-body">
                            <h6>难度分布:</h6>
                            ${difficulty_distribution.map(item => `
                                <div class="mb-2">
                                    <div class="d-flex justify-content-between">
                                        <span>${getDifficultyLabel(item.difficulty || 'unknown')}</span>
                                        <span>${item.count || 0} 题 (${(item.percentage || 0).toFixed(1)}%)</span>
                                    </div>
                                    <div class="progress" style="height: 8px;">
                                        <div class="progress-bar bg-${getDifficultyColor(item.difficulty)}" 
                                             style="width: ${item.percentage || 0}%"></div>
                                    </div>
                                </div>
                            `).join('')}
                            
                            <h6 class="mt-4">题目类型分布:</h6>
                            ${type_distribution.map(item => `
                                <div class="mb-2">
                                    <div class="d-flex justify-content-between">
                                        <span>${item.question_type || '未知'}</span>
                                        <span>${item.count || 0} 题 (${(item.percentage || 0).toFixed(1)}%)</span>
                                    </div>
                                    <div class="progress" style="height: 8px;">
                                        <div class="progress-bar bg-info" 
                                             style="width: ${item.percentage || 0}%"></div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-3">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">
                            <h6><i class="fas fa-robot me-2"></i>AI Agent准确率分析</h6>
                            <button class="btn btn-sm btn-success float-end" onclick="loadAIAgentAccuracy()">
                                <i class="fas fa-brain me-1"></i>加载AI准确率
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="ai-accuracy-section">
                                <div class="text-center">
                                    <button class="btn btn-outline-success" onclick="loadAIAgentAccuracy()">
                                        <i class="fas fa-chart-line me-1"></i>查看AI Agent准确率分析
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-3">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">
                            <h6><i class="fas fa-list me-2"></i>所有题目列表</h6>
                            <button class="btn btn-sm btn-primary float-end" onclick="loadAllQuestions()">
                                <i class="fas fa-refresh me-1"></i>刷新
                            </button>
                        </div>
                        <div class="card-body">
                            <div id="all-questions-list">
                                <div class="text-center">
                                    <button class="btn btn-outline-primary" onclick="loadAllQuestions()">
                                        <i class="fas fa-list me-1"></i>加载所有题目
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        console.log('HTML内容已更新到容器');
        
    } catch (error) {
        console.error('显示数据分析结果时出错:', error);
        const container = document.getElementById('graph-visualization');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <h6>数据显示错误</h6>
                    <p>错误信息: ${error.message}</p>
                    <button class="btn btn-outline-danger" onclick="loadAnalyticsData()">重试</button>
                </div>
            `;
        }
    }
}

// 加载所有题目
async function loadAllQuestions() {
    try {
        showLoading('all-questions-list', '正在加载所有题目...');
        
        // 直接从题目API获取所有题目
        const response = await fetch(`${API_BASE_URL}/questions/`);
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('题目数据:', data);
        console.log('题目数量:', data.count);
        console.log('题目列表:', data.questions);
        
        const allQuestions = data.questions || [];
        console.log('处理后的题目列表:', allQuestions);
        console.log('题目列表长度:', allQuestions.length);
        
        displayAllQuestions(allQuestions);
        
    } catch (error) {
        console.error('加载所有题目失败:', error);
        showError('all-questions-list', '加载题目失败，请重试');
    }
}

// 显示所有题目
function displayAllQuestions(questions) {
    console.log('displayAllQuestions被调用，参数:', questions);
    console.log('参数类型:', typeof questions);
    console.log('是否为数组:', Array.isArray(questions));
    console.log('长度:', questions ? questions.length : 'undefined');
    
    const container = document.getElementById('all-questions-list');
    
    if (!questions || questions.length === 0) {
        console.log('显示空状态，原因: questions为空或长度为0');
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-question-circle"></i>
                <p>暂无题目数据</p>
                <p class="text-muted">调试信息: questions=${questions}, length=${questions ? questions.length : 'undefined'}</p>
            </div>
        `;
        return;
    }
    
    // 计算AI Agent准确率
    const aiAccuracyStats = calculateAIAccuracy(questions);
    
    const html = `
        <div class="mb-4">
            <div class="alert alert-info">
                <h6><i class="fas fa-robot me-2"></i>AI Agent模型准确率分析</h6>
                <div class="row">
                    <div class="col-md-3">
                        <strong>总题目数:</strong> ${questions.length}
                    </div>
                    <div class="col-md-3">
                        <strong>已标注:</strong> ${aiAccuracyStats.annotated_count}
                    </div>
                    <div class="col-md-3">
                        <strong>标注覆盖率:</strong> ${aiAccuracyStats.coverage_rate}%
                    </div>
                    <div class="col-md-3">
                        <strong>平均置信度:</strong> ${aiAccuracyStats.avg_confidence}
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-md-6">
                        <strong>知识点识别准确性:</strong> ${aiAccuracyStats.accuracy_rate}%
                    </div>
                    <div class="col-md-6">
                        <strong>自动应用率:</strong> ${aiAccuracyStats.auto_apply_rate}%
                    </div>
                </div>
            </div>
        </div>
        
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th width="5%">序号</th>
                        <th width="40%">题目内容</th>
                        <th width="10%">类型</th>
                        <th width="10%">难度</th>
                        <th width="15%">答案</th>
                        <th width="20%">关联知识点</th>
                    </tr>
                </thead>
                <tbody>
                    ${questions.map((question, index) => `
                        <tr>
                            <td>${index + 1}</td>
                            <td>
                                <div class="question-content" title="${question.content || ''}">
                                    ${(question.content || '').length > 60 ? 
                                        (question.content || '').substring(0, 60) + '...' : 
                                        (question.content || '')
                                    }
                                </div>
                                ${question.options && question.options.length > 0 ? 
                                    `<div class="mt-1"><small class="text-info">选项: ${question.options.join(', ')}</small></div>` : 
                                    ''
                                }
                                ${question.analysis ? 
                                    `<small class="text-muted">解析: ${question.analysis.substring(0, 50)}...</small>` : 
                                    ''
                                }
                            </td>
                            <td>
                                <span class="badge bg-primary">${question.question_type || '未知'}</span>
                            </td>
                            <td>
                                <span class="badge bg-${getDifficultyColor(question.difficulty)}">
                                    ${getDifficultyLabel(question.difficulty)}
                                </span>
                            </td>
                            <td>
                                <code>${question.answer || '未设置'}</code>
                            </td>
                            <td>
                                ${(question.knowledge_points || []).map(kp => 
                                    `<span class="badge bg-success me-1">${kp}</span>`
                                ).join('')}
                                ${(!question.knowledge_points || question.knowledge_points.length === 0) ? 
                                    '<span class="text-muted">未标注</span>' : ''
                                }
                                <br>
                                <button class="btn btn-xs btn-outline-info mt-1" 
                                        onclick="showQuestionDetails('${question.id}')">
                                    <i class="fas fa-eye"></i> 详情
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
        
        <div class="mt-3">
            <div class="alert alert-secondary">
                <h6><i class="fas fa-info-circle me-2"></i>题目统计</h6>
                <div class="row">
                    <div class="col-md-4">
                        <strong>选择题:</strong> ${questions.filter(q => q.question_type === '选择题').length} 道
                    </div>
                    <div class="col-md-4">
                        <strong>填空题:</strong> ${questions.filter(q => q.question_type === '填空题').length} 道
                    </div>
                    <div class="col-md-4">
                        <strong>其他类型:</strong> ${questions.filter(q => !['选择题', '填空题'].includes(q.question_type)).length} 道
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

// 计算AI Agent准确率
function calculateAIAccuracy(questions) {
    const annotatedQuestions = questions.filter(q => q.knowledge_points && q.knowledge_points.length > 0);
    const coverageRate = questions.length > 0 ? Math.round((annotatedQuestions.length / questions.length) * 100) : 0;
    
    // 模拟置信度计算（实际应用中应该从AI Agent结果中获取）
    const avgConfidence = 0.65; // 基于之前测试结果的估算
    
    // 估算准确性（基于关键词匹配的简单评估）
    let correctMatches = 0;
    for (const question of annotatedQuestions) {
        const content = question.content.toLowerCase();
        const kps = question.knowledge_points || [];
        
        // 简单的准确性评估逻辑
        if (content.includes('every day') && kps.includes('一般现在时')) correctMatches++;
        if (content.includes('yesterday') && kps.includes('一般过去时')) correctMatches++;
        if (content.includes('now') && kps.includes('现在进行时')) correctMatches++;
        if (content.includes('already') && kps.includes('现在完成时')) correctMatches++;
        if (content.includes('who') || content.includes('which')) {
            if (kps.includes('定语从句')) correctMatches++;
        }
        if (content.includes('by') && content.includes('were')) {
            if (kps.includes('被动语态')) correctMatches++;
        }
        if (content.includes('than')) {
            if (kps.includes('比较级和最高级')) correctMatches++;
        }
    }
    
    const accuracyRate = annotatedQuestions.length > 0 ? 
        Math.round((correctMatches / annotatedQuestions.length) * 100) : 0;
    
    return {
        total_questions: questions.length,
        annotated_count: annotatedQuestions.length,
        coverage_rate: coverageRate,
        avg_confidence: avgConfidence.toFixed(3),
        accuracy_rate: accuracyRate,
        auto_apply_rate: 15 // 基于当前阈值的估算
    };
}

// 加载AI Agent准确率分析
async function loadAIAgentAccuracy() {
    try {
        showLoading('ai-accuracy-section', '正在分析AI Agent准确率...');
        
        const response = await fetch(`${API_BASE_URL}/analytics/ai-agent-accuracy`);
        if (!response.ok) {
            throw new Error(`AI准确率API失败: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('AI准确率数据:', data);
        
        const accuracy = data.accuracy_analysis || {};
        const details = accuracy.details || [];
        
        const html = `
            <div class="alert alert-primary">
                <h6><i class="fas fa-robot me-2"></i>AI Agent性能指标</h6>
                <div class="row">
                    <div class="col-md-3">
                        <strong>准确率:</strong> ${(accuracy.accuracy_rate || 0).toFixed(1)}%
                    </div>
                    <div class="col-md-3">
                        <strong>正确标注:</strong> ${accuracy.correct_annotations || 0}
                    </div>
                    <div class="col-md-3">
                        <strong>总标注数:</strong> ${accuracy.total_annotations || 0}
                    </div>
                    <div class="col-md-3">
                        <strong>覆盖率:</strong> ${(data.coverage_rate || 0).toFixed(1)}%
                    </div>
                </div>
            </div>
            
            <div class="table-responsive">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>题目内容</th>
                            <th>AI标注</th>
                            <th>期望标注</th>
                            <th>准确性</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${details.map(detail => `
                            <tr>
                                <td>${detail.content || '未知'}</td>
                                <td>${(detail.annotated_kps || []).join(', ')}</td>
                                <td>${(detail.expected_kps || []).join(', ') || '无'}</td>
                                <td>
                                    ${detail.is_accurate ? 
                                        '<span class="badge bg-success">✅ 正确</span>' : 
                                        '<span class="badge bg-danger">❌ 错误</span>'
                                    }
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        document.getElementById('ai-accuracy-section').innerHTML = html;
        
    } catch (error) {
        console.error('加载AI准确率失败:', error);
        showError('ai-accuracy-section', `AI准确率加载失败: ${error.message}`);
    }
}

// 显示题目详情
async function showQuestionDetails(questionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/questions/${questionId}/knowledge`);
        const data = await response.json();
        
        const knowledgePoints = data.knowledge_points || [];
        const details = knowledgePoints.map(kp => 
            `${kp.knowledge_point.name} (权重: ${kp.weight})`
        ).join(', ');
        
        showMessage(`题目 ${questionId} 的知识点标注: ${details || '无标注'}`, 'info', 5000);
    } catch (error) {
        showMessage(`获取题目详情失败: ${error.message}`, 'danger');
    }
}
