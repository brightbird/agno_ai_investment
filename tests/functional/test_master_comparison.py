#!/usr/bin/env python3
"""
测试投资大师风格比较功能修复
"""

import os
import sys
from dotenv import load_dotenv

# 导入路径现在由conftest.py统一处理

def test_master_comparison():
    """测试投资大师风格比较功能"""
    print("🧪 测试投资大师风格比较功能")
    print("=" * 60)
    
    try:
        # 导入必要的类
        from src.agents.configurable_investment_agent import ConfigurableMultiAgentAnalyzer
        
        # 创建分析器
        analyzer = ConfigurableMultiAgentAnalyzer()
        print("✅ ConfigurableMultiAgentAnalyzer创建成功")
        
        # 测试get_master_comparison方法
        print("\n📋 测试投资大师风格比较显示...")
        print("=" * 60)
        
        analyzer.get_master_comparison()
        
        print("\n✅ 投资大师风格比较功能测试成功！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_available_masters():
    """测试获取可用投资大师列表"""
    print("\n🧪 测试可用投资大师列表")
    print("=" * 60)
    
    try:
        from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent
        
        agent_factory = ConfigurableInvestmentAgent()
        available_masters = agent_factory.get_available_masters()
        
        print(f"📋 可用投资大师 ({len(available_masters)}位):")
        for master in available_masters:
            print(f"   - {master}")
        
        print("\n✅ 投资大师列表获取成功！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_master_info():
    """测试获取投资大师详细信息"""
    print("\n🧪 测试投资大师详细信息获取")
    print("=" * 60)
    
    try:
        from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent
        
        agent_factory = ConfigurableInvestmentAgent()
        available_masters = agent_factory.get_available_masters()
        
        # 测试获取第一个投资大师的信息
        if available_masters:
            test_master = available_masters[0]
            print(f"📊 测试获取 {test_master} 的详细信息...")
            
            info = agent_factory.get_master_info(test_master)
            
            print(f"✅ 成功获取信息:")
            print(f"   🎯 名称: {info['agent_name']}")
            print(f"   📝 描述: {info['description'][:100]}...")
            print(f"   💡 投资哲学数量: {len(info['investment_philosophy'])}")
            print(f"   🎭 风格特征: {info['style_characteristics']['voice']}")
            
        print("\n✅ 投资大师信息获取成功！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试投资大师风格比较功能修复")
    print("=" * 80)
    
    # 测试1: 可用投资大师列表
    success1 = test_available_masters()
    
    # 测试2: 投资大师详细信息
    success2 = test_master_info()
    
    # 测试3: 投资大师风格比较功能
    success3 = test_master_comparison()
    
    if success1 and success2 and success3:
        print("\n🎉 所有测试通过！")
        print("✅ 投资大师风格比较功能已修复")
        print("✅ 现在可以在主菜单中正常使用选项3")
        print("✅ 系统会显示所有可用投资大师的详细信息")
        
        print("\n💡 修复内容:")
        print("   - 不再要求先加载Agent才能查看投资大师信息")
        print("   - 显示所有可用投资大师的完整信息")
        print("   - 提供更详细的投资哲学和风格特征")
        print("   - 增加了当前加载状态的显示")
    else:
        print("\n❌ 部分测试未通过，需要进一步检查")
    
    return success1 and success2 and success3

if __name__ == "__main__":
    main() 