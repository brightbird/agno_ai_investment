#!/bin/bash

# Agno AI 投资分析系统 - 环境配置脚本

echo "🔧 Agno AI 投资分析系统 - 环境配置"
echo "=================================="

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "🐍 Python版本: $python_version"

# 创建虚拟环境 (如果不存在)
if [[ ! -d ".venv" ]]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv .venv
    echo "✅ 虚拟环境创建完成"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境提示
echo ""
echo "💡 请激活虚拟环境:"
echo "   source .venv/bin/activate"
echo ""

# 检查是否已激活虚拟环境
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 虚拟环境已激活"
    
    # 安装依赖
    echo "📦 安装项目依赖..."
    pip install -r requirements.txt
    echo "✅ 依赖安装完成"
else
    echo "⚠️ 请先激活虚拟环境，然后运行:"
    echo "   pip install -r requirements.txt"
fi

# 创建环境配置文件
if [[ ! -f ".env" ]]; then
    echo ""
    echo "⚙️ 创建环境配置文件..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件"
    echo ""
    echo "🔑 请编辑 .env 文件，设置您的 API 密钥:"
    echo "   ALIYUN_API_KEY=your_api_key_here"
    echo ""
else
    echo "✅ .env 文件已存在"
fi

# 创建必要的目录
echo "📁 确保目录结构完整..."
mkdir -p data/agent_storage data/market_data logs

echo ""
echo "🎉 环境配置完成！"
echo ""
echo "📋 下一步操作："
echo "1. 编辑 .env 文件，设置 API 密钥"
echo "2. 运行: ag setup (首次使用需要认证)"  
echo "3. 启动服务: bash scripts/start_playground.sh"
echo "4. 访问: http://app.agno.com/playground"
echo "" 