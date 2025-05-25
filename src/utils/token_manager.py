"""
Token管理工具
处理AI模型的token限制问题
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class TokenBudget:
    """Token预算配置"""
    max_total_tokens: int = 8000  # 总token限制
    max_input_tokens: int = 6000  # 输入token限制
    max_output_tokens: int = 2000  # 输出token限制
    reserve_tokens: int = 500     # 预留token
    

class TokenManager:
    """Token管理器"""
    
    def __init__(self, budget: TokenBudget = None):
        self.budget = budget or TokenBudget()
        
    def estimate_tokens(self, text: str) -> int:
        """
        估算文本的token数量
        简单估算：中文按字数，英文按单词数*1.3
        """
        if not text:
            return 0
            
        # 统计中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        
        # 统计英文单词
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        
        # 统计数字和符号
        other_chars = len(re.sub(r'[\u4e00-\u9fff\sa-zA-Z]', '', text))
        
        # 估算token数
        estimated_tokens = chinese_chars + int(english_words * 1.3) + int(other_chars * 0.5)
        
        return max(estimated_tokens, 1)
    
    def truncate_text(self, text: str, max_tokens: int) -> str:
        """
        截断文本到指定token数
        """
        current_tokens = self.estimate_tokens(text)
        
        if current_tokens <= max_tokens:
            return text
            
        # 计算截断比例
        ratio = max_tokens / current_tokens * 0.9  # 留10%安全边际
        target_length = int(len(text) * ratio)
        
        # 从中间截断，保留开头和结尾
        if target_length < len(text):
            keep_start = target_length // 2
            keep_end = target_length - keep_start
            truncated = text[:keep_start] + "\n\n[... 内容过长，已截断 ...]\n\n" + text[-keep_end:]
            return truncated
        
        return text
    
    def compress_analysis_results(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        压缩分析结果，提取关键信息
        """
        compressed_analyses = []
        
        for analysis in analyses:
            # 提取关键信息
            compressed = {
                "agent": analysis.get("agent", ""),
                "symbol": analysis.get("symbol", ""),
                "style": analysis.get("style", ""),
                "summary": self._extract_summary(analysis.get("analysis", "")),
                "recommendation": self._extract_recommendation(analysis.get("analysis", "")),
                "key_points": self._extract_key_points(analysis.get("analysis", ""))
            }
            compressed_analyses.append(compressed)
        
        return compressed_analyses
    
    def _extract_summary(self, analysis_text: str) -> str:
        """提取分析摘要"""
        if not analysis_text:
            return ""
            
        # 寻找摘要相关的段落
        summary_patterns = [
            r"##?\s*摘要[\s\S]*?(?=##|\n\n|\Z)",
            r"##?\s*总结[\s\S]*?(?=##|\n\n|\Z)",
            r"##?\s*结论[\s\S]*?(?=##|\n\n|\Z)",
            r"##?\s*投资建议[\s\S]*?(?=##|\n\n|\Z)"
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, analysis_text, re.IGNORECASE)
            if match:
                summary = match.group(0)
                return self.truncate_text(summary, 200)
        
        # 如果没找到专门的摘要，取前200个token
        return self.truncate_text(analysis_text, 200)
    
    def _extract_recommendation(self, analysis_text: str) -> str:
        """提取投资建议"""
        if not analysis_text:
            return "未明确"
            
        # 寻找推荐相关的词汇
        buy_patterns = [
            r"强烈推荐|强烈买入|买入|推荐购买",
            r"建议买入|建议购买|值得投资",
            r"BUY|Strong Buy|Outperform"
        ]
        
        hold_patterns = [
            r"持有|继续持有|维持",
            r"HOLD|Neutral"
        ]
        
        sell_patterns = [
            r"卖出|减持|建议卖出",
            r"SELL|Underperform"
        ]
        
        text_lower = analysis_text.lower()
        
        for pattern in buy_patterns:
            if re.search(pattern, analysis_text, re.IGNORECASE):
                return "买入"
        
        for pattern in sell_patterns:
            if re.search(pattern, analysis_text, re.IGNORECASE):
                return "卖出"
                
        for pattern in hold_patterns:
            if re.search(pattern, analysis_text, re.IGNORECASE):
                return "持有"
        
        return "未明确"
    
    def _extract_key_points(self, analysis_text: str) -> List[str]:
        """提取关键要点"""
        if not analysis_text:
            return []
            
        key_points = []
        
        # 寻找列表项或要点
        bullet_patterns = [
            r"[-*•]\s*([^\n]+)",
            r"\d+[.)]\s*([^\n]+)",
            r"[▪▫]\s*([^\n]+)"
        ]
        
        for pattern in bullet_patterns:
            matches = re.findall(pattern, analysis_text)
            for match in matches:
                if len(match.strip()) > 10:  # 过滤太短的内容
                    key_points.append(match.strip())
        
        # 限制要点数量和长度
        key_points = key_points[:5]  # 最多5个要点
        key_points = [self.truncate_text(point, 50) for point in key_points]
        
        return key_points
    
    def split_large_analysis(self, prompt: str, max_tokens: int) -> List[str]:
        """
        将大的分析请求分割为多个小请求
        """
        current_tokens = self.estimate_tokens(prompt)
        
        if current_tokens <= max_tokens:
            return [prompt]
        
        # 尝试按段落分割
        paragraphs = prompt.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            test_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
            
            if self.estimate_tokens(test_chunk) <= max_tokens:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = paragraph
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def create_batched_analysis(self, symbols: List[str], batch_size: int = 3) -> List[List[str]]:
        """
        将股票列表分批处理
        """
        batches = []
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i + batch_size]
            batches.append(batch)
        return batches
    
    def optimize_prompt_template(self, template: str) -> str:
        """
        优化prompt模板，减少token使用
        """
        # 移除多余的空行
        optimized = re.sub(r'\n{3,}', '\n\n', template)
        
        # 压缩重复的分隔符
        optimized = re.sub(r'={3,}', '===', optimized)
        optimized = re.sub(r'-{3,}', '---', optimized)
        
        # 移除多余的空格
        optimized = re.sub(r' {2,}', ' ', optimized)
        
        # 简化表格格式指令
        table_simplifications = {
            r'请严格按照以下格式输出': '按以下格式输出',
            r'请基于以下.*?的分析': '基于以下分析',
            r'生成一份结构化的综合投资报告': '生成综合投资报告'
        }
        
        for pattern, replacement in table_simplifications.items():
            optimized = re.sub(pattern, replacement, optimized)
        
        return optimized.strip()


