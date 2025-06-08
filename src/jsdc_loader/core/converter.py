"""
Core conversion utilities for JSDC Loader.
Handles type conversions during serialization and deserialization processes.
杂鱼♡～这是本喵的转换工具喵～各种类型转换都靠本喵了喵～
"""

import datetime
import uuid
from dataclasses import is_dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Type, Union

from .compat import (
    create_pydantic_from_dict,
    get_cached_args,
    get_cached_origin,
    is_pydantic_instance,
    is_pydantic_model,
    pydantic_to_dict,
)
from .types import T
from .validator import get_cached_type_hints, validate_type


def convert_enum(key: str, value: Any, enum_type: Type[Enum]) -> Enum:
    """
    Converts a value to an Enum member.
    Typically expects `value` to be the string name of the enum member.
    """
    try:
        return enum_type[value]
    except KeyError:
        raise ValueError(f"Invalid Enum value for key {key}: {value}")


def convert_union_type(key: str, value: Any, union_type: Any) -> Any:
    """
    Converts a value to one of the types specified in a Union.
    It tries to match the value against each type in the Union.
    """
    args = get_cached_args(union_type)

    # 杂鱼♡～处理None值喵～
    if value is None and type(None) in args:
        return None

    # 杂鱼♡～首先尝试精确类型匹配，这样可以避免不必要的类型转换喵～
    for arg_type in args:
        if arg_type is type(None):
            continue

        # 杂鱼♡～检查是否是精确的类型匹配喵～
        if _is_exact_type_match(value, arg_type):
            try:
                return convert_value(key, value, arg_type)
            except (ValueError, TypeError):
                continue

    # 杂鱼♡～如果没有精确匹配，再尝试类型转换喵～
    for arg_type in args:
        if arg_type is type(None):
            continue

        # 杂鱼♡～跳过已经尝试过的精确匹配喵～
        if _is_exact_type_match(value, arg_type):
            continue

        try:
            return convert_value(key, value, arg_type)
        except (ValueError, TypeError):
            continue

    # 如果所有转换都失败，则抛出错误喵～
    raise TypeError(f"杂鱼♡～无法将键{key}的值{value}转换为{union_type}喵！～")


def _is_exact_type_match(value: Any, expected_type: Any) -> bool:
    """
    Checks if the value's type is an exact match to the expected_type,
    primarily for optimization before attempting more complex conversions.
    杂鱼♡～检查值是否与期望类型精确匹配喵～
    """
    # 杂鱼♡～处理基本类型喵～
    if expected_type in (int, float, str, bool):
        return type(value) is expected_type

    # 杂鱼♡～处理容器类型喵～
    origin = get_cached_origin(expected_type)
    if origin is list:
        return isinstance(value, list)
    elif origin is dict:
        return isinstance(value, dict)
    elif origin is set:
        return isinstance(value, set)
    elif origin is tuple:
        return isinstance(value, tuple)
    elif expected_type is list: # Check for plain list, set, dict, tuple without origin
        return isinstance(value, list)
    elif expected_type is dict:
        return isinstance(value, dict)
    elif expected_type is set:
        return isinstance(value, set)
    elif expected_type is tuple:
        return isinstance(value, tuple)

    # 杂鱼♡～处理dataclass类型喵～
    if is_dataclass(expected_type):
        return isinstance(value, expected_type)

    # 杂鱼♡～处理Enum类型喵～
    if isinstance(expected_type, type) and issubclass(expected_type, Enum):
        return isinstance(value, expected_type)

    # 杂鱼♡～其他情况返回False，让转换逻辑处理喵～
    return False

# --- New Helper Functions for type conversion ---

def _convert_datetime_like(key: str, value: Any, expected_type: Any) -> Any:
    """
    Handles string-to-datetime object conversions (datetime, date, time)
    and number/dict-to-timedelta conversions.
    """
    if expected_type == datetime.datetime:
        if isinstance(value, str):
            return datetime.datetime.fromisoformat(value)
        # Add other potential source types for datetime if necessary
    elif expected_type == datetime.date:
        if isinstance(value, str):
            return datetime.date.fromisoformat(value)
    elif expected_type == datetime.time:
        if isinstance(value, str):
            return datetime.time.fromisoformat(value)
    elif expected_type == datetime.timedelta:
        if isinstance(value, (int, float)):
            return datetime.timedelta(seconds=value)
        elif isinstance(value, dict):  # For {"days": 1, "seconds": 30} style
            return datetime.timedelta(**value)
    # If value is not a recognized type for the expected_type, fall through to raise error
    raise ValueError(f"杂鱼♡～无法将值 '{value}' 转换为 {expected_type.__name__} 为键 {key}喵！～")


