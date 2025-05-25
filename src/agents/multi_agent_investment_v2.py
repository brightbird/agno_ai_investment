"""
多Agent价值投资分析系统 V2
基于可配置投资Agent系统的升级版本
支持动态配置和更多投资大师
"""

import os
import concurrent.futures
import time
import yaml
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.reasoning import ReasoningTools
from .configurable_investment_agent import ConfigurableInvestmentAgent, ConfigurableMultiAgentAnalyzer

# 导入token管理工具
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.token_manager import TokenManager, TokenBudget, StreamingAnalyzer

# 加载环境变量
load_dotenv()

def load_default_model_from_config():
    """从配置文件中加载默认模型"""
    try:
        current_dir = os.path.dirname(__file__)
        config_file = os.path.join(current_dir, "..", "config", "investment_agents_config.yaml")
        
        with open(config_file, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config['model_config']['default_model']
    except Exception as e:
        print(f"⚠️ 无法加载配置文件中的默认模型，使用fallback: qwen-plus，错误: {e}")
        return "qwen-plus"

class EnhancedInvestmentSynthesizer:
    """
    增强版投资分析综合器
    支持更多投资大师的观点综合和token优化
    """
    def __init__(self, model_id=None, enable_token_optimization=True):
        # 如果没有指定模型ID，从配置文件中读取默认模型
        if model_id is None:
            model_id = load_default_model_from_config()
            print(f"📋 使用配置文件中的默认模型: {model_id}")
        
        # 使用阿里云百炼API
        model = OpenAILike(
            id=model_id,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=os.getenv("ALIYUN_API_KEY")
        )
        
        # 初始化token管理器
        self.token_manager = TokenManager(TokenBudget(
            max_total_tokens=6000,  # 降低总token限制
            max_input_tokens=4500,
            max_output_tokens=1500,
            reserve_tokens=300
        ))
        
        self.enable_token_optimization = enable_token_optimization
        self.streaming_analyzer = StreamingAnalyzer(self.token_manager)
        
        # 创建综合分析Agent
        self.synthesizer = Agent(
            name="多投资大师综合分析师",
            model=model,
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "你是一位资深的投资分析综合师，负责整合多位投资大师的观点。",
                "请生成简洁、结构化的投资分析报告。",
                "重点关注关键信息和可执行的投资建议。",
                "避免重复内容，确保分析精准高效。"
            ],
            markdown=True,
            show_tool_calls=False
        )

    def synthesize_analyses(self, analyses_results: List[Dict[str, Any]], mode: str = "auto") -> str:
        """
        综合多个投资大师的分析结果
        
        Args:
            analyses_results: 多个投资大师的分析结果列表
            mode: 处理模式 ("auto", "compressed", "streaming", "full")
            
        Returns:
            综合分析报告
        """
        if not analyses_results:
            return "❌ 没有可分析的数据"
        
        symbol = analyses_results[0]['symbol'] if analyses_results else "未知"
        master_count = len(analyses_results)
        
        # 估算输入token数
        total_input_tokens = sum(
            self.token_manager.estimate_tokens(str(result)) 
            for result in analyses_results
        )
        
        print(f"📊 输入数据估算: {total_input_tokens} tokens")
        
        # 根据token数量自动选择处理模式
        if mode == "auto":
            if total_input_tokens > self.token_manager.budget.max_input_tokens:
                mode = "compressed"
            elif total_input_tokens > self.token_manager.budget.max_input_tokens * 0.8:
                mode = "streaming"
            else:
                mode = "full"
        
        print(f"🔄 使用处理模式: {mode}")
        
        if mode == "compressed":
            return self._synthesize_compressed(symbol, analyses_results)
        elif mode == "streaming":
            return self._synthesize_streaming(symbol, analyses_results)
        else:
            return self._synthesize_full(symbol, analyses_results)

    def _synthesize_compressed(self, symbol: str, analyses_results: List[Dict[str, Any]]) -> str:
        """压缩模式综合分析"""
        print("🗜️ 使用压缩模式进行分析...")
        
        # 压缩分析结果
        compressed_analyses = self.token_manager.compress_analysis_results(analyses_results)
        
        prompt = f"""
基于{len(compressed_analyses)}位投资大师对{symbol}的分析摘要，生成投资报告：

{self._format_compressed_analyses(compressed_analyses)}

请输出简洁的结构化报告：

# 📊 {symbol} 投资分析报告

## 🎯 投资建议
| 项目 | 结论 |
|------|------|
| 推荐操作 | [买入/持有/卖出] |
| 综合评分 | [X/10分] |
| 风险等级 | [低/中/高] |

## 🎭 大师共识
{self._create_consensus_table(compressed_analyses)}

## ⚠️ 关键风险
- [风险1]
- [风险2]
- [风险3]

## 💰 执行建议
- **买入价位**: $[价格区间]
- **目标仓位**: [X]%
- **止损位**: $[价格]

---
*分析时间: {time.strftime('%Y-%m-%d %H:%M')} | 参与大师: {len(compressed_analyses)}位*
"""
        
        # 优化prompt
        optimized_prompt = self.token_manager.optimize_prompt_template(prompt)
        
        print(f"🔍 优化后prompt长度: {self.token_manager.estimate_tokens(optimized_prompt)} tokens")
        
        response = self.synthesizer.run(optimized_prompt)
        
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
            
        return analysis_text

    def _synthesize_streaming(self, symbol: str, analyses_results: List[Dict[str, Any]]) -> str:
        """流式模式综合分析"""
        print("🌊 使用流式模式进行分析...")
        
        # 使用流式分析器
        streaming_result = self.streaming_analyzer.stream_multi_master_analysis(symbol, analyses_results)
        
        # 组合各个部分
        sections = streaming_result["sections"]
        
        full_report = f"""
# 📊 {symbol} 综合投资分析报告

{sections["executive_summary"]}

{sections["master_opinions"]}

{sections["risk_assessment"]}

{sections["investment_plan"]}

---
*📊 分析完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}*
*🎭 参与分析大师: {len(analyses_results)}位*
*⚡ 处理模式: 流式分析*
"""
        return full_report

    def _synthesize_full(self, symbol: str, analyses_results: List[Dict[str, Any]]) -> str:
        """完整模式综合分析（简化版）"""
        print("📄 使用完整模式进行分析...")
        
        # 生成简化的完整报告
        prompt = f"""
基于以下{len(analyses_results)}位投资大师对股票{symbol}的分析，生成综合投资报告：

{self._format_analyses_summary(analyses_results)}

请生成结构化报告，包含：执行摘要、大师观点对比、风险评估、投资计划
保持内容简洁实用，避免冗余信息。
"""
        
        # 截断prompt以确保不超过限制
        truncated_prompt = self.token_manager.truncate_text(
            prompt, 
            self.token_manager.budget.max_input_tokens - 500
        )
        
        response = self.synthesizer.run(truncated_prompt)
        
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
            
        return analysis_text

    def _format_compressed_analyses(self, compressed_analyses: List[Dict[str, Any]]) -> str:
        """格式化压缩后的分析结果"""
        formatted = ""
        for i, analysis in enumerate(compressed_analyses, 1):
            formatted += f"""
### 大师{i}: {analysis['agent']}
- 建议: {analysis['recommendation']}
- 摘要: {analysis['summary'][:100]}...
- 要点: {', '.join(analysis['key_points'][:3])}
---
"""
        return formatted

    def _format_analyses_summary(self, analyses_results: List[Dict[str, Any]]) -> str:
        """格式化分析结果摘要"""
        summaries = []
        for result in analyses_results:
            # 提取关键信息
            agent = result.get('agent', '')
            analysis = result.get('analysis', '')
            
            # 截取分析的关键部分
            summary = self.token_manager.truncate_text(analysis, 300)
            summaries.append(f"**{agent}**: {summary}")
        
        return "\n\n".join(summaries)

    def _create_consensus_table(self, compressed_analyses: List[Dict[str, Any]]) -> str:
        """创建共识表格"""
        rows = []
        for analysis in compressed_analyses:
            master_name = analysis['agent'].split('价值投资分析师')[0].strip()
            recommendation = analysis['recommendation']
            summary = analysis['summary'][:30] + "..." if len(analysis['summary']) > 30 else analysis['summary']
            rows.append(f"| {master_name} | {recommendation} | {summary} |")
        
        header = "| 投资大师 | 建议 | 核心观点 |\n|----------|------|----------|"
        return header + "\n" + "\n".join(rows)

