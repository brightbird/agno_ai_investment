# 🤖 Agno AI 投资分析系统

![GitHub stars](https://img.shields.io/github/stars/brightbird/agno_ai_investment?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/brightbird/agno_ai_investment?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/brightbird/agno_ai_investment?style=flat-square)
![GitHub license](https://img.shields.io/github/license/brightbird/agno_ai_investment?style=flat-square)
![Python version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![Build Status](https://img.shields.io/github/actions/workflow/status/brightbird/agno_ai_investment/ci.yml?style=flat-square)

基于 [Agno 框架](https://docs.agno.com) 构建的多Agent投资分析系统，集成了多位世界知名投资大师的投资理念和分析方法。

## ✨ 系统特色

- 🎯 **智能大师选择**: 根据投资需求推荐最适合的投资大师
- 🎩 **多投资大师视角**: Warren Buffett, Charlie Munger, Peter Lynch 等7位大师
- 🏦 **投资组合分析**: 综合多角度投资建议和风险评估
- 📊 **实时数据分析**: 集成Yahoo Finance实时股票数据
- 🌐 **统一Web界面**: 基于Agno Playground的现代化对话界面，**同时支持个人Agents和团队协作**
- 🧠 **智能推理**: 使用阿里云通义千问模型驱动分析
- 💾 **历史记录**: 自动保存对话历史和分析结果
- 🏆 **投资大师团队**: 基于Agno Team接口的协作分析
- ⚡ **双模式演示**: 在同一个Playground中体验个人专家分析和团队协作分析

## 🏗️ 项目结构

```
agno_ai_investment/
├── 📁 apps/                    # 应用程序
│   ├── playground.py          # Playground Web界面
│   └── investment_team.py     # 投资大师团队
├── 📁 src/                    # 核心源代码
│   ├── agents/               # 投资大师Agents
│   ├── config/               # 配置管理
│   └── utils/                # 工具函数
├── 📁 scripts/               # 运维脚本
│   ├── setup_env.sh         # 环境配置
│   └── start_playground.sh  # 启动脚本
├── 📁 docs/                  # 项目文档
├── 📁 data/                  # 数据存储
│   ├── agent_storage/       # Agent数据库
│   └── market_data/         # 市场数据
├── 📁 tests/                 # 测试文件
├── 📁 demos/                 # 示例代码
│   └── investment_team_demo.py # 团队演示
└── 📁 .archive/              # 历史文档
```

## 🚀 快速开始

> ✅ **系统状态**：Agno AI投资分析系统运行完全正常！**Playground现在同时支持个人Agents和Teams功能**，您可以在同一个界面中体验不同的分析模式。

### 1. 环境配置

```bash
# 克隆项目
git clone <repository-url>
cd agno_ai_investment

# 运行环境配置脚本
bash scripts/setup_env.sh

# 激活虚拟环境
source .venv/bin/activate
```

### 2. API密钥配置

编辑 `.env` 文件，设置你的阿里云API密钥：

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置文件
# ALIYUN_API_KEY=your_api_key_here
```

获取API密钥：
- 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
- 创建应用并获取API Key

### 3. 启动统一Playground系统

```bash
# 首次使用需要认证
ag setup

# 启动统一Playground服务（同时支持Agents和Teams）
python apps/playground.py

# 或使用快速启动脚本
bash scripts/start_playground.sh
```

### 4. 访问统一界面

1. 访问：**https://app.agno.com/playground**
2. 选择 `localhost:7777` 端点
3. **选择分析模式**：
   - **Agents模式**: 选择个人投资大师进行专业分析
   - **Teams模式**: 选择投资团队进行协作分析
4. 开始与投资大师对话！

## 🎯 双模式分析体验

### 🤖 个人Agents模式
在 **Agents** 部分，您可以选择任意一位投资大师进行专业分析：

## 👨‍💼 投资大师团队

| 大师 | 专长 | 投资风格 |
|------|------|----------|
| 🎯 投资大师选择助手 | 个性化推荐 | 根据需求推荐合适的投资大师 |
| 🎩 Warren Buffett | 价值投资 | 长期持有优质企业 |
| 🧠 Charlie Munger | 多学科思维 | 理性分析与心理学 |
| 📈 Peter Lynch | 成长价值 | 发掘成长股机会 |
| 📚 Benjamin Graham | 价值投资鼻祖 | 安全边际与内在价值 |
| 🌊 Ray Dalio | 全天候策略 | 分散投资与风险平价 |
| 🔢 Joel Greenblatt | 魔法公式 | 量化价值投资 |
| ⚡ David Tepper | 困境投资 | 特殊情况投资 |
| 🏦 投资组合综合分析师 | 综合建议 | 多角度投资组合优化 |

### 🏆 Teams协作模式
在 **Teams** 部分，您可以选择投资团队进行协作分析：

| 团队 | 成员 | 协作特色 |
|------|------|----------|
| 🏆 巴菲特-芒格投资分析团队 | Warren Buffett + Charlie Munger | 价值投资 + 多学科思维的完美结合 |

## 🏆 投资大师团队协作

### 统一Playground中的团队功能

**重要特性**：现在您可以在同一个Playground界面中无缝切换使用个人Agents和投资团队！

#### 🎯 团队协作优势
- **🎩 Warren Buffett**: 价值投资分析，关注企业护城河和长期价值
- **🧠 Charlie Munger**: 多学科思维，逆向思考和认知偏误检查
- **🏆 智能协调者**: 基于Agno Team接口，自动综合两位大师观点
- **📊 结构化输出**: 隐藏技术细节，提供用户友好的分析报告

#### 🚀 在Playground中使用团队

**方法一：Web界面使用（推荐）**
```bash
# 启动统一Playground
python apps/playground.py

# 访问 https://app.agno.com/playground
# 在 Teams 部分选择 "🏆 巴菲特-芒格投资分析团队"
```

**方法二：命令行使用**
```bash
# 运行投资团队分析（默认分析苹果公司）
python apps/investment_team.py

# 运行交互式演示（可选择不同股票）
python demos/investment_team_demo.py
```

## 🎯 统一Playground演示

### 在同一界面中体验Agents和Teams

**核心优势**：无需切换应用，在同一个Playground中即可体验个人专家分析和团队协作分析。

#### 🚀 快速演示

```bash
# 方法一：使用快速演示脚本
bash scripts/demo_agent_ui.sh

# 方法二：运行交互式演示指南
python demos/agent_ui_demo.py

# 方法三：直接启动统一Playground
python apps/playground.py
# 然后访问: https://app.agno.com/playground
```

#### 🏗️ 统一界面使用流程

1. **启动服务**: 运行 `python apps/playground.py`
2. **访问界面**: 打开 https://app.agno.com/playground
3. **连接端点**: 添加 `localhost:7777` 端点
4. **选择分析模式**:
   - **Agents**: 选择个人投资大师（如 🎩 Warren Buffett）
   - **Teams**: 选择投资团队（🏆 巴菲特-芒格投资分析团队）
5. **开始分析**: 输入股票分析请求

#### 🎬 推荐演示场景

**个人Agents模式演示**：
- 选择 🎩 Warren Buffett，询问："请分析苹果公司(AAPL)的投资价值"
- 选择 🧠 Charlie Munger，询问："从多学科角度分析特斯拉的风险"
- 选择 📈 Peter Lynch，询问："推荐一些适合成长投资的股票"

**Teams协作模式演示**：
- 选择 🏆 巴菲特-芒格投资分析团队
- 询问："请分析微软(MSFT)的长期投资前景"
- 体验两位大师的协作分析和综合建议

#### 📊 分析报告对比

| 模式 | 特点 | 适用场景 |
|------|------|----------|
| **个人Agents** | 专业深度分析 | 需要特定投资风格的专业建议 |
| **Teams协作** | 多角度综合分析 | 需要平衡不同观点的全面分析 |

#### 📚 详细文档

- [投资团队使用指南](docs/INVESTMENT_TEAM_GUIDE.md) - 了解团队功能详情
- [Agent UI 演示指南](docs/AGENT_UI_DEMO_GUIDE.md) - 完整的界面使用教程

## 🛠️ 功能特性

### 核心功能
- **实时股票分析**: 获取最新价格、技术指标、财务数据
- **投资建议生成**: 基于大师投资理念的个性化建议
- **风险评估**: 全面的投资风险分析
- **组合优化**: 投资组合配置建议
- **团队协作**: 多Agent协作分析，综合不同观点

### 数据来源
- **Yahoo Finance**: 股票价格、财务数据、技术指标
- **DuckDuckGo**: 最新市场新闻和公司信息
- **通义千问**: AI驱动的分析和推理

### 技术特性
- **多Agent协作**: 不同投资风格的专家意见
- **Team协调**: 基于Agno Team接口的智能协作
- **历史记录**: 对话和分析结果持久化存储
- **Markdown输出**: 结构化的分析报告
- **实时更新**: 基于最新市场数据的动态分析

## 📚 使用指南

### 基本对话示例

```
用户: 帮我分析一下苹果公司(AAPL)的投资价值

Warren Buffett: 从价值投资角度分析AAPL的护城河和长期增长潜力...

Peter Lynch: 作为成长股投资者，我关注AAPL的创新能力和市场扩展...
```

### 团队协作示例

```
用户: 请巴菲特和芒格团队分析苹果公司

🎩 Warren Buffett: 苹果具有强大的品牌护城河和忠实用户群体...

🧠 Charlie Munger: 从心理学角度看，苹果创造了强大的用户粘性...

🏆 团队协调者: 综合两位大师观点，苹果公司具有以下投资价值...
```

### 高级功能
- **多股票对比**: "比较AAPL和MSFT哪个更值得投资"
- **投资组合建议**: "为我设计一个均衡的科技股投资组合"
- **风险分析**: "分析当前市场环境下的投资风险"
- **团队分析**: "请投资团队深度分析特斯拉的投资价值"

## 🔧 开发指南

### 项目架构
- **Agent层**: 基于Agno框架的投资大师智能体
- **Team层**: 基于Agno Team的多Agent协作
- **模型层**: 阿里云通义千问大语言模型
- **工具层**: Yahoo Finance、搜索等外部工具
- **存储层**: SQLite数据库存储对话历史

### 添加新投资大师
1. 在 `src/agents/configurable_investment_agent.py` 添加配置
2. 定义投资哲学、分析方法、风格特征
3. 重启服务即可生效

### 扩展投资团队
1. 在 `apps/investment_team.py` 添加新的Agent创建方法
2. 将新Agent添加到团队成员列表
3. 更新团队协调指令

### 自定义工具
- 在 `src/utils/` 添加新的工具函数
- 在Agent配置中集成新工具
- 支持股票数据、新闻、技术分析等

## 📖 文档索引

- [详细使用指南](docs/README.md)
- [配置指南](docs/CONFIGURATION_GUIDE.md)
- [Playground使用指南](docs/PLAYGROUND_GUIDE.md)
- [投资大师选择指南](docs/MASTER_SELECTION_GUIDE.md)
- [投资团队使用指南](docs/INVESTMENT_TEAM_GUIDE.md)
- [项目结构说明](PROJECT_STRUCTURE.md)

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## ⚠️ 免责声明

本系统仅用于教育和研究目的，不构成投资建议。所有投资决策应基于您自己的研究和风险承受能力。投资有风险，决策需谨慎。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Agno Framework](https://docs.agno.com) - 强大的AI Agent框架
- [阿里云百炼](https://bailian.console.aliyun.com/) - 提供AI模型服务
- Yahoo Finance - 金融数据支持
- 所有投资大师 - 为投资理念提供灵感

## 📋 预防措施

1. **定期备份**：设置定时备份数据库
2. **监控告警**：使用监控脚本检测问题
3. **版本控制**：保持代码和配置同步
4. **环境隔离**：使用虚拟环境避免冲突

## ⚠️ 常见问题解答

### Session 404/405 错误
如果在启动后看到类似以下的日志信息：
```
INFO: ::1:56601 - "GET /v1/playground/agents/.../sessions/... HTTP/1.1" 404 Not Found
```

**这是正常现象，不会影响使用**。这些错误是Agno Playground在尝试获取不存在的session时的预期行为。

### 如何验证系统正常工作
1. 访问 https://app.agno.com/playground
2. 添加 `localhost:7777` 端点
3. 能够看到所有投资大师列表
4. 能够创建新对话并正常交流

### 故障排除
如果遇到问题，请运行：
```bash
# 快速健康检查
python scripts/test_functionality.py quick

# 紧急修复
./scripts/emergency_fix.sh

# 查看详细故障排除指南
open docs/TROUBLESHOOTING.md
``` 