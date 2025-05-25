#!/bin/bash

# Agno AI 投资分析系统 - 快速开始脚本
# 适用于首次使用的用户

echo "🚀 欢迎使用 Agno AI 投资分析系统！"
echo "================================"
echo ""

# 检查Python版本
echo "🔍 检查Python环境..."
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>/dev/null)

if [[ -z "$python_version" ]]; then
    echo "❌ 未找到Python3，请先安装Python 3.8或更高版本"
    exit 1
fi

echo "✅ Python版本: $python_version"

# 检查版本兼容性
if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo "✅ Python版本符合要求"
else
    echo "❌ Python版本过低，需要3.8或更高版本"
    exit 1
fi

# 创建虚拟环境
echo ""
echo "📦 设置虚拟环境..."
if [[ ! -d ".venv" ]]; then
    python3 -m venv .venv
    echo "✅ 虚拟环境创建成功"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo "🔄 激活虚拟环境..."
source .venv/bin/activate

# 安装依赖
echo "📥 安装项目依赖..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ 依赖安装完成"

# 检查环境变量
echo ""
echo "🔐 配置环境变量..."
if [[ ! -f ".env" ]]; then
    if [[ -f "env.example" ]]; then
        cp env.example .env
        echo "✅ 已创建 .env 配置文件"
        echo ""
        echo "📝 请编辑 .env 文件，设置您的阿里云API密钥："
        echo "   1. 访问 https://bailian.console.aliyun.com/ 获取API密钥"
        echo "   2. 编辑 .env 文件: nano .env 或 vim .env"
        echo "   3. 将 your_aliyun_api_key_here 替换为您的真实API密钥"
        echo ""
        echo "⚠️  重要：请保管好您的API密钥，不要分享给他人"
        
        read -p "按回车键继续 (完成API密钥配置后)..."
    else
        echo "❌ 未找到 env.example 文件"
        exit 1
    fi
else
    echo "✅ .env 文件已存在"
fi

# 验证API密钥
echo ""
echo "🔍 验证API密钥配置..."
source .env 2>/dev/null

if [[ -z "$ALIYUN_API_KEY" || "$ALIYUN_API_KEY" == "your_aliyun_api_key_here" ]]; then
    echo "⚠️  警告：API密钥未正确配置"
    echo "   请编辑 .env 文件，设置正确的 ALIYUN_API_KEY"
    echo ""
    echo "💡 提示："
    echo "   1. 打开 .env 文件: nano .env"
    echo "   2. 找到 ALIYUN_API_KEY=your_aliyun_api_key_here"
    echo "   3. 替换为: ALIYUN_API_KEY=sk-xxxxxxxxxxxxx"
    echo ""
    read -p "配置完成后按回车键继续..."
else
    echo "✅ API密钥配置检查通过"
fi

# 测试安装
echo ""
echo "🧪 测试系统安装..."
if python -c "import agno; print('Agno框架导入成功')" 2>/dev/null; then
    echo "✅ Agno框架正常"
else
    echo "❌ Agno框架导入失败，请检查安装"
    echo "💡 尝试重新安装: pip install agno"
fi

echo ""
echo "🎉 快速开始设置完成！"
echo ""
echo "🚀 启动系统："
echo "   方式1 - Web界面: python apps/playground.py"
echo "   方式2 - 命令行: python apps/cli.py"
echo "   方式3 - 启动脚本: bash scripts/start_playground.sh"
echo ""
echo "🌐 使用Web界面："
echo "   1. 运行启动命令"
echo "   2. 访问 https://app.agno.com/playground"
echo "   3. 选择 localhost:7777 端点"
echo "   4. 开始与投资大师对话！"
echo ""
echo "📚 更多帮助："
echo "   - 使用指南: docs/README.md"
echo "   - 大师选择指南: docs/MASTER_SELECTION_GUIDE.md"
echo "   - 故障排除: docs/PLAYGROUND_GUIDE.md"
echo ""
echo "💝 享受您的投资分析之旅！" 