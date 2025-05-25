# Agno AI 投资分析系统 - Agent Playground 使用指南

## 🌟 概述

基于 Agno Agent Playground 的投资分析系统交互界面，提供与多位投资大师 AI Agents 的实时对话功能。

## 🎯 特色功能

### 💼 投资大师 Agents
- **🎩 Warren Buffett** - 价值投资分析师
- **🧠 Charlie Munger** - 多学科投资分析师  
- **📈 Peter Lynch** - 成长价值投资分析师
- **📚 Benjamin Graham** - 价值投资鼻祖
- **🌊 Ray Dalio** - 全天候投资分析师
- **🔢 Joel Greenblatt** - 魔法公式分析师
- **⚡ David Tepper** - 困境投资专家
- **🏦 投资组合综合分析师** - 多角度投资组合建议

### 🔥 核心能力
- 📊 实时股票数据分析
- 💡 个性化投资建议
- 📈 技术指标分析
- 📰 最新财经新闻整合
- 🔍 公司基本面分析
- 📋 投资组合优化建议
- 💬 历史对话记录
- 📝 Markdown 格式输出

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export ALIYUN_API_KEY=your_aliyun_api_key
```

### 2. 启动 Playground

```bash
# 启动服务
python playground.py
```

### 3. 认证设置

#### 方式一：官方 Playground（推荐）
```bash
# 进行认证
ag setup

# 或设置 API 密钥
export AGNO_API_KEY=ag-your_api_key
```

#### 方式二：开源 Agent UI
```bash
# 克隆开源UI
git clone https://github.com/agno-agi/agent-ui.git
cd agent-ui && pnpm install && pnpm dev
```

### 4. 访问界面

- **官方界面**: http://app.agno.com/playground
- **开源界面**: http://localhost:3000
- **API服务**: http://localhost:7777

## 💬 使用示例

### 基础股票分析

**用户**: "帮我分析一下苹果公司(AAPL)的投资价值"

**巴菲特**: 会从价值投资角度分析：
- 护城河分析
- 内在价值评估  
- 安全边际计算
- 长期竞争优势

### 多角度对比

在不同的 Agent 间切换，获得不同投资大师的观点：

- **彼得·林奇**: 关注消费者角度和成长性
- **雷·达里奥**: 从宏观经济和风险管理角度
- **芒格**: 多学科思维和逆向思考

### 投资组合建议

**用户**: "我有10万元，想投资科技股，请给我配置建议"

**投资组合分析师**: 会提供：
- 行业配置比例
- 具体股票推荐
- 风险分散策略
- 定期调仓建议

## 🔧 高级功能

### 1. 工具集成

每个 Agent 都配备了专业工具：

- **YFinance**: 实时股价、财报、技术指标
- **DuckDuckGo**: 最新财经新闻和市场动态
- **Reasoning**: 逻辑推理和决策分析

### 2. 对话历史

- 自动保存对话记录
- 支持上下文连续对话
- 历史分析回顾

### 3. 个性化体验

- 每个投资大师独特的语言风格
- 符合其投资理念的分析方法
- 专业的投资术语和案例引用

## 📊 实用场景

### 1. 日常投资决策
- "今天美股大跌，我应该加仓还是观望？"
- "苹果发布新产品，对股价有什么影响？"

### 2. 投资组合优化
- "我的投资组合风险太集中，如何优化？"
- "科技股占比过高，应该如何调整？"

### 3. 学习投资理念
- "巴菲特和林奇的投资方法有什么区别？"
- "什么是价值投资的安全边际？"

### 4. 市场分析
- "当前市场环境下，应该采用什么投资策略？"
- "通胀对不同行业的影响如何？"

## ⚙️ 配置选项

### 模型设置
在 `src/config/investment_agents_config.yaml` 中可以调整：
- 默认模型选择
- 分析输出格式
- 工具调用显示

### Agent 定制
可以修改每个投资大师的：
- 投资哲学和指令
- 分析框架
- 语言风格特征

## 🛠️ 故障排除

### 常见问题

1. **连接失败**
   ```bash
   # 检查API密钥
   echo $ALIYUN_API_KEY
   
   # 检查网络连接
   curl -I https://dashscope.aliyuncs.com
   ```

2. **Agent 创建失败**
   - 检查配置文件格式
   - 确认所有依赖已安装
   - 查看错误日志

3. **浏览器兼容性**
   - Chrome/Firefox 推荐
   - Safari/Brave 可能需要特殊设置

### 性能优化

- 使用 `qwen-plus-latest` 获得最佳性能
- 启用 Token 优化减少API成本
- 合理设置对话历史长度

## 📱 移动端支持

Playground 界面支持移动设备访问，可以在手机上进行投资分析和决策。

## 🔗 相关资源

- [Agno 官方文档](https://docs.agno.com)
- [Agent UI 开源项目](https://github.com/agno-agi/agent-ui)
- [投资分析系统配置指南](./CONFIGURATION_GUIDE.md)
- [主要功能使用说明](./README.md)

## 🆘 技术支持

如遇到问题，请：
1. 查看控制台错误信息
2. 检查网络和API配置
3. 参考本文档的故障排除部分
4. 在 GitHub 上提交 Issue

---

🎉 **开始您的智能投资分析之旅！** 