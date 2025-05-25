#!/usr/bin/env python3
"""
巴菲特-芒格投资分析团队
===================

基于 Agno Team 接口实现的投资大师团队
综合巴菲特和查理·芒格的投资观点进行股票分析

运行方式:
    python apps/investment_team.py

功能特点:
    - 巴菲特价值投资分析
    - 芒格多学科思维分析  
    - 团队协作综合观点
    - 实时股票数据获取
"""

import os
import sys
from dotenv import load_dotenv

# 添加src路径以导入模块
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.team.team import Team
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.sqlite import SqliteStorage

# 加载环境变量
load_dotenv()

class InvestmentMasterTeam:
    """投资大师团队类"""
    
    def __init__(self):
        """初始化投资大师团队"""
        self.storage_db = os.path.join(project_root, "data/agent_storage/investment_team.db")
        
    def _create_model(self, model_id: str = "qwen-plus-latest") -> OpenAILike:
        """创建模型实例"""
        return OpenAILike(
            id=model_id,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=os.getenv("ALIYUN_API_KEY")
        )
    
    def _create_tools(self) -> list:
        """创建工具集合"""
        return [
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
    
    def create_buffett_agent(self) -> Agent:
        """创建巴菲特投资分析 Agent"""
        instructions = [
            "你是 🎩 Warren Buffett，世界著名的价值投资大师，伯克希尔·哈撒韦公司的CEO。",
            "",
            "**投资哲学：**",
            "- 寻找具有持续竞争优势的优秀企业",
            "- 以合理价格买入优秀公司，而非以便宜价格买入平庸公司",
            "- 长期持有，让复利发挥作用",
            "- 投资于自己理解的业务",
            "- 关注企业的内在价值而非市场波动",
            "",
            "**分析重点：**",
            "- 企业的经济护城河（品牌、规模优势、转换成本等）",
            "- 管理层的诚信和能力",
            "- 财务指标：ROE、ROA、自由现金流、债务水平",
            "- 行业前景和竞争格局",
            "- 估值分析：PE、PB、DCF模型",
            "",
            "**语言风格：**",
            "- 使用简单易懂的比喻和故事",
            "- 强调长期投资的重要性",
            "- 经常引用'投资第一法则：不要亏钱；第二法则：永远不要忘记第一法则'",
            "- 谦逊但坚定地表达观点",
            "",
            "**分析框架：**",
            "1. 企业质量评估（护城河、管理层、财务健康度）",
            "2. 估值分析（内在价值 vs 市场价格）",
            "3. 投资建议（买入/持有/卖出及理由）",
            "4. 风险提示（主要风险因素）"
        ]
        
        return Agent(
            name="🎩 Warren Buffett",
            role="价值投资分析专家",
            model=self._create_model(),
            tools=self._create_tools(),
            instructions=instructions,
            storage=SqliteStorage(
                table_name="buffett_agent", 
                db_file=self.storage_db
            ),
            add_datetime_to_instructions=True,
            markdown=True
        )
    
    def create_munger_agent(self) -> Agent:
        """创建查理·芒格投资分析 Agent"""
        instructions = [
            "你是 🧠 Charlie Munger，巴菲特的黄金搭档，以多学科思维模型著称的投资智者。",
            "",
            "**投资哲学：**",
            "- 运用多学科思维模型进行投资决策",
            "- 逆向思考：考虑什么会导致投资失败",
            "- 寻找'显而易见'的投资机会",
            "- 专注于避免愚蠢，而非追求聪明",
            "- 理性思考，避免认知偏误",
            "",
            "**多学科思维模型：**",
            "- 心理学：投资者行为偏误、市场情绪",
            "- 经济学：供需关系、竞争优势、网络效应",
            "- 数学：概率思维、复利效应、统计分析",
            "- 物理学：临界点、反馈循环、系统思维",
            "- 生物学：适者生存、进化优势",
            "",
            "**分析特点：**",
            "- 逆向思考：首先考虑投资可能失败的原因",
            "- 跨学科分析：从多个角度审视投资机会",
            "- 关注人性和心理因素对投资的影响",
            "- 强调简单和常识的重要性",
            "- 重视企业文化和管理层品格",
            "",
            "**语言风格：**",
            "- 直言不讳，有时略显尖锐",
            "- 经常引用各学科的原理和案例",
            "- 强调'反过来想，总是反过来想'",
            "- 用简单的道理解释复杂的问题",
            "",
            "**分析框架：**",
            "1. 逆向分析（可能的失败因素）",
            "2. 多学科视角（心理学、经济学、数学等）",
            "3. 认知偏误检查（避免常见投资陷阱）",
            "4. 简化建议（用常识判断投资价值）"
        ]
        
        return Agent(
            name="🧠 Charlie Munger",
            role="多学科投资思维专家",
            model=self._create_model(),
            tools=self._create_tools(),
            instructions=instructions,
            storage=SqliteStorage(
                table_name="munger_agent", 
                db_file=self.storage_db
            ),
            add_datetime_to_instructions=True,
            markdown=True
        )
    
    def create_investment_team(self) -> Team:
        """创建巴菲特-芒格投资分析团队"""
        # 创建团队成员
        buffett_agent = self.create_buffett_agent()
        munger_agent = self.create_munger_agent()
        
        # 创建团队领导者
        team_leader = Team(
            name="🏆 巴菲特-芒格投资分析团队",
            mode="coordinate",  # 协调模式，让团队成员协作
            model=self._create_model("qwen-max-latest"),  # 使用更强的模型作为团队领导
            members=[buffett_agent, munger_agent],
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "你是巴菲特-芒格投资分析团队的协调者，负责综合两位投资大师的观点。",
                "",
                "**团队协调原则：**",
                "- 充分听取巴菲特的价值投资分析",
                "- 充分听取芒格的多学科思维分析",
                "- 寻找两位大师观点的共同点和分歧点",
                "- 提供平衡、全面的投资建议",
                "",
                "**最终报告结构：**",
                "1. **执行摘要**：核心投资建议和评级",
                "2. **巴菲特观点**：价值投资角度的分析要点",
                "3. **芒格观点**：多学科思维角度的分析要点",
                "4. **观点综合**：两位大师的共识与分歧",
                "5. **团队建议**：综合投资建议和行动方案",
                "6. **风险提示**：主要投资风险和注意事项",
                "",
                "**输出要求：**",
                "- 使用表格展示关键数据",
                "- 提供明确的投资评级（强烈买入/买入/持有/卖出/强烈卖出）",
                "- 包含具体的目标价格区间",
                "- 标注信息来源",
                "- 使用Markdown格式，结构清晰"
            ],
            markdown=True,
            show_members_responses=True,  # 显示团队成员的回应
            enable_agentic_context=True,  # 启用智能上下文
            add_datetime_to_instructions=True,
            success_criteria="团队已成功提供综合的投资分析报告，包含两位大师的观点和团队建议。"
        )
        
        return team_leader

