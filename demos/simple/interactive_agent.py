"""
交互式价值投资Agent
用户可以通过命令行界面与Agent进行交互
"""

import os
import sys
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.legacy.value_investment_agent import ValueInvestmentAgent

# 加载环境变量
load_dotenv()

def print_menu():
    """打印菜单选项"""
    print("\n" + "="*60)
    print("🤖 价值投资Agent - 交互式界面")
    print("="*60)
    print("请选择操作：")
    print("1. 分析单只股票")
    print("2. 比较多只股票") 
    print("3. 行业分析")
    print("4. 自定义投资问题")
    print("5. 退出")
    print("-" * 60)

def get_stock_input():
    """获取股票代码输入"""
    while True:
        symbol = input("请输入股票代码（如AAPL, TSLA等）: ").strip().upper()
        if symbol:
            return symbol
        print("❌ 请输入有效的股票代码")

def get_stocks_input():
    """获取多个股票代码输入"""
    while True:
        symbols_str = input("请输入股票代码，用逗号分隔（如AAPL,MSFT,GOOGL）: ").strip()
        if symbols_str:
            symbols = [s.strip().upper() for s in symbols_str.split(',')]
            return symbols
        print("❌ 请输入有效的股票代码")

def get_sector_input():
    """获取行业输入"""
    while True:
        sector = input("请输入行业名称（如科技股、银行股、新能源等）: ").strip()
        if sector:
            return sector
        print("❌ 请输入有效的行业名称")

def main():
    """主交互函数"""
    print("🚀 初始化价值投资Agent...")
    
    # 检查API密钥
    if not os.getenv('ALIYUN_API_KEY'):
        print("❌ 错误：未找到阿里云百炼API密钥")
        print("请在环境变量中设置 ALIYUN_API_KEY")
        print("参考 env_example.txt 文件")
        sys.exit(1)
    
    # 初始化Agent
    agent = ValueInvestmentAgent()
    print("✅ Agent初始化完成，使用阿里云百炼Qwen模型")
    
    while True:
        try:
            print_menu()
            choice = input("请输入选项 (1-5): ").strip()
            
            if choice == '1':
                # 分析单只股票
                symbol = get_stock_input()
                show_reasoning = input("是否显示推理过程？(y/n，默认y): ").strip().lower()
                show_reasoning = show_reasoning != 'n'
                
                print(f"\n🔍 正在分析 {symbol}...")
                agent.analyze_stock(symbol, show_reasoning=show_reasoning)
                
            elif choice == '2':
                # 比较多只股票
                symbols = get_stocks_input()
                show_reasoning = input("是否显示推理过程？(y/n，默认n): ").strip().lower()
                show_reasoning = show_reasoning == 'y'
                
                print(f"\n📊 正在比较股票: {', '.join(symbols)}...")
                agent.compare_stocks(symbols, show_reasoning=show_reasoning)
                
            elif choice == '3':
                # 行业分析
                sector = get_sector_input()
                show_reasoning = input("是否显示推理过程？(y/n，默认n): ").strip().lower()
                show_reasoning = show_reasoning == 'y'
                
                print(f"\n🏭 正在分析行业: {sector}...")
                agent.market_sector_analysis(sector, show_reasoning=show_reasoning)
                
            elif choice == '4':
                # 自定义问题
                question = input("请输入您的投资问题: ").strip()
                if question:
                    show_reasoning = input("是否显示推理过程？(y/n，默认n): ").strip().lower()
                    show_reasoning = show_reasoning == 'y'
                    
                    print(f"\n💭 正在思考您的问题...")
                    print("=" * 50)
                    agent.agent.print_response(
                        question,
                        stream=True,
                        show_full_reasoning=show_reasoning,
                        stream_intermediate_steps=True
                    )
                else:
                    print("❌ 请输入有效的问题")
                    
            elif choice == '5':
                # 退出
                print("👋 感谢使用价值投资Agent！")
                break
                
            else:
                print("❌ 无效选项，请选择 1-5")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断，正在退出...")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            print("请重试或检查网络连接")

if __name__ == "__main__":
    main() 