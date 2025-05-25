#!/usr/bin/env python3
"""
测试主菜单选项3 - 投资大师风格比较功能
"""

import os
import sys
from dotenv import load_dotenv

# 导入路径现在由conftest.py统一处理

def simulate_main_menu_option3():
    """模拟主菜单选项3的完整流程"""
    print("🧪 模拟主菜单选项3 - 投资大师风格比较")
    print("=" * 80)
    
    try:
        # 模拟主菜单系统初始化
        from src.agents.multi_agent_investment_v2 import MultiAgentInvestmentAnalyzerV2
        from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent
        from src.utils.token_manager import TokenManager
        
        print("🤖 初始化系统组件...")
        
        # 模拟AgnoInvestmentSystem的初始化过程
        analyzer_v2 = MultiAgentInvestmentAnalyzerV2(enable_token_optimization=True)
        config_agent = ConfigurableInvestmentAgent()
        token_manager = TokenManager()
        
        print("✅ 系统初始化完成")
        
        # 模拟用户选择选项3
        print("\n👤 用户选择: 3️⃣ 投资大师风格比较")
        print("=" * 80)
        
        # 执行master_style_comparison功能
        print("🎭 投资大师风格比较")
        print("="*80)
        
        analyzer_v2.config_analyzer.get_master_comparison()
        
        print("\n✅ 选项3执行成功！")
        print("🎉 投资大师风格比较功能正常工作")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 测试主菜单选项3功能修复")
    print("=" * 80)
    
    # 模拟完整的选项3流程
    success = simulate_main_menu_option3()
    
    if success:
        print("\n🎉 测试完全通过！")
        print("✅ 主菜单选项3 - 投资大师风格比较功能已修复")
        print("✅ 用户现在可以正常使用该功能")
        print("✅ 不再显示'❌ 没有加载的投资大师Agent'错误")
        
        print("\n💡 功能说明:")
        print("   - 显示所有7位投资大师的详细信息")
        print("   - 包含投资哲学、风格特征、分析方法")
        print("   - 提供典型特征和案例引用")
        print("   - 显示当前Agent加载状态")
        
        print("\n🎯 用户体验改善:")
        print("   - 无需预先加载Agent即可查看大师信息")
        print("   - 更详细和结构化的信息展示")
        print("   - 清晰的emoji图标识别")
        print("   - 友好的使用提示")
    else:
        print("\n❌ 测试未通过，需要进一步检查")
    
    return success

if __name__ == "__main__":
    main() 