"""杂鱼♡～这是本喵的转换协调器喵～负责整个转换流程的编排♡～"""

from dataclasses import is_dataclass
from typing import Any, Dict, List, Type, Set, Callable

from ..schema.field_schema import FieldSchema, TypeSchema, ConverterType
from ..schema.schema_builder import build_schema
from .registry import get_global_registry
from .recursive import get_recursive_converter
from ..api.exceptions import ConversionError, SchemaError


class _BaseCoordinator:
    """杂鱼♡～这是协调器的基类喵～放一些共用的东西♡～"""
    
    def __init__(self):
        self.registry = get_global_registry()
        # 杂鱼♡～转换路径栈，用于调试和错误追踪喵～
        self._conversion_path: List[str] = []
        # 杂鱼♡～转换器加载标志喵～
        self._converters_loaded = False

    def _ensure_converters_loaded(self):
        """杂鱼♡～确保所有转换器都已加载喵～"""
        if not self._converters_loaded:
            try:
                # 杂鱼♡～调用转换器注册函数喵～
                from ..converters import initialize_converters
                initialize_converters()
                self._converters_loaded = True
            except ImportError as e:
                raise ConversionError(f"杂鱼♡～无法加载转换器喵：{str(e)}") from e

    def _execute_conversion(
        self,
        conversion_logic: Callable,
        error_message_template: str,
        field_path: str,
        actual_value: Any,
        expected_type: Any = None,
    ):
        """杂鱼♡～本喵把重复的try-except都包在这里了，真是天才喵～"""
        try:
            return conversion_logic()
        except Exception as e:
            if isinstance(e, ConversionError):
                raise
            
            error_message = error_message_template.format(field_path=field_path, error=str(e))
            raise ConversionError(
                message=error_message,
                field_path=field_path,
                expected_type=expected_type,
                actual_value=actual_value
            ) from e

    def get_conversion_path(self) -> List[str]:
        """杂鱼♡～获取当前转换路径喵～用于调试～"""
        return self._conversion_path.copy()


