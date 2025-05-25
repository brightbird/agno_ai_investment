#!/usr/bin/env python3
"""
Agno AI 投资分析系统 - 兼容性启动脚本
=======================================

这是一个向后兼容的启动脚本，重定向到新的应用结构。
推荐使用新的启动方式：python apps/playground.py

运行方式:
    python playground.py  # 兼容性方式
    python apps/playground.py  # 推荐方式
    bash scripts/start_playground.sh  # 脚本方式
"""

import os
import sys
import subprocess

def main():
    """主函数 - 重定向到新的应用程序"""
    print("🔄 重定向到新的应用结构...")
    print("💡 推荐使用: python apps/playground.py")
    print("")
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "apps", "playground.py")
    
    if not os.path.exists(app_path):
        print("❌ 错误: 找不到 apps/playground.py")
        print("请确保项目结构正确")
        sys.exit(1)
    
    # 执行真实的应用程序
    try:
        subprocess.run([sys.executable, app_path] + sys.argv[1:])
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 