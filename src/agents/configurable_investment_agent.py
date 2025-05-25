"""
可配置投资Agent系统
通过YAML配置文件动态创建不同投资风格的Agent
"""

import os
import yaml
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

# 加载环境变量
load_dotenv()

class ConfigurableInvestmentAgent:
    """
    可配置的投资Agent类
    基于YAML配置文件创建不同投资风格的Agent
    """
    
    def __init__(self, config_file: str = None):
        """
        初始化可配置投资Agent系统
        
        Args:
            config_file: 配置文件路径
        """
        if config_file is None:
            # 默认配置文件路径
            current_dir = os.path.dirname(__file__)
            config_file = os.path.join(current_dir, "..", "config", "investment_agents_config.yaml")
        
        self.config_file = config_file
        self.config = self._load_config()
        self.available_masters = list(self.config['investment_masters'].keys())
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                return config
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {self.config_file} 未找到")
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件格式错误: {e}")
    
    def get_available_masters(self) -> List[str]:
        """获取可用的投资大师列表"""
        return self.available_masters
    
    def create_agent(self, master_name: str, model_id: Optional[str] = None) -> 'InvestmentMasterAgent':
        """
        创建指定投资大师的Agent
        
        Args:
            master_name: 投资大师名称
            model_id: 模型ID，如果不指定则使用默认模型
            
        Returns:
            InvestmentMasterAgent实例
        """
        if master_name not in self.available_masters:
            raise ValueError(f"未知的投资大师: {master_name}. 可用选项: {self.available_masters}")
        
        master_config = self.config['investment_masters'][master_name]
        model_id = model_id or self.config['model_config']['default_model']
        
        return InvestmentMasterAgent(master_config, model_id, self.config)
    
    def create_multi_agent_system(self, master_names: List[str], model_id: Optional[str] = None) -> Dict[str, 'InvestmentMasterAgent']:
        """
        创建多Agent系统
        
        Args:
            master_names: 投资大师名称列表
            model_id: 模型ID
            
        Returns:
            投资大师Agent字典
        """
        agents = {}
        for master_name in master_names:
            agents[master_name] = self.create_agent(master_name, model_id)
        return agents
    
    def get_master_info(self, master_name: str) -> Dict[str, Any]:
        """
        获取投资大师的详细信息
        
        Args:
            master_name: 投资大师名称
            
        Returns:
            投资大师配置信息
        """
        if master_name not in self.available_masters:
            raise ValueError(f"未知的投资大师: {master_name}")
        
        return self.config['investment_masters'][master_name]

