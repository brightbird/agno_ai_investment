# 巴菲特-芒格投资分析团队使用指南

## 概述

基于 [Agno Team 接口](https://docs.agno.com/introduction/agents#multi-agent-teams) 实现的投资大师团队，综合巴菲特和查理·芒格的投资观点进行股票分析。

## 功能特点

### 🎩 Warren Buffett Agent
- **投资哲学**: 价值投资，寻找具有持续竞争优势的优秀企业
- **分析重点**: 企业护城河、管理层质量、财务指标、估值分析
- **语言风格**: 简单易懂的比喻，强调长期投资

### 🧠 Charlie Munger Agent  
- **投资哲学**: 多学科思维模型，逆向思考
- **分析重点**: 跨学科分析、认知偏误检查、人性因素
- **语言风格**: 直言不讳，引用各学科原理

### 🏆 团队协调者
- **协调模式**: coordinate 模式，综合两位大师观点
- **输出结构**: 执行摘要、分别观点、综合建议、风险提示
- **智能推理**: 使用 ReasoningTools 进行深度分析

## 快速开始

### 1. 环境准备

```bash
# 确保已安装依赖
pip install -r requirements.txt

# 设置环境变量
export ALIYUN_API_KEY=your_api_key
```

### 2. 运行投资团队

```bash
# 直接运行主程序（分析苹果公司）
python apps/investment_team.py

# 或运行演示程序（可选择不同股票）
python demos/investment_team_demo.py
```

### 3. 自定义分析

```python
from apps.investment_team import InvestmentMasterTeam

# 创建投资团队
team_manager = InvestmentMasterTeam()
investment_team = team_manager.create_investment_team()

# 自定义分析任务
task = """
请分析特斯拉(TSLA)的投资价值，重点关注：
1. 电动车市场竞争格局
2. 自动驾驶技术优势
3. 能源业务发展前景
4. 估值合理性分析
"""

# 执行分析
investment_team.print_response(
    task,
    stream=True,
    stream_intermediate_steps=True,
    show_full_reasoning=True,
)
```

## 团队架构

### Team 模式说明

根据 [Agno 文档](https://docs.agno.com/introduction/agents#multi-agent-teams)，我们使用 `coordinate` 模式：

```python
team_leader = Team(
    name="🏆 巴菲特-芒格投资分析团队",
    mode="coordinate",  # 协调模式
    model=self._create_model("qwen-max-latest"),
    members=[buffett_agent, munger_agent],
    tools=[ReasoningTools(add_instructions=True)],
    show_members_responses=True,  # 显示成员回应
    enable_agentic_context=True,  # 启用智能上下文
)
```

### 工作流程

1. **任务分发**: 团队领导者将分析任务分发给巴菲特和芒格 Agent
2. **独立分析**: 两位大师从各自角度进行深度分析
3. **观点收集**: 团队领导者收集两位大师的分析结果
4. **综合判断**: 寻找共识点和分歧点，形成综合建议
5. **报告输出**: 生成结构化的投资分析报告

## 分析报告结构

### 标准输出格式

```markdown
# 📊 [股票代码] 投资分析报告

## 1. 执行摘要
- 投资评级: [强烈买入/买入/持有/卖出/强烈卖出]
- 目标价格: $XXX - $XXX
- 投资时间框架: [短期/中期/长期]

## 2. 🎩 巴菲特观点
### 企业质量评估
### 估值分析  
### 投资建议

## 3. 🧠 芒格观点
### 逆向分析
### 多学科视角
### 认知偏误检查

## 4. 观点综合
### 共识点
### 分歧点
### 平衡建议

## 5. 团队建议
### 综合评级
### 行动方案
### 监控指标

## 6. 风险提示
### 主要风险
### 缓解措施
```

## 高级功能

### 1. 自定义分析重点

```python
# 重点关注ESG因素
task = """
请从ESG（环境、社会、治理）角度分析微软(MSFT)：
1. 环境责任和可持续发展
2. 社会影响和员工福利
3. 公司治理和透明度
4. ESG对长期投资价值的影响
"""
```

### 2. 行业对比分析

```python
# 行业对比
task = """
请对比分析科技巨头的投资价值：
- 苹果(AAPL) vs 微软(MSFT)
- 从护城河、成长性、估值等维度对比
- 给出配置建议
"""
```

### 3. 宏观环境分析

```python
# 宏观分析
task = """
在当前利率环境下，分析银行股的投资机会：
- 摩根大通(JPM)
- 考虑利率变化对银行业的影响
- 评估风险收益比
"""
```

## 技术特性

### 1. 实时数据获取

使用 YFinanceTools 获取最新的：
- 股价数据
- 财务报表
- 分析师建议
- 技术指标
- 公司新闻

### 2. 智能推理

使用 ReasoningTools 实现：
- 逐步推理过程
- 中间步骤展示
- 完整推理链条

### 3. 持久化存储

使用 SqliteStorage 保存：
- 对话历史
- 分析结果
- 团队状态

## 最佳实践

### 1. 提问技巧

**好的提问示例**:
```
请分析特斯拉(TSLA)在电动车市场的竞争优势，
重点评估其自动驾驶技术的商业价值和风险。
```

**避免的提问**:
```
特斯拉怎么样？
```

### 2. 分析深度控制

```python
# 快速分析
investment_team.print_response(task, stream=False)

# 详细分析（推荐）
investment_team.print_response(
    task,
    stream=True,
    stream_intermediate_steps=True,
    show_full_reasoning=True,
)
```

### 3. 结果解读

- **强烈买入**: 两位大师高度一致，风险较低
- **买入**: 总体积极，但存在一些分歧
- **持有**: 观点分化较大，建议谨慎
- **卖出**: 发现重大风险或高估

## 故障排除

### 常见问题

1. **API 密钥错误**
   ```bash
   export ALIYUN_API_KEY=your_actual_api_key
   ```

2. **模块导入错误**
   ```bash
   # 确保在项目根目录运行
   cd /path/to/agno_ai_investment
   python apps/investment_team.py
   ```

3. **网络连接问题**
   - 检查网络连接
   - 确认 API 服务可用

### 调试模式

```python
# 启用调试模式
investment_team.debug_mode = True
```

## 扩展开发

### 添加新的投资大师

```python
def create_peter_lynch_agent(self) -> Agent:
    """创建彼得·林奇 Agent"""
    instructions = [
        "你是 📈 Peter Lynch，成长价值投资大师...",
        # 添加具体指令
    ]
    
    return Agent(
        name="📈 Peter Lynch",
        role="成长价值投资专家",
        # 其他配置...
    )
```

### 自定义团队模式

```python
# 使用不同的团队模式
team_leader = Team(
    mode="collaborate",  # 协作模式
    # 或 mode="route"    # 路由模式
)
```

## 参考资源

- [Agno 官方文档](https://docs.agno.com/introduction/agents)
- [Multi-Agent Teams](https://docs.agno.com/introduction/agents#multi-agent-teams)
- [YFinance Tools](https://docs.agno.com/tools/yfinance)
- [Reasoning Tools](https://docs.agno.com/tools/reasoning)

## 更新日志

- **v1.0.0**: 初始版本，支持巴菲特-芒格双人团队
- **v1.1.0**: 添加演示程序和自定义分析功能
- **v1.2.0**: 优化报告结构和错误处理 