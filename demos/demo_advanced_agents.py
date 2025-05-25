#!/usr/bin/env python3
"""
高级投资大师Agent演示系统
展示7位投资大师的多维度分析能力和结构化输出
支持单股深度分析、多股对比、投资风格比较等功能
"""

import os
import sys
from typing import List, Optional
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 导入系统模块
from src.agents.warren_buffett_agent_v2 import InvestmentMasterFactory
from src.agents.multi_agent_investment_v2 import MultiAgentInvestmentAnalyzerV2
from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent

# 加载环境变量
load_dotenv()

def print_banner():
    """显示系统横幅"""
    print("=" * 80)
    print("🎯 高级投资大师Agent分析系统")
    print("💫 7位世界级投资大师的智慧结晶")
    print("📊 结构化分析报告，专业级投资建议")
    print("=" * 80)

def print_master_info():
    """显示投资大师信息"""
    masters_info = {
        "warren_buffett": {"emoji": "🎩", "name": "Warren Buffett", "style": "价值投资", "specialty": "长期价值、护城河"},
        "charlie_munger": {"emoji": "🧠", "name": "Charlie Munger", "style": "多学科思维", "specialty": "逆向思维、心理学"},
        "peter_lynch": {"emoji": "📈", "name": "Peter Lynch", "style": "成长价值", "specialty": "消费品、成长股"},
        "benjamin_graham": {"emoji": "📚", "name": "Benjamin Graham", "style": "深度价值", "specialty": "安全边际、基本面"},
        "ray_dalio": {"emoji": "🌐", "name": "Ray Dalio", "style": "全天候策略", "specialty": "宏观经济、风险平价"},
        "joel_greenblatt": {"emoji": "🔢", "name": "Joel Greenblatt", "style": "魔法公式", "specialty": "量化价值、ROIC"},
        "david_tepper": {"emoji": "⚡", "name": "David Tepper", "style": "困境投资", "specialty": "危机机会、宏观敏感"}
    }
    
    print("\n🎭 可选投资大师阵容:")
    print("=" * 60)
    
    for key, info in masters_info.items():
        print(f"{info['emoji']} **{info['name']}**")
        print(f"   📊 投资风格: {info['style']}")
        print(f"   🎯 专业领域: {info['specialty']}")
        print()

def single_master_analysis():
    """单个投资大师深度分析"""
    print("\n🎯 单个投资大师深度分析")
    print("=" * 50)
    
    try:
        # 显示大师选项
        masters = InvestmentMasterFactory.get_available_masters()
        print("📋 可选择的投资大师:")
        for i, master in enumerate(masters, 1):
            print(f"{i}. {master}")
        
        # 选择大师
        choice = input(f"\n请选择投资大师 (1-{len(masters)}): ").strip()
        try:
            master_idx = int(choice) - 1
            if 0 <= master_idx < len(masters):
                selected_master = masters[master_idx]
            else:
                print("❌ 无效选择，使用Warren Buffett")
                selected_master = "warren_buffett"
        except ValueError:
            print("❌ 输入错误，使用Warren Buffett")
            selected_master = "warren_buffett"
        
        # 选择股票
        symbol = input("请输入股票代码 (如 AAPL): ").strip().upper()
        if not symbol:
            symbol = "AAPL"
            print(f"使用默认股票: {symbol}")
        
        # 创建Agent并分析
        print(f"\n🤖 创建{selected_master}投资大师Agent...")
        agent = InvestmentMasterFactory.create_agent(selected_master)
        
        print(f"\n📊 开始深度分析股票: {symbol}")
        print("🎯 生成结构化投资报告...")
        print("=" * 60)
        
        result = agent.analyze_stock(symbol)
        
        print(f"\n✅ 分析完成！")
        print(f"📋 分析师: {result['agent']}")
        print(f"🎯 分析股票: {result['symbol']}")
        print(f"📊 投资风格: {result['style']}")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")

