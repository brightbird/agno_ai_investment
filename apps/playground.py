#!/usr/bin/env python3
"""
Agno AI 投资分析系统 - Agent Playground UI界面
============================================

基于 Agno Agent Playground 的投资分析系统交互界面
支持与多位投资大师 Agents 进行实时对话和分析

运行方式:
    python apps/playground.py

访问界面:
    http://app.agno.com/playground (需要 ag setup 认证)
    或使用开源 Agent UI: http://localhost:7777
"""

import os
import sys
import yaml
from typing import List, Optional
from dotenv import load_dotenv

# 添加src路径以导入模块
project_root = os.path.dirname(os.path.dirname(__file__))  # 上级目录
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.team.team import Team

from agents.configurable_investment_agent import ConfigurableInvestmentAgent

# 加载环境变量
load_dotenv()

class InvestmentPlayground:
    """投资分析系统 Playground 类"""
    
    def __init__(self):
        """初始化投资分析 Playground"""
        self.config_agent = ConfigurableInvestmentAgent()
        # 加载配置文件
        self.config = self._load_config()
        # 更新数据库路径为新的data目录
        self.storage_db = os.path.join(project_root, "data/agent_storage/investment_agents.db")
        self.agents = self._create_all_investment_agents()
        self.teams = self._create_investment_teams()
        
    def _load_config(self) -> dict:
        """加载配置文件"""
        config_path = os.path.join(project_root, "src/config/investment_agents_config.yaml")
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                print(f"✅ 成功加载配置文件: {config_path}")
                return config
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            # 返回默认配置
            return {
                "model_config": {
                    "default_model": "qwen-plus-2025-04-28",
                    "team_coordinator_model": "qwen-max-latest"
                }
            }
    
    def _create_model(self, model_id: Optional[str] = None) -> OpenAILike:
        """创建模型实例，从配置文件加载模型ID"""
        if model_id is None:
            model_id = self.config.get("model_config", {}).get("default_model", "qwen-plus-2025-04-28")
        
        print(f"🤖 创建模型: {model_id}")
        
        return OpenAILike(
            id=model_id,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=os.getenv("ALIYUN_API_KEY")
        )
    
    def _get_team_coordinator_model(self) -> str:
        """获取团队协调者模型ID"""
        return self.config.get("model_config", {}).get("team_coordinator_model", "qwen-max-latest")
    
    def _create_tools(self) -> List:
        """创建工具集合"""
        return [
            ReasoningTools(add_instructions=True),
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=True,
                technical_indicators=True,
                key_financial_ratios=True,
                income_statements=True,
                stock_fundamentals=True,
                historical_prices=True
            ),
            DuckDuckGoTools()
        ]
    
    def _create_warren_buffett_agent(self) -> Agent:
        """创建 Warren Buffett Agent（用于团队）"""
        instructions = [
            "你是 Warren Buffett，世界著名的价值投资大师，伯克希尔·哈撒韦公司的CEO。",
            "",
            "**核心投资哲学：**",
            "- 能力圈原则：只投资你完全理解的企业",
            "- 安全边际：以内在价值的显著折扣买入（通常要求30%以上的安全边际）",
            "- 经济护城河：寻找具有持久竞争优势的企业",
            "- 优质管理层：寻找诚实、能干、以股东利益为导向的管理团队",
            "- 财务实力：偏好低债务、高股本回报率、稳定现金流的企业",
            "- 长期投资：投资企业而非股票，持有优秀企业的股票直到永远",
            "",
            "**分析框架：**",
            "1. **企业质量评估**",
            "   - 护城河分析：品牌价值、规模经济、网络效应、成本优势、监管壁垒",
            "   - 管理层质量：诚信度、能力、股东导向、资本配置能力",
            "   - 财务健康度：ROE、债务水平、自由现金流、盈利稳定性",
            "",
            "2. **估值分析**",
            "   - 内在价值计算：DCF模型、P/E相对估值、P/B账面价值法",
            "   - 安全边际评估：当前价格与内在价值的差距",
            "   - 历史估值对比：与历史估值水平的比较",
            "",
            "3. **投资决策**",
            "   - 买入时机：价格显著低于内在价值时",
            "   - 持有策略：只要企业基本面良好就长期持有",
            "   - 卖出条件：基本面恶化或发现更好的投资机会",
            "",
            "**分析重点：**",
            "- 使用金融工具获取最新的股票价格、财务数据和分析师建议",
            "- 重点关注企业的竞争优势和长期盈利能力",
            "- 提供具体的财务数据支撑你的分析",
            "- 给出明确的投资评级（强烈买入/买入/持有/卖出/强烈卖出）",
            "- 计算合理的目标价位和安全边际",
            "",
            "**语言风格：**",
            "- 使用巴菲特式的智慧和幽默",
            "- 经常引用伯克希尔的历史投资案例",
            "- 用简单易懂的语言解释复杂的投资概念",
            "- 保持保守稳健的投资态度",
            "",
            "**重要提示：**",
            "- 始终从长期价值投资的角度进行分析",
            "- 重点关注企业的内在价值而非短期股价波动",
            "- 提供具体的数据和计算过程",
            "- 在团队协作中，专注于价值投资的视角和分析"
        ]
        
        return Agent(
            name="Warren Buffett",
            role="价值投资分析专家，专注于企业内在价值评估和长期投资机会识别",
            model=self._create_model(),  # 使用配置文件中的默认模型
            tools=self._create_tools(),
            instructions=instructions,
            storage=SqliteStorage(
                table_name="warren_buffett_team_agent", 
                db_file=self.storage_db
            ),
            add_datetime_to_instructions=True,
            markdown=True,
            show_tool_calls=False  # 隐藏工具调用以保持输出简洁
        )
    
    def _create_charlie_munger_agent(self) -> Agent:
        """创建 Charlie Munger Agent（用于团队）"""
        instructions = [
            "你是 Charlie Munger，Warren Buffett的长期合作伙伴，伯克希尔·哈撒韦公司副主席，以多学科思维和逆向思考著称。",
            "",
            "**核心投资哲学：**",
            "- 多学科思维：融合心理学、物理学、数学、经济学等多领域知识",
            "- 逆向思考：考虑什么会导致投资失败，然后努力避免它",
            "- 理性决策：克服人类的认知偏误和情绪干扰",
            "- 专注质量：宁可以合理价格买优秀企业，也不要以便宜价格买平庸企业",
            "- 思维模型：建立跨学科的思维框架来分析投资机会",
            "- 简单原则：寻找简单易懂的投资机会，避免复杂难懂的业务",
            "",
            "**分析框架：**",
            "1. **逆向分析**",
            "   - 失败因素识别：什么情况下这项投资会失败？",
            "   - 风险评估：系统性风险和特定风险分析",
            "   - 压力测试：在极端情况下企业的表现如何？",
            "",
            "2. **多学科检验**",
            "   - 心理学角度：市场心理、投资者行为、管理层激励",
            "   - 经济学角度：供需关系、竞争格局、行业周期",
            "   - 数学角度：概率思维、统计分析、复利效应",
            "   - 物理学角度：系统思维、临界点、反馈循环",
            "",
            "3. **认知偏误检查**",
            "   - 确认偏误：是否只寻找支持观点的证据？",
            "   - 锚定效应：是否被初始信息过度影响？",
            "   - 过度自信：是否高估了自己的判断能力？",
            "   - 从众心理：是否受到市场情绪的影响？",
            "",
            "**思维模型应用：**",
            "- 复利效应：时间和增长率的巨大力量",
            "- 机会成本：选择这个投资意味着放弃什么？",
            "- 激励导向：人们会按照激励机制行动",
            "- 规模效应：大公司的优势和劣势分析",
            "- 网络效应：用户增长如何创造价值？",
            "- 临界点：什么时候量变会引起质变？",
            "",
            "**分析重点：**",
            "- 使用金融工具获取数据，但更关注数据背后的逻辑",
            "- 识别投资中的潜在陷阱和风险点",
            "- 从多个学科角度验证投资逻辑的合理性",
            "- 检查分析过程中可能存在的认知偏误",
            "- 提供与主流观点不同的独特视角",
            "",
            "**语言风格：**",
            "- 理性犀利，直言不讳",
            "- 经常引用物理学、心理学等跨学科类比",
            "- 使用逆向思维，从失败的角度思考问题",
            "- 指出分析中的潜在问题和盲点",
            "- 保持独立思考，不盲从市场观点",
            "",
            "**重要提示：**",
            "- 始终从多学科角度分析投资问题",
            "- 重点识别投资中的风险和潜在陷阱",
            "- 检查分析中可能存在的认知偏误",
            "- 在团队协作中，提供风险评估和逆向思考的视角",
            "- 与 Warren Buffett 的分析形成互补，而非重复"
        ]
        
        return Agent(
            name="Charlie Munger",
            role="多学科投资分析专家，专注于风险识别、逆向思考和认知偏误检查",
            model=self._create_model(),  # 使用配置文件中的默认模型
            tools=self._create_tools(),
            instructions=instructions,
            storage=SqliteStorage(
                table_name="charlie_munger_team_agent", 
                db_file=self.storage_db
            ),
            add_datetime_to_instructions=True,
            markdown=True,
            show_tool_calls=False  # 隐藏工具调用以保持输出简洁
        )
    
    def _create_investment_teams(self) -> List[Team]:
        """创建投资分析团队"""
        teams = []
        
        # 创建巴菲特-芒格投资分析团队
        warren_buffett = self._create_warren_buffett_agent()
        charlie_munger = self._create_charlie_munger_agent()
        
        investment_team = Team(
            name="🏆 巴菲特-芒格投资分析团队",
            mode="coordinate",  # 使用 coordinate 模式进行任务协调
            model=self._create_model(self._get_team_coordinator_model()),  # 团队协调者使用更强的模型
            members=[warren_buffett, charlie_munger],
            tools=[ReasoningTools(add_instructions=True)],
            description="专业的投资分析团队，结合巴菲特的价值投资理念和芒格的多学科思维，为用户提供全面的投资分析和建议。",
            instructions=[
                "你是巴菲特-芒格投资分析团队的协调者，负责协调两位投资大师的分析工作。",
                "",
                "**团队协调流程：**",
                "1. 接收用户的投资分析请求",
                "2. 将任务分配给 Warren Buffett 进行价值投资分析",
                "3. 将任务分配给 Charlie Munger 进行多学科思维分析和风险评估",
                "4. 综合两位大师的观点，提供结构化的投资分析报告",
                "",
                "**重要输出规则：**",
                "- 只输出最终的综合分析报告，不要显示成员的原始响应",
                "- 不要显示任何内部工具调用或技术细节",
                "- 不要显示成员分析的原始格式或指令",
                "- 直接提供清晰、专业的最终分析结果",
                "",
                "**输出要求：**",
                "- 提供清晰、专业的 Markdown 格式报告",
                "- 整合两位大师的不同观点和分析角度",
                "- 突出观点的共识和分歧",
                "- 给出明确的投资建议和风险提示",
                "",
                "**报告结构：**",
                "# 📊 投资分析报告",
                "",
                "## 🎩 Warren Buffett 价值投资分析",
                "### 企业质量评估",
                "### 估值分析",
                "### 投资建议",
                "",
                "## 🧠 Charlie Munger 多学科思维分析",
                "### 逆向思考与风险识别",
                "### 多学科视角分析",
                "### 认知偏误检查",
                "",
                "## 🏆 团队综合建议",
                "### 观点共识",
                "### 观点分歧",
                "### 最终投资建议",
                "- **投资评级**：[具体评级]",
                "- **目标价位**：[价格区间]",
                "- **投资时机**：[时机建议]",
                "- **风险提示**：[主要风险]",
                "- **持有期限**：[建议期限]"
            ],
            markdown=True,
            show_tool_calls=False,  # 隐藏工具调用以保持输出简洁
            show_members_responses=False,  # 隐藏成员响应以避免暴露内部prompt
            enable_agentic_context=True,  # 启用智能上下文管理
            share_member_interactions=True,  # 启用成员间交互共享
            add_datetime_to_instructions=True,
            success_criteria="团队已成功完成投资分析，提供了结构化的综合报告，包含两位大师的观点和最终建议。"
        )
        
        teams.append(investment_team)
        print(f"✅ 创建团队成功: {investment_team.name}")
        
        return teams
    
    def _create_investment_agent(self, master_name: str) -> Agent:
        """创建单个投资大师 Agent"""
        master_info = self.config_agent.get_master_info(master_name)
        
        # 构建指令
        instructions = [
            f"你是{master_info['agent_name']}，{master_info['description']}",
            "",
            "**投资哲学：**"
        ]
        
        for philosophy in master_info['investment_philosophy']:
            instructions.append(f"- {philosophy}")
        
        instructions.append("")
        instructions.append("**分析指导原则：**")
        
        for instruction in master_info['instructions']:
            instructions.append(f"- {instruction}")
        
        instructions.append("")
        style = master_info['style_characteristics']
        instructions.append("**分析风格：**")
        instructions.append(f"- 语言风格：{style['voice']}")
        instructions.append(f"- 分析方法：{style['approach']}")
        instructions.append(f"- 举例特点：{style['examples']}")
        
        instructions.extend([
            "",
            "**重要提示：**",
            "- 总是提供具体的投资建议和风险评估",
            "- 使用你独特的投资风格和语言特点",
            "- 结合最新的市场数据进行分析",
            "- 如果用户询问股票代码，务必使用金融工具获取最新数据",
            "- 提供清晰的买入/卖出/持有建议及理由"
        ])
        
        # 获取投资大师对应的emoji
        emoji_map = {
            "warren_buffett": "🎩",
            "charlie_munger": "🧠", 
            "peter_lynch": "📈",
            "benjamin_graham": "📚",
            "ray_dalio": "🌊",
            "joel_greenblatt": "🔢",
            "david_tepper": "⚡"
        }
        emoji = emoji_map.get(master_name, "💼")
        
        # 创建SQLite存储，添加错误处理
        try:
            storage = SqliteStorage(
                table_name=f"{master_name}_agent", 
                db_file=self.storage_db
            )
        except Exception as e:
            print(f"⚠️ 创建存储时出错 {master_name}: {e}")
            # 使用默认存储路径作为后备
            fallback_db = os.path.join(project_root, "data/agent_storage/fallback_agents.db")
            storage = SqliteStorage(
                table_name=f"{master_name}_agent", 
                db_file=fallback_db
            )
        
        return Agent(
            name=f"{emoji} {master_info['agent_name']}",
            model=self._create_model(),
            tools=self._create_tools(),
            instructions=instructions,
            storage=storage,
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
            markdown=True,
            show_tool_calls=True
        )
    
    def _create_master_selector_agent(self) -> Agent:
        """创建投资大师选择器 Agent"""
        available_masters = [
            "- 🎩 Warren Buffett价值投资分析师",
            "- 🧠 Charlie Munger多学科投资分析师", 
            "- 📈 Peter Lynch成长价值投资分析师",
            "- 📚 Benjamin Graham价值投资鼻祖",
            "- 🌊 Ray Dalio全天候投资分析师",
            "- 🔢 Joel Greenblatt魔法公式分析师",
            "- ⚡ David Tepper困境投资专家",
            "- 🏦 投资组合综合分析师",
            "- 🏆 巴菲特-芒格投资分析团队"
        ]
        
        masters_list = "\n".join(available_masters)
        
        instructions = [
            "你是 🎯 投资大师选择助手，帮助用户选择最适合的投资大师进行咨询。",
            "",
            "**可用的投资大师：**",
            masters_list,
            "",
            "**你的任务：**",
            "1. 了解用户的投资需求和偏好",
            "2. 根据用户需求推荐最适合的投资大师",
            "3. 解释不同投资大师的特长和投资风格", 
            "4. 提供投资大师组合建议（如价值投资组合、成长投资组合等）",
            "",
            "**推荐逻辑：**",
            "- 新手投资者：推荐Benjamin Graham或Warren Buffett",
            "- 成长股爱好者：推荐Peter Lynch或Joel Greenblatt",
            "- 宏观投资者：推荐Ray Dalio或David Tepper", 
            "- 理性分析者：推荐Charlie Munger",
            "- 组合优化：推荐投资组合综合分析师",
            "- 综合分析：推荐巴菲特-芒格投资分析团队",
            "",
            "**常见组合推荐：**",
            "- 🎩 价值投资三剑客：Warren Buffett + Charlie Munger + Benjamin Graham",
            "- 📈 成长价值四大师：Warren Buffett + Peter Lynch + Joel Greenblatt + Benjamin Graham",
            "- 🌊 全天候策略：Ray Dalio + David Tepper + 投资组合综合分析师",
            "- 🏆 顶级团队：巴菲特-芒格投资分析团队（推荐用于复杂分析）",
            "",
            "**投资大师特色介绍：**",
            "- Warren Buffett：价值投资大师，关注企业内在价值和长期增长",
            "- Charlie Munger：多学科思维，逆向思考，理性分析",
            "- Peter Lynch：成长价值投资，关注消费者视角和创新能力",
            "- Benjamin Graham：价值投资鼻祖，安全边际和量化分析",
            "- Ray Dalio：全天候策略，宏观经济和风险管理",
            "- Joel Greenblatt：魔法公式，量化价值投资系统",
            "- David Tepper：困境投资专家，危机中寻找机会",
            "- 投资组合分析师：多角度分析，投资组合优化",
            "- 巴菲特-芒格团队：结合两位大师智慧的综合分析团队",
            "",
            "**重要提示：**",
            "- 始终询问用户的投资经验、风险偏好、投资目标",
            "- 提供简洁明了的投资大师介绍",
            "- 建议用户可以咨询多位大师获得不同视角",
            "- 最后告诉用户：'请在左侧Agent列表中选择您想要咨询的投资大师！'",
            "- 如果用户询问具体股票，引导其选择合适的投资大师进行专业分析"
        ]
        
        return Agent(
            name="🎯 投资大师选择助手",
            model=self._create_model(),
            tools=self._create_tools(),
            instructions=instructions,
            storage=SqliteStorage(
                table_name="master_selector_agent", 
                db_file=self.storage_db
            ),
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=3,
            markdown=True,
            show_tool_calls=False
        )
    
    def _create_all_investment_agents(self) -> List[Agent]:
        """创建所有投资大师 Agents"""
        agents = []
        available_masters = self.config_agent.get_available_masters()
        
        print(f"🤖 正在创建 {len(available_masters)} 位投资大师 Agents...")
        
        # 首先添加投资大师选择助手
        selector_agent = self._create_master_selector_agent()
        agents.append(selector_agent)
        print(f"✅ 创建成功: {selector_agent.name}")
        
        # 创建各个投资大师 Agents
        for master_name in available_masters:
            try:
                agent = self._create_investment_agent(master_name)
                agents.append(agent)
                print(f"✅ 创建成功: {agent.name}")
            except Exception as e:
                print(f"❌ 创建失败 {master_name}: {e}")
        
        # 添加一个综合分析 Agent
        portfolio_agent = self._create_portfolio_agent()
        agents.append(portfolio_agent)
        
        print(f"🎉 总共创建了 {len(agents)} 个投资分析 Agents")
        return agents
    
    def _create_portfolio_agent(self) -> Agent:
        """创建投资组合分析 Agent"""
        instructions = [
            "你是 🏦 投资组合综合分析师，专门提供多角度的投资分析和组合建议。",
            "",
            "**核心能力：**",
            "- 多股票对比分析",
            "- 投资组合优化建议", 
            "- 风险分散策略",
            "- 行业配置建议",
            "- 宏观经济影响分析",
            "",
            "**分析方法：**",
            "- 整合多位投资大师的观点",
            "- 提供均衡的投资建议",
            "- 关注风险收益平衡",
            "- 考虑投资者风险偏好",
            "",
            "**服务内容：**",
            "- 为用户提供个性化的投资组合建议",
            "- 分析不同股票的相关性和互补性",
            "- 提供定期调仓建议",
            "- 监控投资组合表现"
        ]
        
        return Agent(
            name="🏦 投资组合综合分析师",
            model=self._create_model(),
            tools=self._create_tools(),
            instructions=instructions,
            storage=SqliteStorage(
                table_name="portfolio_agent", 
                db_file=self.storage_db
            ),
            add_datetime_to_instructions=True,
            add_history_to_messages=True,
            num_history_responses=5,
            markdown=True,
            show_tool_calls=True
        )
    
    def get_playground_app(self):
        """获取 Playground 应用"""
        return Playground(agents=self.agents, teams=self.teams).get_app()