class InvestmentMasterAgent:
    """
    投资大师Agent类
    基于配置动态创建的投资分析Agent
    """
    
    def __init__(self, master_config: Dict[str, Any], model_id: str, global_config: Dict[str, Any]):
        """
        初始化投资大师Agent
        
        Args:
            master_config: 投资大师配置
            model_id: 模型ID
            global_config: 全局配置
        """
        self.master_config = master_config
        self.model_id = model_id
        self.global_config = global_config
        
        # 创建模型
        model = OpenAILike(
            id=model_id,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=os.getenv("ALIYUN_API_KEY")
        )
        
        # 创建Agent
        self.agent = Agent(
            name=master_config['agent_name'],
            model=model,
            tools=self._create_tools(),
            instructions=self._build_instructions(),
            markdown=global_config['analysis_output']['format'] == 'markdown',
            show_tool_calls=global_config['analysis_output']['show_tool_calls']
        )
        
        # 投资大师信息
        self.agent_name = master_config['agent_name']
        self.description = master_config['description']
        self.investment_philosophy = master_config['investment_philosophy']
        self.analysis_framework = master_config['analysis_framework']
        self.style_characteristics = master_config['style_characteristics']
    
    def _create_tools(self) -> List:
        """创建工具列表"""
        tools = []
        
        # 添加推理工具
        tools.append(ReasoningTools(add_instructions=True))
        
        # 添加金融数据工具
        tools.append(YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
            technical_indicators=True,
            key_financial_ratios=True,
            income_statements=True,
            stock_fundamentals=True,
            historical_prices=True
        ))
        
        # 添加搜索工具
        tools.append(DuckDuckGoTools())
        
        return tools
    
    def _build_instructions(self) -> List[str]:
        """构建Agent指令"""
        instructions = []
        
        # 添加基本身份和描述
        instructions.append(f"你是{self.master_config['agent_name']}，{self.master_config['description']}")
        instructions.append("")
        
        # 添加投资哲学
        instructions.append("**投资哲学：**")
        for philosophy in self.master_config['investment_philosophy']:
            instructions.append(f"- {philosophy}")
        instructions.append("")
        
        # 添加具体指令
        instructions.append("**分析指导原则：**")
        for instruction in self.master_config['instructions']:
            instructions.append(f"- {instruction}")
        instructions.append("")
        
        # 添加风格特征
        style = self.master_config['style_characteristics']
        instructions.append("**分析风格：**")
        instructions.append(f"- 语言风格：{style['voice']}")
        instructions.append(f"- 分析方法：{style['approach']}")
        instructions.append(f"- 举例特点：{style['examples']}")
        
        return instructions
    
    def analyze_stock(self, symbol: str, show_reasoning: bool = True) -> Dict[str, Any]:
        """
        分析股票
        
        Args:
            symbol: 股票代码
            show_reasoning: 是否显示推理过程
            
        Returns:
            分析结果字典
        """
        prompt = self._build_analysis_prompt(symbol)
        
        print(f"\n{self._get_agent_emoji()} {self.agent_name}分析: {symbol}")
        print("=" * 60)

        response = self.agent.run(
            prompt
        )
        
        # 处理RunResponse对象，提取字符串内容
        if hasattr(response, 'content'):
            analysis_text = response.content
        elif hasattr(response, 'text'):
            analysis_text = response.text
        elif hasattr(response, 'message'):
            analysis_text = response.message
        else:
            # 如果没有这些属性，尝试转换为字符串
            analysis_text = str(response)

        return {
            "agent": self.agent_name,
            "symbol": symbol,
            "analysis": analysis_text,
            "style": self.description,
            "philosophy": self.investment_philosophy,
            "framework": self.analysis_framework
        }
    
    def _build_analysis_prompt(self, symbol: str) -> str:
        """构建分析提示词"""
        prompt = f"""
        请以{self.agent_name}的投资哲学分析股票 {symbol}。

        **分析框架：**
        {self._format_analysis_framework()}

        请基于最新财务数据进行深入分析，并用{self.style_characteristics['voice']}的风格表达。
        分析应体现{self.style_characteristics['approach']}的特点。
        """
        
        return prompt
    
    def _format_analysis_framework(self) -> str:
        """格式化分析框架"""
        framework_text = ""
        for i, (key, value) in enumerate(self.analysis_framework.items(), 1):
            if isinstance(value, str):
                framework_text += f"{i}. **{key.replace('_', ' ').title()}** - {value}\n"
            elif isinstance(value, list):
                framework_text += f"{i}. **{key.replace('_', ' ').title()}**\n"
                for item in value:
                    framework_text += f"   - {item}\n"
            elif isinstance(value, dict):
                framework_text += f"{i}. **{key.replace('_', ' ').title()}**\n"
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, list):
                        framework_text += f"   - {sub_key.replace('_', ' ')}:\n"
                        for item in sub_value:
                            framework_text += f"     * {item}\n"
                    else:
                        framework_text += f"   - {sub_key.replace('_', ' ')}: {sub_value}\n"
        
        return framework_text
    
    def _get_agent_emoji(self) -> str:
        """获取Agent对应的emoji"""
        emoji_map = {
            "Warren Buffett": "🎩",
            "Charlie Munger": "🧠", 
            "Peter Lynch": "📈",
            "Benjamin Graham": "📚",
            "Ray Dalio": "🌐"
        }
        
        for name, emoji in emoji_map.items():
            if name in self.agent_name:
                return emoji
        
        return "💼"  # 默认emoji
    
    def get_investment_philosophy(self) -> List[str]:
        """获取投资哲学"""
        return self.investment_philosophy
    
    def get_analysis_framework(self) -> Dict[str, Any]:
        """获取分析框架"""
        return self.analysis_framework
    
    def get_style_info(self) -> Dict[str, str]:
        """获取风格信息"""
        return self.style_characteristics