def multi_master_consensus():
    """多投资大师共识分析"""
    print("\n🎭 多投资大师共识分析")
    print("=" * 50)
    
    # 预设组合选择
    print("📊 请选择投资大师组合:")
    print("1. 🎩 经典价值三剑客 (Buffett + Munger + Graham)")
    print("2. 📈 价值成长四大师 (Buffett + Munger + Lynch + Graham)")
    print("3. 🌟 全明星七大师 (所有投资大师)")
    print("4. 🔧 自定义组合")
    
    choice = input("\n请选择组合 (1-4): ").strip()
    
    # 设置组合
    if choice == "1":
        selected_masters = ["warren_buffett", "charlie_munger", "benjamin_graham"]
        combo_name = "经典价值三剑客"
    elif choice == "2":
        selected_masters = ["warren_buffett", "charlie_munger", "peter_lynch", "benjamin_graham"]
        combo_name = "价值成长四大师"
    elif choice == "3":
        analyzer = MultiAgentInvestmentAnalyzerV2()
        selected_masters = analyzer.available_masters
        combo_name = "全明星七大师"
    elif choice == "4":
        analyzer = MultiAgentInvestmentAnalyzerV2()
        selected_masters = analyzer.get_master_selection_menu()
        combo_name = "自定义组合"
    else:
        selected_masters = ["warren_buffett", "charlie_munger", "benjamin_graham"]
        combo_name = "经典价值三剑客"
        print("❌ 无效选择，使用默认组合")
    
    # 选择股票
    symbol = input("请输入股票代码 (如 AAPL): ").strip().upper()
    if not symbol:
        symbol = "AAPL"
        print(f"使用默认股票: {symbol}")
    
    try:
        print(f"\n🎯 启动{combo_name}分析")
        print(f"📊 分析股票: {symbol}")
        print(f"🎭 参与大师: {len(selected_masters)}位")
        print("=" * 60)
        
        # 创建多Agent分析器
        if 'analyzer' not in locals():
            analyzer = MultiAgentInvestmentAnalyzerV2()
        
        # 执行分析
        result = analyzer.analyze_stock_multi_master(
            symbol=symbol,
            selected_masters=selected_masters,
            parallel=True,
            show_reasoning=False
        )
        
        print(f"\n✅ {combo_name}分析完成！")
        print(f"⏱️  总耗时: {result['performance']['total_time']:.1f}秒")
        print(f"🎭 参与大师: {result['performance']['masters_count']}位")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")

