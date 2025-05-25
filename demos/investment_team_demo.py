#!/usr/bin/env python3
"""
投资大师团队演示
===============

演示如何使用巴菲特-芒格投资分析团队进行股票分析

使用方法:
    python demos/investment_team_demo.py
"""

import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from apps.investment_team import InvestmentMasterTeam

def analyze_stock(stock_symbol: str, company_name: str = None):
    """分析指定股票"""
    print(f"🔍 正在分析 {stock_symbol} {f'({company_name})' if company_name else ''}")
    print("=" * 80)
    
    # 创建投资团队
    team_manager = InvestmentMasterTeam()
    investment_team = team_manager.create_investment_team()
    
    # 构建分析任务
    task = f"""
请分析 {stock_symbol} {f'({company_name})' if company_name else ''} 的投资价值，包括：

1. **基本面分析**：
   - 最新财务数据和关键指标
   - 盈利能力和成长性分析
   - 现金流和债务状况

2. **竞争优势分析**：
   - 企业护城河和竞争地位
   - 品牌价值和市场份额
   - 技术优势和创新能力

3. **估值分析**：
   - 当前估值水平（PE、PB等）
   - 与历史估值和同行对比
   - 内在价值评估

4. **投资建议**：
   - 明确的买入/持有/卖出建议
   - 目标价格区间
   - 投资时间框架

5. **风险评估**：
   - 主要投资风险
   - 行业和宏观风险
   - 风险缓解措施

请提供详细的分析报告，并给出明确的投资建议。
    """
    
    # 执行分析
    investment_team.print_response(
        task,
        stream=True,
        stream_intermediate_steps=True,
        show_full_reasoning=True,
    )

def main():
    """主演示函数"""
    print("🏆 巴菲特-芒格投资分析团队演示")
    print("=" * 80)
    print()
    
    # 检查环境变量
    if not os.getenv("ALIYUN_API_KEY"):
        print("❌ 错误: 未设置 ALIYUN_API_KEY 环境变量")
        print("💡 请在 .env 文件中设置您的阿里云 API 密钥")
        return
    
    # 预设的股票分析示例
    stocks_to_analyze = [
        ("AAPL", "苹果公司"),
        ("MSFT", "微软公司"), 
        ("BRK-B", "伯克希尔·哈撒韦"),
        ("TSLA", "特斯拉"),
        ("NVDA", "英伟达")
    ]
    
    print("📋 可分析的股票示例:")
    for i, (symbol, name) in enumerate(stocks_to_analyze, 1):
        print(f"   {i}. {symbol} - {name}")
    print("   6. 自定义股票代码")
    print()
    
    try:
        choice = input("请选择要分析的股票 (1-6): ").strip()
        
        if choice in ['1', '2', '3', '4', '5']:
            idx = int(choice) - 1
            symbol, name = stocks_to_analyze[idx]
            analyze_stock(symbol, name)
            
        elif choice == '6':
            custom_symbol = input("请输入股票代码 (如 AAPL): ").strip().upper()
            custom_name = input("请输入公司名称 (可选): ").strip()
            if custom_symbol:
                analyze_stock(custom_symbol, custom_name if custom_name else None)
            else:
                print("❌ 股票代码不能为空")
                
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n👋 分析已取消")
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")

if __name__ == "__main__":
    main() 