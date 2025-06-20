"""杂鱼♡～这是本喵为Union类型写的转换器喵～处理复杂的联合类型转换♡～"""

from typing import Any, Type, Union, get_args, get_origin
from enum import Enum

from .base import BaseConverter
from ..schema.field_schema import FieldSchema


class UnionConverter(BaseConverter):
    """杂鱼♡～联合类型转换器喵～处理Union和Optional类型♡～"""
    
    def get_priority(self) -> int:
        # 杂鱼♡～Union类型优先级较低，让具体类型先尝试喵～
        return 90
    
    def can_convert(self, target_type: Type) -> bool:
        """杂鱼♡～检查是否能转换指定类型喵～"""
        origin = get_origin(target_type)
        return origin is Union
    
    def convert(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～执行Union类型转换喵～
        
        Args:
            value: 要转换的值
            field_schema: 字段模式信息
            
        Returns:
            Any: 转换后的值
            
        Raises:
            ValueError: 转换失败时
        """
        target_type = field_schema.exact_type
        field_path = field_schema.field_path
        
        # 杂鱼♡～获取Union的所有类型参数喵～
        union_args = get_args(target_type)
        
        # 杂鱼♡～处理None值喵～
        if value is None:
            if type(None) in union_args:
                return None
            else:
                raise ValueError(f"杂鱼♡～字段 '{field_path}' 的Union类型不允许None值喵！～")
        
        # 杂鱼♡～过滤掉None类型，获取实际的类型选项喵～
        non_none_types = [t for t in union_args if t is not type(None)]
        
        # 杂鱼♡～定义类型优先级策略喵～枚举类型优先，然后是特殊类型，最后是基本类型
        def get_type_priority(t: Type) -> int:
            """杂鱼♡～获取类型的转换优先级，数字越小优先级越高喵～"""
            # 杂鱼♡～枚举类型最高优先级喵～
            if isinstance(t, type) and issubclass(t, Enum):
                return 1
                
            # 杂鱼♡～特殊类型较高优先级喵～
            import uuid
            import datetime
            from decimal import Decimal
            special_types = (uuid.UUID, datetime.datetime, datetime.date, datetime.time, datetime.timedelta, Decimal)
            if t in special_types:
                return 2
                
            # 杂鱼♡～容器类型中等优先级喵～
            container_origins = (list, dict, set, frozenset, tuple)
            if get_origin(t) in container_origins or t in container_origins:
                return 3
                
            # 杂鱼♡～基本类型较低优先级喵～
            if t in (int, float, bool):
                return 4
                
            # 杂鱼♡～字符串类型最低优先级，因为很多类型都能转成字符串喵～
            if t is str:
                return 5
                
            # 杂鱼♡～其他类型默认优先级喵～
            return 3
        
        # 杂鱼♡～按优先级排序类型喵～
        sorted_types = sorted(non_none_types, key=get_type_priority)
        
        # 杂鱼♡～收集所有转换错误，用于最终错误消息喵～
        conversion_errors = []
        
        # 杂鱼♡～按优先级尝试转换每个类型喵～
        for attempt_type in sorted_types:
            try:
                # 杂鱼♡～创建临时的字段模式用于转换喵～
                temp_schema = FieldSchema(
                    field_path=field_path,
                    exact_type=attempt_type,
                    converter_type=self._get_converter_type_for_type(attempt_type),
                    is_optional=False,  # 杂鱼♡～这里不是Optional，而是Union中的一个选项喵～
                    union_types=[]
                )
                
                # 杂鱼♡～延迟导入避免循环引用喵～
                from ..pipeline.registry import get_global_registry
                
                # 杂鱼♡～获取对应的转换器并尝试转换喵～
                registry = get_global_registry()
                converter = registry.get_converter(attempt_type, temp_schema.converter_type)
                
                # 杂鱼♡～尝试转换喵～
                converted_value = converter.convert(value, temp_schema)
                
                # 杂鱼♡～转换成功，返回结果喵～
                return converted_value
                
            except Exception as e:
                # 杂鱼♡～转换失败，记录错误继续尝试下一个类型喵～
                conversion_errors.append(f"{attempt_type.__name__}: {str(e)}")
                continue
        
        # 杂鱼♡～所有类型都转换失败，抛出详细错误喵～
        error_details = " | ".join(conversion_errors)
        available_types = [t.__name__ for t in sorted_types]
        raise ValueError(
            f"杂鱼♡～字段 '{field_path}' 无法转换为Union[{', '.join(available_types)}]喵！～ "
            f"尝试的转换错误: {error_details}"
        )
    
    def _get_converter_type_for_type(self, target_type: Type):
        """杂鱼♡～根据类型获取对应的转换器类型喵～"""
        from ..schema.type_analyzer import TypeAnalyzer
        
        analyzer = TypeAnalyzer()
        analysis = analyzer.analyze_type(target_type)
        return analysis['converter_type']
    
    def convert_to_dict(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～将Union类型序列化为JSON兼容格式喵～
        
        Args:
            value: 要序列化的Union类型值
            field_schema: 字段模式信息
            
        Returns:
            Any: 序列化后的值
            
        Raises:
            ValueError: 序列化失败时
        """
        field_path = field_schema.field_path
        
        # 杂鱼♡～处理None值喵～
        if value is None:
            return None
        
        # 杂鱼♡～根据实际类型序列化喵～
        try:
            from ..schema.type_analyzer import TypeAnalyzer
            analyzer = TypeAnalyzer()
            actual_type = type(value)
            analysis = analyzer.analyze_type(actual_type)
            
            # 杂鱼♡～创建临时schema用于序列化喵～
            temp_schema = FieldSchema(
                field_path=field_path,
                exact_type=actual_type,
                converter_type=analysis['converter_type'],
                is_optional=False,
                union_types=[]
            )
            
            # 杂鱼♡～获取对应的转换器并尝试序列化喵～
            from ..pipeline.registry import get_global_registry
            registry = get_global_registry()
            converter = registry.get_converter(actual_type, temp_schema.converter_type)
            
            # 杂鱼♡～如果转换器有convert_to_dict方法，使用它；否则直接返回值喵～
            if hasattr(converter, 'convert_to_dict'):
                return converter.convert_to_dict(value, temp_schema)
            else:
                return value
                
        except Exception as e:
            # 杂鱼♡～序列化失败，fallback到字符串喵～
            return str(value) 