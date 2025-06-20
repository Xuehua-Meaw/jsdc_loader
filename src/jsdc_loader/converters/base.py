"""杂鱼♡～这是本喵定义的基础转换器接口喵～所有转换器都要遵循这个契约♡～"""

from abc import ABC, abstractmethod
from typing import Any, Type

from ..schema.field_schema import FieldSchema


class BaseConverter(ABC):
    """杂鱼♡～基础转换器抽象类喵～定义转换器的统一接口♡～"""
    
    @abstractmethod
    def can_convert(self, target_type: Type) -> bool:
        """杂鱼♡～检查是否可以转换指定类型喵～
        
        Args:
            target_type: 目标类型
            
        Returns:
            bool: 是否可以转换
        """
        pass
    
    @abstractmethod  
    def convert(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～执行类型转换喵～
        
        Args:
            value: 要转换的值
            field_schema: 字段Schema信息
            
        Returns:
            Any: 转换后的值
            
        Raises:
            ConversionError: 转换失败时抛出
        """
        pass
    
    def get_priority(self) -> int:
        """杂鱼♡～获取转换器优先级喵～数字越小优先级越高♡～
        
        Returns:
            int: 优先级，默认为100
        """
        return 100
    
    def apply_custom_decoder(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～应用自定义解码器喵～
        
        Args:
            value: 要解码的值
            field_schema: 字段Schema信息
            
        Returns:
            Any: 解码后的值
        """
        if field_schema.custom_decoder:
            try:
                return field_schema.custom_decoder(value)
            except Exception as e:
                from ..api.exceptions import ConversionError
                raise ConversionError(
                    f"杂鱼♡～自定义解码器执行失败喵：{str(e)}",
                    field_path=field_schema.field_path,
                    expected_type=field_schema.exact_type,
                    actual_value=value
                ) from e
        return value
    
    def apply_custom_encoder(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～应用自定义编码器喵～
        
        Args:
            value: 要编码的值
            field_schema: 字段Schema信息
            
        Returns:
            Any: 编码后的值
        """
        if field_schema.custom_encoder:
            try:
                return field_schema.custom_encoder(value)
            except Exception as e:
                from ..api.exceptions import ConversionError
                raise ConversionError(
                    f"杂鱼♡～自定义编码器执行失败喵：{str(e)}",
                    field_path=field_schema.field_path,
                    expected_type=field_schema.exact_type,
                    actual_value=value
                ) from e
        return value
    
    def should_exclude_value(self, value: Any, field_schema: FieldSchema, default_value: Any = None) -> bool:
        """杂鱼♡～检查是否应该排除此值喵～
        
        Args:
            value: 要检查的值
            field_schema: 字段Schema信息
            default_value: 字段的默认值
            
        Returns:
            bool: 是否应该排除
        """
        # 杂鱼♡～检查是否应该排除None值喵～
        if field_schema.exclude_if_none and value is None:
            return True
        
        # 杂鱼♡～检查是否应该排除默认值喵～
        if field_schema.exclude_if_default and value == default_value:
            return True
        
        return False 