class ConfigurableMultiAgentAnalyzer:
    """
    可配置的多Agent分析器
    """
    
    def __init__(self, config_file: str = None):
        """
        初始化多Agent分析器
        
        Args:
            config_file: 配置文件路径
        """
        if config_file is None:
            # 默认配置文件路径
            current_dir = os.path.dirname(__file__)
            config_file = os.path.join(current_dir, "..", "config", "investment_agents_config.yaml")
        
        self.agent_factory = ConfigurableInvestmentAgent(config_file)
        self.active_agents = {}
    
    def load_agents(self, master_names: List[str], model_id: Optional[str] = None) -> None:
        """
        加载指定的投资大师Agent
        
        Args:
            master_names: 投资大师名称列表
            model_id: 模型ID
        """
        print(f"🤖 加载投资大师Agent: {', '.join(master_names)}")
        
        self.active_agents = self.agent_factory.create_multi_agent_system(master_names, model_id)
        
        print("✅ Agent加载完成！")
        print(f"📋 已加载 {len(self.active_agents)} 位投资大师:")
        for name, agent in self.active_agents.items():
            print(f"   - {agent.agent_name}")
    
    def analyze_stock_multi_perspective(self, symbol: str, show_reasoning: bool = False) -> Dict[str, Any]:
        """
        多视角分析股票
        
        Args:
            symbol: 股票代码
            show_reasoning: 是否显示推理过程
            
        Returns:
            分析结果字典
        """
        if not self.active_agents:
            raise ValueError("请先使用 load_agents() 加载投资大师Agent")
        
        print(f"\n🎯 开始多视角分析股票: {symbol}")
        print("💡 将从以下投资大师的角度进行分析:")
        for name, agent in self.active_agents.items():
            print(f"   - {agent.agent_name}")
        print("=" * 80)
        
        # 并行分析（如果需要的话可以实现）
        analyses_results = []
        for name, agent in self.active_agents.items():
            try:
                result = agent.analyze_stock(symbol, show_reasoning)
                analyses_results.append(result)
            except Exception as exc:
                print(f"❌ {agent.agent_name} 分析失败: {exc}")
                analyses_results.append({
                    "agent": agent.agent_name,
                    "symbol": symbol,
                    "analysis": f"分析失败: {str(exc)}",
                    "style": "错误"
                })
        
        # 显示分析结果
        self._display_individual_analyses(analyses_results)
        
        return {
            "symbol": symbol,
            "individual_analyses": analyses_results,
            "active_masters": list(self.active_agents.keys())
        }
    
    def _display_individual_analyses(self, analyses_results: List[Dict[str, Any]]) -> None:
        """显示各位大师的分析结果"""
        print(f"\n📋 各位投资大师的分析结果:")
        print("=" * 80)
        
        for i, result in enumerate(analyses_results, 1):
            agent_name = result['agent']
            symbol = result['symbol']
            style = result['style']
            analysis = result['analysis']
            
            # 获取Agent对应的emoji
            emoji = self._get_master_emoji(agent_name)
            
            print(f"\n{emoji} 【第{i}位大师】 {agent_name}")
            print(f"🎯 分析股票: {symbol}")
            print(f"📝 投资风格: {style}")
            print("=" * 60)
            print(f"\n{analysis}")
            print("\n" + "─" * 60)
    
    def _get_master_emoji(self, agent_name: str) -> str:
        """根据投资大师名称获取对应的emoji"""
        emoji_map = {
            "Warren Buffett": "🎩",
            "Charlie Munger": "🧠", 
            "Peter Lynch": "📈",
            "Benjamin Graham": "📚",
            "Ray Dalio": "🌐",
            "Joel Greenblatt": "🔢",
            "David Tepper": "⚡"
        }
        
        for name, emoji in emoji_map.items():
            if name in agent_name:
                return emoji
        
        return "💼"  # 默认emoji
    
    def get_master_comparison(self) -> None:
        """显示投资大师对比"""
        print("\n📊 投资大师风格对比:")
        print("=" * 80)
        
        # 获取所有可用的投资大师
        available_masters = self.agent_factory.get_available_masters()
        
        print(f"📋 系统支持 {len(available_masters)} 位投资大师:")
        print("=" * 60)
        
        for master_name in available_masters:
            try:
                info = self.agent_factory.get_master_info(master_name)
                
                # 获取对应的emoji
                emoji = self._get_master_emoji(info['agent_name'])
                
                print(f"\n{emoji} **{info['agent_name']}**")
                print(f"📝 描述: {info['description']}")
                print("💡 核心投资哲学:")
                for philosophy in info['investment_philosophy'][:3]:  # 显示前3条
                    print(f"   - {philosophy}")
                print(f"🎭 投资风格: {info['style_characteristics']['voice']}")
                print(f"🔬 分析方法: {info['style_characteristics']['approach']}")
                
                # 显示一个示例类比
                if 'examples' in info['style_characteristics']:
                    print(f"🎯 典型特征: {info['style_characteristics']['examples']}")
                
                print("-" * 60)
                
            except Exception as e:
                print(f"❌ 获取 {master_name} 信息失败: {e}")
        
        # 如果有已加载的Agent，也显示出来
        if self.active_agents:
            print(f"\n🟢 当前已加载的投资大师 ({len(self.active_agents)}位):")
            for name, agent in self.active_agents.items():
                emoji = self._get_master_emoji(agent.agent_name)
                print(f"   {emoji} {agent.agent_name}")
        else:
            print(f"\n🔵 当前没有加载任何投资大师")
            print(f"💡 提示: 选择'单股深度分析'或'多股对比分析'时会自动加载所需的投资大师")

