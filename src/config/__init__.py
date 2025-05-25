"""
Configuration Module
===================

This module contains configuration files and settings for the Agno AI Investment System.

Configuration files:
- investment_agents_config.yaml: Investment master agent configurations

"""

import os

# 配置文件路径
CONFIG_DIR = os.path.dirname(__file__)
INVESTMENT_AGENTS_CONFIG = os.path.join(CONFIG_DIR, "investment_agents_config.yaml")

__all__ = [
    "CONFIG_DIR",
    "INVESTMENT_AGENTS_CONFIG"
] 