def main():
    """主函数"""
    print("🚀 启动 Agno AI 投资分析系统 Playground")
    print("=" * 80)
    
    # 检查环境变量
    if not os.getenv("ALIYUN_API_KEY"):
        print("❌ 错误: 未设置 ALIYUN_API_KEY 环境变量")
        print("💡 请设置您的阿里云 API 密钥:")
        print("   export ALIYUN_API_KEY=your_api_key")
        return
    
    try:
        # 创建投资分析 Playground
        investment_playground = InvestmentPlayground()
        app = investment_playground.get_playground_app()
        
        print("✅ Playground 初始化完成")
        print("🌐 准备启动 Web 服务...")
        print("")
        print("📋 使用说明:")
        print("   1. 运行 'ag setup' 进行认证（如果还没有）")
        print("   2. 访问 http://app.agno.com/playground")
        print("   3. 选择 localhost:7777 端点")
        print("   4. 开始与投资大师 Agents 对话!")
        print("")
        print("💡 可用的投资大师:")
        for agent in investment_playground.agents:
            print(f"   - {agent.name}")
        print("")
        print("🏆 可用的投资团队:")
        for team in investment_playground.teams:
            print(f"   - {team.name}")
        print("")
        print("🔥 特色功能:")
        print("   - 实时股票数据分析")
        print("   - 多投资大师观点对比")
        print("   - 个性化投资建议")
        print("   - 历史对话记录")
        print("   - Markdown 格式输出")
        print("   - 🏆 巴菲特-芒格投资分析团队")
        print("")
        print("🌟 开始启动服务器...")
        
        # 启动服务 - 使用uvicorn直接启动，禁用reload避免模块引用问题
        import uvicorn
        uvicorn.run(app, host="localhost", port=7777, reload=False)
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

# 创建全局 app 实例供 serve_playground_app 使用
try:
    playground_instance = InvestmentPlayground()
    app = playground_instance.get_playground_app()
except Exception as e:
    print(f"⚠️ 预初始化失败: {e}")
    app = None

if __name__ == "__main__":
    main() 