def _convert_uuid_type(key: str, value: Any, expected_type: Type[uuid.UUID]) -> uuid.UUID:
    """Handles string-to-UUID conversion."""
    if isinstance(value, str):
        try:
            return uuid.UUID(value)
        except ValueError:
            raise ValueError(f"杂鱼♡～无效的UUID字符串 '{value}' 为键 {key}喵！～")
    raise ValueError(f"杂鱼♡～无法将值 '{value}' 转换为UUID为键 {key}喵！～ (需要字符串)～")


def _convert_decimal_type(key: str, value: Any, expected_type: Type[Decimal]) -> Decimal:
    """Handles string/int/float-to-Decimal conversion."""
    if isinstance(value, (str, int, float)):
        try:
            return Decimal(str(value))  # Convert to string first for robust Decimal conversion
        except Exception as e: # Broad exception for Decimal conversion issues
            raise ValueError(f"杂鱼♡～无法将值 '{value}' 转换为Decimal为键 {key}喵！错误: {e}～")
    raise ValueError(f"杂鱼♡～无法将值 '{value}' 转换为Decimal为键 {key}喵！～ (需要字符串,整数或浮点数)～")


def convert_simple_type(key: str, value: Any, e_type: Any) -> Any:
    """
    Converts a value to a 'simple' type.
    This includes primitives (int, str, bool, float), datetime-related types,
    UUID, and Decimal. It acts as a fallback converter for types not handled
    by more specific converters in the main `convert_value` dispatcher.
    """
    # Dispatch to specialized handlers for known complex simple types
    if e_type == datetime.datetime or e_type == datetime.date or e_type == datetime.time or e_type == datetime.timedelta:
        return _convert_datetime_like(key, value, e_type)
    elif e_type == uuid.UUID:
        return _convert_uuid_type(key, value, e_type)
    elif e_type == Decimal:
        return _convert_decimal_type(key, value, e_type)
    # Fallback for basic types (int, float, str, bool) and other direct constructions
    else:
        try:
            return e_type(value)
        except (TypeError, ValueError) as e: # Catch ValueError for things like int("abc")
            # This error message is now more generic as specific type errors are caught by helpers
            raise TypeError(f"杂鱼♡～无法将键 '{key}' 的值 '{value}' (类型 {type(value).__name__}) 转换为类型 {e_type.__name__}喵！原始错误: {e}～")


def _convert_list_type(key: str, value: Any, e_type: Any) -> list:
    """
    Handles conversion for list types. If the list is typed (e.g., List[MyClass]),
    it recursively calls `convert_value` for each item.
    """
    if not isinstance(value, list):
        # If list is expected but not provided, this is a type error.
        # Unless e_type is just 'list' (not List[T]) and we want to allow non-list values?
        # Current logic: convert_value's main dispatcher only calls this if isinstance(value, list)
        # for List[T]. If e_type is plain 'list', it also comes here.
        # If e_type is 'list' and value is not a list, convert_simple_type would try list(value).
        # For consistency, if e_type implies a list structure, value should be a list.
        raise TypeError(f"杂鱼♡～期望列表但得到 {type(value).__name__} 为键 {key}喵！～")

    args = get_cached_args(e_type)
    if args:  # Handles List[T]
        element_type = args[0]
        if is_dataclass(element_type):
            return [convert_dict_to_dataclass(item_val, element_type) for item_val in value]
        elif is_pydantic_model(element_type):
            return [create_pydantic_from_dict(element_type, item_val) for item_val in value]
        else:
            return [convert_value(f"{key}[{i}]", item_val, element_type) for i, item_val in enumerate(value)]
    return value # For plain 'list' expected_type or List without type args, return as is.


def _convert_set_type(key: str, value: list, e_type: Any) -> set:
    """
    Handles conversion for set types from a list input. If the set is typed
    (e.g., Set[MyClass]), it recursively calls `convert_value` for each item.
    """
    # Assumes value is a list, as per the check in the dispatcher (convert_value)
    args = get_cached_args(e_type)
    if args:  # Handles Set[T]
        element_type = args[0]
        return {convert_value(f"{key}[*]", item, element_type) for item in value}
    return set(value) # For plain 'set' or Set without type args


