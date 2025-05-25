# 🛠️ 故障排除指南

## 常见问题与解决方案

### 1. Session 404 错误

**问题现象：**
```
INFO: ::1:56601 - "GET /v1/playground/agents/{agent_id}/sessions/{session_id}?user_id={user_id} HTTP/1.1" 404 Not Found
```

**重要说明：**
⚠️ **这个404错误通常是正常现象**，不会影响实际使用。Agno Playground在尝试获取不存在的session时会返回404，这是预期行为。

**何时需要关注：**
- ✅ 如果能正常创建新对话 → 忽略404错误
- ❌ 如果无法创建对话或对话功能异常 → 需要修复

**原因分析：**
- Session记录在数据库中不存在或已过期 (正常)
- Agent ID与数据库记录不匹配 (正常)
- 服务重启导致session状态丢失 (正常)
- 前端缓存了无效的session ID (正常)
- 真正的系统问题 (需要修复)

**解决方案：**

#### 方案1: 快速修复（推荐）
```bash
# 1. 运行修复脚本
python scripts/fix_sessions.py

# 2. 重启服务
python apps/playground.py
```

#### 方案2: 数据库清理
```bash
# 清理6小时前的过期记录
python scripts/session_monitor.py clean 6

# 测试修复结果
python scripts/session_monitor.py test
```

#### 方案3: 完全重置（会丢失历史数据）
```bash
# 重置所有agent数据
python scripts/fix_sessions.py --reset

# 重启服务
python apps/playground.py
```

#### 方案4: 前端解决
- 刷新浏览器页面
- 清除浏览器缓存
- 重新选择agent

### 2. 服务启动失败

**问题现象：**
```
❌ 启动失败: [各种错误信息]
```

**解决方案：**

#### 检查API密钥
```bash
# 确认环境变量设置
echo $ALIYUN_API_KEY

# 如果没有设置
export ALIYUN_API_KEY=your_api_key_here
```

#### 检查端口占用
```bash
# 查看7777端口使用情况
lsof -i :7777

# 如果被占用，终止进程
kill [进程ID]
```

#### 检查依赖包
```bash
# 重新安装依赖
pip install -r requirements.txt

# 检查Agno版本
pip list | grep agno
```

### 3. Agent创建失败

**问题现象：**
```
❌ 创建失败 [master_name]: [错误信息]
```

**解决方案：**

#### 检查配置文件
```bash
# 验证配置文件语法
python -c "from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent; print('配置文件正常')"
```

#### 检查存储目录
```bash
# 确保存储目录存在
mkdir -p data/agent_storage

# 检查权限
ls -la data/agent_storage/
```

### 4. 数据库连接问题

**问题现象：**
- SQLite数据库锁定
- 数据库文件损坏
- 权限问题

**解决方案：**

#### 数据库诊断
```bash
# 检查数据库文件
sqlite3 data/agent_storage/investment_agents.db ".tables"

# 检查数据库完整性
sqlite3 data/agent_storage/investment_agents.db "PRAGMA integrity_check;"
```

#### 修复损坏的数据库
```bash
# 备份现有数据库
cp data/agent_storage/investment_agents.db data/agent_storage/investment_agents.db.backup

# 导出数据
sqlite3 data/agent_storage/investment_agents.db ".dump" > backup.sql

# 重新创建数据库
rm data/agent_storage/investment_agents.db
sqlite3 data/agent_storage/investment_agents.db < backup.sql
```

### 5. 网络连接问题

**问题现象：**
- 无法获取股票数据
- API调用失败
- 超时错误

**解决方案：**

#### 检查网络连接
```bash
# 测试Yahoo Finance连接
curl -I "https://finance.yahoo.com"

# 测试阿里云API连接
curl -I "https://dashscope.aliyuncs.com"
```

#### 配置代理（如需要）
```bash
# 设置HTTP代理
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
```

### 6. 性能问题

**问题现象：**
- 响应速度慢
- 内存占用高
- CPU使用率高

**解决方案：**

#### 启用监控
```bash
# 启动性能监控
python scripts/session_monitor.py monitor
```

#### 优化配置
- 减少历史记录数量：修改 `num_history_responses` 参数
- 限制并发请求：调整uvicorn worker数量
- 定期清理数据库：使用定时任务运行清理脚本

### 7. 开发环境问题

**问题现象：**
- 模块导入错误
- 路径问题
- 环境变量问题

**解决方案：**

#### 环境设置
```bash
# 激活虚拟环境
source .venv/bin/activate

# 设置Python路径
export PYTHONPATH="${PYTHONPATH}:${PWD}/src"

# 验证环境
python -c "import sys; print('\\n'.join(sys.path))"
```

## 🔧 诊断工具

### 健康检查
```bash
# 全面健康检查
python scripts/session_monitor.py health
python scripts/session_monitor.py test
```

### 日志分析
```bash
# 查看服务日志（如果有）
tail -f logs/playground.log

# 实时监控请求
python scripts/session_monitor.py monitor
```

### 系统信息
```bash
# Python版本和依赖
python --version
pip list

# 系统资源
top -l 1 | grep -E "CPU usage|Load Avg"
df -h
```

## 🚨 紧急恢复

如果所有方法都失败，使用紧急恢复：

```bash
# 1. 停止所有相关进程
pkill -f "python.*playground"

# 2. 备份现有数据
cp -r data/agent_storage data/agent_storage.backup.$(date +%Y%m%d_%H%M%S)

# 3. 完全重置
rm -rf data/agent_storage/*

# 4. 重新启动
python apps/playground.py
```

## 🔍 获取帮助

1. **查看详细日志**：启用详细日志记录
2. **检查GitHub Issues**：搜索类似问题
3. **社区支持**：提交issue并附上错误日志
4. **文档参考**：查看官方Agno文档

## 📋 预防措施

1. **定期备份**：设置定时备份数据库
2. **监控告警**：使用监控脚本检测问题
3. **版本控制**：保持代码和配置同步
4. **环境隔离**：使用虚拟环境避免冲突 