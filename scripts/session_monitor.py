#!/usr/bin/env python3
"""
Session监控和自动恢复脚本
监控playground运行状态，自动处理session错误
"""

import requests
import time
import sqlite3
import os
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

class SessionMonitor:
    def __init__(self):
        self.base_url = "http://localhost:7777"
        self.project_root = Path(__file__).parent.parent
        self.db_path = self.project_root / "data" / "agent_storage" / "investment_agents.db"
        
    def check_service_health(self):
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.base_url}/v1/playground/status", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_agents(self):
        """获取agent列表"""
        try:
            response = requests.get(f"{self.base_url}/v1/playground/agents", timeout=10)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def clean_expired_sessions(self, hours=24):
        """清理过期的session记录"""
        if not self.db_path.exists():
            return False
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # 获取所有agent表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%agent%';")
            tables = cursor.fetchall()
            
            total_cleaned = 0
            cutoff_time = datetime.now() - timedelta(hours=hours)
            cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')
            
            for table_name, in tables:
                try:
                    # 检查表是否有created_at字段
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    if 'created_at' in columns:
                        cursor.execute(f"DELETE FROM {table_name} WHERE created_at < ?;", (cutoff_str,))
                        cleaned = cursor.rowcount
                        total_cleaned += cleaned
                        if cleaned > 0:
                            print(f"   清理表 {table_name}: {cleaned} 条记录")
                except Exception as e:
                    print(f"   警告: 清理表 {table_name} 时出错: {e}")
            
            conn.commit()
            conn.close()
            
            print(f"✅ 总共清理了 {total_cleaned} 条过期记录")
            return True
            
        except Exception as e:
            print(f"❌ 数据库清理失败: {e}")
            return False
    
    def test_agent_sessions(self):
        """测试所有agent的session创建"""
        agents = self.get_agents()
        if not agents:
            print("❌ 无法获取agent列表")
            return False
        
        print(f"🧪 测试 {len(agents)} 个agents...")
        
        failed_agents = []
        for agent in agents:
            agent_id = agent.get('id')
            agent_name = agent.get('name', 'Unknown')
            
            try:
                # 测试获取sessions
                response = requests.get(
                    f"{self.base_url}/v1/playground/agents/{agent_id}/sessions",
                    params={"user_id": "test_user"},
                    timeout=10
                )
                
                if response.status_code != 200:
                    failed_agents.append(agent_name)
                    print(f"   ❌ {agent_name}: HTTP {response.status_code}")
                else:
                    print(f"   ✅ {agent_name}: 正常")
                    
            except Exception as e:
                failed_agents.append(agent_name)
                print(f"   ❌ {agent_name}: {e}")
        
        if failed_agents:
            print(f"\n⚠️  {len(failed_agents)} 个agents有问题: {', '.join(failed_agents)}")
            return False
        else:
            print("✅ 所有agents测试通过")
            return True
    
    def auto_fix_sessions(self):
        """自动修复session问题"""
        print("🔧 开始自动修复...")
        
        # 1. 清理过期sessions
        print("1. 清理过期sessions...")
        self.clean_expired_sessions(hours=6)  # 清理6小时前的记录
        
        # 2. 测试agents
        print("\n2. 测试agent状态...")
        agents_ok = self.test_agent_sessions()
        
        if not agents_ok:
            print("\n3. 尝试数据库修复...")
            # 可以在这里添加更多修复逻辑
            return False
        
        return True
    
    def monitor_loop(self, interval=300):  # 5分钟检查一次
        """持续监控循环"""
        print(f"🔍 开始监控playground服务 (每{interval}秒检查一次)")
        print("按 Ctrl+C 停止监控")
        
        try:
            while True:
                print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 健康检查")
                
                if not self.check_service_health():
                    print("❌ 服务不可用")
                    time.sleep(30)  # 服务不可用时等待短一些
                    continue
                
                # 定期清理session
                if datetime.now().minute % 30 == 0:  # 每30分钟清理一次
                    print("🧹 定期清理过期sessions...")
                    self.clean_expired_sessions(hours=24)
                
                print("✅ 服务正常运行")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 监控已停止")

def main():
    monitor = SessionMonitor()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "health":
            print("🏥 检查服务健康状态...")
            if monitor.check_service_health():
                print("✅ 服务正常运行")
            else:
                print("❌ 服务不可用")
                
        elif cmd == "clean":
            hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
            print(f"🧹 清理 {hours} 小时前的session记录...")
            monitor.clean_expired_sessions(hours)
            
        elif cmd == "test":
            print("🧪 测试所有agent sessions...")
            monitor.test_agent_sessions()
            
        elif cmd == "fix":
            print("🔧 自动修复session问题...")
            success = monitor.auto_fix_sessions()
            if success:
                print("✅ 修复完成")
            else:
                print("❌ 修复失败，可能需要手动处理")
                
        elif cmd == "monitor":
            monitor.monitor_loop()
            
        else:
            print("❌ 未知命令")
            print_usage()
    else:
        print_usage()

def print_usage():
    print("""
🛠️  Session监控工具使用说明：

命令:
  health     - 检查服务健康状态
  clean [小时] - 清理指定小时前的session记录 (默认24小时)
  test       - 测试所有agent的session功能
  fix        - 自动修复session问题
  monitor    - 开始持续监控 (Ctrl+C停止)

示例:
  python scripts/session_monitor.py health
  python scripts/session_monitor.py clean 6
  python scripts/session_monitor.py fix
  python scripts/session_monitor.py monitor
""")

if __name__ == "__main__":
    main() 