def main():
    """演示可配置投资Agent系统"""
    print("🎯 可配置投资Agent系统")
    print("💫 基于YAML配置文件的多投资风格分析")
    print("=" * 80)
    
    try:
        # 创建配置分析器
        analyzer = ConfigurableMultiAgentAnalyzer()
        
        # 显示可用投资大师
        available_masters = analyzer.agent_factory.get_available_masters()
        print(f"📋 可用的投资大师: {', '.join(available_masters)}")
        
        while True:
            print(f"\n📋 请选择操作:")
            print("1. 查看所有投资大师信息")
            print("2. 加载投资大师并分析股票")
            print("3. 查看当前加载的投资大师")
            print("4. 退出")
            
            choice = input("\n请输入选择 (1-4): ").strip()
            
            if choice == "1":
                print(f"\n🎭 投资大师详细信息:")
                print("=" * 60)
                for master in available_masters:
                    info = analyzer.agent_factory.get_master_info(master)
                    print(f"\n📚 **{info['agent_name']}**")
                    print(f"描述: {info['description']}")
                    print("投资哲学:")
                    for p in info['investment_philosophy'][:2]:
                        print(f"  - {p}")
                    print(f"风格: {info['style_characteristics']['voice']}")
                    print("-" * 30)
            
            elif choice == "2":
                print(f"\n可选投资大师: {', '.join(available_masters)}")
                masters_input = input("请选择投资大师（用逗号分隔，如 warren_buffett,charlie_munger）: ").strip()
                
                if masters_input:
                    selected_masters = [m.strip() for m in masters_input.split(",")]
                    
                    # 验证选择
                    invalid_masters = [m for m in selected_masters if m not in available_masters]
                    if invalid_masters:
                        print(f"❌ 无效的投资大师: {', '.join(invalid_masters)}")
                        continue
                    
                    # 加载Agent
                    analyzer.load_agents(selected_masters)
                    
                    # 分析股票
                    symbol = input("请输入股票代码 (如 AAPL): ").strip().upper()
                    if symbol:
                        analyzer.analyze_stock_multi_perspective(symbol, show_reasoning=False)
            
            elif choice == "3":
                analyzer.get_master_comparison()
            
            elif choice == "4":
                print("👋 感谢使用可配置投资Agent系统！")
                break
            
            else:
                print("❌ 无效选择，请重新输入")
                
    except Exception as e:
        print(f"❌ 系统错误: {e}")

if __name__ == "__main__":
    main() 