#!/usr/bin/env python3
"""
Agent UI 演示指南
================

演示如何在 Agno Agent UI 中使用投资大师团队功能

使用方法:
    python demos/agent_ui_demo.py
"""

import os
import sys
import webbrowser
import time

def print_header():
    """打印演示标题"""
    print("🎯 Agent UI 投资团队演示指南")
    print("=" * 60)
    print()

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    # 检查 API 密钥
    if not os.getenv("ALIYUN_API_KEY"):
        print("❌ 未设置 ALIYUN_API_KEY 环境变量")
        print("💡 请先设置您的阿里云 API 密钥:")
        print("   export ALIYUN_API_KEY=your_api_key")
        return False
    
    print("✅ API 密钥已配置")
    return True

def show_startup_instructions():
    """显示启动说明"""
    print("🚀 启动 Agent UI 演示")
    print("-" * 40)
    print()
    print("📋 步骤 1: 启动 Playground 服务")
    print("   在终端中运行:")
    print("   python apps/playground.py")
    print()
    print("📋 步骤 2: 访问 Agent UI")
    print("   1. 打开浏览器访问: https://app.agno.com/playground")
    print("   2. 添加端点: localhost:7777")
    print("   3. 连接到本地服务")
    print()

def show_agent_list():
    """显示可用的 Agent 列表"""
    print("👥 可用的投资分析 Agents:")
    print("-" * 40)
    agents = [
        "🎯 投资大师选择助手 - 帮助选择合适的投资大师",
        "🏆 巴菲特-芒格投资团队 - 综合两位大师的观点",
        "🎩 Warren Buffett - 价值投资大师",
        "🧠 Charlie Munger - 多学科思维专家",
        "📈 Peter Lynch - 成长价值投资专家",
        "📚 Benjamin Graham - 价值投资鼻祖",
        "🌊 Ray Dalio - 全天候投资策略",
        "🔢 Joel Greenblatt - 魔法公式投资",
        "⚡ David Tepper - 困境投资专家",
        "🏦 投资组合综合分析师 - 组合优化专家"
    ]
    
    for i, agent in enumerate(agents, 1):
        print(f"   {i:2d}. {agent}")
    print()

def show_team_demo_examples():
    """显示团队演示示例"""
    print("🏆 投资团队演示示例")
    print("-" * 40)
    print()
    print("💡 选择 '🏆 巴菲特-芒格投资团队' 后，可以尝试以下对话:")
    print()
    
    examples = [
        {
            "title": "📊 基础股票分析",
            "prompt": "请分析苹果公司(AAPL)的投资价值",
            "description": "团队会从巴菲特和芒格两个角度分析苹果公司"
        },
        {
            "title": "🔍 深度价值分析", 
            "prompt": "请深度分析特斯拉(TSLA)，重点关注其竞争优势和估值合理性",
            "description": "获得价值投资和多学科思维的双重视角"
        },
        {
            "title": "⚖️ 对比分析",
            "prompt": "请对比分析微软(MSFT)和苹果(AAPL)，哪个更值得长期投资？",
            "description": "团队会综合两位大师的观点进行对比分析"
        },
        {
            "title": "🌊 宏观分析",
            "prompt": "在当前经济环境下，银行股是否值得投资？以摩根大通(JPM)为例",
            "description": "从宏观经济和价值投资角度分析行业机会"
        },
        {
            "title": "🎯 风险评估",
            "prompt": "请分析投资中国概念股的主要风险，以阿里巴巴(BABA)为例",
            "description": "重点关注风险因素和投资陷阱"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"   {i}. {example['title']}")
        print(f"      提问: \"{example['prompt']}\"")
        print(f"      说明: {example['description']}")
        print()

def show_expected_output():
    """显示预期输出格式"""
    print("📋 团队分析报告格式")
    print("-" * 40)
    print()
    print("投资团队会按以下结构提供分析:")
    print()
    print("## 🎩 巴菲特观点")
    print("- 企业护城河分析")
    print("- 管理层质量评估") 
    print("- 财务健康度检查")
    print("- 内在价值估算")
    print()
    print("## 🧠 芒格观点")
    print("- 逆向思考：可能的失败因素")
    print("- 多学科视角分析")
    print("- 认知偏误检查")
    print("- 常识判断")
    print()
    print("## 🏆 团队综合建议")
    print("- 观点共识与分歧")
    print("- 综合投资评级")
    print("- 具体行动建议")
    print("- 风险提示")
    print()

def show_ui_tips():
    """显示 UI 使用技巧"""
    print("💡 Agent UI 使用技巧")
    print("-" * 40)
    print()
    print("🎯 选择 Agent:")
    print("   - 在左侧列表中点击 '🏆 巴菲特-芒格投资团队'")
    print("   - 或先选择 '🎯 投资大师选择助手' 获得推荐")
    print()
    print("💬 对话技巧:")
    print("   - 提供具体的股票代码 (如 AAPL, TSLA)")
    print("   - 明确分析重点 (估值、风险、对比等)")
    print("   - 可以追问具体细节")
    print()
    print("📊 查看结果:")
    print("   - 团队分析会显示结构化报告")
    print("   - 包含实时股票数据")
    print("   - 支持 Markdown 格式显示")
    print()
    print("🔄 继续对话:")
    print("   - 可以基于分析结果继续提问")
    print("   - 系统会记住对话历史")
    print("   - 支持多轮深度讨论")
    print()

def open_browser():
    """打开浏览器"""
    print("🌐 正在打开 Agent UI...")
    try:
        webbrowser.open("https://app.agno.com/playground")
        print("✅ 浏览器已打开，请按照说明操作")
    except Exception as e:
        print(f"❌ 无法自动打开浏览器: {e}")
        print("💡 请手动访问: https://app.agno.com/playground")

def main():
    """主演示函数"""
    print_header()
    
    if not check_environment():
        return
    
    print("🎬 开始演示...")
    print()
    
    # 显示启动说明
    show_startup_instructions()
    
    # 等待用户确认
    input("按 Enter 继续查看 Agent 列表...")
    print()
    
    # 显示 Agent 列表
    show_agent_list()
    
    # 等待用户确认
    input("按 Enter 继续查看团队演示示例...")
    print()
    
    # 显示演示示例
    show_team_demo_examples()
    
    # 等待用户确认
    input("按 Enter 继续查看输出格式...")
    print()
    
    # 显示预期输出
    show_expected_output()
    
    # 等待用户确认
    input("按 Enter 继续查看使用技巧...")
    print()
    
    # 显示使用技巧
    show_ui_tips()
    
    # 询问是否打开浏览器
    print()
    choice = input("是否现在打开 Agent UI？(y/n): ").strip().lower()
    if choice in ['y', 'yes', '是']:
        open_browser()
    
    print()
    print("🎉 演示完成！")
    print("💡 现在您可以:")
    print("   1. 启动 playground: python apps/playground.py")
    print("   2. 访问 Agent UI: https://app.agno.com/playground")
    print("   3. 选择投资团队开始分析")

if __name__ == "__main__":
    main() 