class MultiAgentInvestmentAnalyzerV2:
    """
    多Agent投资分析系统 V2
    集成token优化功能
    """
    
    def __init__(self, model_id: str = None, enable_token_optimization: bool = True):
        """
        初始化多Agent系统V2
        
        Args:
            model_id: 模型ID，如果不指定则从配置文件读取默认模型
            enable_token_optimization: 是否启用token优化
        """
        print("🤖 初始化多Agent投资分析系统 V2...")
        
        # 如果没有指定模型ID，从配置文件中读取默认模型
        if model_id is None:
            model_id = load_default_model_from_config()
            print(f"📋 使用配置文件中的默认模型: {model_id}")
        
        self.enable_token_optimization = enable_token_optimization
        
        # 创建配置化多Agent分析器
        self.config_analyzer = ConfigurableMultiAgentAnalyzer()
        
        # 创建增强版综合分析器
        self.synthesizer = EnhancedInvestmentSynthesizer(model_id, enable_token_optimization)
        
        # 获取所有可用的投资大师
        self.available_masters = self.config_analyzer.agent_factory.get_available_masters()
        
        # 初始化token管理器
        if enable_token_optimization:
            self.token_manager = TokenManager()
            print("✅ Token优化功能已启用")
        else:
            self.token_manager = None
        
        print("✅ 多Agent系统V2初始化完成！")
        print(f"📋 支持的投资大师: {', '.join(self.available_masters)}")

    def analyze_stock_multi_master(self, 
                                   symbol: str, 
                                   selected_masters: Optional[List[str]] = None,
                                   parallel: bool = True,
                                   show_reasoning: bool = False,
                                   analysis_mode: str = "auto") -> Dict[str, Any]:
        """
        使用多位投资大师分析股票（支持token优化）
        
        Args:
            symbol: 股票代码
            selected_masters: 选择的投资大师列表
            parallel: 是否并行分析
            show_reasoning: 是否显示推理过程
            analysis_mode: 分析模式 ("auto", "compressed", "streaming", "full")
            
        Returns:
            分析结果字典
        """
        # Token优化：限制大师数量
        if self.enable_token_optimization and selected_masters:
            if len(selected_masters) > 5:
                print(f"⚠️ Token优化：限制分析大师数量从{len(selected_masters)}位减少到5位")
                selected_masters = selected_masters[:5]
        
        # 选择投资大师
        if selected_masters is None:
            selected_masters = self.available_masters
            if self.enable_token_optimization:
                selected_masters = selected_masters[:5]  # 限制到5位大师
        else:
            # 验证选择的投资大师
            invalid_masters = [m for m in selected_masters if m not in self.available_masters]
            if invalid_masters:
                raise ValueError(f"无效的投资大师: {invalid_masters}")
        
        print(f"\n🎯 开始多投资大师分析股票: {symbol}")
        print(f"💡 选择的投资大师: {', '.join(selected_masters)}")
        if self.enable_token_optimization:
            print(f"🗜️ Token优化模式: {analysis_mode}")
        print("=" * 80)
        
        start_time = time.time()
        
        # 加载选择的Agent
        self.config_analyzer.load_agents(selected_masters)
        
        # 进行多视角分析
        multi_analysis_result = self.config_analyzer.analyze_stock_multi_perspective(
            symbol, 
            show_reasoning=show_reasoning
        )
        
        analysis_time = time.time() - start_time
        
        # Token优化的综合分析
        print(f"\n{'='*80}")
        print("📋 正在生成综合投资报告...")
        synthesis_result = self.synthesizer.synthesize_analyses(
            multi_analysis_result['individual_analyses'],
            mode=analysis_mode
        )
        
        # 清晰地显示分析结果
        print(f"\n{'='*80}")
        print("📊 综合投资分析报告")
        print("="*80)
        print(synthesis_result)
        
        synthesis_time = time.time() - start_time - analysis_time
        
        # 显示性能统计
        print(f"\n⏱️  分析完成!")
        print(f"   📊 分析时间: {analysis_time:.1f}秒")
        print(f"   🔄 综合时间: {synthesis_time:.1f}秒")
        print(f"   ⚡ 总用时: {time.time() - start_time:.1f}秒")
        print(f"   🎭 参与大师: {len(selected_masters)}位")
        if self.enable_token_optimization:
            print(f"   🗜️ 优化模式: {analysis_mode}")
        
        return {
            "symbol": symbol,
            "selected_masters": selected_masters,
            "individual_analyses": multi_analysis_result['individual_analyses'],
            "synthesis": synthesis_result,
            "analysis_mode": analysis_mode,
            "performance": {
                "analysis_time": analysis_time,
                "synthesis_time": synthesis_time,
                "total_time": time.time() - start_time,
                "masters_count": len(selected_masters),
                "token_optimization": self.enable_token_optimization
            }
        }

    def compare_stocks_multi_master(self, 
                                    symbols: List[str],
                                    selected_masters: Optional[List[str]] = None,
                                    show_reasoning: bool = False,
                                    batch_size: int = 3) -> Dict[str, Any]:
        """
        使用多位投资大师比较多只股票（支持批处理）
        
        Args:
            symbols: 股票代码列表
            selected_masters: 选择的投资大师列表
            show_reasoning: 是否显示推理过程
            batch_size: 批处理大小
            
        Returns:
            对比分析结果
        """
        # Token优化：分批处理股票
        if self.enable_token_optimization and len(symbols) > batch_size:
            print(f"🔄 Token优化：将{len(symbols)}只股票分{batch_size}只一批进行处理")
            
            # 分批处理
            stock_batches = self.token_manager.create_batched_analysis(symbols, batch_size)
            all_results = {}
            
            for i, batch in enumerate(stock_batches, 1):
                print(f"\n📊 处理第{i}批股票: {', '.join(batch)}")
                
                for symbol in batch:
                    result = self.analyze_stock_multi_master(
                        symbol=symbol,
                        selected_masters=selected_masters,
                        parallel=True,
                        show_reasoning=show_reasoning,
                        analysis_mode="compressed"  # 批处理时使用压缩模式
                    )
                    all_results[symbol] = result
                
                if i < len(stock_batches):
                    print("⏸️ 批次间暂停2秒...")
                    time.sleep(2)
        else:
            # 常规处理
            all_results = {}
            for symbol in symbols:
                result = self.analyze_stock_multi_master(
                    symbol=symbol,
                    selected_masters=selected_masters,
                    parallel=True,
                    show_reasoning=show_reasoning
                )
                all_results[symbol] = result
        
        # 生成简化的对比报告
        comparison_report = self._generate_simplified_comparison_report(all_results)
        print(f"\n{'='*80}")
        print("📈 多股票对比分析报告")
        print("="*80)
        print(comparison_report)
        
        return {
            "symbols": symbols,
            "selected_masters": selected_masters,
            "individual_stock_analyses": all_results,
            "comparison_report": comparison_report,
            "batch_processing": self.enable_token_optimization and len(symbols) > batch_size
        }

    def _generate_simplified_comparison_report(self, all_results: Dict[str, Any]) -> str:
        """生成简化版对比报告"""
        symbols = list(all_results.keys())
        
        # 提取关键信息
        summary_data = []
        for symbol, result in all_results.items():
            summary_data.append({
                "symbol": symbol,
                "masters_count": result["performance"]["masters_count"],
                "total_time": result["performance"]["total_time"]
            })
        
        report = f"""
# 📊 股票对比分析报告

## 🎯 分析概况
- **对比股票**: {', '.join(symbols)}
- **参与大师**: {summary_data[0]['masters_count']}位
- **总分析时间**: {sum(item['total_time'] for item in summary_data):.1f}秒

## 📈 投资排名
| 排名 | 股票 | 推荐度 | 备注 |
|------|------|--------|------|
{self._create_ranking_rows(all_results)}

## 💡 投资建议
基于多位投资大师的分析，建议重点关注排名靠前的股票。
具体投资决策请参考各股票的详细分析报告。

---
*⚡ 简化报告模式 | 📊 分析时间: {time.strftime('%Y-%m-%d %H:%M')}*
"""
        return report

    def _create_ranking_rows(self, all_results: Dict[str, Any]) -> str:
        """创建排名表格行"""
        rows = []
        for i, (symbol, result) in enumerate(all_results.items(), 1):
            rows.append(f"| {i} | {symbol} | 待评估 | 详见个股分析 |")
        return "\n".join(rows)

