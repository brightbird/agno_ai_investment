#!/usr/bin/env python3
"""
Agno AI 投资分析系统 安装配置
"""

from setuptools import setup, find_packages
import os

# 读取长描述
def read_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Agno AI 投资分析系统 - 基于多Agent的智能投资分析平台"

# 读取依赖
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "agno>=0.1.0",
            "openai>=1.0.0", 
            "fastapi[standard]>=0.100.0",
            "uvicorn[standard]>=0.23.0",
            "pandas>=1.5.0",
            "yfinance>=0.2.0",
            "python-dotenv>=1.0.0"
        ]

# 版本信息
__version__ = "1.0.0"

setup(
    name="agno-ai-investment",
    version=__version__,
    author="Agno AI Investment Team",
    author_email="your-email@domain.com",  # 替换为您的邮箱
    description="基于 Agno 框架的多Agent投资分析系统",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/agno_ai_investment",  # 替换为您的GitHub仓库
    project_urls={
        "Bug Reports": "https://github.com/your-username/agno_ai_investment/issues",
        "Source": "https://github.com/your-username/agno_ai_investment",
        "Documentation": "https://github.com/your-username/agno_ai_investment/blob/main/docs/README.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agno-investment=apps.playground:main",
            "agno-investment-cli=apps.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
    keywords=[
        "investment",
        "ai",
        "agent",
        "finance",
        "stock",
        "analysis",
        "buffett",
        "munger",
        "agno",
        "multi-agent",
    ],
    zip_safe=False,
) 