def convert_dict_type(key: str, value: dict, e_type: Any) -> dict:
    """
    Converts a dictionary's keys and/or values based on its type annotation (e.g., Dict[int, MyClass]).
    JSON keys are always strings, so this function handles conversion of string keys
    to other supported primitive types if specified in `e_type`.
    """
    # Ensure value is a dict before processing
    if not isinstance(value, dict):
        raise TypeError(f"杂鱼♡～期望字典但得到 {type(value).__name__} 为键 {key}喵！～")

    origin = get_cached_origin(e_type)
    # Handles plain 'dict' or Dict without type args
    if e_type is dict and not origin: # e_type is literally <class 'dict'>
         return value

    if origin is dict: # Handles Dict[K, V]
        args = get_cached_args(e_type)
        if not args: # Should imply plain dict, return value
            return value
        key_type, val_type = args

        # 杂鱼♡～本喵扩展支持更多键类型了喵～
        # 支持字符串、整数、浮点数、布尔值以及UUID作为键喵～
        supported_key_types = (str, int, float, bool, uuid.UUID)
        if key_type not in supported_key_types:
            raise ValueError(
                f"杂鱼♡～字典键类型 {key_type} 暂不支持喵！支持的键类型: {supported_key_types}～"
            )

        # 杂鱼♡～如果键类型不是字符串，需要转换JSON中的字符串键为目标类型喵～
        converted_dict = {}
        for k, v in value.items(): # k is always str when parsing from JSON
            # 杂鱼♡～JSON中的键总是字符串，需要转换为目标键类型喵～
            if key_type == str:
                converted_key = k
            elif key_type == int:
                try:
                    converted_key = int(k)
                except ValueError:
                    raise ValueError(f"杂鱼♡～无法将键 '{k}' 转换为整数喵！～")
            elif key_type == float:
                try:
                    converted_key = float(k)
                except ValueError:
                    raise ValueError(f"杂鱼♡～无法将键 '{k}' 转换为浮点数喵！～")
            elif key_type == bool:
                if k.lower() in ("true", "1"):
                    converted_key = True
                elif k.lower() in ("false", "0"):
                    converted_key = False
                else:
                    raise ValueError(f"杂鱼♡～无法将键 '{k}' 转换为布尔值喵！～")
            elif key_type == uuid.UUID:
                try:
                    converted_key = uuid.UUID(k)
                except ValueError:
                    raise ValueError(f"杂鱼♡～无法将键 '{k}' 转换为UUID喵！～")
            else:
                # This case should ideally not be reached if key_type is in supported_key_types
                # and not handled above.
                converted_key = k

            # 杂鱼♡～转换值喵～
            if is_dataclass(val_type) or get_cached_origin(val_type) is Union:
                converted_dict[converted_key] = convert_value(f"{key}.{k}", v, val_type)
            else:
                converted_dict[converted_key] = v

        return converted_dict

    # Default case, just return the dict
    return value


def convert_tuple_type(key: str, value: list, e_type: Any) -> tuple:
    """
    Converts a list (typically from JSON array) to a tuple, handling typed tuples.
    For Tuple[X, ...] or Tuple[X, Y, Z], recursively calls `convert_value` for items.
    杂鱼♡～本喵帮你把列表转换成元组喵～
    """
    if get_cached_origin(e_type) is tuple:
        args = get_cached_args(e_type)
        if len(args) == 2 and args[1] is Ellipsis:  # Tuple[X, ...]
            element_type = args[0]
            return tuple(
                convert_value(f"{key}[{i}]", item, element_type)
                for i, item in enumerate(value)
            )
        elif args:  # Tuple[X, Y, Z]
            if len(value) != len(args):
                raise ValueError(
                    f"杂鱼♡～元组{key}的长度不匹配喵！期望{len(args)}，得到{len(value)}～"
                )
            return tuple(
                convert_value(f"{key}[{i}]", item, arg_type)
                for i, (item, arg_type) in enumerate(zip(value, args))
            )

    # 如果没有参数类型或者其他情况，直接转换为元组喵～
    return tuple(value)


