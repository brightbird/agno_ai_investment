#!/usr/bin/env python3
"""
测试修复后的系统功能
"""

import os
import sys
from dotenv import load_dotenv

# 导入路径现在由conftest.py统一处理

def test_system_initialization():
    """测试系统初始化"""
    print("🧪 测试系统初始化")
    print("=" * 60)
    
    try:
        from src.agents.multi_agent_investment_v2 import MultiAgentInvestmentAnalyzerV2
        from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent
        from src.utils.token_manager import TokenManager
        
        # 测试各组件初始化
        analyzer = MultiAgentInvestmentAnalyzerV2(enable_token_optimization=True)
        print("✅ MultiAgentInvestmentAnalyzerV2初始化成功")
        
        config_agent = ConfigurableInvestmentAgent()
        print("✅ ConfigurableInvestmentAgent初始化成功")
        
        token_manager = TokenManager()
        print("✅ TokenManager初始化成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 系统初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration_loading():
    """测试配置加载"""
    print("\n🧪 测试配置加载")
    print("=" * 60)
    
    try:
        import yaml
        
        # 获取配置文件路径
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        config_file = os.path.join(project_root, "src", "config", "investment_agents_config.yaml")
        
        with open(config_file, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        print("✅ 配置文件加载成功")
        print(f"📋 默认模型: {config['model_config']['default_model']}")
        print(f"📋 可用大师: {len(config['investment_masters'])}位")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置加载失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_master_agents():
    """测试投资大师Agent创建"""
    print("\n🧪 测试投资大师Agent创建")
    print("=" * 60)
    
    try:
        from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent
        
        config_agent = ConfigurableInvestmentAgent()
        available_masters = config_agent.get_available_masters()
        
        print(f"📋 可用投资大师: {len(available_masters)}位")
        
        # 测试创建第一个大师Agent
        if available_masters:
            test_master = available_masters[0]
            master_agent = config_agent.create_agent(test_master)
            print(f"✅ 成功创建: {master_agent.agent_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 投资大师Agent测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试修复后的系统功能")
    print("=" * 80)
    
    # 测试系统初始化
    success1 = test_system_initialization()
    
    # 测试配置加载
    success2 = test_configuration_loading()
    
    # 测试投资大师Agent
    success3 = test_master_agents()
    
    if success1 and success2 and success3:
        print("\n🎉 所有测试通过！")
        print("✅ 系统初始化功能正常")
        print("✅ 配置加载功能正常")
        print("✅ 投资大师Agent创建正常")
        
        print("\n💡 修复内容:")
        print("   - 系统各组件能正确初始化")
        print("   - 配置文件能正确读取和解析")
        print("   - 投资大师Agent能正常创建和使用")
    else:
        print("\n❌ 部分测试未通过，需要进一步检查")
    
    return success1 and success2 and success3

if __name__ == "__main__":
    main() 