#!/bin/bash

# Agno AI 投资分析系统 - Playground 启动脚本

echo "🚀 启动 Agno AI 投资分析系统 Playground"
echo "=========================================="

# 检查是否在项目根目录
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查关键文件
if [[ ! -f "apps/playground.py" ]]; then
    echo "❌ 错误: 找不到 apps/playground.py"
    echo "💡 请确保项目结构正确"
    exit 1
fi

# 检查虚拟环境
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️ 建议激活虚拟环境:"
    echo "   source .venv/bin/activate"
    echo ""
fi

# 检查环境变量
if [[ -z "$ALIYUN_API_KEY" ]]; then
    echo "❌ 错误: 未设置 ALIYUN_API_KEY 环境变量"
    echo "💡 请先设置您的 API 密钥:"
    echo "   export ALIYUN_API_KEY=your_api_key"
    echo "   或复制 .env.example 为 .env 并配置"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 显示访问信息
echo "📋 使用说明:"
echo "1. 等待服务启动完成"
echo "2. 运行认证命令: ag setup (如果还没有)"
echo "3. 访问界面: http://app.agno.com/playground"
echo "4. 选择 localhost:7777 端点"
echo "5. 开始与投资大师对话！"
echo ""

echo "💡 可用的投资大师:"
echo "   🎩 Warren Buffett - 价值投资分析师"
echo "   🧠 Charlie Munger - 多学科投资分析师"
echo "   📈 Peter Lynch - 成长价值投资分析师"
echo "   📚 Benjamin Graham - 价值投资鼻祖"
echo "   🌊 Ray Dalio - 全天候投资分析师"
echo "   🔢 Joel Greenblatt - 魔法公式分析师"
echo "   ⚡ David Tepper - 困境投资专家"
echo "   🏦 投资组合综合分析师 - 多角度投资建议"
echo ""

echo "🌟 正在启动 Playground 服务器..."
echo "按 Ctrl+C 停止服务"
echo ""

# 启动 Playground
python apps/playground.py 