def convert_value(key: str, value: Any, e_type: Any) -> Any:
    """
    Main dispatcher function to convert a value to the expected type `e_type`.
    It delegates to specialized conversion functions based on `e_type`.
    This is used during deserialization.
    """
    # 杂鱼♡～处理None值和Any类型喵～
    if value is None and (
        e_type is Any
        or (get_cached_origin(e_type) is Union and type(None) in get_cached_args(e_type))
    ):
        return None

    # 杂鱼♡～如果期望类型是Any，直接返回值喵～
    if e_type is Any:
        return value

    origin = get_cached_origin(e_type)

    # 杂鱼♡～Union类型必须优先处理，因为它可能包含None或其他特殊类型喵～
    if origin is Union:
        return convert_union_type(key, value, e_type)

    # 杂鱼♡～处理特定类型喵～
    # isinstance(e_type, type) is important for issubclass check
    if isinstance(e_type, type) and issubclass(e_type, Enum):
        return convert_enum(key, value, e_type) # Existing helper
    if is_dataclass(e_type): # e_type is the dataclass type itself
        if not isinstance(value, dict):
            raise TypeError(f"杂鱼♡～期望字典来创建dataclass {e_type.__name__} 但得到 {type(value).__name__} 为键 {key}喵！～")
        return convert_dict_to_dataclass(value, e_type) # Existing helper
    if is_pydantic_model(e_type): # e_type is the Pydantic model type itself
        if not isinstance(value, dict):
            raise TypeError(f"杂鱼♡～期望字典来创建Pydantic模型 {e_type.__name__} 但得到 {type(value).__name__} 为键 {key}喵！～")
        return create_pydantic_from_dict(e_type, value) # Existing helper

    # 杂鱼♡～处理集合类型喵～
    # Note: For these collection helpers, they expect `value` to be of the source collection type (e.g., list for set/tuple).
    if (origin is set or e_type is set):
        if not isinstance(value, list): # JSON arrays become Python lists
            raise TypeError(f"杂鱼♡～期望列表来创建set但得到 {type(value).__name__} 为键 {key}喵！～")
        return _convert_set_type(key, value, e_type) # New helper
    if (origin is tuple or e_type is tuple):
        if not isinstance(value, list): # JSON arrays become Python lists
            raise TypeError(f"杂鱼♡～期望列表来创建tuple但得到 {type(value).__name__} 为键 {key}喵！～")
        return convert_tuple_type(key, value, e_type) # Existing helper
    if origin is list or e_type is list: # Handles List[T] and plain 'list'
        # _convert_list_type will check isinstance(value, list)
        return _convert_list_type(key, value, e_type) # New helper
    if origin is dict or e_type is dict: # Handles Dict[K,V] and plain 'dict'
        # convert_dict_type will check isinstance(value, dict)
        return convert_dict_type(key, value, e_type) # Existing helper

    # 杂鱼♡～其他简单类型或无法识别的类型由 convert_simple_type 处理喵～
    return convert_simple_type(key, value, e_type) # Refactored helper


# // 杂鱼♡～本喵添加了这个函数来检查一个dataclass是否是frozen的喵～
def is_frozen_dataclass(cls: Type) -> bool:
    """
    Checks if a given class is a frozen dataclass.
    """
    # Added type hint for cls
    return (
        is_dataclass(cls)
        and hasattr(cls, "__dataclass_params__")
        and getattr(cls.__dataclass_params__, "frozen", False)
    )


def convert_dict_to_dataclass(data: dict, cls: Type[T]) -> T:
    """
    Converts a dictionary to an instance of the given dataclass `cls`.
    It recursively calls `convert_value` for each field in the dataclass.
    """
    # Added Type hint for cls
    if not data: # data being None is handled by convert_value if target is Optional[Dataclass]
        # This function specifically expects a dictionary for populating fields.
        # An empty dict means no fields can be populated, which might be an issue
        # if the dataclass has required fields without defaults.
        # Current behavior: raises ValueError, which seems reasonable.
        raise ValueError("Empty data dictionary provided for dataclass conversion.")

    if is_pydantic_model(cls):
        # 杂鱼♡～使用兼容层来创建 Pydantic 模型喵～
        return create_pydantic_from_dict(cls, data)

    # // 杂鱼♡～本喵统一使用构造函数来创建实例喵～这样更一致喵～
    init_kwargs = {}
    t_hints = get_cached_type_hints(cls)

    for field_name, field_value in data.items():
        if field_name in t_hints:
            expected_field_type = t_hints.get(field_name)
            # 杂鱼♡～如果字段在类型提示中但没有具体类型（例如Any），则直接使用原始值或进行基础转换喵～
            # 但 get_type_hints 通常会解析类型，所以 expected_field_type 不应为 None
            if expected_field_type is not None:
                init_kwargs[field_name] = convert_value(
                    field_name, field_value, expected_field_type
                )
            else:
                # This case should ideally not be reached if t_hints is populated correctly.
                # If it means the type is Any or unspecified in a way that get_type_hints returns None for it,
                # we might pass it through, but this could hide issues.
                # For now, let's assume get_type_hints provides a valid type or raises.
                # If a field is in data but not in t_hints, it's handled by the else below.
                init_kwargs[field_name] = field_value # Fallback, though potentially risky
        else:
            # 杂鱼♡～如果数据中的键不在dataclass的字段中，就抛出错误喵～
            raise ValueError(f"Unknown data key: {field_name} for class {cls.__name__}")

    return cls(**init_kwargs)


