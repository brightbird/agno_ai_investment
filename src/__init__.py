"""
Agno AI Investment Analysis System
==================================

A configurable multi-agent investment analysis system powered by 7 world-class investment masters.
Provides structured, professional-grade investment reports and recommendations.

主要模块:
- agents: 投资大师Agent实现
- config: 配置文件和设置
- utils: 工具函数和通用代码
"""

__version__ = "2.0.0"
__author__ = "Agno AI Investment Team"

# 导入主要模块
from .agents.configurable_investment_agent import ConfigurableInvestmentAgent, ConfigurableMultiAgentAnalyzer
from .agents.multi_agent_investment_v2 import MultiAgentInvestmentAnalyzerV2
from .agents.warren_buffett_agent_v2 import InvestmentMasterFactory

__all__ = [
    "ConfigurableInvestmentAgent",
    "ConfigurableMultiAgentAnalyzer", 
    "MultiAgentInvestmentAnalyzerV2",
    "InvestmentMasterFactory"
] 