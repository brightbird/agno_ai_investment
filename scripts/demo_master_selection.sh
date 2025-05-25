#!/bin/bash

# 投资大师选择功能演示脚本

echo "🎯 Agno AI 投资大师选择功能演示"
echo "=================================="
echo ""

echo "✨ 功能亮点："
echo "1. 🎯 智能推荐最适合的投资大师"
echo "2. 🎭 9位不同风格的投资专家"
echo "3. 💡 个性化投资建议流程"
echo "4. 📊 多角度投资分析"
echo ""

echo "🚀 使用流程："
echo "第一步：访问 🎯 投资大师选择助手"
echo "第二步：描述你的投资需求和偏好"  
echo "第三步：根据推荐选择具体的投资大师"
echo "第四步：开始专业的投资分析对话"
echo ""

echo "📋 可用的投资大师："
echo ""

# 检查服务是否运行
if curl -s http://localhost:7777/v1/playground/status >/dev/null 2>&1; then
    echo "✅ 服务正在运行，获取最新的大师列表："
    echo ""
    
    # 获取并显示投资大师列表
    curl -s "http://localhost:7777/v1/playground/agents" | \
    grep -o '"name":"[^"]*投资[^"]*"' | \
    sed 's/"name":"//g' | \
    sed 's/"//g' | \
    while read -r name; do
        echo "   ✨ $name"
    done
    
    echo ""
    echo "🌐 访问方式："
    echo "1. 打开浏览器访问：https://app.agno.com/playground"
    echo "2. 选择端点：localhost:7777"
    echo "3. 在左侧选择：🎯 投资大师选择助手"
    echo "4. 开始对话！"
    
else
    echo "❌ 服务未运行，请先启动："
    echo "   python apps/playground.py"
    echo ""
    echo "然后运行此脚本查看演示"
fi

echo ""
echo "📚 更多信息："
echo "   - 详细指南：docs/MASTER_SELECTION_GUIDE.md"
echo "   - 使用手册：docs/PLAYGROUND_GUIDE.md"
echo ""
echo "🎉 开始您的智能投资咨询之旅！" 