def convert_dataclass_to_dict(
    obj: Any, parent_key: str = "", parent_type: Any = None
) -> Any:
    """
    Converts a dataclass instance (or other supported types) to a dictionary
    suitable for JSON serialization. It handles nested structures, dataclasses,
    Pydantic models, enums, and various primitive/collection types recursively.
    Type validation via `validate_type` is performed for collection items and
    dataclass fields if `parent_type` provides sufficient type information.
    """
    if obj is None:
        return None

    # Handle types that have a direct serializable representation
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    if isinstance(obj, datetime.timedelta):
        return obj.total_seconds()
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, Decimal):
        return str(obj)

    # Handle Pydantic instances using its optimized converter
    if is_pydantic_instance(obj):
        return pydantic_to_dict(obj) # Assumes pydantic_to_dict handles internal recursion

    if isinstance(obj, Enum):
        return obj.name

    # For tuples, recursively convert items; JSON represents tuples as lists.
    if isinstance(obj, tuple):
        # Determine element type for tuples like Tuple[X, ...] or Tuple[X,Y]
        # For simplicity, if parent_type is Tuple[X, ...], use X.
        # If Tuple[X,Y], this simple element_type extraction might be too naive if items are heterogeneous
        # and validate_type is used. However, convert_dataclass_to_dict's element_type is for recursion.
        tuple_element_type = None
        if parent_type and get_cached_origin(parent_type) is tuple:
            args = get_cached_args(parent_type)
            if args:
                if len(args) == 2 and args[1] is Ellipsis: # Tuple[X, ...]
                    tuple_element_type = args[0]
                # For fixed-length tuples (Tuple[X,Y,Z]), a single element_type is not quite right
                # if X,Y,Z are different. The recursive call will use the specific type of each item
                # if tuple_element_type is None, or this general one.
                # The original code passed `get_cached_args(parent_type)[0]` which is also a simplification.
                # Let's keep it simple for now, relying on deeper validation if needed.
                # For serialization, the actual type of `item` is often more important than `parent_type`'s arg.
                # The `parent_type` for the recursive call is more about guiding the next step of serialization.
                # The original code's `parent_type` for tuple item recursion was:
                # `(get_cached_args(parent_type)[0] if parent_type and get_cached_args(parent_type) else None)`
                # This is effectively passing the type of the *first* element of the tuple annotation.
                if args and not (len(args) == 2 and args[1] is Ellipsis) : # Fixed length tuple e.g. Tuple[int, str]
                     # For fixed-length tuples, we don't pass a single element_type for all items to the recursive call's parent_type.
                     # Instead, the recursive call will use the actual type of the item.
                     # The parent_key is generic here.
                     return [convert_dataclass_to_dict(item, f"{parent_key}[{i}]" , get_cached_args(parent_type)[i] if args and i < len(args) else None) for i, item in enumerate(obj)]

                # Fallback for Tuple[Any,...] or if logic is complex
                if args : tuple_element_type = args[0]


        return [
            _convert_collection_item_to_dict(
                item,
                f"{parent_key}[{i}]", # Generic key for tuple items
                # For Tuple[X, ...], all items are of type X.
                # For Tuple[X, Y], this is tricky. The original code used args[0].
                # It's better to pass the specific type from the tuple annotation if available for that position.
                # However, _convert_collection_item_to_dict takes a single element_type.
                # The recursive convert_dataclass_to_dict will use the actual type of `item` if element_type is None.
                # Let's pass the specific type of the annotation if fixed-length, else the general one.
                tuple_element_type # This will be used for validation if not None
            )
            for i,item in enumerate(obj)
        ]


    # Helper for list and set items
    if isinstance(obj, (list, set)):
        collection_name = 'list' if isinstance(obj, list) else 'set'
        element_type = None
        if parent_type and get_cached_origin(parent_type) in (list, set) and get_cached_args(parent_type):
            element_type = get_cached_args(parent_type)[0]

        return [
            _convert_collection_item_to_dict(
                item, f"{parent_key or collection_name}[{i}]", element_type
            )
            for i, item in enumerate(obj) # enumerate works for sets too in Python 3.7+ (though order isn't guaranteed for JSON)
        ]

    if isinstance(obj, dict):
        # 杂鱼♡～需要检查字典中键和值的类型喵～
        key_type, val_type = None, None
        if (
            parent_type
            and get_cached_origin(parent_type) is dict
            and len(get_cached_args(parent_type)) == 2
        ):
            key_type, val_type = get_cached_args(parent_type)

        result = {}
        for k, v in obj.items():
            if key_type:
                # 杂鱼♡～验证字典键的类型喵～
                key_name = f"{parent_key or 'dict'}.key"
                try:
                    validate_type(key_name, k, key_type)
                except (TypeError, ValueError) as e:
                    raise TypeError(
                        f"杂鱼♡～序列化时字典键类型验证失败喵：{key_name} {str(e)}～"
                    )

            if val_type:
                # 杂鱼♡～验证字典值的类型喵～
                val_key = f"{parent_key or 'dict'}[{k}]"
                try:
                    validate_type(val_key, v, val_type)
                except (TypeError, ValueError) as e:
                    raise TypeError(
                        f"杂鱼♡～序列化时字典值类型验证失败喵：{val_key} {str(e)}～"
                    )

            # 杂鱼♡～将键转换为字符串以支持JSON序列化喵～
            # JSON只支持字符串键，所以本喵需要将其他类型的键转换为字符串～
            json_key = str(k)
            result[json_key] = convert_dataclass_to_dict(
                v, f"{parent_key}[{k}]", val_type
            )

        return result
    elif is_dataclass(obj): # This must be after specific types like datetime, Enum, etc.
        result = {}
        # Obtain type hints for the specific dataclass type of obj, not from parent_type
        obj_type = type(obj)
        t_hints = get_cached_type_hints(obj_type)

        for field_name, field_value in vars(obj).items():
            # The expected type for the field comes from the dataclass's own type hints
            field_expected_type = t_hints.get(field_name)
            current_field_key = f"{parent_key}.{field_name}" if parent_key else field_name

            # Validate the field's value against its type hint before serialization
            if field_expected_type is not None:
                try:
                    validate_type(current_field_key, field_value, field_expected_type)
                except (TypeError, ValueError) as e:
                    # Provide a more specific error message for dataclass field validation
                    raise TypeError(
                        f"杂鱼♡～序列化时dataclass字段 '{current_field_key}' (类型: {type(field_value).__name__}) "
                        f"类型验证失败喵 (期望类型: {field_expected_type.__name__ if hasattr(field_expected_type, '__name__') else field_expected_type}): {str(e)}～"
                    )

            # Recursively convert the field value.
            # The `parent_type` for the recursive call is the field's own expected type.
            result[field_name] = convert_dataclass_to_dict(
                field_value, current_field_key, field_expected_type
            )
        return result

    # Fallback for primitive types (int, str, bool, float) and any other unhandled types
    return obj


# --- Helper for convert_dataclass_to_dict (serialization path) ---
def _convert_collection_item_to_dict(item: Any, item_key: str, element_type: Any) -> Any:
    """
    Helper to validate (if `element_type` is known) and then recursively convert
    an item from a list or set for dictionary representation during serialization.
    """
    # Validate the item against the expected element type if provided
    if element_type:
        try:
            validate_type(item_key, item, element_type)
        except (TypeError, ValueError) as e:
            # This error message is more generic for items from lists or sets
            raise TypeError(
                f"杂鱼♡～序列化时集合/列表元素 '{item_key}' (类型: {type(item).__name__}) "
                f"类型验证失败喵 (期望类型: {element_type.__name__ if hasattr(element_type, '__name__') else element_type}): {str(e)}～"
            )
    # Recursively call convert_dataclass_to_dict for the item.
    # The `parent_type` for this recursive call is the `element_type`.
    return convert_dataclass_to_dict(item, item_key, element_type)
