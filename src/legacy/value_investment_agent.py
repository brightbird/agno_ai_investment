"""
价值投资Agent - 使用Agno框架
基于价值投资理念分析股票，提供投资建议
整合多位投资大师的观点
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from multi_agent_investment import MultiAgentInvestmentAnalyzer

# 加载环境变量
load_dotenv()

class ValueInvestmentAgent:
    def __init__(self, model_id="qwen-plus"):
        """
        初始化价值投资Agent
        
        Args:
            model_id: 阿里云百炼模型ID，可选：
                     - qwen-plus (推荐，平衡性能和成本)
                     - qwen-max (最强性能)
                     - qwen-turbo (最快速度)
                     - qwen2.5-72b-instruct
                     - qwen2.5-32b-instruct
        """
        # 使用阿里云百炼API
        model = OpenAILike(
            id=model_id,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=os.getenv("ALIYUN_API_KEY")
        )
        
        # 创建单一综合Agent
        self.agent = Agent(
            name="巴菲特式价值投资分析师",
            model=model,
            tools=[
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
            ],
            instructions=[
                "你是一位专业的价值投资分析师，遵循巴菲特和格雷厄姆的投资理念",
                "进行深入的基本面分析，重点关注：",
                "1. 财务健康状况：债务水平、现金流、ROE、ROA等",
                "2. 估值指标：PE、PB、PEG、股息收益率等",
                "3. 竞争优势：护城河、市场地位、品牌价值等",
                "4. 管理层质量：资本配置能力、股东回报等",
                "5. 行业前景：增长潜力、竞争格局等",
                "使用表格清晰展示财务数据",
                "提供明确的投资建议：买入/持有/卖出，并说明理由",
                "所有分析必须基于事实和数据，避免情绪化判断",
                "如果数据不足，要明确指出并建议进一步研究的方向"
            ],
            markdown=True,
            show_tool_calls=True
        )
        
        # 初始化多Agent分析器
        self.multi_agent_analyzer = MultiAgentInvestmentAnalyzer(model_id)
    
    def analyze_stock(self, symbol, show_reasoning=True):
        """
        分析单只股票
        
        Args:
            symbol: 股票代码，如 'AAPL', 'TSLA'
            show_reasoning: 是否显示推理过程
        """
        prompt = f"""
        请对股票 {symbol} 进行全面的价值投资分析。

        分析框架：
        1. **公司概况** - 基本信息、业务模式、行业地位
        2. **财务健康状况分析**
           - 资产负债表分析
           - 现金流状况
           - 盈利能力指标
        3. **估值分析**
           - 关键估值比率（PE、PB、PEG等）
           - 与历史均值和行业均值的比较
           - DCF估值（如果可能）
        4. **竞争优势分析**
           - 护城河评估
           - 市场地位
           - 技术或品牌优势
        5. **风险评估**
           - 主要风险因素
           - 行业风险
           - 公司特定风险
        6. **投资建议**
           - 明确的买入/持有/卖出建议
           - 目标价位（如果适用）
           - 投资逻辑总结

        请确保所有分析都基于最新的财务数据和市场信息。
        """
        
        print(f"\n🔍 开始分析股票: {symbol}")
        print("=" * 50)
        
        self.agent.print_response(
            prompt,
            stream=True,
            show_full_reasoning=show_reasoning,
            stream_intermediate_steps=True
        )
    
    def analyze_stock_multi_master(self, symbol, show_reasoning=False):
        """
        使用多位投资大师的观点分析股票
        
        Args:
            symbol: 股票代码
            show_reasoning: 是否显示推理过程
        """
        print(f"\n🎯 启动多大师投资分析: {symbol}")
        print("🏆 整合Warren Buffett和Charlie Munger的投资智慧")
        print("=" * 60)
        
        return self.multi_agent_analyzer.analyze_stock_multi_perspective(
            symbol, 
            parallel=True, 
            show_reasoning=show_reasoning
        )
    
    def compare_stocks(self, symbols, show_reasoning=False):
        """
        比较多只股票
        
        Args:
            symbols: 股票代码列表，如 ['AAPL', 'MSFT', 'GOOGL']
            show_reasoning: 是否显示推理过程
        """
        symbols_str = ', '.join(symbols)
        prompt = f"""
        请比较以下股票的投资价值：{symbols_str}

        比较维度：
        1. **财务指标对比**
           - 盈利能力（ROE、ROA、净利润率）
           - 成长性（营收增长、利润增长）
           - 估值水平（PE、PB、PEG）
           - 财务健康（债务比率、现金比率）

        2. **竞争优势对比**
           - 各自的护城河
           - 市场地位对比
           - 业务模式分析

        3. **风险收益评估**
           - 风险水平对比
           - 预期收益评估
           - 投资时间期限建议

        4. **投资建议排序**
           - 按投资价值排序
           - 每只股票的具体建议
           - 投资组合建议

        请使用表格对比关键指标，并给出明确的投资优先级。
        """
        
        print(f"\n📊 开始比较股票: {symbols_str}")
        print("=" * 50)
        
        self.agent.print_response(
            prompt,
            stream=True,
            show_full_reasoning=show_reasoning
        )
    
    def compare_stocks_multi_master(self, symbols, show_reasoning=False):
        """
        使用多位投资大师的观点比较多只股票
        
        Args:
            symbols: 股票代码列表
            show_reasoning: 是否显示推理过程
        """
        print(f"\n📊 启动多大师股票对比分析")
        print("🏆 整合多位投资大师的对比观点")
        print("=" * 60)
        
        return self.multi_agent_analyzer.compare_stocks_multi_perspective(
            symbols, 
            show_reasoning=show_reasoning
        )
    
    def market_sector_analysis(self, sector, show_reasoning=False):
        """
        分析特定行业或板块
        
        Args:
            sector: 行业名称，如 "科技股"、"银行股"、"新能源"等
            show_reasoning: 是否显示推理过程
        """
        prompt = f"""
        请对 {sector} 行业进行价值投资角度的分析：

        分析内容：
        1. **行业概况**
           - 行业规模和增长趋势
           - 主要驱动因素
           - 政策环境影响

        2. **竞争格局**
           - 主要参与者分析
           - 市场集中度
           - 竞争优势来源

        3. **价值投资机会**
           - 行业内优质公司筛选
           - 估值水平分析
           - 长期投资逻辑

        4. **风险因素**
           - 周期性风险
           - 技术变革风险
           - 监管风险

        5. **投资建议**
           - 推荐的投资标的
           - 投资时机建议
           - 风险控制措施

        请重点关注具有长期竞争优势和合理估值的投资机会。
        """
        
        print(f"\n🏭 开始分析行业: {sector}")
        print("=" * 50)
        
        self.agent.print_response(
            prompt,
            stream=True,
            show_full_reasoning=show_reasoning
        )

def main():
    """主函数 - 演示价值投资Agent的功能"""
    print("🤖 价值投资Agent启动中...")
    print("基于Agno框架，整合多位投资大师的智慧")
    print("=" * 60)
    
    # 创建Agent实例
    agent = ValueInvestmentAgent()
    
    while True:
        print(f"\n📋 请选择分析模式:")
        print("1. 单一Agent分析")
        print("2. 多大师对比分析 (推荐)")
        print("3. 行业分析")
        print("4. 退出")
        
        mode = input("\n请输入选择 (1-4): ").strip()
        
        if mode == "1":
            print(f"\n📋 单一Agent分析选项:")
            print("1. 单股分析")
            print("2. 多股对比")
            
            choice = input("请输入选择 (1-2): ").strip()
            
            if choice == "1":
                symbol = input("请输入股票代码 (如 AAPL): ").strip().upper()
                if symbol:
                    agent.analyze_stock(symbol, show_reasoning=False)
            
            elif choice == "2":
                symbols_input = input("请输入股票代码，用逗号分隔 (如 AAPL,MSFT,GOOGL): ").strip().upper()
                if symbols_input:
                    symbols = [s.strip() for s in symbols_input.split(",")]
                    agent.compare_stocks(symbols, show_reasoning=False)
        
        elif mode == "2":
            print(f"\n🏆 多大师分析选项:")
            print("1. 单股多视角分析")
            print("2. 多股多视角对比")
            
            choice = input("请输入选择 (1-2): ").strip()
            
            if choice == "1":
                symbol = input("请输入股票代码 (如 AAPL): ").strip().upper()
                if symbol:
                    agent.analyze_stock_multi_master(symbol, show_reasoning=False)
            
            elif choice == "2":
                symbols_input = input("请输入股票代码，用逗号分隔 (如 AAPL,MSFT,GOOGL): ").strip().upper()
                if symbols_input:
                    symbols = [s.strip() for s in symbols_input.split(",")]
                    agent.compare_stocks_multi_master(symbols, show_reasoning=False)
        
        elif mode == "3":
            sector = input("请输入行业名称 (如 人工智能、新能源等): ").strip()
            if sector:
                agent.market_sector_analysis(sector, show_reasoning=False)
        
        elif mode == "4":
            print("👋 感谢使用价值投资Agent！")
            break
        
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main() 