def investment_style_comparison():
    """投资风格对比分析"""
    print("\n📊 投资风格对比分析")
    print("=" * 50)
    
    print("🎯 选择对比维度:")
    print("1. 💰 价值 vs 成长投资风格")
    print("2. ⏰ 短期 vs 长期投资视角") 
    print("3. 🔬 基本面 vs 宏观经济分析")
    print("4. 🛡️ 保守 vs 激进投资策略")
    print("5. 🎭 全维度风格对比")
    
    choice = input("\n请选择对比维度 (1-5): ").strip()
    
    # 设置对比组合
    comparison_sets = {
        "1": {
            "name": "价值 vs 成长投资风格",
            "group1": {"name": "价值投资派", "masters": ["warren_buffett", "benjamin_graham"]},
            "group2": {"name": "成长投资派", "masters": ["peter_lynch"]}
        },
        "2": {
            "name": "短期 vs 长期投资视角",
            "group1": {"name": "长期投资派", "masters": ["warren_buffett", "charlie_munger"]},
            "group2": {"name": "灵活投资派", "masters": ["peter_lynch", "david_tepper"]}
        },
        "3": {
            "name": "基本面 vs 宏观经济分析",
            "group1": {"name": "基本面分析派", "masters": ["warren_buffett", "peter_lynch", "benjamin_graham"]},
            "group2": {"name": "宏观分析派", "masters": ["ray_dalio"]}
        },
        "4": {
            "name": "保守 vs 激进投资策略",
            "group1": {"name": "保守投资派", "masters": ["warren_buffett", "benjamin_graham"]},
            "group2": {"name": "激进投资派", "masters": ["david_tepper", "joel_greenblatt"]}
        },
        "5": {
            "name": "全维度风格对比",
            "group1": {"name": "传统价值派", "masters": ["warren_buffett", "charlie_munger", "benjamin_graham"]},
            "group2": {"name": "现代策略派", "masters": ["ray_dalio", "joel_greenblatt", "david_tepper"]}
        }
    }
    
    if choice not in comparison_sets:
        choice = "1"
        print("❌ 无效选择，使用默认对比")
    
    comparison = comparison_sets[choice]
    
    # 选择股票
    symbol = input("请输入股票代码 (如 AAPL): ").strip().upper()
    if not symbol:
        symbol = "AAPL"
        print(f"使用默认股票: {symbol}")
    
    try:
        print(f"\n🎯 启动投资风格对比: {comparison['name']}")
        print(f"📊 分析股票: {symbol}")
        print(f"⚖️  {comparison['group1']['name']} vs {comparison['group2']['name']}")
        print("=" * 60)
        
        # 创建分析器
        analyzer = MultiAgentInvestmentAnalyzerV2()
        
        # 组合两组大师
        all_masters = comparison['group1']['masters'] + comparison['group2']['masters']
        
        # 执行分析
        result = analyzer.analyze_stock_multi_master(
            symbol=symbol,
            selected_masters=all_masters,
            parallel=True,
            show_reasoning=False
        )
        
        print(f"\n✅ 投资风格对比分析完成！")
        print(f"⏱️  总耗时: {result['performance']['total_time']:.1f}秒")
        print(f"🎭 参与大师: {result['performance']['masters_count']}位")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")

def magic_formula_screening():
    """魔法公式股票筛选"""
    print("\n🔢 Joel Greenblatt魔法公式筛选")
    print("=" * 50)
    
    print("🎯 魔法公式投资策略:")
    print("   - 高资本回报率 (ROIC)")
    print("   - 低市盈率 (P/E)")
    print("   - 系统化投资方法")
    print("   - 长期超额收益")
    
    # 输入多只股票
    stocks_input = input("\n请输入多只股票代码，用逗号分隔 (如 AAPL,MSFT,GOOGL): ").strip().upper()
    if not stocks_input:
        stocks = ["AAPL", "MSFT", "GOOGL"]
        print("使用默认股票组合: AAPL, MSFT, GOOGL")
    else:
        stocks = [s.strip() for s in stocks_input.split(",")]
    
    try:
        print(f"\n🎯 启动魔法公式筛选")
        print(f"📊 分析股票: {', '.join(stocks)}")
        print(f"🔢 使用Joel Greenblatt魔法公式策略")
        print("=" * 60)
        
        # 创建Joel Greenblatt Agent
        greenblatt_agent = InvestmentMasterFactory.create_joel_greenblatt()
        
        # 分析每只股票
        results = []
        for stock in stocks:
            print(f"\n🔍 分析股票: {stock}")
            result = greenblatt_agent.analyze_stock(stock)
            results.append(result)
        
        print(f"\n✅ 魔法公式筛选完成！")
        print(f"📊 已分析 {len(stocks)} 只股票")
        
    except Exception as e:
        print(f"❌ 筛选失败: {e}")

