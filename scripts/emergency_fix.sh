#!/bin/bash
# 🚨 Agno AI Investment - 紧急修复脚本
# 用于快速解决Session 404和其他常见问题

set -e  # 遇到错误时停止

echo "🚨 Agno AI Investment - 紧急修复工具"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否在正确的目录
if [ ! -f "apps/playground.py" ]; then
    echo -e "${RED}❌ 错误: 请在项目根目录运行此脚本${NC}"
    exit 1
fi

# 激活虚拟环境
if [ -d ".venv" ]; then
    echo -e "${BLUE}🔧 激活虚拟环境...${NC}"
    source .venv/bin/activate
else
    echo -e "${YELLOW}⚠️  虚拟环境不存在，使用系统Python${NC}"
fi

# 1. 停止现有服务
echo -e "${BLUE}🛑 停止现有playground服务...${NC}"
pkill -f "python.*playground" 2>/dev/null || echo "   没有运行的playground进程"

# 等待进程完全停止
sleep 3

# 2. 检查端口
echo -e "${BLUE}🔍 检查端口7777...${NC}"
if lsof -i :7777 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  端口7777仍被占用，尝试强制释放...${NC}"
    lsof -ti:7777 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# 3. 备份数据库
echo -e "${BLUE}📦 备份现有数据库...${NC}"
if [ -f "data/agent_storage/investment_agents.db" ]; then
    BACKUP_FILE="data/agent_storage/investment_agents.db.backup.$(date +%Y%m%d_%H%M%S)"
    cp "data/agent_storage/investment_agents.db" "$BACKUP_FILE"
    echo -e "${GREEN}✅ 已备份到: $BACKUP_FILE${NC}"
else
    echo -e "${YELLOW}⚠️  数据库文件不存在，跳过备份${NC}"
fi

# 4. 清理session数据
echo -e "${BLUE}🧹 清理过期session数据...${NC}"
if [ -f "scripts/fix_sessions.py" ]; then
    python scripts/fix_sessions.py
else
    echo -e "${YELLOW}⚠️  修复脚本不存在，手动清理数据库...${NC}"
    if [ -f "data/agent_storage/investment_agents.db" ]; then
        # 使用sqlite3直接清理
        sqlite3 data/agent_storage/investment_agents.db "
        DELETE FROM warren_buffett_agent WHERE created_at < datetime('now', '-1 days');
        DELETE FROM master_selector_agent WHERE created_at < datetime('now', '-1 days'); 
        DELETE FROM portfolio_agent WHERE created_at < datetime('now', '-1 days');
        DELETE FROM david_tepper_agent WHERE created_at < datetime('now', '-1 days');
        DELETE FROM charlie_munger_agent WHERE created_at < datetime('now', '-1 days');
        VACUUM;
        " 2>/dev/null || echo "   数据库清理失败，将重置数据库"
    fi
fi

# 5. 检查环境变量
echo -e "${BLUE}🔑 检查API密钥配置...${NC}"
if [ -z "$ALIYUN_API_KEY" ]; then
    if [ -f ".env" ]; then
        echo -e "${YELLOW}⚠️  从.env文件加载环境变量...${NC}"
        source .env
        export ALIYUN_API_KEY
    fi
    
    if [ -z "$ALIYUN_API_KEY" ]; then
        echo -e "${RED}❌ 错误: ALIYUN_API_KEY未设置${NC}"
        echo -e "${YELLOW}💡 请设置API密钥:${NC}"
        echo "   1. 编辑 .env 文件设置 ALIYUN_API_KEY"
        echo "   2. 或运行: export ALIYUN_API_KEY=your_key_here"
        exit 1
    fi
fi

# 6. 检查依赖
echo -e "${BLUE}📦 检查Python依赖...${NC}"
python -c "import agno" 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Agno包未安装，正在安装依赖...${NC}"
    pip install -r requirements.txt
}

# 7. 测试配置
echo -e "${BLUE}🧪 测试配置文件...${NC}"
python -c "
try:
    from src.agents.configurable_investment_agent import ConfigurableInvestmentAgent
    config = ConfigurableInvestmentAgent()
    print('✅ 配置文件正常')
except Exception as e:
    print(f'❌ 配置文件错误: {e}')
    exit(1)
" || {
    echo -e "${RED}❌ 配置文件有问题，请检查src/agents/目录${NC}"
    exit 1
}

# 8. 重启服务
echo -e "${BLUE}🚀 重启playground服务...${NC}"
echo -e "${YELLOW}💡 服务将在后台启动，请等待10秒...${NC}"

# 后台启动服务
nohup python apps/playground.py > playground.log 2>&1 &
PLAYGROUND_PID=$!
echo "   进程ID: $PLAYGROUND_PID"

# 等待服务启动
echo -e "${BLUE}⏳ 等待服务启动...${NC}"
for i in {1..10}; do
    if curl -s "http://localhost:7777/v1/playground/status" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 服务启动成功！${NC}"
        break
    fi
    echo -n "."
    sleep 1
done
echo

# 9. 健康检查
echo -e "${BLUE}🏥 运行健康检查...${NC}"
if python scripts/session_monitor.py health 2>/dev/null; then
    echo -e "${GREEN}✅ 服务健康检查通过${NC}"
else
    echo -e "${YELLOW}⚠️  健康检查失败，但服务可能仍在启动中${NC}"
fi

# 10. 显示结果
echo
echo -e "${GREEN}🎉 修复完成！${NC}"
echo "=========================================="
echo -e "${BLUE}📋 接下来的步骤:${NC}"
echo "1. 访问: https://app.agno.com/playground"
echo "2. 选择: localhost:7777 端点"
echo "3. 开始与投资大师对话!"
echo
echo -e "${BLUE}🔧 如果仍有问题:${NC}"
echo "1. 查看日志: tail playground.log"
echo "2. 运行测试: python scripts/session_monitor.py test"
echo "3. 查看故障排除: docs/TROUBLESHOOTING.md"
echo
echo -e "${BLUE}💾 数据备份位置:${NC}"
ls -la data/agent_storage/*.backup.* 2>/dev/null | tail -3 || echo "   无备份文件"
echo
echo -e "${YELLOW}⚠️  如果问题持续存在，请运行完全重置:${NC}"
echo "   python scripts/fix_sessions.py --reset" 