class Deserializer(_BaseCoordinator):
    """杂鱼♡～这是反序列化器喵～把字典变成dataclass♡～"""
    
    def __init__(self):
        super().__init__()
        self.recursive_converter = get_recursive_converter()
        # 哼～本喵用字典来做分派，比你那堆if/else优雅多了喵～♡
        self._dispatch_table = {
            ConverterType.BASIC: self._delegate_to_converter,
            ConverterType.CONTAINER: self._delegate_to_converter,
            ConverterType.SPECIAL: self._delegate_to_converter,
            ConverterType.UNION: self._delegate_to_converter,
            ConverterType.DATACLASS: self._convert_nested_dataclass,
        }

    def convert(self, data: Dict[str, Any], target_type: Type) -> Any:
        """杂鱼♡～从字典数据转换为目标类型喵～"""
        if not is_dataclass(target_type):
            raise SchemaError(f"杂鱼♡～只能转换到dataclass类型喵！～得到: {target_type}")
        
        if not isinstance(data, dict):
            raise ConversionError(f"杂鱼♡～输入数据必须是字典类型喵！～得到: {type(data)}")
        
        try:
            self._ensure_converters_loaded()
            schema = build_schema(target_type)
            self._conversion_path.clear()
            return self._convert_dataclass_from_dict(data, schema, target_type.__name__)
        except Exception as e:
            if isinstance(e, (ConversionError, SchemaError)):
                raise
            raise ConversionError(f"杂鱼♡～转换过程中出现未知错误喵：{str(e)}") from e

    def _convert_dataclass_from_dict(self, data: Dict[str, Any], schema: TypeSchema, context_name: str) -> Any:
        self._conversion_path.append(f"dataclass:{context_name}")
        
        try:
            target_type = schema.root_type
            converted_fields = {}
            
            for field_name, field_schema in schema.field_schemas.items():
                field_path = f"{context_name}.{field_name}"
                
                if field_name not in data:
                    if field_schema.is_optional:
                        converted_fields[field_name] = None
                        continue
                    else:
                        from dataclasses import fields
                        dataclass_fields = {f.name: f for f in fields(target_type)}
                        if field_name in dataclass_fields:
                            field_def = dataclass_fields[field_name]
                            if field_def.default is not field_def.default_factory or \
                               field_def.default_factory is not field_def.default_factory.__class__():
                                continue
                        
                        raise ConversionError(f"杂鱼♡～必需字段缺失喵：{field_path}", field_path=field_path, expected_type=field_schema.exact_type)
                
                field_value = data[field_name]
                
                if field_value is None:
                    if field_schema.is_optional or field_schema.exact_type is type(None):
                        converted_fields[field_name] = None
                        continue
                    else:
                        raise ConversionError(f"杂鱼♡～非可选字段不能为None喵：{field_path}", field_path=field_path, expected_type=field_schema.exact_type)
                
                converted_fields[field_name] = self._convert_field_value(field_value, field_schema, field_path)
            
            return target_type(**converted_fields)
        finally:
            self._conversion_path.pop()

    def _convert_field_value(self, value: Any, field_schema: FieldSchema, field_path: str) -> Any:
        handler = self._dispatch_table.get(field_schema.converter_type)
        if handler is None:
            raise ConversionError(f"杂鱼♡～不支持的转换器类型喵：{field_schema.converter_type}", field_path=field_path)
        return handler(value, field_schema, field_path)

    def _delegate_to_converter(self, value: Any, field_schema: FieldSchema, field_path: str) -> Any:
        """杂鱼♡～本喵把所有相似的转换都交给这个函数了喵～哼～"""
        converter_type = field_schema.converter_type
        # 杂鱼♡～本喵动态生成错误信息，厉害吧～
        error_template = f"杂鱼♡～{converter_type.name.capitalize()}类型转换失败喵：{{field_path}} - {{error}}"
        
        return self._execute_conversion(
            lambda: self.registry.get_converter(field_schema.exact_type, converter_type).convert(value, field_schema),
            error_template,
            field_path, value, field_schema.exact_type)

    def _convert_nested_dataclass(self, value: Any, field_schema: FieldSchema, field_path: str) -> Any:
        if not isinstance(value, dict):
            raise ConversionError(f"杂鱼♡～嵌套dataclass需要字典数据喵：{field_path}", field_path=field_path, expected_type=dict, actual_value=value)
        
        sub_schema = field_schema.sub_schema
        if sub_schema is None or not sub_schema.field_schemas:
            sub_schema = build_schema(field_schema.exact_type)
        
        return self._convert_dataclass_from_dict(value, sub_schema, field_path)


