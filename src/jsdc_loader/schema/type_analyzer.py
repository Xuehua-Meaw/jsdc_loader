"""杂鱼♡～这是本喵的类型分析器喵～能分析各种复杂的typing注解♡～"""

import sys
from dataclasses import is_dataclass, fields
from typing import Any, Dict, List, Optional, Set, Type, Union, get_args, get_origin
from enum import Enum

from .field_schema import ConverterType

# 杂鱼♡～Python版本兼容性处理喵～
if sys.version_info >= (3, 10):
    import types
    UnionType = types.UnionType
else:
    UnionType = None

# 杂鱼♡～尝试导入新版本的typing特性喵～
try:
    from typing import Literal, TypeVar, Generic, Annotated, ForwardRef
except ImportError:
    Literal = None
    TypeVar = None
    Generic = None
    Annotated = None
    ForwardRef = None

# 杂鱼♡～Python 3.7+兼容性处理喵～
try:
    from typing import _ForwardRef
except ImportError:
    _ForwardRef = None

# 杂鱼♡～确定ForwardRef类型喵～
ForwardRefType = ForwardRef or _ForwardRef


class TypeAnalyzer:
    """杂鱼♡～类型分析器喵～分析各种复杂的类型注解♡～"""
    
    def __init__(self):
        # 杂鱼♡～缓存分析结果，避免重复计算喵～
        self._analysis_cache: Dict[Type, Dict[str, Any]] = {}
        # 杂鱼♡～ForwardRef解析缓存喵～
        self._forward_ref_cache: Dict[str, Type] = {}
    
    def analyze_type(self, target_type: Type) -> Dict[str, Any]:
        """杂鱼♡～分析类型并返回详细信息喵～
        
        Args:
            target_type: 要分析的类型
            
        Returns:
            Dict[str, Any]: 类型分析结果
        """
        if target_type in self._analysis_cache:
            return self._analysis_cache[target_type]
        
        result = self._do_analyze_type(target_type)
        self._analysis_cache[target_type] = result
        return result
    
    def _do_analyze_type(self, target_type: Type) -> Dict[str, Any]:
        """杂鱼♡～执行实际的类型分析喵～"""
        origin = get_origin(target_type)
        args = get_args(target_type)
        
        # 杂鱼♡～处理ForwardRef类型喵～
        if ForwardRefType and isinstance(target_type, ForwardRefType):
            return self._analyze_forward_ref(target_type)
        
        # 杂鱼♡～处理基本类型喵～
        if target_type in (str, int, float, bool):
            return {
                'converter_type': ConverterType.BASIC,
                'is_container': False,
                'is_optional': False,
                'is_union': False,
                'element_types': [],
                'origin_type': target_type,
                'type_args': []
            }
        
        # 杂鱼♡～处理None类型喵～
        if target_type is type(None):
            return {
                'converter_type': ConverterType.BASIC,
                'is_container': False,
                'is_optional': True,
                'is_union': False,
                'element_types': [],
                'origin_type': target_type,
                'type_args': []
            }
        
        # 杂鱼♡～处理泛型dataclass类型喵～（如GenericContainer[Dict[str, Any]]）
        if origin and is_dataclass(origin):
            return {
                'converter_type': ConverterType.DATACLASS,
                'is_container': False,
                'is_optional': False,
                'is_union': False,
                'element_types': [self.analyze_type(arg) for arg in args] if args else [],
                'origin_type': origin,
                'type_args': args
            }
        
        # 杂鱼♡～处理普通dataclass类型喵～
        if is_dataclass(target_type):
            return {
                'converter_type': ConverterType.DATACLASS,
                'is_container': False,
                'is_optional': False,
                'is_union': False,
                'element_types': [],
                'origin_type': target_type,
                'type_args': []
            }
        
        # 杂鱼♡～处理Enum类型喵～
        if isinstance(target_type, type) and issubclass(target_type, Enum):
            return {
                'converter_type': ConverterType.SPECIAL,
                'is_container': False,
                'is_optional': False,
                'is_union': False,
                'element_types': [],
                'origin_type': target_type,
                'type_args': []
            }
        
        # 杂鱼♡～处理Union类型（包括Optional）喵～
        is_union_type = (origin is Union or 
                        (UnionType and isinstance(target_type, UnionType)))
        
        if is_union_type:
            # 杂鱼♡～检查是否是Optional（Union[T, None]）喵～
            if len(args) == 2 and type(None) in args:
                non_none_type = args[0] if args[1] is type(None) else args[1]
                result = self.analyze_type(non_none_type)
                result['is_optional'] = True
                return result
            else:
                # 杂鱼♡～真正的Union类型喵～
                return {
                    'converter_type': ConverterType.UNION,
                    'is_container': False,
                    'is_optional': type(None) in args,
                    'is_union': True,
                    'element_types': [self.analyze_type(arg) for arg in args if arg is not type(None)],
                    'origin_type': target_type,
                    'type_args': args
                }
        
        # 杂鱼♡～处理容器类型喵～
        if origin in (list, List):
            return {
                'converter_type': ConverterType.CONTAINER,
                'is_container': True,
                'is_optional': False,
                'is_union': False,
                'element_types': [self.analyze_type(args[0])] if args else [],
                'origin_type': list,
                'type_args': args
            }
        
        if origin in (dict, Dict):
            element_types = []
            if args:
                if len(args) >= 2:
                    element_types = [self.analyze_type(args[0]), self.analyze_type(args[1])]
                else:
                    element_types = [self.analyze_type(args[0])]
            return {
                'converter_type': ConverterType.CONTAINER,
                'is_container': True,
                'is_optional': False,
                'is_union': False,
                'element_types': element_types,
                'origin_type': dict,
                'type_args': args
            }
        
        if origin in (set, Set):
            return {
                'converter_type': ConverterType.CONTAINER,
                'is_container': True,
                'is_optional': False,
                'is_union': False,
                'element_types': [self.analyze_type(args[0])] if args else [],
                'origin_type': set,
                'type_args': args
            }
        
        if origin in (frozenset, frozenset if hasattr(__builtins__, 'frozenset') else type(frozenset())):
            return {
                'converter_type': ConverterType.CONTAINER,
                'is_container': True,
                'is_optional': False,
                'is_union': False,
                'element_types': [self.analyze_type(args[0])] if args else [],
                'origin_type': frozenset,
                'type_args': args
            }
        
        if origin in (tuple, tuple):
            element_types = []
            if args:
                # 杂鱼♡～处理Tuple[T, ...]或Tuple[T1, T2, T3]喵～
                if len(args) == 2 and args[1] is ...:
                    # Tuple[T, ...] - 可变长度tuple
                    element_types = [self.analyze_type(args[0])]
                else:
                    # Tuple[T1, T2, T3] - 固定长度tuple
                    element_types = [self.analyze_type(arg) for arg in args]
            return {
                'converter_type': ConverterType.CONTAINER,
                'is_container': True,
                'is_optional': False,
                'is_union': False,
                'element_types': element_types,
                'origin_type': tuple,
                'type_args': args
            }
        
        # 杂鱼♡～处理deque类型喵～
        from collections import deque
        if origin is deque:
            return {
                'converter_type': ConverterType.CONTAINER,
                'is_container': True,
                'is_optional': False,
                'is_union': False,
                'element_types': [self.analyze_type(args[0])] if args else [],
                'origin_type': deque,
                'type_args': args
            }
        
        # 杂鱼♡～处理Literal类型喵～
        if Literal and origin is Literal:
            return {
                'converter_type': ConverterType.SPECIAL,
                'is_container': False,
                'is_optional': False,
                'is_union': False,
                'element_types': [],
                'origin_type': target_type,
                'type_args': args,
                'literal_values': args
            }
        
        # 杂鱼♡～处理特殊类型喵～
        import uuid
        import datetime
        from decimal import Decimal
        
        special_types = {
            uuid.UUID, datetime.datetime, datetime.date, datetime.time, 
            datetime.timedelta, Decimal, bytes, bytearray
        }
        
        if target_type in special_types:
            return {
                'converter_type': ConverterType.SPECIAL,
                'is_container': False,
                'is_optional': False,
                'is_union': False,
                'element_types': [],
                'origin_type': target_type,
                'type_args': []
            }
        

        
        # 杂鱼♡～其他情况，尝试按特殊类型处理喵～
        return {
            'converter_type': ConverterType.SPECIAL,
            'is_container': False,
            'is_optional': False,
            'is_union': False,
            'element_types': [],
            'origin_type': target_type,
            'type_args': args or []
        }
    
    def _analyze_forward_ref(self, forward_ref: ForwardRefType) -> Dict[str, Any]:
        """杂鱼♡～分析ForwardRef类型喵～
        
        Args:
            forward_ref: ForwardRef实例
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        # 杂鱼♡～获取ForwardRef的字符串表示喵～
        if hasattr(forward_ref, '__forward_arg__'):
            ref_string = forward_ref.__forward_arg__
        elif hasattr(forward_ref, 'arg'):
            ref_string = forward_ref.arg
        else:
            ref_string = str(forward_ref)
        
        # 杂鱼♡～尝试从缓存获取已解析的类型喵～
        if ref_string in self._forward_ref_cache:
            resolved_type = self._forward_ref_cache[ref_string]
            return self.analyze_type(resolved_type)
        
        # 杂鱼♡～使用增强的ForwardRef解析逻辑喵～
        resolved_type = self._resolve_forward_ref_enhanced(forward_ref, ref_string)
        if resolved_type is not None:
            self._forward_ref_cache[ref_string] = resolved_type
            return self.analyze_type(resolved_type)
        
        # 杂鱼♡～如果无法解析，按特殊类型处理但记录警告喵～
        print(f"杂鱼♡～警告：无法解析ForwardRef '{ref_string}'，按特殊类型处理喵～")
        return {
            'converter_type': ConverterType.SPECIAL,
            'is_container': False,
            'is_optional': False,
            'is_union': False,
            'element_types': [],
            'origin_type': forward_ref,
            'type_args': []
        }
    
    def _resolve_forward_ref_enhanced(self, forward_ref: ForwardRefType, ref_string: str) -> Type:
        """杂鱼♡～增强的ForwardRef解析喵～
        
        Args:
            forward_ref: ForwardRef实例
            ref_string: 引用字符串
            
        Returns:
            Type: 解析后的类型，如果解析失败返回None
        """
        # 杂鱼♡～方法1：直接从__main__模块查找喵～
        try:
            import sys
            if '__main__' in sys.modules:
                main_module = sys.modules['__main__']
                if hasattr(main_module, ref_string):
                    resolved_type = getattr(main_module, ref_string)
                    if isinstance(resolved_type, type) and is_dataclass(resolved_type):
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
                        return resolved_type
                except:
                    continue
                    
        except Exception:
            pass
        
        # 杂鱼♡～方法4：尝试使用typing原生解析喵～
        try:
            import sys
            
            # 杂鱼♡～尝试在__main__模块的上下文中解析喵～
            if '__main__' in sys.modules:
                main_module = sys.modules['__main__']
                main_globals = main_module.__dict__
                
                # 杂鱼♡～使用ForwardRef的原生解析方法喵～
                try:
                    if hasattr(forward_ref, '_evaluate'):
                        resolved_type = forward_ref._evaluate(main_globals, main_globals, set())
                    elif hasattr(forward_ref, '_eval_type'):
                        resolved_type = forward_ref._eval_type(main_globals, main_globals)
                    else:
                        # 杂鱼♡～fallback到直接查找喵～
                        resolved_type = main_globals.get(ref_string)
                    
                    if resolved_type and isinstance(resolved_type, type) and is_dataclass(resolved_type):
                        return resolved_type
                except:
                    pass
                    
        except Exception:
            pass
        
        # 杂鱼♡～方法5：扫描所有已知的dataclass类型喵～
        try:
            import gc
            for obj in gc.get_objects():
                if (isinstance(obj, type) and 
                    is_dataclass(obj) and 
                    obj.__name__ == ref_string):
                    return obj
        except Exception:
            pass
        
        return None
    
    def get_dataclass_fields(self, dataclass_type: Type) -> Dict[str, Type]:
        """杂鱼♡～获取dataclass的字段类型信息喵～
        
        Args:
            dataclass_type: dataclass类型
            
        Returns:
            Dict[str, Type]: 字段名 -> 字段类型的映射
        """
        # 杂鱼♡～检查是否是泛型dataclass实例喵～
        origin = get_origin(dataclass_type)
        args = get_args(dataclass_type)
        
        if origin and is_dataclass(origin):
            # 杂鱼♡～这是泛型dataclass，如 GenericContainer[Dict[str, Any]]喵～
            try:
                # 杂鱼♡～使用typing.get_type_hints来解析带泛型参数的类型喵～
                import typing
                # 杂鱼♡～为泛型类型创建一个适当的命名空间喵～
                type_hints = typing.get_type_hints(origin)
                
                # 杂鱼♡～构建泛型参数映射喵～
                if hasattr(origin, '__parameters__') and args:
                    type_param_map = {}
                    for param, arg in zip(origin.__parameters__, args):
                        type_param_map[param] = arg
                    
                    # 杂鱼♡～替换字段类型中的泛型参数喵～
                    resolved_field_types = {}
                    for field_name, field_type in type_hints.items():
                        resolved_type = self._substitute_type_vars(field_type, type_param_map)
                        resolved_field_types[field_name] = resolved_type
                    
                    return resolved_field_types
                else:
                    # 杂鱼♡～没有泛型参数，直接返回type hints喵～
                    return type_hints
                    
            except Exception:
                # 杂鱼♡～fallback到原始方式喵～
                pass
        
        # 杂鱼♡～普通dataclass或fallback情况喵～
        target_type = origin if origin and is_dataclass(origin) else dataclass_type
        
        if not is_dataclass(target_type):
            raise ValueError(f"杂鱼♡～{target_type}不是dataclass类型喵！～")
        
        field_types = {}
        for field in fields(target_type):
            field_types[field.name] = field.type
        
        return field_types
    
    def _substitute_type_vars(self, field_type: Type, type_param_map: Dict[Type, Type]) -> Type:
        """杂鱼♡～在字段类型中替换泛型参数喵～
        
        Args:
            field_type: 字段类型，可能包含泛型参数
            type_param_map: 泛型参数到具体类型的映射
            
        Returns:
            Type: 替换后的类型
        """
        # 杂鱼♡～如果是TypeVar，直接替换喵～
        if field_type in type_param_map:
            return type_param_map[field_type]
        
        # 杂鱼♡～如果是复合类型，递归替换喵～
        origin = get_origin(field_type)
        args = get_args(field_type)
        
        if origin and args:
            # 杂鱼♡～递归替换所有参数喵～
            new_args = []
            for arg in args:
                new_arg = self._substitute_type_vars(arg, type_param_map)
                new_args.append(new_arg)
            
            # 杂鱼♡～重构类型喵～
            try:
                if origin is Union:
                    from typing import Union
                    return Union[tuple(new_args)]
                else:
                    return origin[tuple(new_args)]
            except:
                # 杂鱼♡～如果重构失败，返回原类型喵～
                return field_type
        
        # 杂鱼♡～基本类型，直接返回喵～
        return field_type 