def main():
    """主函数"""
    print("🚀 启动巴菲特-芒格投资分析团队")
    print("=" * 60)
    
    # 检查环境变量
    if not os.getenv("ALIYUN_API_KEY"):
        print("❌ 错误: 未设置 ALIYUN_API_KEY 环境变量")
        print("💡 请设置您的阿里云 API 密钥:")
        print("   export ALIYUN_API_KEY=your_api_key")
        return
    
    try:
        # 创建投资团队
        team_manager = InvestmentMasterTeam()
        investment_team = team_manager.create_investment_team()
        
        print("✅ 投资分析团队初始化完成")
        print("👥 团队成员:")
        for member in investment_team.members:
            print(f"   - {member.name}: {member.role}")
        print("")
        
        # 示例分析任务
        print("📊 开始股票分析任务...")
        print("")
        
        # 用户可以修改这里的股票代码和分析要求
        task = """
请分析苹果公司(AAPL)的投资价值，包括：

1. 基本面分析：财务状况、盈利能力、成长性
2. 竞争优势：护城河、品牌价值、生态系统
3. 估值分析：当前估值是否合理
4. 投资建议：买入/持有/卖出建议及目标价格
5. 风险评估：主要投资风险和注意事项

请提供详细的分析报告，并给出明确的投资建议。
        """
        
        # 执行分析
        investment_team.print_response(
            task,
            stream=True,
            stream_intermediate_steps=True,
            show_full_reasoning=True,
        )
        
    except Exception as e:
        print(f"❌ 团队运行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 