# K12英语知识图谱系统安装指南

## 📋 系统要求

### 硬件要求
- CPU: 2核心以上
- 内存: 8GB以上推荐
- 硬盘: 10GB可用空间
- 网络: 稳定的互联网连接

### 软件要求
- Python 3.8 或更高版本
- Neo4j 4.0 或更高版本
- 操作系统: Windows 10/11, macOS 10.15+, Ubuntu 18.04+

## 🔧 详细安装步骤

### 1. 安装Python环境

#### Windows
```bash
# 下载并安装Python 3.8+
# 从 https://www.python.org/downloads/ 下载

# 验证安装
python --version
pip --version
```

#### macOS
```bash
# 使用Homebrew安装
brew install python@3.9

# 或下载安装包
# 从 https://www.python.org/downloads/ 下载
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.9 python3.9-pip python3.9-venv
```

### 2. 安装Neo4j数据库

#### 方法一：Neo4j Desktop（推荐）
1. 访问 https://neo4j.com/download/
2. 下载Neo4j Desktop
3. 安装并启动Neo4j Desktop
4. 创建新项目和数据库
5. 设置用户名和密码（记住这些信息）
6. 启动数据库实例

#### 方法二：Docker安装
```bash
# 拉取Neo4j镜像
docker pull neo4j:latest

# 运行Neo4j容器
docker run \
    --name neo4j-kg \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/your_password \
    neo4j:latest
```

#### 方法三：系统包管理器
```bash
# Ubuntu/Debian
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j

# macOS
brew install neo4j

# 启动服务
sudo systemctl start neo4j  # Linux
brew services start neo4j   # macOS
```

### 3. 克隆并配置项目

```bash
# 克隆项目（如果从Git仓库）
git clone <repository-url>
cd 英语知识图库

# 或者如果是本地项目，直接进入目录
cd /path/to/英语知识图库
```

### 4. 创建Python虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 5. 安装Python依赖

```bash
# 升级pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

### 6. 配置环境变量

```bash
# 复制配置文件
cp config.env.example config.env

# 编辑配置文件
vim config.env  # 或使用其他编辑器
```

配置内容示例：
```env
# Neo4j数据库配置
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password_here

# 应用配置
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

### 7. 初始化数据库

```bash
# 初始化数据库结构
python scripts/init_database.py

# 加载示例数据
python scripts/load_sample_data.py
```

### 8. 测试系统

```bash
# 运行系统测试
python scripts/test_system.py
```

### 9. 启动系统

```bash
# 启动系统
python run.py
```

## 🔍 验证安装

### 检查服务状态

1. **Neo4j数据库**
   - 访问 http://localhost:7474
   - 使用配置的用户名密码登录
   - 执行查询: `MATCH (n) RETURN count(n)`

2. **应用服务**
   - 访问 http://localhost:8000
   - 检查主界面是否正常显示
   - 访问 http://localhost:8000/docs 查看API文档

3. **功能测试**
   - 在知识点管理中搜索"时态"
   - 在智能标注中测试AI推荐功能
   - 在数据分析中查看统计图表

## 🐛 常见问题解决

### 问题1: Neo4j连接失败
```
错误: Failed to connect to Neo4j
```

**解决方案:**
1. 检查Neo4j服务是否启动
2. 验证连接配置（URI、用户名、密码）
3. 检查防火墙设置
4. 确认端口7687未被占用

### 问题2: Python依赖安装失败
```
错误: Could not install packages due to an EnvironmentError
```

**解决方案:**
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或者逐个安装依赖
pip install fastapi uvicorn neo4j python-dotenv
```

### 问题3: 端口被占用
```
错误: Address already in use
```

**解决方案:**
```bash
# 查找占用端口的进程
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# 终止进程或更改配置文件中的端口
```

### 问题4: 权限不足
```
错误: Permission denied
```

**解决方案:**
```bash
# 确保有足够权限
chmod +x scripts/*.py

# 或使用管理员权限运行
sudo python run.py  # Linux/macOS
```

### 问题5: 中文编码问题
```
错误: UnicodeDecodeError
```

**解决方案:**
- 确保系统支持UTF-8编码
- Windows用户可能需要设置环境变量:
```bash
set PYTHONIOENCODING=utf-8
```

## 📞 获取帮助

如果遇到其他问题，请：

1. 查看日志文件（如果有生成）
2. 运行测试脚本诊断问题
3. 检查系统要求是否满足
4. 参考项目文档或联系支持

## 🔄 升级指南

### 更新代码
```bash
git pull origin main  # 如果使用Git
```

### 更新依赖
```bash
pip install --upgrade -r requirements.txt
```

### 数据库迁移
```bash
# 备份现有数据
python scripts/backup_data.py  # 如果有此脚本

# 运行迁移
python scripts/migrate_database.py  # 如果有此脚本
```

---

🎉 安装完成后，您就可以开始使用K12英语知识图谱系统了！