class Serializer(_BaseCoordinator):
    """杂鱼♡～这是序列化器喵～把dataclass变成字典♡～"""
    
    def __init__(self):
        super().__init__()
        # 杂鱼♡～循环引用检测，记录正在转换的对象喵～
        self._converting_objects: Set[int] = set()
        # 哼～序列化也有自己的分派表喵～♡
        self._dispatch_table = {
            ConverterType.BASIC: self._convert_basic_type_to_dict,
            ConverterType.CONTAINER: self._convert_container_type_to_dict,
            ConverterType.SPECIAL: self._convert_special_type_to_dict,
            ConverterType.DATACLASS: self._convert_nested_dataclass_to_dict,
            ConverterType.UNION: self._convert_union_type_to_dict,
        }

    def convert(self, obj: Any) -> Dict[str, Any]:
        """杂鱼♡～将对象转换为字典数据喵～"""
        if obj is None:
            raise ConversionError("杂鱼♡～不能转换None值喵！～")
        
        if not is_dataclass(obj):
            raise SchemaError(f"杂鱼♡～只能转换dataclass实例喵！～得到: {type(obj)}")
        
        try:
            self._ensure_converters_loaded()
            schema = build_schema(type(obj))
            self._conversion_path.clear()
            self._converting_objects.clear()
            return self._convert_dataclass_to_dict(obj, schema, type(obj).__name__)
        except Exception as e:
            if isinstance(e, (ConversionError, SchemaError)):
                raise
            raise ConversionError(f"杂鱼♡～转换过程中出现未知错误喵：{str(e)}") from e

    def _convert_dataclass_to_dict(self, obj: Any, schema: TypeSchema, context_name: str) -> Dict[str, Any]:
        self._conversion_path.append(f"dataclass_to_dict:{context_name}")
        
        obj_id = id(obj)
        if obj_id in self._converting_objects:
            return {"__circular_ref__": True, "__type__": obj.__class__.__name__, "__id__": obj_id}
        
        self._converting_objects.add(obj_id)
        
        try:
            result = {}
            for field_name, field_schema in schema.field_schemas.items():
                field_path = f"{context_name}.{field_name}"
                if hasattr(obj, field_name):
                    field_value = getattr(obj, field_name)
                    if field_value is None:
                        result[field_name] = None
                        continue
                    result[field_name] = self._convert_field_value_to_dict(field_value, field_schema, field_path)
            return result
        finally:
            self._converting_objects.discard(obj_id)
            self._conversion_path.pop()

    def _convert_field_value_to_dict(self, value: Any, field_schema: FieldSchema, field_path: str) -> Any:
        handler = self._dispatch_table.get(field_schema.converter_type)
        if handler is None:
            raise ConversionError(f"杂鱼♡～不支持的转换器类型喵：{field_schema.converter_type}", field_path=field_path)
        return handler(value, field_schema, field_path)

    def _convert_basic_type_to_dict(self, value: Any, field_schema: FieldSchema, field_path: str) -> Any:
        def logic():
            if isinstance(value, (str, int, float, bool, type(None))):
                return value
            return str(value)
        return self._execute_conversion(logic, "杂鱼♡～基本类型序列化失败喵：{field_path} - {error}", field_path, value)

    def _convert_container_type_to_dict(self, value: Any, field_schema: FieldSchema, field_path: str) -> Any:
        return self._execute_conversion(
            lambda: self.registry.get_converter(field_schema.exact_type, ConverterType.CONTAINER).convert_to_dict(value, field_schema, self),
            "杂鱼♡～容器类型序列化失败喵：{field_path} - {error}",
            field_path, value)

    def _convert_special_type_to_dict(self, value: Any, field_schema: FieldSchema, field_path: str) -> Any:
        def logic():
            converter = self.registry.get_converter(field_schema.exact_type, ConverterType.SPECIAL)
            return converter.convert_to_dict(value, field_schema) if hasattr(converter, 'convert_to_dict') else str(value)
        return self._execute_conversion(logic, "杂鱼♡～特殊类型序列化失败喵：{field_path} - {error}", field_path, value)

    def _convert_union_type_to_dict(self, value: Any, field_schema: FieldSchema, field_path: str) -> Any:
        def logic():
            converter = self.registry.get_converter(field_schema.exact_type, ConverterType.UNION)
            if hasattr(converter, 'convert_to_dict'):
                return converter.convert_to_dict(value, field_schema)
            
            from ..schema.type_analyzer import TypeAnalyzer
            analysis = TypeAnalyzer().analyze_type(type(value))
            temp_schema = FieldSchema(field_path, type(value), analysis['converter_type'], False, [])
            return self._convert_field_value_to_dict(value, temp_schema, field_path)

        return self._execute_conversion(logic, "杂鱼♡～Union类型序列化失败喵：{field_path} - {error}", field_path, value)

    def _convert_nested_dataclass_to_dict(self, value: Any, field_schema: FieldSchema, field_path: str) -> Any:
        obj_id = id(value)
        if obj_id in self._converting_objects:
            return {"__circular_ref__": True, "__type__": value.__class__.__name__, "__id__": obj_id}
        
        sub_schema = field_schema.sub_schema if field_schema.sub_schema else build_schema(type(value))
        return self._convert_dataclass_to_dict(value, sub_schema, field_path)


# 杂鱼♡～全局转换协调器实例喵～
_deserializer = Deserializer()
_serializer = Serializer()


def convert_from_dict(data: Dict[str, Any], target_type: Type) -> Any:
    """杂鱼♡～从字典转换为目标类型喵～"""
    return _deserializer.convert(data, target_type)


def convert_to_dict(obj: Any) -> Dict[str, Any]:
    """杂鱼♡～将对象转换为字典喵～"""
    return _serializer.convert(obj) 