def main():
    """主函数 - 演示多Agent投资分析系统V2"""
    print("🎯 多Agent价值投资分析系统 V2")
    print("💫 支持5位投资大师的多视角智慧分析")
    print("🔧 基于可配置Agent系统的升级版本")
    print("=" * 80)
    
    # 创建多Agent分析器V2
    analyzer = MultiAgentInvestmentAnalyzerV2()
    
    while True:
        print(f"\n📋 请选择分析类型:")
        print("1. 多投资大师单股分析")
        print("2. 多投资大师多股对比")
        print("3. 查看投资大师信息")
        print("4. 退出")
        
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            # 选择投资大师
            selected_masters = analyzer.get_master_selection_menu()
            
            # 输入股票代码
            symbol = input("\n请输入股票代码 (如 AAPL): ").strip().upper()
            if symbol:
                analyzer.analyze_stock_multi_master(
                    symbol=symbol,
                    selected_masters=selected_masters,
                    parallel=True,
                    show_reasoning=False
                )
        
        elif choice == "2":
            # 选择投资大师
            selected_masters = analyzer.get_master_selection_menu()
            
            # 输入股票代码
            symbols_input = input("\n请输入股票代码，用逗号分隔 (如 AAPL,MSFT,GOOGL): ").strip().upper()
            if symbols_input:
                symbols = [s.strip() for s in symbols_input.split(",")]
                analyzer.compare_stocks_multi_master(
                    symbols=symbols,
                    selected_masters=selected_masters,
                    show_reasoning=False
                )
        
        elif choice == "3":
            analyzer.config_analyzer.get_master_comparison()
        
        elif choice == "4":
            print("👋 感谢使用多Agent投资分析系统V2！")
            break
        
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main() 