class StreamingAnalyzer:
    """流式分析器，支持大内容的分段处理"""
    
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager
        
    def stream_multi_master_analysis(self, symbol: str, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        流式处理多投资大师分析
        """
        # 压缩分析结果
        compressed_analyses = self.token_manager.compress_analysis_results(analyses)
        
        # 生成分段报告
        sections = {
            "executive_summary": self._generate_executive_summary(symbol, compressed_analyses),
            "master_opinions": self._generate_master_opinions(compressed_analyses),
            "risk_assessment": self._generate_risk_assessment(symbol, compressed_analyses),
            "investment_plan": self._generate_investment_plan(symbol, compressed_analyses)
        }
        
        return {
            "symbol": symbol,
            "sections": sections,
            "compressed_analyses": compressed_analyses
        }
    
    def _generate_executive_summary(self, symbol: str, analyses: List[Dict[str, Any]]) -> str:
        """生成执行摘要"""
        prompt = f"""
基于以下{len(analyses)}位投资大师对{symbol}的分析摘要，生成简洁的执行摘要：

{json.dumps(analyses, ensure_ascii=False, indent=2)}

请输出：
## 🎯 执行摘要

| 项目 | 结论 |
|------|------|
| 最终建议 | [买入/持有/卖出] |
| 综合评分 | [X/10分] |
| 风险等级 | [低/中/高] |

## 📊 一致性观点
- [3句话总结大师们的一致观点]

## ⚠️ 主要风险
- [最重要的2-3个风险点]
"""
        return self.token_manager.truncate_text(prompt, 1000)
    
    def _generate_master_opinions(self, analyses: List[Dict[str, Any]]) -> str:
        """生成大师观点对比"""
        prompt = f"""
基于以下投资大师观点摘要，生成观点对比：

{json.dumps(analyses, ensure_ascii=False, indent=2)}

请输出：
## 🎭 投资大师观点对比

| 大师 | 建议 | 核心逻辑 | 信心度 |
|------|------|----------|--------|
{self._create_master_table_rows(analyses)}

## 观点分析
- 一致观点：[总结]
- 主要分歧：[总结]
"""
        return self.token_manager.truncate_text(prompt, 1000)
    
    def _generate_risk_assessment(self, symbol: str, analyses: List[Dict[str, Any]]) -> str:
        """生成风险评估"""
        prompt = f"""
基于投资大师分析，为{symbol}生成风险评估：

请输出：
## ⚠️ 风险评估

| 风险类型 | 程度 | 应对策略 |
|----------|------|----------|
| 估值风险 | [高/中/低] | [策略] |
| 业绩风险 | [高/中/低] | [策略] |
| 市场风险 | [高/中/低] | [策略] |

## 风险控制
- 止损位：[价格]
- 监控指标：[关键指标]
"""
        return self.token_manager.truncate_text(prompt, 800)
    
    def _generate_investment_plan(self, symbol: str, analyses: List[Dict[str, Any]]) -> str:
        """生成投资计划"""
        prompt = f"""
为{symbol}生成投资执行计划：

## 🎯 投资执行计划

### 买入策略
| 投资者类型 | 建议仓位 | 买入价位 |
|------------|----------|----------|
| 保守型 | [X]% | $[价格] |
| 平衡型 | [X]% | $[价格] |
| 激进型 | [X]% | $[价格] |

### 时间规划
- 短期目标：[1-6个月]
- 中期目标：[6-18个月]
- 长期目标：[18个月+]
"""
        return self.token_manager.truncate_text(prompt, 600)
    
    def _create_master_table_rows(self, analyses: List[Dict[str, Any]]) -> str:
        """创建大师观点表格行"""
        rows = []
        for analysis in analyses:
            master = analysis.get("agent", "").split("价值投资分析师")[0].strip()
            recommendation = analysis.get("recommendation", "未明确")
            summary = analysis.get("summary", "")[:50]  # 截断到50字符
            rows.append(f"| {master} | {recommendation} | {summary} | 中等 |")
        return "\n".join(rows)


def create_token_optimized_agents():
    """创建token优化的agent配置"""
    return {
        "model_config": {
            "max_tokens": 1500,  # 减少单次输出token
            "temperature": 0.7,
            "stream": True  # 启用流式输出
        },
        "prompt_optimization": {
            "use_compression": True,
            "batch_processing": True,
            "summary_mode": True
        }
    } 