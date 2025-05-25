#!/usr/bin/env python3
"""
Agno AI 投资分析系统
=====================

多投资大师智能分析平台
支持7位世界级投资大师的多维度投资分析
集成token优化和流式处理技术

运行: python main.py
"""

import os
import sys
from typing import List, Optional
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.multi_agent_investment_v2 import MultiAgentInvestmentAnalyzerV2
from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent
from src.utils.token_manager import TokenManager, TokenBudget

# 加载环境变量
load_dotenv()

class AgnoInvestmentSystem:
    """Agno AI 投资分析系统主类"""
    
    def __init__(self):
        """初始化系统"""
        self.check_environment()
        
        # 初始化各个组件
        self.analyzer_v2 = MultiAgentInvestmentAnalyzerV2(enable_token_optimization=True)
        self.config_agent = ConfigurableInvestmentAgent()
        self.token_manager = TokenManager()
        
        print("✅ Agno AI 投资分析系统初始化完成！")
        
    def check_environment(self):
        """检查环境配置"""
        print("🔍 检查系统环境...")
        
        # 检查API密钥
        if not os.getenv("ALIYUN_API_KEY"):
            print("❌ 未设置ALIYUN_API_KEY环境变量")
            print("请在.env文件中设置：ALIYUN_API_KEY=your_api_key")
            sys.exit(1)
        
        # 检查配置文件
        config_path = os.path.join("src", "config", "investment_agents_config.yaml")
        if not os.path.exists(config_path):
            print("❌ 配置文件不存在：src/config/investment_agents_config.yaml")
            sys.exit(1)
        
        print("✅ 环境检查通过")
    
    def show_banner(self):
        """显示系统横幅"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🎯 Agno AI 投资分析系统                              ║
║                     📊 多投资大师智能决策平台 V2.0                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🎭 支持投资大师:                                                            ║
║     🎩 Warren Buffett  |  🧠 Charlie Munger  |  📈 Peter Lynch               ║
║     📚 Benjamin Graham |  🌊 Ray Dalio       |  🔢 Joel Greenblatt           ║
║     ⚡ David Tepper                                                          ║
║                                                                              ║
║  🚀 核心功能:                                                                ║
║     • 多大师协同分析     • 智能投资建议      • 风险评估报告                   ║
║     • 股票对比分析       • Token智能优化     • 流式处理分析                   ║
║                                                                              ║
║  ⚡ V2.0 新特性:                                                             ║
║     • Token超限处理     • 批量股票分析      • 压缩模式分析                    ║
║     • 流式输出优化       • 结构化报告        • 性能监控统计                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def show_main_menu(self):
        """显示主菜单"""
        menu = """
🔷 主菜单选项:

