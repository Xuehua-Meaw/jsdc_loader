"""杂鱼♡～这是本喵调试Optional类型解析的脚本喵～"""

import sys
sys.path.insert(0, 'src')

from typing import Optional, Union, get_args, get_origin
from jsdc_loader.schema.type_analyzer import TypeAnalyzer


def debug_optional_type():
    """杂鱼♡～调试Optional类型解析喵～"""
    print("杂鱼♡～调试Optional类型解析喵～")
    
    # 杂鱼♡～测试不同的类型表示法喵～
    test_types = [
        Optional[str],          # typing.Optional[str]
        Union[str, None],       # typing.Union[str, None]
        str,                    # 普通str类型
    ]
    
    analyzer = TypeAnalyzer()
    
    for test_type in test_types:
        print(f"\n测试类型: {test_type}")
        print(f"  get_origin: {get_origin(test_type)}")
        print(f"  get_args: {get_args(test_type)}")
        
        # 杂鱼♡～使用本喵的类型分析器分析喵～
        try:
            analysis = analyzer.analyze_type(test_type)
            print(f"  分析结果:")
            print(f"    converter_type: {analysis['converter_type']}")
            print(f"    is_optional: {analysis['is_optional']}")
            print(f"    origin_type: {analysis['origin_type']}")
            print(f"    is_union: {analysis['is_union']}")
        except Exception as e:
            print(f"  分析失败: {e}")


if __name__ == "__main__":
    debug_optional_type() 