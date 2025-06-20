"""杂鱼♡～这是本喵重构的递归转换中间件喵～负责分发转换任务给相应的转换器♡～"""

from typing import Any

from ..schema.field_schema import FieldSchema, ConverterType
from ..api.exceptions import ConversionError


class RecursiveConverter:
    """杂鱼♡～递归转换中间件喵～分发转换任务而不是自己实现转换逻辑♡～"""
    
    def __init__(self):
        # 杂鱼♡～递归深度限制，防止无限递归喵～
        self.max_depth = 100
        # 杂鱼♡～当前递归深度喵～
        self._current_depth = 0
    
    def convert_recursive(self, value: Any, field_schema: FieldSchema, coordinator, direction: str = "from_dict") -> Any:
        """杂鱼♡～递归分发转换任务喵～
        
        Args:
            value: 要转换的值
            field_schema: 字段Schema信息
            coordinator: 转换协调器
            direction: 转换方向 "from_dict" 或 "to_dict"
            
        Returns:
            Any: 转换后的值
            
        Raises:
            ConversionError: 转换失败时抛出
        """
        # 杂鱼♡～检查递归深度喵～
        if self._current_depth >= self.max_depth:
            raise ConversionError(
                f"杂鱼♡～递归深度超限喵：{self._current_depth} >= {self.max_depth}",
                field_path=field_schema.field_path
            )
        
        self._current_depth += 1
        try:
            # 杂鱼♡～分发给coordinator处理，不自己实现转换逻辑喵～
            if direction == "from_dict":
                return coordinator._convert_field_value(value, field_schema, field_schema.field_path)
            elif direction == "to_dict":
                return coordinator._convert_field_value_to_dict(value, field_schema, field_schema.field_path)
            else:
                raise ConversionError(
                    f"杂鱼♡～不支持的转换方向喵：{direction}",
                    field_path=field_schema.field_path
                )
        finally:
            self._current_depth -= 1


# 杂鱼♡～全局递归转换器实例喵～
_global_recursive_converter = RecursiveConverter()


def get_recursive_converter() -> RecursiveConverter:
    """杂鱼♡～获取全局递归转换器喵～"""
    return _global_recursive_converter 