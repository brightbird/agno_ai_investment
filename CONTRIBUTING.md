# 🤝 贡献指南

感谢您对 Agno AI 投资分析系统的关注！我们欢迎所有形式的贡献。

## 🌟 贡献方式

### 💡 功能建议
- 在 [Issues](../../issues) 中创建功能请求
- 描述您希望添加的功能及其用途
- 讨论实现方案

### 🐛 报告问题
- 在 [Issues](../../issues) 中报告 Bug
- 提供详细的错误信息和复现步骤
- 包含系统环境信息

### 💻 代码贡献
1. Fork 项目
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 进行开发
4. 提交代码: `git commit -m 'Add some amazing feature'`
5. 推送分支: `git push origin feature/amazing-feature`
6. 创建 Pull Request

## 🔧 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/your-username/agno_ai_investment.git
cd agno_ai_investment
```

### 2. 设置虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

### 4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，添加您的 API 密钥
```

### 5. 运行测试
```bash
pytest tests/
```

## 📝 代码规范

### Python 代码风格
- 遵循 [PEP 8](https://pep8.org/) 规范
- 使用 `black` 进行代码格式化
- 使用 `flake8` 进行代码检查
- 最大行长度：88 字符

### 提交信息规范
使用语义化提交信息：
- `feat:` 新功能
- `fix:` 错误修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建或辅助工具变动

示例：
```
feat: 添加新的投资大师 Ray Dalio
fix: 修复股票数据获取错误
docs: 更新 README 使用说明
```

## 🧪 测试指南

### 单元测试
- 为新功能编写测试
- 确保测试覆盖率 > 80%
- 使用有意义的测试名称

### 集成测试
- 测试 Agent 创建和交互
- 测试 API 端点
- 测试数据库操作

## 📚 添加投资大师

### 1. 配置投资大师
在 `src/agents/configurable_investment_agent.py` 中添加：

```python
def get_master_config(self, master_name: str):
    masters = {
        "new_master": {
            "agent_name": "新投资大师",
            "description": "描述",
            "investment_philosophy": ["理念1", "理念2"],
            "instructions": ["指令1", "指令2"],
            "style_characteristics": {
                "voice": "语言风格",
                "approach": "分析方法",
                "examples": "举例特点"
            }
        }
    }
```

### 2. 添加 emoji 图标
在 `apps/playground.py` 的 `emoji_map` 中添加：
```python
emoji_map = {
    "new_master": "🎯",
    # ...
}
```

### 3. 编写测试
为新投资大师编写单元测试。

## 🔒 安全指南

### API 密钥处理
- **绝不**在代码中硬编码 API 密钥
- 使用环境变量存储敏感信息
- 在 `.gitignore` 中排除配置文件
- 提供 `.env.example` 模板

### 数据安全
- 不在代码中存储真实的财务数据
- 确保用户对话隐私
- 定期更新依赖包

## 📖 文档贡献

### 文档类型
- **用户文档**: 面向最终用户的使用指南
- **开发文档**: 面向开发者的技术文档
- **API 文档**: API 接口说明

### 文档规范
- 使用 Markdown 格式
- 包含代码示例
- 添加截图说明（如适用）
- 保持中英文版本同步

## 🏷️ 发布流程

### 版本号规范
遵循 [语义化版本](https://semver.org/lang/zh-CN/)：
- **主版本号**: 不兼容的 API 修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的 Bug 修复

### 发布清单
- [ ] 更新版本号
- [ ] 更新 CHANGELOG.md
- [ ] 运行完整测试套件
- [ ] 更新文档
- [ ] 创建 Git tag
- [ ] 发布 GitHub Release

## ❓ 获取帮助

如果您有任何问题：

1. **查看文档**: 先查看项目文档和 Wiki
2. **搜索 Issues**: 查看是否已有相关问题
3. **创建 Issue**: 描述您的问题
4. **参与讨论**: 在 Discussions 中交流

## 👥 社区

- **GitHub Discussions**: 项目讨论和问答
- **Issues**: Bug 报告和功能请求
- **Pull Requests**: 代码贡献

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

再次感谢您的贡献！每一个贡献都让这个项目变得更好。 🎉 