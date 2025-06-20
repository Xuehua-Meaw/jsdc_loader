"""杂鱼♡～这是本喵为容器类型写的转换器喵～处理List、Dict、Set、Tuple、Deque、FrozenSet等♡～"""

from typing import Any, Type, get_origin, get_args, Dict, List
from collections import deque

from .base import BaseConverter
from ..schema.field_schema import FieldSchema
from ..api.exceptions import ConversionError


class ContainerConverter(BaseConverter):
    """杂鱼♡～容器类型转换器喵～处理各种容器类型♡～"""
    
    def __init__(self):
        # 杂鱼♡～当前coordinator，用于保持循环引用检测状态喵～
        self._current_coordinator = None
    
    def get_priority(self) -> int:
        # 杂鱼♡～容器类型优先级中等喵～
        return 50
    
    def can_convert(self, target_type: Type) -> bool:
        """杂鱼♡～检查是否能转换指定类型喵～"""
        # 杂鱼♡～支持的容器类型喵～
        container_types = {list, dict, set, frozenset, tuple, deque}
        
        # 杂鱼♡～检查原始类型或origin类型喵～
        origin = get_origin(target_type)
        return target_type in container_types or origin in container_types
    
    def convert(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～执行容器类型转换喵～
        
        Args:
            value: 要转换的值
            field_schema: 字段模式信息
            
        Returns:
            Any: 转换后的值
            
        Raises:
            ConversionError: 转换失败时
        """
        target_type = field_schema.exact_type
        field_path = field_schema.field_path
        
        # 杂鱼♡～处理None值喵～
        if value is None:
            if field_schema.is_optional:
                return None
            else:
                raise ConversionError(f"杂鱼♡～字段 '{field_path}' 不允许为None喵！～")
        
        try:
            # 杂鱼♡～根据目标类型分发转换喵～
            if target_type == list or get_origin(target_type) == list:
                return self._convert_to_list(value, field_schema)
            
            elif target_type == dict or get_origin(target_type) == dict:
                return self._convert_to_dict(value, field_schema)
            
            elif target_type == set or get_origin(target_type) == set:
                return self._convert_to_set(value, field_schema)
            
            elif target_type == frozenset or get_origin(target_type) == frozenset:
                return self._convert_to_frozenset(value, field_schema)
            
            elif target_type == tuple or get_origin(target_type) == tuple:
                return self._convert_to_tuple(value, field_schema)
            
            elif target_type == deque or get_origin(target_type) == deque:
                return self._convert_to_deque(value, field_schema)
            
            else:
                raise ConversionError(f"杂鱼♡～不支持的容器类型 {target_type} 喵！～")
            
        except Exception as e:
            if isinstance(e, ConversionError):
                raise
            else:
                raise ConversionError(f"杂鱼♡～字段 '{field_path}' 容器类型转换失败喵！～ 错误: {str(e)}") from e
    
    def convert_to_dict(self, value: Any, field_schema: FieldSchema, coordinator: 'Serializer') -> Any:
        """杂鱼♡～将容器对象转换为字典喵～"""
        origin = get_origin(field_schema.exact_type) or field_schema.exact_type

        # 杂鱼♡～根据类型调用不同的序列化方法喵～
        if origin in (list, set, frozenset, deque):
            return self._serialize_sequence(value, field_schema, coordinator)
        elif origin is tuple:
            return self._serialize_tuple(value, field_schema, coordinator)
        elif origin is dict:
            return self._serialize_dict(value, field_schema, coordinator)
        else:
            raise ConversionError(f"杂鱼♡～不支持的容器类型序列化喵: {origin}")
    
    def _convert_to_list(self, value: Any, field_schema: FieldSchema) -> list:
        """杂鱼♡～转换为List类型喵～"""
        if not isinstance(value, list):
            raise ConversionError(f"杂鱼♡～无法将 {type(value)} 转换为list喵！～")
        
        # 杂鱼♡～递归转换元素喵～
        return self._convert_sequence_elements(value, field_schema, list)
    
    def _convert_to_dict(self, value: Any, field_schema: FieldSchema) -> dict:
        """杂鱼♡～转换为Dict类型喵～"""
        if not isinstance(value, dict):
            raise ConversionError(f"杂鱼♡～无法将 {type(value)} 转换为dict喵！～")
        
        # 杂鱼♡～递归转换键值对喵～
        return self._convert_dict_elements(value, field_schema)
    
    def _convert_to_set(self, value: Any, field_schema: FieldSchema) -> set:
        """杂鱼♡～转换为Set类型喵～"""
        if not isinstance(value, list):
            raise ConversionError(f"杂鱼♡～无法将 {type(value)} 转换为set喵！～")
        
        # 杂鱼♡～从list转换为set喵～
        converted_list = self._convert_sequence_elements(value, field_schema, list)
        return set(converted_list)
    
    def _convert_to_frozenset(self, value: Any, field_schema: FieldSchema) -> frozenset:
        """杂鱼♡～转换为FrozenSet类型喵～"""
        if not isinstance(value, list):
            raise ConversionError(f"杂鱼♡～无法将 {type(value)} 转换为frozenset喵！～")
        
        # 杂鱼♡～从list转换为frozenset喵～
        converted_list = self._convert_sequence_elements(value, field_schema, list)
        return frozenset(converted_list)
    
    def _convert_to_tuple(self, value: Any, field_schema: FieldSchema) -> tuple:
        """杂鱼♡～转换为Tuple类型喵～"""
        if not isinstance(value, list):
            raise ConversionError(f"杂鱼♡～无法将 {type(value)} 转换为tuple喵！～")
        
        # 杂鱼♡～从list转换为tuple喵～
        converted_list = self._convert_sequence_elements(value, field_schema, list)
        return tuple(converted_list)
    
    def _convert_to_deque(self, value: Any, field_schema: FieldSchema) -> deque:
        """杂鱼♡～转换为Deque类型喵～"""
        if not isinstance(value, list):
            raise ConversionError(f"杂鱼♡～无法将 {type(value)} 转换为deque喵！～")
        
        # 杂鱼♡～从list转换为deque喵～
        converted_list = self._convert_sequence_elements(value, field_schema, list)
        return deque(converted_list)
    
    def _serialize_sequence(self, value: Any, field_schema: FieldSchema, coordinator: 'Serializer') -> list:
        """杂鱼♡～序列化序列类型喵～"""
        return self._serialize_sequence_elements(value, field_schema, coordinator)
    
    def _serialize_tuple(self, value: Any, field_schema: FieldSchema, coordinator: 'Serializer') -> tuple:
        """杂鱼♡～序列化元组类型喵～"""
        return tuple(self._serialize_sequence_elements(value, field_schema, coordinator))
    
    def _serialize_dict(self, value: Any, field_schema: FieldSchema, coordinator: 'Serializer') -> dict:
        """杂鱼♡～序列化字典类型喵～"""
        return self._serialize_dict_elements(value, field_schema, coordinator)
    
    def _convert_sequence_elements(self, value: list, field_schema: FieldSchema, sequence_type: type) -> Any:
        """杂鱼♡～转换序列中的每个元素喵～"""
        if not isinstance(value, (list, tuple)):
            raise ConversionError(f"杂鱼♡～无法将 {type(value)} 转换为{sequence_type.__name__}喵！～")

        type_args = get_args(field_schema.exact_type)

        # 杂鱼♡～没有类型参数的序列（比如List）
        if not type_args:
            return sequence_type(value)

        element_type = type_args[0]
        # 杂鱼♡～变长元组 Tuple[T, ...]
        if element_type is Ellipsis:
            return sequence_type()

        # 杂鱼♡～固定长度元组 Tuple[T1, T2]
        if get_origin(field_schema.exact_type) is tuple and len(type_args) > 1 and type_args[1] is not Ellipsis:
            if len(value) != len(type_args):
                raise ConversionError(f"杂鱼♡～元组长度不匹配喵！～期望 {len(type_args)}，得到 {len(value)}")
            
            converted_elements = []
            for i, (item, item_type) in enumerate(zip(value, type_args)):
                # 杂鱼♡～为每个元素创建临时的FieldSchema喵～
                element_schema = self._build_element_schema(item_type, f"{field_schema.field_path}[{i}]")
                converted_elements.append(
                    self.convert_recursive(item, element_schema)
                )
            return tuple(converted_elements)

        # 杂鱼♡～List[T], Set[T], Deque[T], Tuple[T, ...]
        element_schema = self._build_element_schema(element_type, f"{field_schema.field_path}.<item>")
        
        converted_list = [
            self.convert_recursive(item, element_schema)
            for i, item in enumerate(value)
        ]
        return sequence_type(converted_list)

    def _serialize_sequence_elements(self, value: Any, field_schema: FieldSchema, coordinator: 'Serializer') -> list:
        """杂鱼♡～序列化序列的每个元素喵～"""
        type_args = get_args(field_schema.exact_type)
        if not type_args:
            return list(value)

        element_type = type_args[0]
        if element_type is Ellipsis:
            return []

        # 杂鱼♡～固定长度元组 Tuple[T1, T2]
        if get_origin(field_schema.exact_type) is tuple and len(type_args) > 1 and type_args[1] is not Ellipsis:
            result = []
            for i, (item, item_type) in enumerate(zip(value, type_args)):
                # 杂鱼♡～为每个元素创建临时的FieldSchema喵～
                from ..pipeline.recursive import get_recursive_converter # 避免循环引用
                analyzer = get_recursive_converter().type_analyzer
                analysis = analyzer.analyze_type(item_type)
                
                element_schema = FieldSchema(
                    field_path=f"{field_schema.field_path}[{i}]",
                    exact_type=item_type,
                    **analysis
                )
                result.append(
                    coordinator._convert_field_value_to_dict(item, element_schema, f"{field_schema.field_path}[{i}]")
                )
            return result

        # 杂鱼♡～List[T], Set[T], Deque[T], Tuple[T, ...]
        from ..pipeline.recursive import get_recursive_converter # 避免循环引用
        analyzer = get_recursive_converter().type_analyzer
        analysis = analyzer.analyze_type(element_type)
        
        element_schema = FieldSchema(
            field_path=f"{field_schema.field_path}.<item>",
            exact_type=element_type,
            **analysis
        )
        
        return [
            coordinator._convert_field_value_to_dict(item, element_schema, f"{field_schema.field_path}[{i}]")
            for i, item in enumerate(value)
        ]

    def _convert_dict_elements(self, value: dict, field_schema: FieldSchema) -> dict:
        """杂鱼♡～转换字典的键和值喵～"""
        if not isinstance(value, dict):
            raise ConversionError(f"杂鱼♡～无法将 {type(value)} 转换为dict喵！～")

        type_args = get_args(field_schema.exact_type)
        if not type_args:
            return value  # 杂鱼♡～没有类型参数，直接返回喵～

        # 杂鱼♡～本喵来决定具体用哪个转换器喵～
        key_type_arg = type_args[0] if type_args else Any
        value_type_arg = type_args[1] if len(type_args) > 1 else Any

        # 杂鱼♡～转换字典的每一个键值对喵～
        converted_dict = {}
        for k, v in value.items():
            # 哼～本喵现在自己动手，丰衣足食喵～
            key_schema = self._build_element_schema(key_type_arg, f"{field_schema.field_path}.<key>")
            new_key = self.convert_recursive(k, key_schema)

            value_schema = self._build_element_schema(value_type_arg, f"{field_schema.field_path}[{k}]")
            new_value = self.convert_recursive(v, value_schema)
            
            converted_dict[new_key] = new_value

        return converted_dict

    def _build_element_schema(self, element_type: Type, element_path: str) -> FieldSchema:
        """杂鱼♡～为容器的元素构建临时的FieldSchema喵～"""
        from ..schema.type_analyzer import TypeAnalyzer
        analyzer = TypeAnalyzer()
        analysis = analyzer.analyze_type(element_type)
        
        return FieldSchema(
            field_path=element_path,
            exact_type=element_type,
            **analysis
        )

    def convert_recursive(self, value: Any, schema: FieldSchema) -> Any:
        """杂鱼♡～本喵自己的递归转换方法喵～哼～"""
        # 哼～本喵把反序列化器里的逻辑搬过来了，厉害吧～
        # 才...才不是因为形成了新的循环依赖喵！
        from ..pipeline.coordinator import Deserializer
        
        # 杂鱼♡～每次都创建一个新的实例，避免状态污染喵～
        deserializer = Deserializer()
        
        # 杂鱼♡～把自己的转换路径嫁接过去，方便调试喵～
        if hasattr(self, '_conversion_path'):
            deserializer._conversion_path = self._conversion_path
            
        return deserializer._convert_field_value(value, schema, schema.field_path)

    def _serialize_dict_elements(self, value: dict, field_schema: FieldSchema, coordinator: 'Serializer') -> dict:
        """杂鱼♡～序列化字典的键和值喵～"""
        type_args = get_args(field_schema.exact_type)
        if not type_args:
            return value

        key_type = type_args[0]
        value_type = type_args[1]

        # 杂鱼♡～又要麻烦递归转换器了喵～
        from ..pipeline.recursive import get_recursive_converter # 避免循环引用
        analyzer = get_recursive_converter().type_analyzer
        
        key_analysis = analyzer.analyze_type(key_type)
        key_schema = FieldSchema(field_path=f"{field_schema.field_path}.<key>", exact_type=key_type, **key_analysis)
        
        value_analysis = analyzer.analyze_type(value_type)
        value_schema = FieldSchema(field_path=f"{field_schema.field_path}.<value>", exact_type=value_type, **value_analysis)

        result = {}
        for k, v in value.items():
            # 哼～键必须是能变成字符串的类型喵～
            # 这里直接用str，因为JSON的key必须是字符串
            new_key = str(coordinator._convert_field_value_to_dict(k, key_schema, f"{field_schema.field_path}[{k}].<key>"))

            new_value = coordinator._convert_field_value_to_dict(v, value_schema, f"{field_schema.field_path}[{k}].<value>")
            result[new_key] = new_value
        return result 