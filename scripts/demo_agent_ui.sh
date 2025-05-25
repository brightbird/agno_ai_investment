#!/bin/bash
"""
Agent UI 快速演示脚本
===================

快速启动投资团队演示

使用方法:
    bash scripts/demo_agent_ui.sh
"""

echo "🎯 Agent UI 投资团队快速演示"
echo "=================================="
echo

# 检查环境变量
if [ -z "$ALIYUN_API_KEY" ]; then
    echo "❌ 错误: 未设置 ALIYUN_API_KEY 环境变量"
    echo "💡 请先设置您的阿里云 API 密钥:"
    echo "   export ALIYUN_API_KEY=your_api_key"
    exit 1
fi

echo "✅ API 密钥已配置"
echo

# 检查虚拟环境
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  建议激活虚拟环境:"
    echo "   source .venv/bin/activate"
    echo
fi

echo "🚀 启动演示..."
echo

# 显示说明
echo "📋 演示步骤:"
echo "1. 🖥️  启动 Playground 服务 (localhost:7777)"
echo "2. 🌐 打开 Agent UI (https://app.agno.com/playground)"
echo "3. 🔗 连接到本地端点"
echo "4. 🏆 选择投资团队开始分析"
echo

# 询问是否继续
read -p "按 Enter 开始启动 Playground 服务..."

echo
echo "🌟 正在启动 Playground..."
echo "💡 启动后请访问: https://app.agno.com/playground"
echo "🔗 添加端点: localhost:7777"
echo

# 启动 playground
python apps/playground.py 