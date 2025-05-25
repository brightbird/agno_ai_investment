#!/usr/bin/env python3
"""
Agno AI 投资分析系统 - 测试包
============================

包含所有测试用例：
- test_agents.py: Agent测试
- test_playground.py: Playground测试
- fixtures/: 测试数据和工具

测试套件组织结构：
- unit/: 单元测试 - 测试单个模块和函数
- functional/: 功能测试 - 测试完整功能流程
- integration/: 集成测试 - 测试系统组件集成

运行所有测试: python -m pytest tests/
运行特定测试: python tests/run_tests.py
"""

import os
import sys

# 添加src目录到Python路径，确保测试能正确导入源代码
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path) 