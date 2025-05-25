# 配置使用指南

## 🛠️ 模型配置

### 如何修改默认模型

系统的模型配置位于 `src/config/investment_agents_config.yaml` 文件中：

```yaml
model_config:
  default_model: "qwen-plus-latest"  # 👈 在这里修改默认模型
  available_models:
    - "qwen-plus-latest"
    - "qwen-max"
    - "qwen-turbo"
```

### 可用模型说明

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| `qwen-plus-latest` | 平衡性能和成本 | 推荐日常使用 |
| `qwen-max` | 最高性能 | 复杂分析任务 |
| `qwen-turbo` | 快速响应 | 简单查询 |

### 使用方式

#### 1. 使用配置文件默认模型
```python
# 自动使用配置文件中的default_model
analyzer = MultiAgentInvestmentAnalyzerV2()
```

#### 2. 手动指定模型
```python
# 覆盖配置文件设置
analyzer = MultiAgentInvestmentAnalyzerV2(model_id="qwen-max")
```

#### 3. 针对特定大师指定模型
```python
# 在configurable_investment_agent中为特定大师指定模型
agent = agent_factory.create_agent("warren_buffett", model_id="qwen-max")
```

## 🔧 配置修复说明

### 问题
之前系统存在硬编码模型ID的问题，即使修改了配置文件中的`default_model`，系统仍然使用硬编码的`"qwen-plus"`。

### 解决方案
- 添加了`load_default_model_from_config()`函数来从配置文件读取默认模型
- 修改了`EnhancedInvestmentSynthesizer`和`MultiAgentInvestmentAnalyzerV2`类，使其在未指定模型时自动从配置文件读取
- 保持了手动指定模型的优先级

### 验证
运行 `python test_model_config.py` 来验证配置加载是否正常。

## 📋 配置文件结构

完整的配置文件包含以下部分：

1. **模型配置** (`model_config`)
2. **输出格式** (`analysis_output`)
3. **投资大师配置** (`investment_masters`)

每个投资大师都有独立的配置，包括：
- 投资哲学 (`investment_philosophy`)
- 分析指令 (`instructions`)
- 分析框架 (`analysis_framework`)
- 风格特征 (`style_characteristics`)

## 🚀 最佳实践

1. **开发环境**: 使用 `qwen-plus-latest` 平衡成本和性能
2. **生产环境**: 根据需求选择合适模型
3. **复杂分析**: 使用 `qwen-max` 获得最佳结果
4. **快速测试**: 使用 `qwen-turbo` 加快响应速度

## ⚠️ 注意事项

- 确保阿里云API密钥正确配置在环境变量中
- 不同模型的token限制和价格不同
- 修改配置文件后重启应用以生效
- 系统会在模型配置加载失败时使用fallback模型 