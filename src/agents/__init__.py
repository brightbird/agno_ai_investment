"""
Investment Agents Module
=======================

This module contains all investment master agents and multi-agent systems.

Available agents:
- ConfigurableInvestmentAgent: YAML-based configurable agent system
- MultiAgentInvestmentAnalyzerV2: Enhanced multi-agent analysis system  
- InvestmentMasterFactory: Factory for creating individual master agents

Supported Investment Masters:
- Warren Buffett: Value investing, moats, long-term thinking
- Charlie Munger: Multi-disciplinary thinking, inverse reasoning
- Peter Lynch: Growth at reasonable price, consumer-focused
- Benjamin Graham: Deep value, margin of safety
- Ray Dalio: All-weather strategy, macro economics
- Joel Greenblatt: Magic formula, quantitative value
- David Tepper: Distressed investing, macro sensitivity
"""

from .configurable_investment_agent import (
    ConfigurableInvestmentAgent,
    InvestmentMasterAgent, 
    ConfigurableMultiAgentAnalyzer
)
from .multi_agent_investment_v2 import (
    MultiAgentInvestmentAnalyzerV2,
    EnhancedInvestmentSynthesizer
)
from .warren_buffett_agent_v2 import InvestmentMasterFactory

__all__ = [
    "ConfigurableInvestmentAgent",
    "InvestmentMasterAgent",
    "ConfigurableMultiAgentAnalyzer",
    "MultiAgentInvestmentAnalyzerV2", 
    "EnhancedInvestmentSynthesizer",
    "InvestmentMasterFactory"
] 