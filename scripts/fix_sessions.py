#!/usr/bin/env python3
"""
Session修复脚本 - 解决404 session not found错误
"""

import sqlite3
import os
import sys
from pathlib import Path

def fix_sessions():
    """修复session相关问题"""
    
    # 获取数据库路径
    project_root = Path(__file__).parent.parent
    db_path = project_root / "data" / "agent_storage" / "investment_agents.db"
    
    if not db_path.exists():
        print(f"❌ 数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        print("🔍 检查数据库表结构...")
        
        # 检查现有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ 找到表: {[table[0] for table in tables]}")
        
        # 清理过期或无效的session记录
        print("🧹 清理无效session记录...")
        
        for table_name, in tables:
            if 'agent' in table_name.lower():
                try:
                    # 检查表结构
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = [col[1] for col in cursor.fetchall()]
                    print(f"   表 {table_name}: {columns}")
                    
                    # 如果有session相关字段，清理旧数据
                    if 'session_id' in columns:
                        cursor.execute(f"DELETE FROM {table_name} WHERE created_at < datetime('now', '-7 days');")
                        deleted = cursor.rowcount
                        if deleted > 0:
                            print(f"   🗑️  清理了 {deleted} 条过期记录")
                    
                except Exception as e:
                    print(f"   ⚠️  处理表 {table_name} 时出错: {e}")
        
        # 提交更改
        conn.commit()
        print("✅ 数据库清理完成")
        
    except Exception as e:
        print(f"❌ 数据库操作失败: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()
    
    return True

def reset_agents():
    """重置所有agent配置"""
    
    project_root = Path(__file__).parent.parent
    db_path = project_root / "data" / "agent_storage" / "investment_agents.db"
    
    print("🔄 重置agent数据库...")
    
    # 备份现有数据库
    if db_path.exists():
        backup_path = db_path.with_suffix('.db.backup')
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"📦 已备份数据库到: {backup_path}")
        
        # 删除现有数据库，让系统重新创建
        db_path.unlink()
        print("🗑️  已删除旧数据库")
    
    print("✅ 数据库重置完成，重启服务时将自动重新创建")

if __name__ == "__main__":
    print("🛠️  Agno AI Investment - Session修复工具")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print("⚠️  警告：将重置所有agent数据（包括对话历史）")
        confirm = input("是否继续？(y/N): ")
        if confirm.lower() == 'y':
            reset_agents()
        else:
            print("❌ 已取消重置")
    else:
        print("🔧 修复session问题...")
        success = fix_sessions()
        
        if success:
            print("\n🎉 修复完成！建议重启playground服务：")
            print("   python apps/playground.py")
        else:
            print("\n💡 如果问题仍然存在，可以尝试完全重置：")
            print("   python scripts/fix_sessions.py --reset")
    
    print("\n📚 更多帮助: docs/PLAYGROUND_GUIDE.md") 