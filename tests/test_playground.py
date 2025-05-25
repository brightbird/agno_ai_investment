#!/usr/bin/env python3
"""
测试 Agno Agent Playground 功能
验证投资分析系统的 UI 界面是否正常工作
"""

import os
import sys
from dotenv import load_dotenv

# 添加src路径
project_root = os.path.dirname(__file__)
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def test_environment():
    """测试环境配置"""
    print("🧪 测试环境配置")
    print("=" * 60)
    
    # 检查环境变量
    load_dotenv()
    api_key = os.getenv("ALIYUN_API_KEY")
    
    if api_key:
        print("✅ ALIYUN_API_KEY 已设置")
    else:
        print("❌ ALIYUN_API_KEY 未设置")
        return False
    
    # 检查必要文件
    required_files = [
        "src/config/investment_agents_config.yaml",
        "src/agents/configurable_investment_agent.py",
        "playground.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
            return False
    
    return True

def test_dependencies():
    """测试依赖包"""
    print("\n🧪 测试依赖包")
    print("=" * 60)
    
    required_packages = [
        ("agno", "Agno核心框架"),
        ("fastapi", "FastAPI Web框架"),
        ("uvicorn", "ASGI服务器"),
        ("sqlalchemy", "数据库ORM"),
        ("pandas", "数据处理"),
        ("yfinance", "金融数据"),
        ("yaml", "配置文件解析"),
        ("dotenv", "环境变量")
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            if package == "yaml":
                import yaml
            elif package == "dotenv":
                from dotenv import load_dotenv
            else:
                __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"❌ {package} - {description} (缺失)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ 缺少依赖包: {', '.join(missing_packages)}")
        print("💡 请运行: pip install -r requirements.txt")
        return False
    
    return True

def test_agent_creation():
    """测试Agent创建"""
    print("\n🧪 测试Agent创建")
    print("=" * 60)
    
    try:
        from agents.configurable_investment_agent import ConfigurableInvestmentAgent
        
        # 创建配置代理
        config_agent = ConfigurableInvestmentAgent()
        print("✅ ConfigurableInvestmentAgent 创建成功")
        
        # 获取可用投资大师
        masters = config_agent.get_available_masters()
        print(f"✅ 可用投资大师: {len(masters)}位")
        
        for master in masters:
            print(f"   - {master}")
        
        # 测试创建单个Agent
        if masters:
            test_master = masters[0]
            master_info = config_agent.get_master_info(test_master)
            print(f"✅ 获取 {test_master} 信息成功")
            print(f"   名称: {master_info['agent_name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent创建测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_playground_creation():
    """测试Playground创建"""
    print("\n🧪 测试Playground创建")
    print("=" * 60)
    
    try:
        # 导入Playground相关模块
        from agno.agent import Agent
        from agno.models.openai.like import OpenAILike
        from agno.playground import Playground
        print("✅ Agno模块导入成功")
        
        # 测试模型创建
        model = OpenAILike(
            id="qwen-plus-latest",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=os.getenv("ALIYUN_API_KEY")
        )
        print("✅ 模型创建成功")
        
        # 创建简单测试Agent
        test_agent = Agent(
            name="测试Agent",
            model=model,
            instructions=["你是一个测试用的投资分析师"]
        )
        print("✅ 测试Agent创建成功")
        
        # 创建Playground
        playground = Playground(agents=[test_agent])
        print("✅ Playground创建成功")
        
        # 获取app
        app = playground.get_app()
        print("✅ FastAPI应用创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ Playground创建测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_playground():
    """测试完整Playground系统"""
    print("\n🧪 测试完整Playground系统")
    print("=" * 60)
    
    try:
        # 导入自定义Playground
        import playground
        
        # 创建投资Playground实例（不启动服务器）
        investment_playground = playground.InvestmentPlayground()
        print("✅ InvestmentPlayground创建成功")
        
        # 检查创建的Agents数量
        agents = investment_playground.agents
        print(f"✅ 创建了 {len(agents)} 个投资分析Agents")
        
        for agent in agents:
            print(f"   - {agent.name}")
        
        # 获取Playground应用
        app = investment_playground.get_playground_app()
        print("✅ Playground应用获取成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 完整Playground测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试 Agno Agent Playground 功能")
    print("=" * 80)
    
    tests = [
        ("环境配置", test_environment),
        ("依赖包", test_dependencies),
        ("Agent创建", test_agent_creation),
        ("Playground创建", test_playground_creation),
        ("完整系统", test_full_playground)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试项目: {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"✅ {test_name} 测试通过")
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
    
    # 测试总结
    print("\n" + "=" * 80)
    print("📊 测试总结")
    print("=" * 80)
    
    success_rate = (passed / total) * 100
    print(f"📈 测试通过率: {passed}/{total} ({success_rate:.1f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        print("✅ Agno Agent Playground 系统可以正常运行")
        print("")
        print("🚀 启动命令:")
        print("   python playground.py")
        print("")
        print("🌐 访问方式:")
        print("   1. 运行 'ag setup' 进行认证")
        print("   2. 访问 http://app.agno.com/playground")
        print("   3. 选择 localhost:7777 端点")
        print("   4. 开始与投资大师对话！")
        
    elif passed >= total * 0.8:
        print("\n⚠️ 大部分测试通过，系统基本可用")
        print("🔧 请检查失败的测试项目")
        
    else:
        print("\n❌ 测试失败过多，请修复问题后再次测试")
        print("💡 常见解决方案:")
        print("   - 检查环境变量设置")
        print("   - 安装缺失的依赖包")
        print("   - 确认配置文件正确")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 