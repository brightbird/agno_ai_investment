# 🏗️ Agno AI 投资分析系统 - 项目结构

## 📁 优化后的项目结构

```
agno_ai_investment/
├── README.md                          # 项目主要介绍
├── requirements.txt                   # Python依赖
├── .env.example                      # 环境变量示例
├── .gitignore                        # Git忽略文件
│
├── 📁 src/                           # 核心源代码
│   ├── __init__.py
│   ├── 📁 agents/                    # 投资大师Agents
│   │   ├── __init__.py
│   │   ├── configurable_investment_agent.py
│   │   ├── multi_agent_investment_v2.py
│   │   └── warren_buffett_agent_v2.py
│   ├── 📁 config/                    # 配置管理
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── masters_config.py
│   ├── 📁 utils/                     # 工具函数
│   │   ├── __init__.py
│   │   ├── data_utils.py
│   │   └── validation.py
│   └── 📁 models/                    # 数据模型
│       ├── __init__.py
│       └── investment_models.py
│
├── 📁 apps/                          # 应用程序入口
│   ├── playground.py                 # Agno Playground应用
│   ├── cli.py                       # 命令行界面
│   └── api.py                       # REST API应用
│
├── 📁 scripts/                       # 脚本工具
│   ├── start_playground.sh          # Playground启动脚本
│   ├── setup_env.sh                 # 环境设置脚本
│   └── deploy.sh                    # 部署脚本
│
├── 📁 docs/                          # 项目文档
│   ├── README.md                     # 详细使用指南
│   ├── CONFIGURATION_GUIDE.md       # 配置指南
│   ├── PLAYGROUND_GUIDE.md          # Playground使用指南
│   ├── API_REFERENCE.md             # API参考文档
│   └── DEPLOYMENT.md                # 部署指南
│
├── 📁 tests/                         # 测试文件
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_playground.py
│   └── fixtures/
│
├── 📁 demos/                         # 示例和演示
│   ├── simple/                      # 简单示例
│   ├── advanced/                    # 高级示例
│   └── jupyter_notebooks/           # Jupyter笔记本
│
├── 📁 data/                          # 数据文件
│   ├── portfolio_data.json
│   ├── market_data/
│   └── agent_storage/               # Agent数据存储
│       └── agents.db
│
├── 📁 logs/                          # 日志文件
│   ├── playground.log
│   └── agents.log
│
└── 📁 .archive/                      # 归档文件
    ├── legacy/                      # 旧版本代码
    ├── bugfix_summaries/            # 问题修复记录
    └── project_status/              # 项目状态记录
```

## 🎯 优化要点

### 1. **分离关注点**
- `src/`: 核心业务逻辑
- `apps/`: 应用程序入口
- `scripts/`: 运维脚本
- `docs/`: 项目文档

### 2. **模块化设计**
- 按功能域组织代码
- 清晰的依赖关系
- 易于测试和维护

### 3. **标准化配置**
- 统一的环境变量管理
- 配置文件集中管理
- 数据文件分类存储

### 4. **文档组织**
- 用户文档集中在docs/
- 技术文档与代码分离
- 归档历史文档

### 5. **开发友好**
- 清晰的测试结构
- 丰富的示例代码
- 完善的脚本工具

## 🚀 迁移指南

### 文件移动计划：
1. 创建新目录结构
2. 移动现有文件到对应位置
3. 更新导入路径
4. 更新文档引用
5. 测试功能完整性

### 配置更新：
- 更新 `playground.py` 中的导入路径
- 修改脚本中的文件引用
- 更新环境变量配置

## 📝 维护建议

1. **新功能开发**：按模块添加到对应目录
2. **文档更新**：及时更新docs/中的相关文档  
3. **测试覆盖**：为新功能添加对应测试
4. **定期清理**：将过时文件移到.archive/ 