"""
Warren Buffett投资Agent V2
向后兼容的投资大师工厂类
基于配置化投资Agent系统的包装器
"""

import os
import sys
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# 确保导入路径正确
from .configurable_investment_agent import ConfigurableInvestmentAgent, InvestmentMasterAgent

# 加载环境变量
load_dotenv()

class InvestmentMasterFactory:
    """
    投资大师工厂类
    提供便捷的投资大师Agent创建方法
    向后兼容原有接口
    """
    
    _config_agent = None
    
    @classmethod
    def _get_config_agent(cls) -> ConfigurableInvestmentAgent:
        """获取配置化投资Agent实例"""
        if cls._config_agent is None:
            cls._config_agent = ConfigurableInvestmentAgent()
        return cls._config_agent
    
    @classmethod
    def create_warren_buffett(cls) -> InvestmentMasterAgent:
        """
        创建Warren Buffett投资Agent
        
        Returns:
            Warren Buffett投资分析Agent
        """
        config_agent = cls._get_config_agent()
        return config_agent.create_agent("warren_buffett")
    
    @classmethod
    def create_charlie_munger(cls) -> InvestmentMasterAgent:
        """
        创建Charlie Munger投资Agent
        
        Returns:
            Charlie Munger投资分析Agent
        """
        config_agent = cls._get_config_agent()
        return config_agent.create_agent("charlie_munger")
    
    @classmethod
    def create_peter_lynch(cls) -> InvestmentMasterAgent:
        """
        创建Peter Lynch投资Agent
        
        Returns:
            Peter Lynch投资分析Agent
        """
        config_agent = cls._get_config_agent()
        return config_agent.create_agent("peter_lynch")
    
    @classmethod
    def create_benjamin_graham(cls) -> InvestmentMasterAgent:
        """
        创建Benjamin Graham投资Agent
        
        Returns:
            Benjamin Graham投资分析Agent
        """
        config_agent = cls._get_config_agent()
        return config_agent.create_agent("benjamin_graham")
    
    @classmethod
    def create_ray_dalio(cls) -> InvestmentMasterAgent:
        """
        创建Ray Dalio投资Agent
        
        Returns:
            Ray Dalio投资分析Agent
        """
        config_agent = cls._get_config_agent()
        return config_agent.create_agent("ray_dalio")
    
    @classmethod
    def create_joel_greenblatt(cls) -> InvestmentMasterAgent:
        """
        创建Joel Greenblatt投资Agent
        
        Returns:
            Joel Greenblatt投资分析Agent
        """
        config_agent = cls._get_config_agent()
        return config_agent.create_agent("joel_greenblatt")
    
    @classmethod
    def create_david_tepper(cls) -> InvestmentMasterAgent:
        """
        创建David Tepper投资Agent
        
        Returns:
            David Tepper投资分析Agent
        """
        config_agent = cls._get_config_agent()
        return config_agent.create_agent("david_tepper")
    
    @classmethod
    def create_agent(cls, master_name: str) -> InvestmentMasterAgent:
        """
        创建指定投资大师Agent
        
        Args:
            master_name: 投资大师名称
            
        Returns:
            投资大师Agent
        """
        config_agent = cls._get_config_agent()
        return config_agent.create_agent(master_name)
    
    @classmethod
    def get_available_masters(cls) -> List[str]:
        """
        获取所有可用的投资大师列表
        
        Returns:
            投资大师名称列表
        """
        config_agent = cls._get_config_agent()
        return config_agent.get_available_masters()
    
    @classmethod
    def get_master_info(cls, master_name: str) -> Dict[str, Any]:
        """
        获取投资大师详细信息
        
        Args:
            master_name: 投资大师名称
            
        Returns:
            投资大师信息字典
        """
        config_agent = cls._get_config_agent()
        return config_agent.get_master_config(master_name)


# 向后兼容的别名
WarrenBuffettAgent = InvestmentMasterFactory.create_warren_buffett
CharlieMungerAgent = InvestmentMasterFactory.create_charlie_munger
PeterLynchAgent = InvestmentMasterFactory.create_peter_lynch
BenjaminGrahamAgent = InvestmentMasterFactory.create_benjamin_graham
RayDalioAgent = InvestmentMasterFactory.create_ray_dalio
JoelGreenblatAgent = InvestmentMasterFactory.create_joel_greenblatt
DavidTepperAgent = InvestmentMasterFactory.create_david_tepper


def main():
    """演示投资大师工厂类的使用"""
    print("🎯 投资大师工厂类演示")
    print("=" * 60)
    
    # 显示可用投资大师
    available_masters = InvestmentMasterFactory.get_available_masters()
    print(f"📋 可用投资大师: {', '.join(available_masters)}")
    
    # 创建Warren Buffett Agent
    print(f"\n🎩 创建Warren Buffett Agent...")
    buffett = InvestmentMasterFactory.create_warren_buffett()
    print(f"✅ Warren Buffett Agent创建成功: {buffett.agent_name}")
    
    # 创建任意投资大师Agent
    print(f"\n🧠 创建Charlie Munger Agent...")
    munger = InvestmentMasterFactory.create_agent("charlie_munger")
    print(f"✅ Charlie Munger Agent创建成功: {munger.agent_name}")
    
    # 显示投资大师信息
    print(f"\n📊 Warren Buffett投资理念:")
    buffett_info = InvestmentMasterFactory.get_master_info("warren_buffett")
    for philosophy in buffett_info['investment_philosophy'][:3]:
        print(f"  • {philosophy}")
    
    print(f"\n🎉 投资大师工厂类演示完成！")


if __name__ == "__main__":
    main()