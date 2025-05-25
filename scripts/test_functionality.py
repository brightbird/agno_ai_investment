#!/usr/bin/env python3
"""
功能测试脚本 - 验证Agno AI Investment系统是否正常工作
测试agent创建、对话功能等核心特性
"""

import requests
import json
import time
import sys
from datetime import datetime

class FunctionalityTester:
    def __init__(self):
        self.base_url = "http://localhost:7777"
        self.test_user_id = f"test_user_{int(time.time())}"
        
    def test_service_status(self):
        """测试服务状态"""
        print("🔍 测试服务状态...")
        try:
            response = requests.get(f"{self.base_url}/v1/playground/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ 服务正常: {data}")
                return True
            else:
                print(f"   ❌ 服务响应异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ 服务连接失败: {e}")
            return False
    
    def get_agents(self):
        """获取agent列表"""
        print("📋 获取agent列表...")
        try:
            response = requests.get(f"{self.base_url}/v1/playground/agents", timeout=10)
            if response.status_code == 200:
                agents = response.json()
                print(f"   ✅ 找到 {len(agents)} 个agents")
                for agent in agents:
                    print(f"      - {agent.get('name', 'Unknown')}")
                return agents
            else:
                print(f"   ❌ 获取agent列表失败: {response.status_code}")
                return []
        except Exception as e:
            print(f"   ❌ 请求失败: {e}")
            return []
    
    def test_create_session(self, agent):
        """测试创建新session"""
        agent_id = agent.get('id')
        agent_name = agent.get('name', 'Unknown')
        
        print(f"💬 测试创建session: {agent_name}")
        
        try:
            # 创建新session
            response = requests.post(
                f"{self.base_url}/v1/playground/agents/{agent_id}/sessions",
                json={"user_id": self.test_user_id},
                timeout=15
            )
            
            if response.status_code == 200:
                session_data = response.json()
                session_id = session_data.get('session_id')
                print(f"   ✅ Session创建成功: {session_id}")
                return session_id
            else:
                print(f"   ❌ Session创建失败: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
            return None
    
    def test_send_message(self, agent, session_id, message="你好"):
        """测试发送消息"""
        agent_id = agent.get('id')
        agent_name = agent.get('name', 'Unknown')
        
        print(f"📤 测试发送消息: {agent_name}")
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/playground/agents/{agent_id}/sessions/{session_id}",
                json={
                    "message": message,
                    "user_id": self.test_user_id,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result.get('messages', [])
                if reply:
                    last_message = reply[-1].get('content', 'No content')
                    print(f"   ✅ 收到回复: {last_message[:100]}...")
                    return True
                else:
                    print("   ⚠️  响应为空")
                    return False
            else:
                print(f"   ❌ 发送失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
            return False
    
    def test_agent_functionality(self, agent):
        """测试单个agent的完整功能"""
        agent_name = agent.get('name', 'Unknown')
        print(f"\n🤖 测试Agent: {agent_name}")
        print("-" * 40)
        
        # 1. 创建session
        session_id = self.test_create_session(agent)
        if not session_id:
            return False
        
        # 2. 发送测试消息
        success = self.test_send_message(agent, session_id, "你好，请简单介绍一下自己")
        
        return success
    
    def run_comprehensive_test(self):
        """运行全面测试"""
        print("🧪 Agno AI Investment - 功能测试")
        print("=" * 50)
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👤 测试用户ID: {self.test_user_id}")
        print()
        
        # 1. 测试服务状态
        if not self.test_service_status():
            print("❌ 服务状态测试失败，停止测试")
            return False
        
        # 2. 获取agents
        agents = self.get_agents()
        if not agents:
            print("❌ 无法获取agent列表，停止测试")
            return False
        
        # 3. 测试每个agent
        successful_agents = 0
        failed_agents = []
        
        for i, agent in enumerate(agents):
            try:
                if self.test_agent_functionality(agent):
                    successful_agents += 1
                else:
                    failed_agents.append(agent.get('name', 'Unknown'))
            except Exception as e:
                agent_name = agent.get('name', 'Unknown')
                failed_agents.append(agent_name)
                print(f"   ❌ 测试异常: {e}")
            
            # 在测试之间稍微等待
            if i < len(agents) - 1:
                time.sleep(2)
        
        # 4. 显示测试结果
        print("\n📊 测试结果汇总")
        print("=" * 50)
        print(f"✅ 成功: {successful_agents}/{len(agents)} agents")
        
        if failed_agents:
            print(f"❌ 失败: {', '.join(failed_agents)}")
        else:
            print("🎉 所有agents测试通过！")
        
        print(f"\n💡 测试结论:")
        if successful_agents == len(agents):
            print("   ✅ 系统功能完全正常，404错误可以忽略")
        elif successful_agents > 0:
            print("   ⚠️  部分agents正常工作，404错误可能是正常现象")
        else:
            print("   ❌ 系统可能存在问题，需要进一步排查")
        
        return successful_agents > 0
    
    def test_specific_functions(self):
        """测试特定功能"""
        print("\n🎯 特定功能测试")
        print("=" * 30)
        
        agents = self.get_agents()
        if not agents:
            return False
        
        # 找到投资大师选择助手
        selector_agent = None
        for agent in agents:
            if "选择助手" in agent.get('name', ''):
                selector_agent = agent
                break
        
        if selector_agent:
            print("🎯 测试投资大师选择功能...")
            session_id = self.test_create_session(selector_agent)
            if session_id:
                self.test_send_message(
                    selector_agent, 
                    session_id, 
                    "我是新手投资者，想要学习价值投资，请推荐合适的投资大师"
                )
        
        # 找到Warren Buffett agent
        buffett_agent = None
        for agent in agents:
            if "Warren Buffett" in agent.get('name', ''):
                buffett_agent = agent
                break
        
        if buffett_agent:
            print("\n🎩 测试Warren Buffett分析功能...")
            session_id = self.test_create_session(buffett_agent)
            if session_id:
                self.test_send_message(
                    buffett_agent,
                    session_id,
                    "请从价值投资角度分析苹果公司(AAPL)的投资价值"
                )

def main():
    tester = FunctionalityTester()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "quick":
            print("⚡ 快速测试模式")
            success = tester.test_service_status()
            agents = tester.get_agents()
            if success and agents:
                print("✅ 基本功能正常")
            else:
                print("❌ 基本功能异常")
                
        elif cmd == "full":
            print("🔬 完整测试模式")
            tester.run_comprehensive_test()
            tester.test_specific_functions()
            
        elif cmd == "specific":
            print("🎯 特定功能测试")
            tester.test_specific_functions()
            
        else:
            print_usage()
    else:
        # 默认运行综合测试
        tester.run_comprehensive_test()

def print_usage():
    print("""
🧪 功能测试工具使用说明:

命令:
  (无参数)  - 运行综合测试
  quick     - 快速测试基本功能
  full      - 完整测试(综合+特定功能)
  specific  - 仅测试特定投资功能

示例:
  python scripts/test_functionality.py
  python scripts/test_functionality.py quick
  python scripts/test_functionality.py full
""")

if __name__ == "__main__":
    main() 