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
from agno.team import Team

from agents.configurable_investment_agent import ConfigurableInvestmentAgent

# 加载环境变量
load_dotenv()

class InvestmentPlayground:
    """投资分析系统 Playground 类"""
    
    def __init__(self):
        """初始化投资分析 Playground"""
        self.config_agent = ConfigurableInvestmentAgent()
        # 更新数据库路径为新的data目录
        self.storage_db = os.path.join(project_root, "data/agent_storage/investment_agents.db")
        self.agents = self._create_all_investment_agents()
        
    def _create_model(self, model_id: str = "qwen-plus-latest") -> OpenAILike:
        """创建模型实例"""
        return OpenAILike(
            id=model_id,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=os.getenv("ALIYUN_API_KEY")
        )
    
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
        
        return Agent(
            name=f"{emoji} {master_info['agent_name']}",
            model=self._create_model(),
            tools=self._create_tools(),
            instructions=instructions,
            storage=SqliteStorage(
                table_name=f"{master_name}_agent", 
                db_file=self.storage_db
            ),
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
            "- 🏦 投资组合综合分析师"
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
            "",
            "**常见组合推荐：**",
            "- 🎩 价值投资三剑客：Warren Buffett + Charlie Munger + Benjamin Graham",
            "- 📈 成长价值四大师：Warren Buffett + Peter Lynch + Joel Greenblatt + Benjamin Graham",
            "- 🌊 全天候策略：Ray Dalio + David Tepper + 投资组合综合分析师",
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
        return Playground(agents=self.agents).get_app()

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
        print("🔥 特色功能:")
        print("   - 实时股票数据分析")
        print("   - 多投资大师观点对比")
        print("   - 个性化投资建议")
        print("   - 历史对话记录")
        print("   - Markdown 格式输出")
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