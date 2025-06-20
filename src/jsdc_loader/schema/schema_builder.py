"""杂鱼♡～这是本喵的Schema构建器喵～能构建超级复杂的TypeSchema♡～"""

from dataclasses import is_dataclass, fields
from typing import Any, Dict, List, Set, Type, Optional
import hashlib

from .field_schema import FieldSchema, TypeSchema, ConverterType
from .type_analyzer import TypeAnalyzer
from ..api.exceptions import SchemaError

# 杂鱼♡～导入配置系统喵～
try:
    from ..api.config import get_field_config, get_dataclass_config, transform_field_name, LetterCase
except ImportError:
    # 杂鱼♡～如果config还没创建，提供兜底喵～
    def get_field_config(metadata): return {}
    def get_dataclass_config(cls): return {}
    def transform_field_name(name, case): return name
    class LetterCase: SNAKE = "snake_case"

# 杂鱼♡～ForwardRef处理喵～
try:
    from typing import ForwardRef
except ImportError:
    ForwardRef = None

try:
    from typing import _ForwardRef
except ImportError:
    _ForwardRef = None

ForwardRefType = ForwardRef or _ForwardRef


class SchemaBuilder:
    """杂鱼♡～Schema构建器喵～构建完整的类型Schema♡～"""
    
    def __init__(self):
        self.type_analyzer = TypeAnalyzer()
        # 杂鱼♡～缓存已构建的schema，避免重复构建和循环引用喵～
        self._schema_cache: Dict[str, TypeSchema] = {}
        # 杂鱼♡～跟踪正在构建的类型，防止无限递归喵～
        self._building_types: Set[Type] = set()
        # 杂鱼♡～ForwardRef解析缓存喵～
        self._forward_ref_cache: Dict[str, Type] = {}
    
    def build_schema(self, target_type: Type) -> TypeSchema:
        """杂鱼♡～构建目标类型的完整Schema喵～
        
        Args:
            target_type: 目标类型
            
        Returns:
            TypeSchema: 完整的类型Schema
            
        Raises:
            SchemaError: Schema构建失败时
        """
        # 杂鱼♡～检查是否是dataclass或泛型dataclass喵～
        from typing import get_origin
        origin = get_origin(target_type)
        if not (is_dataclass(target_type) or (origin and is_dataclass(origin))):
            raise SchemaError(f"杂鱼♡～只能为dataclass类型构建Schema喵！～得到: {target_type}")
        
        # 杂鱼♡～生成缓存键值喵～
        cache_key = self._generate_cache_key(target_type)
        
        if cache_key in self._schema_cache:
            return self._schema_cache[cache_key]
        
        # 杂鱼♡～检查循环引用喵～
        if target_type in self._building_types:
            # 杂鱼♡～创建一个简单的引用Schema避免无限递归喵～
            return TypeSchema(
                root_type=target_type,
                field_schemas={},
                cache_key=cache_key
            )
        
        try:
            self._building_types.add(target_type)
            schema = self._build_schema_recursive(target_type, cache_key)
            self._schema_cache[cache_key] = schema
            return schema
        finally:
            self._building_types.discard(target_type)
    
    def _build_schema_recursive(self, target_type: Type, cache_key: str) -> TypeSchema:
        """杂鱼♡～递归构建Schema喵～"""
        field_schemas: Dict[str, FieldSchema] = {}
        
        # 杂鱼♡～提取类级别配置喵～
        dataclass_config = get_dataclass_config(target_type)
        global_letter_case = dataclass_config.get("letter_case")
        unhandled_keys = dataclass_config.get("unhandled_keys", "exclude")
        exclude_none = dataclass_config.get("exclude_none", False)
        validate_schema = dataclass_config.get("validate_schema", False)
        
        # 杂鱼♡～获取dataclass的所有字段喵～
        dataclass_fields = fields(target_type)
        
        for field in dataclass_fields:
            field_name = field.name
            field_type = field.type
            field_metadata = field.metadata
            
            # 杂鱼♡～提取字段级配置喵～
            field_config = get_field_config(field_metadata)
            
            # 杂鱼♡～确定JSON字段名喵～
            json_field_name = field_config.get("field_name")
            if not json_field_name and global_letter_case:
                json_field_name = transform_field_name(field_name, global_letter_case)
            elif field_config.get("letter_case"):
                json_field_name = transform_field_name(field_name, field_config["letter_case"])
            
            field_path = field_name  # 杂鱼♡～根路径就是字段名喵～
            field_schema = self._build_field_schema(
                field_path, field_type, field_config, json_field_name, exclude_none
            )
            field_schemas[field_path] = field_schema
        
        return TypeSchema(
            root_type=target_type,
            field_schemas=field_schemas,
            cache_key=cache_key,
            global_letter_case=global_letter_case.value if global_letter_case else None,
            unhandled_keys_strategy=unhandled_keys.value if hasattr(unhandled_keys, 'value') else str(unhandled_keys),
            exclude_none_globally=exclude_none,
            validate_schema=validate_schema
        )
    
    def _build_field_schema(
        self, 
        field_path: str, 
        field_type: Type, 
        field_config: Dict[str, Any],
        json_field_name: Optional[str],
        global_exclude_none: bool
    ) -> FieldSchema:
        """杂鱼♡～构建单个字段的Schema喵～
        
        Args:
            field_path: 字段路径，如 "user.profile.bio"
            field_type: 字段类型
            field_config: 字段配置字典
            json_field_name: JSON中的字段名
            global_exclude_none: 全局排除None设置
            
        Returns:
            FieldSchema: 字段Schema
        """
        # 杂鱼♡～分析字段类型喵～
        type_analysis = self.type_analyzer.analyze_type(field_type)
        
        converter_type = type_analysis['converter_type']
        is_optional = type_analysis['is_optional']
        origin_type = type_analysis['origin_type']
        
        # 杂鱼♡～处理Union类型喵～
        union_types = None
        if type_analysis['is_union']:
            union_types = [elem['origin_type'] for elem in type_analysis['element_types']]
        
        # 杂鱼♡～处理嵌套dataclass喵～
        sub_schema = None
        if converter_type == ConverterType.DATACLASS:
            # 杂鱼♡～对于泛型dataclass，需要使用完整的类型信息喵～
            schema_type = field_type if type_analysis.get('type_args') else origin_type
            if origin_type not in self._building_types:  # 杂鱼♡～避免循环引用喵～
                sub_schema = self.build_schema(schema_type)
        
        # 杂鱼♡～处理容器类型的元素Schema喵～
        elif converter_type == ConverterType.CONTAINER:
            sub_schema = self._build_container_sub_schema(field_path, type_analysis)
        
        # 杂鱼♡～提取自定义编码器和解码器喵～
        custom_encoder = field_config.get("encoder")
        custom_decoder = field_config.get("decoder")
        
        # 杂鱼♡～处理排除选项喵～
        exclude_if_none = field_config.get("exclude_if_none", global_exclude_none)
        exclude_if_default = field_config.get("exclude_if_default", False)
        
        return FieldSchema(
            field_path=field_path,
            exact_type=origin_type,  # 杂鱼♡～使用解析后的基础类型，而不是原始类型喵～
            converter_type=converter_type,
            sub_schema=sub_schema,
            is_optional=is_optional,
            union_types=union_types,
            # 杂鱼♡～新增的配置字段喵～
            custom_encoder=custom_encoder,
            custom_decoder=custom_decoder,
            json_field_name=json_field_name,
            exclude_if_none=exclude_if_none,
            exclude_if_default=exclude_if_default,
            description=field_config.get("description"),
            examples=field_config.get("examples")
        )
    
    def _build_container_sub_schema(self, field_path: str, type_analysis: Dict[str, Any]) -> TypeSchema:
        """杂鱼♡～构建容器类型的子Schema喵～"""
        origin_type = type_analysis['origin_type']
        element_types = type_analysis['element_types']
        
        field_schemas: Dict[str, FieldSchema] = {}
        
        # 杂鱼♡～根据容器类型构建不同的子Schema喵～
        if origin_type == dict:
            # 杂鱼♡～Dict[K, V] - 键和值都需要Schema喵～
            if len(element_types) >= 2:
                key_schema = self._build_element_schema(f"{field_path}.<key>", element_types[0])
                value_schema = self._build_element_schema(f"{field_path}.<value>", element_types[1])
                field_schemas[f"{field_path}.<key>"] = key_schema
                field_schemas[f"{field_path}.<value>"] = value_schema
        
        elif origin_type in (list, set, frozenset):
            # 杂鱼♡～List[T], Set[T], FrozenSet[T] - 只有元素类型喵～
            if element_types:
                element_schema = self._build_element_schema(f"{field_path}.<item>", element_types[0])
                field_schemas[f"{field_path}.<item>"] = element_schema
        
        elif origin_type == tuple:
            # 杂鱼♡～Tuple[T1, T2, T3]或Tuple[T, ...]喵～
            if element_types:
                if len(element_types) == 1:
                    # Tuple[T, ...] - 可变长度
                    element_schema = self._build_element_schema(f"{field_path}.<item>", element_types[0])
                    field_schemas[f"{field_path}.<item>"] = element_schema
                else:
                    # Tuple[T1, T2, T3] - 固定长度
                    for i, elem_analysis in enumerate(element_types):
                        element_schema = self._build_element_schema(f"{field_path}.<{i}>", elem_analysis)
                        field_schemas[f"{field_path}.<{i}>"] = element_schema
        
        from collections import deque
        if origin_type == deque:
            # 杂鱼♡～Deque[T]喵～
            if element_types:
                element_schema = self._build_element_schema(f"{field_path}.<item>", element_types[0])
                field_schemas[f"{field_path}.<item>"] = element_schema
        
        return TypeSchema(
            root_type=origin_type,
            field_schemas=field_schemas,
            cache_key=f"container_{origin_type.__name__}_{hash(str(element_types))}"
        )
    
    def _build_element_schema(self, element_path: str, element_analysis: Dict[str, Any]) -> FieldSchema:
        """杂鱼♡～构建容器元素的Schema喵～
        
        Args:
            element_path: 元素路径
            element_analysis: 元素类型分析结果（可以是类型或分析字典）
            
        Returns:
            FieldSchema: 元素Schema
        """
        # 杂鱼♡～如果element_analysis是分析结果字典喵～
        if isinstance(element_analysis, dict):
            type_analysis = element_analysis
            element_type = type_analysis['origin_type']
        else:
            # 杂鱼♡～如果element_analysis是类型，需要重新分析喵～
            element_type = element_analysis
            type_analysis = self.type_analyzer.analyze_type(element_type)
        
        # 杂鱼♡～特殊处理ForwardRef喵～
        if ForwardRefType and isinstance(element_type, ForwardRefType):
            resolved_type = self._resolve_forward_ref(element_type)
            if resolved_type is not None:
                element_type = resolved_type
                type_analysis = self.type_analyzer.analyze_type(element_type)
            else:
                # 杂鱼♡～无法解析ForwardRef，但可能在type_analysis中已解析喵～
                converter_type = type_analysis['converter_type']
                if converter_type == ConverterType.SPECIAL:
                    # 杂鱼♡～再次尝试解析，使用字符串查找喵～
                    if hasattr(element_type, '__forward_arg__'):
                        ref_string = element_type.__forward_arg__
                    elif hasattr(element_type, 'arg'):
                        ref_string = element_type.arg
                    else:
                        ref_string = str(element_type)
                    
                    # 杂鱼♡～直接从__main__模块查找喵～
                    try:
                        import sys
                        if '__main__' in sys.modules:
                            main_module = sys.modules['__main__']
                            if hasattr(main_module, ref_string):
                                resolved_type = getattr(main_module, ref_string)
                                if isinstance(resolved_type, type) and is_dataclass(resolved_type):
                                    element_type = resolved_type
                                    type_analysis = self.type_analyzer.analyze_type(element_type)
                    except Exception:
                        pass
        
        converter_type = type_analysis['converter_type']
        is_optional = type_analysis['is_optional']
        
        # 杂鱼♡～处理嵌套dataclass喵～
        sub_schema = None
        if converter_type == ConverterType.DATACLASS:
            if element_type not in self._building_types:
                # 杂鱼♡～这里element_type已经是完整的类型了，直接使用喵～
                sub_schema = self.build_schema(element_type)
            else:
                # 杂鱼♡～循环引用情况，延迟解析，在运行时动态构建schema喵～
                # 杂鱼♡～这里不创建空schema，而是设为None，让coordinator动态处理喵～
                sub_schema = None
        
        # 杂鱼♡～处理嵌套容器喵～
        elif converter_type == ConverterType.CONTAINER:
            sub_schema = self._build_container_sub_schema(element_path, type_analysis)
        
        # 杂鱼♡～处理Union类型喵～
        union_types = None
        if type_analysis['is_union']:
            union_types = [elem['origin_type'] for elem in type_analysis['element_types']]
        
        return FieldSchema(
            field_path=element_path,
            exact_type=element_type,
            converter_type=converter_type,
            sub_schema=sub_schema,
            is_optional=is_optional,
            union_types=union_types
        )
    
    def _resolve_forward_ref(self, forward_ref: ForwardRefType) -> Type:
        """杂鱼♡～解析ForwardRef喵～
        
        Args:
            forward_ref: ForwardRef实例
            
        Returns:
            Type: 解析后的类型，如果解析失败返回None
        """
        # 杂鱼♡～获取ForwardRef的字符串表示喵～
        if hasattr(forward_ref, '__forward_arg__'):
            ref_string = forward_ref.__forward_arg__
        elif hasattr(forward_ref, 'arg'):
            ref_string = forward_ref.arg
        else:
            ref_string = str(forward_ref)
        
        # 杂鱼♡～从缓存获取喵～
        if ref_string in self._forward_ref_cache:
            return self._forward_ref_cache[ref_string]
        
        # 杂鱼♡～方法1：直接从__main__模块查找喵～
        try:
            import sys
            if '__main__' in sys.modules:
                main_module = sys.modules['__main__']
                if hasattr(main_module, ref_string):
                    resolved_type = getattr(main_module, ref_string)
                    if isinstance(resolved_type, type) and is_dataclass(resolved_type):
                        self._forward_ref_cache[ref_string] = resolved_type
                        return resolved_type
        except Exception:
            pass
        
        # 杂鱼♡～方法2：从调用栈中的globals解析喵～
        try:
            import inspect
            frame = inspect.currentframe()
            
            for _ in range(20):  # 杂鱼♡～向上查找更多层喵～
                frame = frame.f_back
                if frame is None:
                    break
                
                globals_dict = frame.f_globals
                
                # 杂鱼♡～在globals中查找类型喵～
                if ref_string in globals_dict:
                    resolved_type = globals_dict[ref_string]
                    if isinstance(resolved_type, type) and is_dataclass(resolved_type):
                        self._forward_ref_cache[ref_string] = resolved_type
                        return resolved_type
        except Exception:
            pass
        
        # 杂鱼♡～方法3：尝试使用eval在当前命名空间中解析喵～
        try:
            import sys
            # 杂鱼♡～收集所有可能的命名空间喵～
            namespaces = []
            
            # 杂鱼♡～添加__main__命名空间喵～
            if '__main__' in sys.modules:
                namespaces.append(sys.modules['__main__'].__dict__)
            
            # 杂鱼♡～添加当前模块命名空间喵～
            import inspect
            frame = inspect.currentframe()
            for _ in range(15):
                frame = frame.f_back
                if frame is None:
                    break
                namespaces.append(frame.f_globals)
            
            # 杂鱼♡～在每个命名空间中尝试解析喵～
            for namespace in namespaces:
                try:
                    resolved_type = eval(ref_string, namespace)
                    if isinstance(resolved_type, type) and is_dataclass(resolved_type):
                        self._forward_ref_cache[ref_string] = resolved_type
                        return resolved_type
                except:
                    continue
                    
        except Exception:
            pass
        
        # 杂鱼♡～方法4：尝试使用typing.get_type_hints强制解析喵～
        try:
            import typing
            import sys
            
            # 杂鱼♡～尝试在__main__模块的上下文中解析喵～
            if '__main__' in sys.modules:
                main_module = sys.modules['__main__']
                main_globals = main_module.__dict__
                
                # 杂鱼♡～创建一个包含ForwardRef的虚拟类型来强制解析喵～
                try:
                    if hasattr(forward_ref, '_evaluate'):
                        resolved_type = forward_ref._evaluate(main_globals, main_globals, set())
                    elif hasattr(forward_ref, '_eval_type'):
                        resolved_type = forward_ref._eval_type(main_globals, main_globals)
                    else:
                        # 杂鱼♡～fallback到直接查找喵～
                        resolved_type = main_globals.get(ref_string)
                    
                    if resolved_type and isinstance(resolved_type, type) and is_dataclass(resolved_type):
                        self._forward_ref_cache[ref_string] = resolved_type
                        return resolved_type
                except:
                    pass
                    
        except Exception:
            pass
        
        # 杂鱼♡～方法5：简单策略，在当前构建的类型中查找喵～
        for building_type in self._building_types:
            if building_type.__name__ == ref_string:
                self._forward_ref_cache[ref_string] = building_type
                return building_type
        
        # 杂鱼♡～方法6：扫描所有已知的dataclass类型喵～
        try:
            import gc
            for obj in gc.get_objects():
                if (isinstance(obj, type) and 
                    is_dataclass(obj) and 
                    obj.__name__ == ref_string):
                    self._forward_ref_cache[ref_string] = obj
                    return obj
        except Exception:
            pass
        
        return None
    
    def _generate_cache_key(self, target_type: Type) -> str:
        """杂鱼♡～生成Schema的缓存键值喵～"""
        type_str = f"{target_type.__module__}.{target_type.__qualname__}"
        return hashlib.md5(type_str.encode()).hexdigest()[:12]


# 杂鱼♡～全局Schema构建器实例喵～
_global_builder = SchemaBuilder()


def build_schema(target_type: Type) -> TypeSchema:
    """杂鱼♡～构建目标类型的Schema喵～
    
    Args:
        target_type: 目标dataclass类型
        
    Returns:
        TypeSchema: 构建的Schema
    """
    return _global_builder.build_schema(target_type)


def get_schema_builder() -> SchemaBuilder:
    """杂鱼♡～获取全局Schema构建器喵～"""
    return _global_builder 