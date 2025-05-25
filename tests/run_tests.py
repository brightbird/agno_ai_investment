#!/usr/bin/env python3
"""
Agno AI 投资分析系统 - 统一测试运行器
=======================================

运行所有或指定类型的测试

使用方法:
    python tests/run_tests.py                # 运行所有测试
    python tests/run_tests.py unit           # 只运行单元测试
    python tests/run_tests.py functional     # 只运行功能测试
    python tests/run_tests.py integration    # 只运行集成测试
"""

import os
import sys
import argparse
import importlib.util
from pathlib import Path

def run_test_file(test_file_path):
    """运行单个测试文件"""
    print(f"\n🔄 运行测试: {test_file_path.name}")
    print("=" * 60)
    
    try:
        # 动态导入测试模块
        spec = importlib.util.spec_from_file_location(
            test_file_path.stem, 
            test_file_path
        )
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        # 运行测试
        if hasattr(test_module, 'main'):
            result = test_module.main()
            return result if result is not None else True
        else:
            print("⚠️ 测试文件没有main函数")
            return False
            
    except Exception as e:
        print(f"❌ 测试执行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_tests_in_directory(test_dir):
    """运行目录中的所有测试"""
    if not test_dir.exists():
        print(f"⚠️ 测试目录不存在: {test_dir}")
        return True, 0
    
    test_files = list(test_dir.glob("test_*.py"))
    if not test_files:
        print(f"📋 {test_dir.name}目录中没有测试文件")
        return True, 0
    
    print(f"\n📂 运行{test_dir.name}测试 ({len(test_files)}个文件)")
    print("=" * 80)
    
    passed = 0
    total = len(test_files)
    
    for test_file in test_files:
        success = run_test_file(test_file)
        if success:
            passed += 1
            print(f"✅ {test_file.name} - 通过")
        else:
            print(f"❌ {test_file.name} - 失败")
    
    print(f"\n📊 {test_dir.name}测试结果: {passed}/{total} 通过")
    return passed == total, total

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Agno AI 投资分析系统测试运行器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
测试类型说明:
  unit         - 单元测试: 测试单个模块和函数
  functional   - 功能测试: 测试完整的用户功能流程  
  integration  - 集成测试: 测试系统组件集成

示例:
  python tests/run_tests.py                # 运行所有测试
  python tests/run_tests.py unit           # 只运行单元测试
  python tests/run_tests.py functional     # 只运行功能测试
        """
    )
    
    parser.add_argument(
        'test_type', 
        nargs='?', 
        choices=['unit', 'functional', 'integration', 'all'],
        default='all',
        help='要运行的测试类型 (默认: all)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )
    
    args = parser.parse_args()
    
    # 确保我们在正确的目录中
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🚀 Agno AI 投资分析系统 - 测试运行器")
    print("=" * 80)
    
    tests_dir = Path("tests")
    
    # 定义测试目录
    test_directories = {
        'unit': tests_dir / "unit",
        'functional': tests_dir / "functional", 
        'integration': tests_dir / "integration"
    }
    
    total_passed = 0
    total_tests = 0
    all_success = True
    
    # 运行指定类型的测试
    if args.test_type == 'all':
        for test_name, test_dir in test_directories.items():
            success, count = run_tests_in_directory(test_dir)
            all_success &= success
            total_tests += count
            if success:
                total_passed += count
    else:
        test_dir = test_directories.get(args.test_type)
        if test_dir:
            success, count = run_tests_in_directory(test_dir)
            all_success = success
            total_tests = count
            if success:
                total_passed = count
        else:
            print(f"❌ 未知的测试类型: {args.test_type}")
            return False
    
    # 总结
    print("\n" + "=" * 80)
    print("📊 测试总结")
    print("=" * 80)
    
    if total_tests == 0:
        print("⚠️ 没有找到可运行的测试")
        return True
    
    success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"📈 总测试数: {total_tests}")
    print(f"✅ 通过测试: {total_passed}")
    print(f"❌ 失败测试: {total_tests - total_passed}")
    print(f"📊 成功率: {success_rate:.1f}%")
    
    if all_success:
        print("\n🎉 所有测试都通过了！")
        print("✨ Agno AI 投资分析系统运行正常")
        
        if args.test_type == 'all':
            print("\n💡 系统功能验证:")
            print("   ✅ 单元测试: 基础组件功能正常")
            print("   ✅ 功能测试: 用户功能流程正常")
            print("   ✅ 集成测试: 系统集成协作正常")
    else:
        print("\n❌ 部分测试失败")
        print("🔧 请检查失败的测试并修复相关问题")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 