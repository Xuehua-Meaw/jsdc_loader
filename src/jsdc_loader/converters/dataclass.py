"""杂鱼♡～这是本喵为dataclass类型写的转换器喵～处理嵌套的dataclass对象♡～"""

from dataclasses import is_dataclass
from typing import Any, Type, Dict

from .base import BaseConverter
from ..schema.field_schema import FieldSchema


class DataclassConverter(BaseConverter):
    """杂鱼♡～dataclass类型转换器喵～处理嵌套的dataclass对象♡～"""
    
    def get_priority(self) -> int:
        # 杂鱼♡～dataclass转换器优先级中等喵～
        return 30
    
    def can_convert(self, target_type: Type) -> bool:
        """杂鱼♡～检查是否能转换指定类型喵～"""
        # 杂鱼♡～只处理dataclass类型喵～
        return is_dataclass(target_type)
    
    def convert(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～执行dataclass类型转换喵～
        
        Args:
            value: 要转换的值（通常是dict）
            field_schema: 字段模式信息
            
        Returns:
            Any: 转换后的dataclass实例
            
        Raises:
            ValueError: 转换失败时
        """
        target_type = field_schema.exact_type
        field_path = field_schema.field_path
        
        # 杂鱼♡～处理None值喵～
        if value is None:
            if field_schema.is_optional:
                return None
            else:
                raise ValueError(f"杂鱼♡～字段 '{field_path}' 不允许为None喵！～")
        
        # 杂鱼♡～dataclass转换需要字典输入喵～
        if not isinstance(value, dict):
            raise ValueError(f"杂鱼♡～dataclass转换需要字典输入，得到{type(value)}喵！～")
        
        # 杂鱼♡～处理循环引用情况：如果没有子schema，动态构建喵～
        if field_schema.sub_schema is None:
            from ..schema.schema_builder import build_schema
            sub_schema = build_schema(target_type)
        else:
            sub_schema = field_schema.sub_schema
        
        try:
            # 杂鱼♡～委托给coordinator进行递归转换喵～
            from ..pipeline.coordinator import get_global_coordinator
            coordinator = get_global_coordinator()
            
            return coordinator._convert_dataclass_from_dict(
                value, sub_schema, field_path
            )
            
        except Exception as e:
            raise ValueError(f"杂鱼♡～字段 '{field_path}' dataclass转换失败喵！～ 错误: {str(e)}") from e
    
    def convert_to_dict(self, value: Any, field_schema: FieldSchema) -> Dict[str, Any]:
        """杂鱼♡～将dataclass对象序列化为字典格式喵～
        
        Args:
            value: 要序列化的dataclass实例
            field_schema: 字段模式信息
            
        Returns:
            Dict[str, Any]: 序列化后的字典
            
        Raises:
            ValueError: 序列化失败时
        """
        target_type = field_schema.exact_type
        field_path = field_schema.field_path
        
        # 杂鱼♡～处理None值喵～
        if value is None:
            return None
        
        # 杂鱼♡～检查输入类型喵～
        if not is_dataclass(value):
            raise ValueError(f"杂鱼♡～期望dataclass实例，得到{type(value)}喵！～")
        
        # 杂鱼♡～处理循环引用情况：如果没有子schema，动态构建喵～
        if field_schema.sub_schema is None:
            from ..schema.schema_builder import build_schema
            sub_schema = build_schema(type(value))
        else:
            sub_schema = field_schema.sub_schema
        
        try:
            # 杂鱼♡～委托给coordinator进行递归序列化喵～
            from ..pipeline.coordinator import get_global_coordinator
            coordinator = get_global_coordinator()
            
            return coordinator._convert_dataclass_to_dict(
                value, sub_schema, field_path
            )
            
        except Exception as e:
            raise ValueError(f"杂鱼♡～字段 '{field_path}' dataclass序列化失败喵！～ 错误: {str(e)}") from e 