1️⃣  单股深度分析         - 多投资大师协同分析单只股票
2️⃣  多股对比分析         - 横向对比多只股票投资价值  
3️⃣  投资大师风格比较     - 了解不同大师的投资理念
4️⃣  配置化Agent测试     - 测试可配置投资Agent系统
5️⃣  Token优化设置       - 调整token使用策略
6️⃣  系统性能测试        - 测试各组件运行状态
7️⃣  使用帮助说明        - 查看详细使用指南
0️⃣  退出系统           - 安全退出

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        print(menu)
    
    def select_masters(self) -> List[str]:
        """选择投资大师"""
        available_masters = self.analyzer_v2.available_masters
        
        print("\n🎭 可选择的投资大师:")
        print("=" * 60)
        
        # 显示大师信息
        master_info = {
            "warren_buffett": {"emoji": "🎩", "desc": "价值投资之父，长期持有策略"},
            "charlie_munger": {"emoji": "🧠", "desc": "多元思维模型，逆向思考大师"},
            "peter_lynch": {"emoji": "📈", "desc": "成长股猎手，消费者导向投资"},
            "benjamin_graham": {"emoji": "📚", "desc": "证券分析鼻祖，安全边际理论"},
            "ray_dalio": {"emoji": "🌊", "desc": "全天候策略，宏观经济分析"},
            "joel_greenblatt": {"emoji": "🔢", "desc": "魔法公式创始人，量化价值投资"},
            "david_tepper": {"emoji": "⚡", "desc": "困境反转专家，宏观敏感度投资"}
        }
        
        for i, master in enumerate(available_masters, 1):
            info = master_info.get(master, {"emoji": "🎯", "desc": "专业投资分析师"})
            print(f"{i}. {info['emoji']} {master.replace('_', ' ').title()}")
            print(f"   {info['desc']}")
            print()
        
        print("0. 🌟 全部大师 (推荐)")
        print("Q. 🔄 智能推荐 (基于token优化)")
        print("-" * 60)
        
        choice = input("请选择投资大师 (用逗号分隔数字，如 1,2,3): ").strip()
        
        if choice.upper() == "Q":
            # 智能推荐：根据token限制选择5位核心大师
            selected = available_masters[:5]
            print(f"🧠 智能推荐大师: {', '.join(selected)}")
            return selected
        elif choice == "0":
            return available_masters
        
        try:
            selected_indices = [int(x.strip()) for x in choice.split(",")]
            selected_masters = []
            
            for idx in selected_indices:
                if 1 <= idx <= len(available_masters):
                    selected_masters.append(available_masters[idx - 1])
                else:
                    print(f"⚠️ 忽略无效选择: {idx}")
            
            if not selected_masters:
                print("❌ 没有有效选择，使用智能推荐")
                return available_masters[:5]
            
            print(f"✅ 已选择: {', '.join(selected_masters)}")
            return selected_masters
            
        except ValueError:
            print("❌ 输入格式错误，使用智能推荐")
            return available_masters[:5]
    
    def single_stock_analysis(self):
        """单股深度分析"""
        print("\n" + "="*80)
        print("🔍 单股深度分析")
        print("="*80)
        
        # 选择投资大师
        selected_masters = self.select_masters()
        
        # 输入股票代码
        symbol = input("\n📈 请输入股票代码 (如 AAPL, TSLA, 000001.SZ): ").strip().upper()
        if not symbol:
            print("❌ 股票代码不能为空")
            return
        
        # 选择分析模式
        print("\n🔧 选择分析模式:")
        print("1. 🤖 自动模式 (智能选择最优处理方式)")
        print("2. 🗜️ 压缩模式 (快速分析，节省token)")
        print("3. 🌊 流式模式 (分段处理，详细分析)")
        print("4. 📄 完整模式 (传统完整分析)")
        
        mode_choice = input("请选择模式 (1-4，默认1): ").strip() or "1"
        mode_map = {"1": "auto", "2": "compressed", "3": "streaming", "4": "full"}
        analysis_mode = mode_map.get(mode_choice, "auto")
        
        print(f"\n🚀 开始分析 {symbol}...")
        print(f"🎭 参与大师: {len(selected_masters)}位")
        print(f"🔧 分析模式: {analysis_mode}")
        
        try:
            result = self.analyzer_v2.analyze_stock_multi_master(
                symbol=symbol,
                selected_masters=selected_masters,
                parallel=True,
                show_reasoning=False,
                analysis_mode=analysis_mode
            )
            
            print(f"\n🎉 分析完成! 用时 {result['performance']['total_time']:.1f}秒")
            
        except Exception as e:
            print(f"❌ 分析出错: {str(e)}")
    
    def multi_stock_comparison(self):
        """多股对比分析"""
        print("\n" + "="*80)
        print("📊 多股对比分析")
        print("="*80)
        
        # 选择投资大师
        selected_masters = self.select_masters()
        
        # 输入股票代码
        symbols_input = input("\n📈 请输入股票代码，用逗号分隔 (如 AAPL,TSLA,MSFT): ").strip().upper()
        if not symbols_input:
            print("❌ 股票代码不能为空")
            return
        
        symbols = [s.strip() for s in symbols_input.split(",") if s.strip()]
        if len(symbols) < 2:
            print("❌ 至少需要2只股票进行对比")
            return
        
        # 选择批处理大小
        if len(symbols) > 3:
            print(f"\n🔄 检测到{len(symbols)}只股票，建议使用批处理模式")
            batch_size = input("请输入批处理大小 (默认3，输入0禁用批处理): ").strip()
            try:
                batch_size = int(batch_size) if batch_size else 3
            except ValueError:
                batch_size = 3
        else:
            batch_size = len(symbols)
        
        print(f"\n🚀 开始对比分析...")
        print(f"📈 对比股票: {', '.join(symbols)}")
        print(f"🎭 参与大师: {len(selected_masters)}位")
        print(f"📦 批处理大小: {batch_size}")
        
        try:
            result = self.analyzer_v2.compare_stocks_multi_master(
                symbols=symbols,
                selected_masters=selected_masters,
                show_reasoning=False,
                batch_size=batch_size
            )
            
            print(f"\n🎉 对比分析完成!")
            
        except Exception as e:
            print(f"❌ 分析出错: {str(e)}")
    
    def master_style_comparison(self):
        """投资大师风格比较"""
        print("\n" + "="*80)
        print("🎭 投资大师风格比较")
        print("="*80)
        
        self.analyzer_v2.config_analyzer.get_master_comparison()
    
    def test_configurable_agent(self):
        """测试配置化Agent"""
        print("\n" + "="*80)
        print("🔧 配置化Agent测试")
        print("="*80)
        
        symbol = input("请输入测试股票代码 (如 AAPL): ").strip().upper()
        if not symbol:
            print("❌ 股票代码不能为空")
            return
        
        try:
            print(f"\n🧪 测试配置化Agent分析 {symbol}...")
            
            # 获取可用的投资大师列表
            available_masters = self.config_agent.get_available_masters()
            print(f"📋 可用投资大师: {', '.join(available_masters)}")
            
            # 使用warren_buffett进行测试
            test_master = "warren_buffett"
            print(f"🎯 使用 {test_master} 进行测试...")
            
            # 创建单个投资大师Agent
            master_agent = self.config_agent.create_agent(test_master)
            print(f"✅ 创建 {master_agent.agent_name} 成功")
            
            # 进行股票分析
            result = master_agent.analyze_stock(symbol, show_reasoning=False)
            print(f"✅ 配置化Agent分析完成")
            
            # 显示简要结果信息
            print(f"\n📊 分析结果预览:")
            print(f"   🎭 分析师: {result['agent']}")
            print(f"   📈 股票: {result['symbol']}")
            print(f"   📝 风格: {result['style']}")
            print(f"   📏 分析长度: {len(result['analysis'])}字符")
            
        except Exception as e:
            print(f"❌ 测试出错: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def token_optimization_settings(self):
        """Token优化设置"""
        print("\n" + "="*80)
        print("🗜️ Token优化设置")
        print("="*80)
        
        current_budget = self.token_manager.budget
        
        print(f"当前Token配置:")
        print(f"  📊 总Token限制: {current_budget.max_total_tokens}")
        print(f"  📥 输入Token限制: {current_budget.max_input_tokens}")
        print(f"  📤 输出Token限制: {current_budget.max_output_tokens}")
        print(f"  🔒 预留Token: {current_budget.reserve_tokens}")
        
        print(f"\n🔧 优化建议:")
        print(f"  • 如遇到token超限，建议启用压缩模式")
        print(f"  • 大量股票分析时，建议使用批处理")
        print(f"  • 选择5位以下投资大师可获得最佳性能")
        
        # 简单的token估算工具
        test_text = input("\n🧮 输入文本进行token估算 (可选): ").strip()
        if test_text:
            tokens = self.token_manager.estimate_tokens(test_text)
            print(f"📏 估算Token数: {tokens}")
    
    def system_performance_test(self):
        """系统性能测试"""
        print("\n" + "="*80)
        print("⚡ 系统性能测试")
        print("="*80)
        
        print("🧪 开始系统组件测试...")
        
        # 测试配置加载
        try:
            test_config = ConfigurableInvestmentAgent()
            print("✅ 配置化Agent初始化成功")
        except Exception as e:
            print(f"❌ 配置化Agent初始化失败: {e}")
        
        # 测试Token管理器
        try:
            test_manager = TokenManager()
            test_tokens = test_manager.estimate_tokens("测试文本 test text")
            print(f"✅ Token管理器工作正常 (测试token数: {test_tokens})")
        except Exception as e:
            print(f"❌ Token管理器测试失败: {e}")
        
        # 测试环境变量
        if os.getenv("ALIYUN_API_KEY"):
            print("✅ API密钥配置正常")
        else:
            print("❌ API密钥未配置")
        
        print("\n📊 性能测试完成")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🔷 Agno AI 投资分析系统使用指南

📋 主要功能:
  • 单股深度分析: 使用多位投资大师分析单只股票
  • 多股对比分析: 横向对比多只股票的投资价值
  • 大师风格比较: 了解不同投资大师的理念和方法
  • Token优化处理: 自动处理token超限问题

🎯 投资大师介绍:
  🎩 Warren Buffett  - 价值投资，护城河理论，长期持有
  🧠 Charlie Munger  - 多元思维，逆向思考，理性决策
  📈 Peter Lynch     - 成长投资，消费者洞察，灵活策略
  📚 Benjamin Graham - 安全边际，深度价值，基本面分析
  🌊 Ray Dalio       - 全天候策略，宏观经济，风险平价
  🔢 Joel Greenblatt - 魔法公式，量化价值，统计套利
  ⚡ David Tepper    - 困境反转，宏观敏感，高风险高收益

🔧 Token优化模式:
  • 自动模式: 根据内容大小智能选择处理方式
  • 压缩模式: 提取关键信息，快速生成简化报告
  • 流式模式: 分段处理大内容，保证分析质量
  • 完整模式: 传统完整分析，适合小内容量

💡 使用技巧:
  • 股票代码支持: 美股(AAPL)、A股(000001.SZ)、港股(0700.HK)
  • 批量分析时建议选择3-5位核心投资大师
  • 遇到token超限时优先使用压缩或流式模式
  • 可随时使用Q键快速选择智能推荐的投资大师组合

⚠️ 注意事项:
  • 投资有风险，分析结果仅供参考
  • 请结合实际情况和专业建议做出投资决策
  • 本系统基于公开信息和投资理论，不构成投资建议

📞 技术支持:
  • 检查.env文件中的API密钥配置
  • 确保网络连接正常
  • 如遇问题请查看错误提示信息
"""
        print(help_text)
    
    def run(self):
        """运行主程序"""
        self.show_banner()
        
        while True:
            self.show_main_menu()
            choice = input("请选择操作 (0-7): ").strip()
            
            if choice == "1":
                self.single_stock_analysis()
            elif choice == "2":
                self.multi_stock_comparison()
            elif choice == "3":
                self.master_style_comparison()
            elif choice == "4":
                self.test_configurable_agent()
            elif choice == "5":
                self.token_optimization_settings()
            elif choice == "6":
                self.system_performance_test()
            elif choice == "7":
                self.show_help()
            elif choice == "0":
                print("\n🎉 感谢使用 Agno AI 投资分析系统!")
                print("💰 投资有风险，决策需谨慎!")
                print("🚀 祝您投资顺利，财富增长!")
                break
            else:
                print("❌ 无效选择，请输入 0-7")
            
            # 暂停等待用户确认
            input("\n按回车键继续...")


def main():
    """主函数"""
    try:
        system = AgnoInvestmentSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，系统安全退出")
    except Exception as e:
        print(f"\n❌ 系统错误: {str(e)}")
        print("请检查配置并重试")


if __name__ == "__main__":
    main() 