"""
投资组合管理Agent - 基于Agno框架
提供投资组合分析、优化和风险管理功能
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

# 加载环境变量
load_dotenv()

class PortfolioAgent:
    def __init__(self, model_id="qwen-plus"):
        """
        初始化投资组合管理Agent
        
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
        
        # 创建Agent
        self.agent = Agent(
            name="专业投资组合管理师",
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
                "你是一位经验丰富的投资组合管理师，专注于价值投资策略",
                "你的目标是帮助客户构建和管理多元化的投资组合",
                "重点关注：",
                "1. 风险管理：分散投资、相关性分析、波动率控制",
                "2. 资产配置：股票、债券、行业分配比例优化",
                "3. 价值发现：寻找被低估的优质资产",
                "4. 长期收益：关注可持续的复合增长",
                "5. 成本控制：考虑交易费用和税务影响",
                "使用表格和图表清晰展示投资组合数据",
                "提供具体的买入/卖出/调仓建议",
                "所有建议都要基于量化分析和基本面研究"
            ],
            markdown=True,
            show_tool_calls=True
        )
        
        # 投资组合数据存储
        self.portfolio_file = "portfolio_data.json"
        self.portfolio = self.load_portfolio()
    
    def load_portfolio(self):
        """加载投资组合数据"""
        try:
            if os.path.exists(self.portfolio_file):
                with open(self.portfolio_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {"holdings": {}, "cash": 100000, "history": []}
        except Exception as e:
            print(f"加载投资组合数据失败: {e}")
            return {"holdings": {}, "cash": 100000, "history": []}
    
    def save_portfolio(self):
        """保存投资组合数据"""
        try:
            with open(self.portfolio_file, 'w', encoding='utf-8') as f:
                json.dump(self.portfolio, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存投资组合数据失败: {e}")
    
    def analyze_portfolio(self, show_reasoning=True):
        """分析当前投资组合"""
        if not self.portfolio["holdings"]:
            print("📊 当前投资组合为空，请先添加持仓")
            return
        
        holdings_str = ", ".join([f"{symbol}: {shares}股" 
                                for symbol, shares in self.portfolio["holdings"].items()])
        
        prompt = f"""
        请分析我的当前投资组合：

        **当前持仓：**
        {holdings_str}
        现金余额：${self.portfolio["cash"]:,.2f}

        请进行全面的投资组合分析：

        1. **投资组合概览**
           - 总市值计算
           - 各股票当前价值和权重
           - 现金配置比例

        2. **风险分析**
           - 行业集中度风险
           - 个股集中度风险
           - 整体波动率评估
           - 相关性分析

        3. **业绩表现**
           - 各持仓股票近期表现
           - 整体收益率估算
           - 与市场基准比较

        4. **基本面健康度**
           - 各股票基本面评分
           - 财务健康状况
           - 估值水平分析

        5. **优化建议**
           - 资产配置调整建议
           - 个股调仓建议
           - 风险管理措施
           - 新投资机会推荐

        请使用表格展示关键数据，并提供具体的操作建议。
        """
        
        print("\n📊 投资组合全面分析")
        print("=" * 50)
        
        self.agent.print_response(
            prompt,
            stream=True,
            show_full_reasoning=show_reasoning,
            stream_intermediate_steps=True
        )
    
    def optimize_portfolio(self, target_amount=None, risk_level="medium", show_reasoning=False):
        """优化投资组合配置"""
        total_value = self.portfolio["cash"]
        
        # 计算当前总价值（需要获取股票当前价格）
        holdings_str = ", ".join([f"{symbol}: {shares}股" 
                                for symbol, shares in self.portfolio["holdings"].items()])
        
        if target_amount:
            total_value = target_amount
        
        prompt = f"""
        请为我优化投资组合配置：

        **当前状况：**
        - 持仓：{holdings_str if holdings_str else "无"}
        - 现金：${self.portfolio["cash"]:,.2f}
        - 目标投资金额：${total_value:,.2f}
        - 风险偏好：{risk_level} (low/medium/high)

        **优化要求：**
        1. **资产配置策略**
           - 股票/现金/其他资产的最优比例
           - 基于风险偏好的配置建议
           - 考虑当前市场环境

        2. **股票选择**
           - 推荐5-10只优质价值股票
           - 每只股票的投资逻辑
           - 建议投资比例和金额

        3. **行业分散**
           - 确保行业多元化
           - 避免过度集中风险
           - 平衡成长性和稳定性

        4. **实施计划**
           - 分批买入策略
           - 时间安排建议
           - 风险控制措施

        5. **监控指标**
           - 关键业绩指标
           - 风险监控点
           - 调仓触发条件

        请提供具体的股票代码、买入价格区间和投资金额建议。
        """
        
        print(f"\n🎯 投资组合优化 (目标金额: ${total_value:,.2f})")
        print("=" * 50)
        
        self.agent.print_response(
            prompt,
            stream=True,
            show_full_reasoning=show_reasoning
        )
    
    def risk_assessment(self, show_reasoning=False):
        """投资组合风险评估"""
        if not self.portfolio["holdings"]:
            print("📊 当前投资组合为空，无法进行风险评估")
            return
        
        holdings_str = ", ".join([f"{symbol}: {shares}股" 
                                for symbol, shares in self.portfolio["holdings"].items()])
        
        prompt = f"""
        请对我的投资组合进行全面的风险评估：

        **当前持仓：**
        {holdings_str}

        **风险评估框架：**
        1. **市场风险**
           - 系统性风险暴露
           - Beta系数分析
           - 市场相关性

        2. **集中度风险**
           - 个股集中度
           - 行业集中度
           - 地域集中度

        3. **流动性风险**
           - 各股票流动性评估
           - 市场深度分析
           - 紧急变现能力

        4. **基本面风险**
           - 公司特定风险
           - 财务健康风险
           - 管理层风险

        5. **估值风险**
           - 当前估值水平
           - 估值修正风险
           - 泡沫风险

        6. **压力测试**
           - 市场下跌10%/20%/30%情况
           - 经济衰退场景
           - 黑天鹅事件影响

        请提供风险评分、预警指标和风险缓解策略。
        """
        
        print("\n⚠️ 投资组合风险评估")
        print("=" * 50)
        
        self.agent.print_response(
            prompt,
            stream=True,
            show_full_reasoning=show_reasoning
        )
    
    def add_position(self, symbol, shares):
        """添加持仓"""
        symbol = symbol.upper()
        if symbol in self.portfolio["holdings"]:
            self.portfolio["holdings"][symbol] += shares
        else:
            self.portfolio["holdings"][symbol] = shares
        
        # 记录交易历史
        self.portfolio["history"].append({
            "date": datetime.now().isoformat(),
            "action": "buy",
            "symbol": symbol,
            "shares": shares
        })
        
        self.save_portfolio()
        print(f"✅ 已添加 {symbol}: {shares}股")
    
    def remove_position(self, symbol, shares=None):
        """移除持仓"""
        symbol = symbol.upper()
        if symbol not in self.portfolio["holdings"]:
            print(f"❌ 未找到 {symbol} 持仓")
            return
        
        if shares is None:
            shares = self.portfolio["holdings"][symbol]
        
        if shares >= self.portfolio["holdings"][symbol]:
            del self.portfolio["holdings"][symbol]
        else:
            self.portfolio["holdings"][symbol] -= shares
        
        # 记录交易历史
        self.portfolio["history"].append({
            "date": datetime.now().isoformat(),
            "action": "sell",
            "symbol": symbol,
            "shares": shares
        })
        
        self.save_portfolio()
        print(f"✅ 已卖出 {symbol}: {shares}股")
    
    def show_portfolio(self):
        """显示当前投资组合"""
        print("\n📊 当前投资组合")
        print("=" * 40)
        
        if not self.portfolio["holdings"]:
            print("投资组合为空")
        else:
            for symbol, shares in self.portfolio["holdings"].items():
                print(f"{symbol}: {shares:,}股")
        
        print(f"现金余额: ${self.portfolio['cash']:,.2f}")
        print(f"交易记录数: {len(self.portfolio.get('history', []))}")

def main():
    """演示投资组合Agent功能"""
    print("🤖 投资组合管理Agent启动中...")
    print("基于Agno框架，提供专业的投资组合管理服务")
    print("=" * 60)
    
    # 创建Agent实例
    agent = PortfolioAgent()
    
    # 演示功能
    print("\n📈 演示功能:")
    
    # 添加一些示例持仓
    agent.add_position("AAPL", 100)
    agent.add_position("MSFT", 150)
    agent.add_position("GOOGL", 50)
    
    # 显示当前组合
    agent.show_portfolio()
    
    # 分析投资组合
    agent.analyze_portfolio(show_reasoning=False)
    
    # 风险评估
    agent.risk_assessment(show_reasoning=False)
    
    # 优化建议
    agent.optimize_portfolio(target_amount=500000, risk_level="medium")

if __name__ == "__main__":
    main() 