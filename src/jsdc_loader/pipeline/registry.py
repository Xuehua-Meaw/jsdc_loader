"""杂鱼♡～这是本喵的转换器注册表喵～负责管理所有的转换器♡～"""

from typing import Dict, List, Type
from ..converters.base import BaseConverter
from ..schema.field_schema import ConverterType


class ConverterRegistry:
    """杂鱼♡～转换器注册表喵～管理所有的转换器实例♡～"""
    
    def __init__(self):
        # 杂鱼♡～按转换器类型分组存储喵～
        self._converters: Dict[ConverterType, List[BaseConverter]] = {
            ConverterType.BASIC: [],
            ConverterType.CONTAINER: [],
            ConverterType.SPECIAL: [],
            ConverterType.DATACLASS: [],
            ConverterType.UNION: []
        }
    
    def register(self, converter: BaseConverter, converter_type: ConverterType) -> None:
        """杂鱼♡～注册转换器喵～
        
        Args:
            converter: 转换器实例
            converter_type: 转换器类型
        """
        converters = self._converters[converter_type]
        converters.append(converter)
        # 杂鱼♡～按优先级排序喵～优先级数字越小越优先♡～
        converters.sort(key=lambda c: c.get_priority())
    
    def get_converter(self, target_type: Type, converter_type: ConverterType) -> BaseConverter:
        """杂鱼♡～获取能处理指定类型的转换器喵～
        
        Args:
            target_type: 目标类型
            converter_type: 转换器类型
            
        Returns:
            BaseConverter: 匹配的转换器
            
        Raises:
            ValueError: 没有找到合适的转换器时
        """
        for converter in self._converters[converter_type]:
            if converter.can_convert(target_type):
                return converter
        
        raise ValueError(f"杂鱼♡～没有找到能处理类型 {target_type} 的 {converter_type.value} 转换器喵～")


# 杂鱼♡～全局转换器注册表实例喵～
_global_registry = ConverterRegistry()


def get_global_registry() -> ConverterRegistry:
    """杂鱼♡～获取全局转换器注册表喵～"""
    return _global_registry


def register_converter(converter: BaseConverter, converter_type: ConverterType) -> None:
    """杂鱼♡～注册转换器到全局注册表喵～"""
    _global_registry.register(converter, converter_type) 