def distressed_investment_analysis():
    """困境投资机会分析"""
    print("\n⚡ David Tepper困境投资分析")
    print("=" * 50)
    
    print("🎯 困境投资策略特点:")
    print("   - 危机中寻找机会")
    print("   - 宏观敏感度高")
    print("   - 逆向投资思维")
    print("   - 高风险高收益")
    
    # 选择分析类型
    print("\n📊 请选择分析类型:")
    print("1. 🔥 单股困境分析")
    print("2. 📉 市场困境机会扫描")
    print("3. 🌐 宏观风险评估")
    
    choice = input("\n请选择分析类型 (1-3): ").strip()
    
    if choice == "1":
        # 单股分析
        symbol = input("请输入困境股票代码 (如 股价大跌的股票): ").strip().upper()
        if not symbol:
            symbol = "AAPL"
            print(f"使用示例股票: {symbol}")
        
        try:
            print(f"\n🎯 启动困境投资分析")
            print(f"📊 分析股票: {symbol}")
            print(f"⚡ 使用David Tepper困境投资策略")
            print("=" * 60)
            
            # 创建David Tepper Agent
            tepper_agent = InvestmentMasterFactory.create_david_tepper()
            
            result = tepper_agent.analyze_stock(symbol)
            
            print(f"\n✅ 困境投资分析完成！")
            print(f"📊 分析股票: {result['symbol']}")
            
        except Exception as e:
            print(f"❌ 分析失败: {e}")
    
    elif choice == "2" or choice == "3":
        print("🚧 该功能正在开发中，敬请期待...")
    
    else:
        print("❌ 无效选择")

def multi_stock_comparison():
    """多股票对比分析"""
    print("\n📈 多股票多大师对比分析")
    print("=" * 50)
    
    # 输入股票
    stocks_input = input("请输入多只股票代码，用逗号分隔 (如 AAPL,MSFT,GOOGL): ").strip().upper()
    if not stocks_input:
        stocks = ["AAPL", "MSFT", "GOOGL"]
        print("使用默认股票组合: AAPL, MSFT, GOOGL")
    else:
        stocks = [s.strip() for s in stocks_input.split(",")]
    
    try:
        print(f"\n🎯 启动多股票对比分析")
        print(f"📊 对比股票: {', '.join(stocks)}")
        print(f"🎭 使用全部投资大师视角")
        print("=" * 60)
        
        # 创建分析器
        analyzer = MultiAgentInvestmentAnalyzerV2()
        
        # 执行对比分析
        result = analyzer.compare_stocks_multi_master(
            symbols=stocks,
            selected_masters=None,  # 使用所有大师
            show_reasoning=False
        )
        
        print(f"\n✅ 多股票对比分析完成！")
        print(f"📊 已对比 {len(stocks)} 只股票")
        
    except Exception as e:
        print(f"❌ 对比分析失败: {e}")

def main():
    """主程序"""
    try:
        print_banner()
        print_master_info()
        
        while True:
            print("\n" + "=" * 80)
            print("🎯 请选择分析功能:")
            print("=" * 80)
            print("1. 🎭 单个投资大师深度分析")
            print("2. 🤝 多投资大师共识分析") 
            print("3. ⚖️  投资风格对比分析")
            print("4. 🔢 魔法公式股票筛选 (Joel Greenblatt)")
            print("5. ⚡ 困境投资机会分析 (David Tepper)")
            print("6. 📈 多股票多大师对比分析")
            print("7. 📋 查看投资大师详细信息")
            print("8. 🚪 退出系统")
            print("-" * 80)
            
            choice = input("请输入选择 (1-8): ").strip()
            
            if choice == "1":
                single_master_analysis()
            elif choice == "2":
                multi_master_consensus()
            elif choice == "3":
                investment_style_comparison()
            elif choice == "4":
                magic_formula_screening()
            elif choice == "5":
                distressed_investment_analysis()
            elif choice == "6":
                multi_stock_comparison()
            elif choice == "7":
                print_master_info()
            elif choice == "8":
                print("\n👋 感谢使用高级投资大师Agent分析系统！")
                print("💡 愿投资大师的智慧伴您投资成功！")
                break
            else:
                print("❌ 无效选择，请重新输入")
            
            input("\n按Enter键继续...")
                
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，系统退出")
    except Exception as e:
        print(f"\n❌ 系统错误: {e}")

if __name__ == "__main__":
    main() 