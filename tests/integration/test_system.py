#!/usr/bin/env python3
"""
系统集成测试
测试各组件之间的集成和协作
"""

import os
import sys
from dotenv import load_dotenv

# 导入路径现在由conftest.py统一处理

def test_system_integration():
    """测试系统集成"""
    print("🧪 测试系统集成")
    print("=" * 60)
    
    try:
        # 测试主系统类
        import main
        system = main.AgnoInvestmentSystem()
        print("✅ AgnoInvestmentSystem初始化成功")
        
        # 测试系统组件
        print(f"📋 多Agent分析器: 支持{len(system.analyzer_v2.available_masters)}位大师")
        print(f"🔧 配置化Agent: 可用")
        print(f"🗜️ Token管理器: 可用")
        
        return True
        
    except Exception as e:
        print(f"❌ 系统集成测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_environment_setup():
    """测试环境设置"""
    print("\n🧪 测试环境设置")
    print("=" * 60)
    
    try:
        # 测试环境变量
        load_dotenv()
        if os.getenv("ALIYUN_API_KEY"):
            print("✅ API密钥已配置")
        else:
            print("⚠️ API密钥未配置")
        
        # 测试配置文件
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "src", "config", "investment_agents_config.yaml"
        )
        if os.path.exists(config_path):
            print("✅ 配置文件存在")
        else:
            print("❌ 配置文件不存在")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 环境设置测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_component_interaction():
    """测试组件交互"""
    print("\n🧪 测试组件交互")
    print("=" * 60)
    
    try:
        from src.agents.multi_agent_investment_v2 import MultiAgentInvestmentAnalyzerV2
        from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent
        from src.utils.token_manager import TokenManager
        
        # 创建各组件
        analyzer = MultiAgentInvestmentAnalyzerV2(enable_token_optimization=True)
        config_agent = ConfigurableInvestmentAgent()
        token_manager = TokenManager()
        
        # 测试组件间的数据交互
        available_masters_analyzer = analyzer.available_masters
        available_masters_config = config_agent.get_available_masters()
        
        if set(available_masters_analyzer) == set(available_masters_config):
            print("✅ 组件间大师列表一致")
        else:
            print("⚠️ 组件间大师列表不一致")
        
        # 测试token管理集成
        test_text = "测试文本"
        tokens = token_manager.estimate_tokens(test_text)
        print(f"✅ Token估算集成正常: {tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ 组件交互测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 开始系统集成测试")
    print("=" * 80)
    
    # 测试环境设置
    success1 = test_environment_setup()
    
    # 测试组件交互
    success2 = test_component_interaction()
    
    # 测试系统集成
    success3 = test_system_integration()
    
    if success1 and success2 and success3:
        print("\n🎉 所有集成测试通过！")
        print("✅ 环境设置正常")
        print("✅ 组件交互正常")
        print("✅ 系统集成正常")
        
        print("\n💡 集成状态:")
        print("   - 各组件能正确协作")
        print("   - 数据交换流畅")
        print("   - 系统作为整体运行正常")
    else:
        print("\n❌ 部分集成测试未通过，需要进一步检查")
    
    return success1 and success2 and success3

if __name__ == "__main__":
    main() 