# 🤖 Agno AI 投资分析系统

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/agno_ai_investment?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/agno_ai_investment?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/agno_ai_investment?style=flat-square)
![GitHub license](https://img.shields.io/github/license/YOUR_USERNAME/agno_ai_investment?style=flat-square)
![Python version](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square)
![Build Status](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/agno_ai_investment/ci.yml?style=flat-square)

基于 [Agno 框架](https://docs.agno.com) 构建的多Agent投资分析系统，集成了多位世界知名投资大师的投资理念和分析方法。

## ✨ 系统特色

- 🎯 **智能大师选择**: 根据投资需求推荐最适合的投资大师
- 🎩 **多投资大师视角**: Warren Buffett, Charlie Munger, Peter Lynch 等7位大师
- 🏦 **投资组合分析**: 综合多角度投资建议和风险评估
- 📊 **实时数据分析**: 集成Yahoo Finance实时股票数据
- 🌐 **Web界面**: 基于Agno Playground的现代化对话界面
- 🧠 **智能推理**: 使用阿里云通义千问模型驱动分析
- 💾 **历史记录**: 自动保存对话历史和分析结果

## 🏗️ 项目结构

```
agno_ai_investment/
├── 📁 apps/                    # 应用程序
│   └── playground.py          # Playground Web界面
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
└── 📁 .archive/              # 历史文档
```

## 🚀 快速开始

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

### 3. 启动系统

```bash
# 首次使用需要认证
ag setup

# 启动Playground服务
bash scripts/start_playground.sh
```

### 4. 访问界面

1. 访问：**https://app.agno.com/playground**
2. 选择 `localhost:7777` 端点
3. 开始与投资大师对话！

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
| 🏦 投资组合分析师 | 综合建议 | 多角度投资组合优化 |

## 🛠️ 功能特性

### 核心功能
- **实时股票分析**: 获取最新价格、技术指标、财务数据
- **投资建议生成**: 基于大师投资理念的个性化建议
- **风险评估**: 全面的投资风险分析
- **组合优化**: 投资组合配置建议

### 数据来源
- **Yahoo Finance**: 股票价格、财务数据、技术指标
- **DuckDuckGo**: 最新市场新闻和公司信息
- **通义千问**: AI驱动的分析和推理

### 技术特性
- **多Agent协作**: 不同投资风格的专家意见
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

### 高级功能
- **多股票对比**: "比较AAPL和MSFT哪个更值得投资"
- **投资组合建议**: "为我设计一个均衡的科技股投资组合"
- **风险分析**: "分析当前市场环境下的投资风险"

## 🔧 开发指南

### 项目架构
- **Agent层**: 基于Agno框架的投资大师智能体
- **模型层**: 阿里云通义千问大语言模型
- **工具层**: Yahoo Finance、搜索等外部工具
- **存储层**: SQLite数据库存储对话历史

### 添加新投资大师
1. 在 `src/agents/configurable_investment_agent.py` 添加配置
2. 定义投资哲学、分析方法、风格特征
3. 重启服务即可生效

### 自定义工具
- 在 `src/utils/` 添加新的工具函数
- 在Agent配置中集成新工具
- 支持股票数据、新闻、技术分析等

## 📖 文档索引

- [详细使用指南](docs/README.md)
- [配置指南](docs/CONFIGURATION_GUIDE.md)
- [Playground使用指南](docs/PLAYGROUND_GUIDE.md)
- [投资大师选择指南](docs/MASTER_SELECTION_GUIDE.md)
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