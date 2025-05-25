#!/usr/bin/env python3
"""
Agno AI 投资分析系统 - 命令行界面
===============================

提供传统的菜单式命令行交互界面
支持投资分析的各种功能

运行方式:
    python apps/cli.py
"""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

# 添加src路径以导入模块
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agents.configurable_investment_agent import ConfigurableInvestmentAgent
from agents.multi_agent_investment_v2 import MultiAgentInvestmentAnalyzer

# 加载环境变量
load_dotenv()

class InvestmentCLI:
    """投资分析命令行界面"""
    
    def __init__(self):
        """初始化CLI"""
        self.config_agent = ConfigurableInvestmentAgent()
        self.multi_agent = MultiAgentInvestmentAnalyzer()
        
    def show_welcome(self):
        """显示欢迎界面"""
        print("🎯 Agno AI 投资分析系统 - 命令行界面")
        print("=" * 50)
        print("💼 集成多位投资大师的智慧，为您提供专业投资分析")
        print("")
        
    def show_menu(self):
        """显示主菜单"""
        print("📋 请选择功能:")
        print("1️⃣  单股深度分析        - 多投资大师协同分析")
        print("2️⃣  多股对比分析        - 横向对比投资价值")  
        print("3️⃣  投资大师风格比较    - 了解不同投资理念")
        print("4️⃣  投资组合建议        - 智能资产配置")
        print("5️⃣  市场趋势分析        - 宏观市场判断")
        print("6️⃣  系统配置            - 调整系统设置")
        print("0️⃣  退出系统")
        print("")
        
    def get_user_choice(self) -> str:
        """获取用户选择"""
        while True:
            try:
                choice = input("👉 请输入选项 (0-6): ").strip()
                if choice in ['0', '1', '2', '3', '4', '5', '6']:
                    return choice
                else:
                    print("❌ 无效选项，请重新输入")
            except KeyboardInterrupt:
                print("\n👋 用户取消操作")
                return '0'
            except Exception as e:
                print(f"❌ 输入错误: {e}")
                
    def single_stock_analysis(self):
        """单股深度分析"""
        print("\n📊 单股深度分析")
        print("-" * 30)
        
        # 获取股票代码
        symbol = input("请输入股票代码 (如: AAPL): ").strip().upper()
        if not symbol:
            print("❌ 股票代码不能为空")
            return
            
        print(f"\n🔍 正在分析 {symbol}...")
        
        # 这里可以调用多Agent分析
        try:
            # TODO: 实现具体的分析逻辑
            print("💡 功能开发中，请使用 Web 界面进行分析")
            print(f"   python apps/playground.py")
            print(f"   然后访问: https://app.agno.com/playground")
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            
    def multi_stock_comparison(self):
        """多股对比分析"""
        print("\n📈 多股对比分析")
        print("-" * 30)
        
        symbols_input = input("请输入股票代码，用逗号分隔 (如: AAPL,MSFT,GOOGL): ").strip()
        if not symbols_input:
            print("❌ 股票代码不能为空")
            return
            
        symbols = [s.strip().upper() for s in symbols_input.split(',')]
        print(f"\n🔍 正在对比分析: {', '.join(symbols)}")
        
        try:
            # TODO: 实现具体的对比分析逻辑
            print("💡 功能开发中，请使用 Web 界面进行分析")
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            
    def master_style_comparison(self):
        """投资大师风格比较"""
        print("\n🎭 投资大师风格比较")
        print("-" * 30)
        
        available_masters = self.config_agent.get_available_masters()
        
        print("💼 可用的投资大师:")
        for i, master in enumerate(available_masters, 1):
            master_info = self.config_agent.get_master_info(master)
            print(f"{i}. {master_info['agent_name']} - {master_info['description']}")
            
        print("\n💡 每位大师都有独特的投资哲学和分析方法")
        print("建议使用 Web 界面与大师们直接对话，获得个性化分析")
        
    def portfolio_recommendation(self):
        """投资组合建议"""
        print("\n💼 投资组合建议")
        print("-" * 30)
        
        try:
            # 获取投资金额
            amount_input = input("请输入投资金额 (元): ").strip()
            if not amount_input:
                print("❌ 投资金额不能为空")
                return
                
            amount = float(amount_input)
            
            # 获取风险偏好
            print("\n风险偏好:")
            print("1. 保守型 2. 平衡型 3. 积极型")
            risk_choice = input("请选择风险偏好 (1-3): ").strip()
            
            risk_map = {'1': '保守型', '2': '平衡型', '3': '积极型'}
            risk_preference = risk_map.get(risk_choice, '平衡型')
            
            print(f"\n📊 投资金额: {amount:,.2f} 元")
            print(f"📈 风险偏好: {risk_preference}")
            print("\n💡 建议使用 Web 界面获得详细的投资组合建议")
            
        except ValueError:
            print("❌ 金额格式错误，请输入数字")
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            
    def market_trend_analysis(self):
        """市场趋势分析"""
        print("\n🌊 市场趋势分析")
        print("-" * 30)
        
        print("📊 市场趋势分析功能包括:")
        print("- 大盘指数分析")
        print("- 行业轮动分析")  
        print("- 宏观经济指标")
        print("- 市场情绪分析")
        print("")
        print("💡 请使用 Web 界面获得实时的市场分析")
        
    def system_config(self):
        """系统配置"""
        print("\n⚙️ 系统配置")
        print("-" * 30)
        
        # 检查环境变量
        api_key = os.getenv("ALIYUN_API_KEY")
        if api_key:
            print("✅ API 密钥已配置")
        else:
            print("❌ API 密钥未配置")
            print("💡 请设置环境变量: ALIYUN_API_KEY")
            
        # 显示系统信息
        print(f"📂 项目路径: {project_root}")
        print(f"🗄️ 数据目录: {os.path.join(project_root, 'data')}")
        
        print("\n🔧 配置选项:")
        print("1. 重新设置 API 密钥")
        print("2. 查看系统状态")
        print("3. 返回主菜单")
        
        choice = input("请选择 (1-3): ").strip()
        if choice == '1':
            new_key = input("请输入新的 API 密钥: ").strip()
            if new_key:
                print("💡 请将 API 密钥添加到 .env 文件中")
                print(f"   ALIYUN_API_KEY={new_key}")
        elif choice == '2':
            self.show_system_status()
            
    def show_system_status(self):
        """显示系统状态"""
        print("\n🔍 系统状态检查")
        print("-" * 30)
        
        # 检查各种状态
        checks = {
            "Python 环境": sys.version_info >= (3, 8),
            "API 密钥": bool(os.getenv("ALIYUN_API_KEY")),
            "数据目录": os.path.exists(os.path.join(project_root, 'data')),
            "配置文件": os.path.exists(os.path.join(project_root, '.env')),
        }
        
        for item, status in checks.items():
            icon = "✅" if status else "❌"
            print(f"{icon} {item}")
            
    def run(self):
        """运行CLI主循环"""
        # 检查环境
        if not os.getenv("ALIYUN_API_KEY"):
            print("❌ 错误: 未设置 ALIYUN_API_KEY 环境变量")
            print("💡 请先配置 API 密钥:")
            print("   1. 复制 .env.example 为 .env")
            print("   2. 编辑 .env 文件，设置 ALIYUN_API_KEY")
            return
            
        self.show_welcome()
        
        while True:
            try:
                self.show_menu()
                choice = self.get_user_choice()
                
                if choice == '0':
                    print("👋 感谢使用 Agno AI 投资分析系统！")
                    break
                elif choice == '1':
                    self.single_stock_analysis()
                elif choice == '2':
                    self.multi_stock_comparison()
                elif choice == '3':
                    self.master_style_comparison()
                elif choice == '4':
                    self.portfolio_recommendation()
                elif choice == '5':
                    self.market_trend_analysis()
                elif choice == '6':
                    self.system_config()
                    
                input("\n⏎ 按回车键继续...")
                print("\n" + "="*50)
                
            except KeyboardInterrupt:
                print("\n\n👋 用户取消操作，退出系统")
                break
            except Exception as e:
                print(f"\n❌ 系统错误: {e}")
                print("请重试或联系技术支持")

def main():
    """主函数"""
    cli = InvestmentCLI()
    cli.run()

if __name__ == "__main__":
    main() 