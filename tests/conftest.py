#!/usr/bin/env python3
"""
pytest配置文件
设置测试环境，处理导入路径和公共fixture
"""

import os
import sys
import pytest
from dotenv import load_dotenv

# 确保能正确导入src模块
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 加载环境变量
load_dotenv()

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """设置测试环境"""
    print("\n🧪 正在设置测试环境...")
    
    # 检查必要的环境变量
    if not os.getenv("ALIYUN_API_KEY"):
        print("⚠️ 警告: 未设置ALIYUN_API_KEY环境变量，某些测试可能无法运行")
    
    yield
    
    print("\n🏁 测试环境清理完成") 