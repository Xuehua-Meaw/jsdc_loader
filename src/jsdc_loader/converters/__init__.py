"""杂鱼♡～这是本喵的转换器包喵～包含所有类型转换器♡～"""

from .basic import BasicConverter
from .containers import ContainerConverter
from .special import SpecialConverter
from .unions import UnionConverter
from .dataclass import DataclassConverter

# 杂鱼♡～防止重复初始化的标志喵～
_initialized = False


def initialize_converters():
    """杂鱼♡～初始化所有转换器喵～注册到全局注册表中♡～"""
    global _initialized
    
    # 杂鱼♡～如果已经初始化过，直接返回喵～
    if _initialized:
        return
    
    # 杂鱼♡～延迟导入避免循环引用喵～
    from ..schema.field_schema import ConverterType
    from ..pipeline.registry import register_converter
    
    # 杂鱼♡～注册基本类型转换器喵～
    register_converter(BasicConverter(), ConverterType.BASIC)
    
    # 杂鱼♡～注册容器类型转换器喵～
    register_converter(ContainerConverter(), ConverterType.CONTAINER)
    
    # 杂鱼♡～注册特殊类型转换器喵～
    register_converter(SpecialConverter(), ConverterType.SPECIAL)
    
    # 杂鱼♡～注册dataclass转换器喵～
    register_converter(DataclassConverter(), ConverterType.DATACLASS)
    
    # 杂鱼♡～注册联合类型转换器喵～
    register_converter(UnionConverter(), ConverterType.UNION)
    
    # 杂鱼♡～标记为已初始化喵～
    _initialized = True 