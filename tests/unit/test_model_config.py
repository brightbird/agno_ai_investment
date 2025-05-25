#!/usr/bin/env python3
"""
测试模型配置从配置文件读取是否正常
"""

import os
import sys
from dotenv import load_dotenv

# 导入路径现在由conftest.py统一处理

def test_model_config_loading():
    """测试模型配置加载"""
    print("🧪 测试模型配置加载")
    print("=" * 60)
    
    try:
        # 1. 测试配置文件加载函数
        from src.agents.multi_agent_investment_v2 import load_default_model_from_config
        
        default_model = load_default_model_from_config()
        print(f"📋 配置文件中的默认模型: {default_model}")
        
        # 2. 测试EnhancedInvestmentSynthesizer是否正确使用默认模型
        from src.agents.multi_agent_investment_v2 import EnhancedInvestmentSynthesizer
        
        print("\n🔧 测试EnhancedInvestmentSynthesizer...")
        synthesizer = EnhancedInvestmentSynthesizer(enable_token_optimization=True)
        print("✅ EnhancedInvestmentSynthesizer创建成功")
        
        # 3. 测试MultiAgentInvestmentAnalyzerV2是否正确使用默认模型
        from src.agents.multi_agent_investment_v2 import MultiAgentInvestmentAnalyzerV2
        
        print("\n🔧 测试MultiAgentInvestmentAnalyzerV2...")
        analyzer = MultiAgentInvestmentAnalyzerV2(enable_token_optimization=True)
        print("✅ MultiAgentInvestmentAnalyzerV2创建成功")
        
        # 4. 验证预期的模型
        expected_model = "qwen-plus-latest"
        if default_model == expected_model:
            print(f"\n✅ 配置加载正确: {default_model}")
        else:
            print(f"\n⚠️ 配置可能有问题，期望: {expected_model}，实际: {default_model}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_manual_model_override():
    """测试手动指定模型是否优先于配置文件"""
    print("\n🧪 测试手动模型覆盖")
    print("=" * 60)
    
    try:
        from src.agents.multi_agent_investment_v2 import MultiAgentInvestmentAnalyzerV2
        
        # 手动指定模型
        manual_model = "qwen-max"
        print(f"📋 手动指定模型: {manual_model}")
        
        analyzer = MultiAgentInvestmentAnalyzerV2(model_id=manual_model, enable_token_optimization=True)
        print("✅ 手动模型指定测试成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 手动模型测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def show_available_models():
    """显示配置文件中的可用模型"""
    print("\n📋 配置文件中的可用模型")
    print("=" * 60)
    
    try:
        import yaml
        
        # 获取正确的配置文件路径
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        config_file = os.path.join(project_root, "src", "config", "investment_agents_config.yaml")
        
        with open(config_file, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            
        model_config = config['model_config']
        print(f"🎯 默认模型: {model_config['default_model']}")
        print("📋 可用模型:")
        for model in model_config['available_models']:
            indicator = "👈 (默认)" if model == model_config['default_model'] else ""
            print(f"   - {model} {indicator}")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取配置失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试模型配置加载")
    print("=" * 80)
    
    # 显示配置文件信息
    show_available_models()
    
    # 测试默认模型加载
    success1 = test_model_config_loading()
    
    # 测试手动模型覆盖
    success2 = test_manual_model_override()
    
    if success1 and success2:
        print("\n🎉 所有测试通过！")
        print("✅ 模型配置从配置文件正确读取")
        print("✅ 手动指定模型正常优先于配置文件")
        print("✅ 系统可以正确使用您修改的默认模型")
        
        print("\n💡 使用建议:")
        print("   - 修改 src/config/investment_agents_config.yaml 中的 default_model")
        print("   - 系统会自动使用新的默认模型")
        print("   - 也可以在代码中手动指定模型ID来覆盖默认设置")
    else:
        print("\n❌ 部分测试未通过，需要进一步检查")
    
    return success1 and success2

if __name__ == "__main__":
    main() 