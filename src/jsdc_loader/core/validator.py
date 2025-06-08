"""
Core validation utilities for JSDC Loader.
Provides type validation for objects during serialization and deserialization.
杂鱼♡～这是本喵的验证工具喵～本喵可是非常严格的，不会让杂鱼传入错误的类型呢～
"""

from dataclasses import is_dataclass
from enum import Enum
from typing import Any, Dict, List, Set, Tuple, Type, Union

from .compat import (
    HAS_PYDANTIC,
    PYDANTIC_V2,
    get_cached_args,
    get_cached_origin,
    is_pydantic_instance,
    is_pydantic_model,
)
from .types import _TYPE_HINTS_CACHE


def get_cached_type_hints(cls: Type) -> Dict[str, Any]:
    """
    Retrieves type hints for a class, using a cache for performance.
    杂鱼♡～本喵用缓存来获取类型提示，这样速度更快喵～
    """
    if cls not in _TYPE_HINTS_CACHE:
        from typing import get_type_hints

        _TYPE_HINTS_CACHE[cls] = get_type_hints(cls)
    return _TYPE_HINTS_CACHE[cls]


def validate_dataclass(cls: Type) -> None:
    """
    Validates if the provided class `cls` is a dataclass or a Pydantic BaseModel.
    杂鱼♡～本喵帮你验证提供的类是否为dataclass或BaseModel喵～杂鱼总是分不清这些～

    Args:
        cls (Type): The class to validate.

    Raises:
        TypeError: If `cls` is None or not a dataclass/Pydantic BaseModel.
    """
    # Added Type hint for cls
    if not cls:
        raise TypeError("杂鱼♡～data_class不能为None喵！～")
    if not (is_dataclass(cls) or is_pydantic_model(cls)):
        raise TypeError("杂鱼♡～data_class必须是dataclass或Pydantic BaseModel喵！～")

# --- Validation Helper Functions ---

def _validate_union(key: str, value: Any, expected_type: Any) -> None:
    """
    Helper to validate a value against a Union type.
    The value must match at least one of the types in the Union.
    """
    args = get_cached_args(expected_type)
    if value is None and type(None) in args:
        return

    valid = False
    for arg_type in args:
        if arg_type is type(None) and value is None: # Handles Optional[X] where value is None
            valid = True
            break
        try:
            validate_type(key, value, arg_type) # Recursive call
            valid = True
            break
        except (TypeError, ValueError):
            continue
    if not valid:
        raise TypeError(
            f"杂鱼♡～键{key}的类型无效喵：期望{expected_type}，得到{type(value).__name__}～你连类型都搞不清楚吗？～"
        )

def _validate_list(key: str, value: Any, expected_type: Any) -> None:
    """
    Helper to validate a value against a List type.
    Ensures the value is a list and recursively validates its elements if type arguments are provided.
    """
    if not isinstance(value, list):
        raise TypeError(
            f"杂鱼♡～键{key}的类型无效喵：期望list，得到{type(value).__name__}～真是个笨蛋呢～"
        )
    args = get_cached_args(expected_type)
    if args: # List has type arguments, e.g., List[int]
        element_type = args[0]
        for i, item in enumerate(value):
            try:
                validate_type(f"{key}[{i}]", item, element_type)
            except (TypeError, ValueError) as e:
                raise TypeError(f"杂鱼♡～列表{key}的第{i}个元素类型无效喵：{str(e)}")

def _validate_set(key: str, value: Any, expected_type: Any) -> None:
    """
    Helper to validate a value against a Set type.
    Ensures the value is a set and recursively validates its elements if type arguments are provided.
    """
    if not isinstance(value, set):
        raise TypeError(
            f"杂鱼♡～键{key}的类型无效喵：期望set，得到{type(value).__name__}～真是个笨蛋呢～"
        )
    args = get_cached_args(expected_type)
    if args: # Set has type arguments, e.g., Set[str]
        element_type = args[0]
        # Note: Iterating set for indexed error key f"{key}[{i}]" is okay for error reporting,
        # though sets are unordered.
        for i, item in enumerate(list(value)): # Convert to list for consistent indexing in error
            try:
                validate_type(f"{key}[{i}]", item, element_type)
            except (TypeError, ValueError) as e:
                raise TypeError(f"杂鱼♡～集合{key}的元素'{item}'类型无效喵：{str(e)}")

def _validate_dict(key: str, value: Any, expected_type: Any) -> None:
    """
    Helper to validate a value against a Dict type.
    Ensures the value is a dict and recursively validates its keys and values if type arguments are provided.
    """
    if not isinstance(value, dict):
        raise TypeError(
            f"杂鱼♡～键{key}的类型无效喵：期望dict，得到{type(value).__name__}～真是个笨蛋呢～"
        )
    args = get_cached_args(expected_type)
    if len(args) == 2: # Dict has key and value type arguments, e.g., Dict[str, int]
        key_type, val_type = args
        for k, v in value.items():
            try:
                validate_type(f"{key}.key_of({k})", k, key_type) # Modified key for clarity
            except (TypeError, ValueError) as e:
                raise TypeError(f"杂鱼♡～字典{key}的键'{k}'类型无效喵：{str(e)}")
            try:
                validate_type(f"{key}[{k}]", v, val_type)
            except (TypeError, ValueError) as e:
                raise TypeError(f"杂鱼♡～字典{key}的值(键:'{k}')类型无效喵：{str(e)}")

def _validate_tuple(key: str, value: Any, expected_type: Any) -> None:
    """
    Helper to validate a value against a Tuple type.
    Ensures the value is a tuple and handles validation for both fixed-length
    (Tuple[X, Y]) and variable-length (Tuple[X, ...]) typed tuples.
    """
    if not isinstance(value, tuple):
        raise TypeError(
            f"杂鱼♡～键{key}的类型无效喵：期望tuple，得到{type(value).__name__}～真是个笨蛋呢～"
        )
    args = get_cached_args(expected_type)
    if not args: # e.g. plain 'tuple'
        return
    if len(args) == 2 and args[1] is Ellipsis: # Tuple[X, ...]
        element_type = args[0]
        for i, item in enumerate(value):
            try:
                validate_type(f"{key}[{i}]", item, element_type)
            except (TypeError, ValueError) as e:
                raise TypeError(f"杂鱼♡～变长元组{key}的第{i}个元素类型无效喵：{str(e)}")
    else: # Tuple[X, Y, Z]
        if len(value) != len(args):
            raise TypeError(
                f"杂鱼♡～定长元组{key}的长度无效喵：期望{len(args)}，得到{len(value)}～"
            )
        for i, (item, arg_type) in enumerate(zip(value, args)):
            try:
                validate_type(f"{key}[{i}]", item, arg_type)
            except (TypeError, ValueError) as e:
                raise TypeError(f"杂鱼♡～定长元组{key}的第{i}个元素类型无效喵：{str(e)}")

def _validate_dataclass(key: str, value: Any, expected_type: Type) -> None:
    """
    Helper to validate a value against a dataclass type.
    Ensures the value is an instance of the expected dataclass and recursively validates its fields.
    """
    if not isinstance(value, expected_type): # Ensure it's an instance of the specified dataclass
        raise TypeError(
            f"杂鱼♡～键{key}的类型无效喵：期望dataclass {expected_type.__name__}，得到{type(value).__name__}～"
        )
    # Recursively validate each field of the dataclass
    type_hints = get_cached_type_hints(expected_type)
    for field_name, field_type in type_hints.items():
        try:
            field_value = getattr(value, field_name)
        except AttributeError:
            # This should ideally not happen if 'value' is a proper instance of 'expected_type'
            raise TypeError(
                f"杂鱼♡～Dataclass {expected_type.__name__} 实例缺少字段 {field_name} 喵！ (键: {key})～"
            )
        validate_type(f"{key}.{field_name}", field_value, field_type)

def _validate_pydantic_model(key: str, value: Any, expected_type: Type) -> None:
    """
    Helper to validate a value against a Pydantic model type.
    Ensures the value is an instance of the expected model and recursively validates its fields.
    """
    if not is_pydantic_instance(value) or not isinstance(value, expected_type):
        raise TypeError(
            f"杂鱼♡～键{key}的类型无效喵：期望Pydantic模型 {expected_type.__name__}，得到{type(value).__name__}～"
        )
    # Recursively validate each field of the Pydantic model
    fields_to_check = {}
    if PYDANTIC_V2:
        fields_to_check = {name: field_info.annotation for name, field_info in value.model_fields.items()}
    else: # Pydantic V1
        fields_to_check = {name: field.outer_type_ for name, field in value.__fields__.items()}

    for field_name, field_type in fields_to_check.items():
        try:
            field_value = getattr(value, field_name)
        except AttributeError:
            raise TypeError(
                f"杂鱼♡～Pydantic模型 {expected_type.__name__} 实例缺少字段 {field_name} 喵！ (键: {key})～"
            )
        validate_type(f"{key}.{field_name}", field_value, field_type)

def _validate_enum(key: str, value: Any, expected_type: Type[Enum]) -> None:
    """
    Helper to validate a value against an Enum type.
    Accepts the enum member itself, its string name, or its underlying value.
    """
    if isinstance(value, expected_type): # Value is already an instance of the Enum
        return
    if isinstance(value, str): # Check if string value matches any Enum member name
        try:
            _ = expected_type[value] # Attempt to access Enum member by string name
            return
        except KeyError:
            pass # If string does not match any member name, fall through to raise error
    # Check if value matches any Enum member's value (e.g. for IntEnum, StrEnum)
    if not isinstance(value, expected_type): # Double check after string name check
        for member in expected_type:
            if member.value == value:
                return
    raise TypeError(
        f"杂鱼♡～键{key}的类型无效喵：期望{expected_type.__name__} (或其成员名称/值)，得到{type(value).__name__} '{value}'～"
    )

def _validate_other_generic(key: str, value: Any, expected_type: Any, origin_type: Any) -> None:
    """
    Helper to validate against other generic types from 'typing' (e.g., Callable, Deque)
    not specifically handled by other validators.
    This primarily checks if the value is an instance of the origin type.
    """
    # This is a basic check for generic types where only the origin is known (e.g. Callable, Deque)
    # It does not validate type arguments for these generics.
    if not isinstance(value, origin_type):
        raise TypeError(
            f"杂鱼♡～键{key}的类型无效喵：期望类型基于 {origin_type.__name__}，得到{type(value).__name__}～此乃其他泛型类型验证喵～"
        )

def _validate_simple_type(key: str, value: Any, expected_type: Any) -> None:
    """
    Helper to validate a value against a simple, non-generic type (e.g., int, str, bool).
    Performs a basic isinstance check.
    """
    if not isinstance(value, expected_type):
        raise TypeError(
            f"杂鱼♡～键{key}的类型无效喵：期望{expected_type.__name__ if hasattr(expected_type, '__name__') else expected_type}，得到{type(value).__name__}～此乃简单类型验证喵～"
        )

# --- Main validate_type Function (Dispatcher) ---

def validate_type(key: str, value: Any, e_type: Any) -> None:
    """
    Main dispatcher function to validate if a value matches an expected type.
    Delegates to specialized helper functions based on the `e_type`.
    杂鱼♡～本喵帮你验证值是否匹配预期类型喵～本喵很擅长发现杂鱼的类型错误哦～
    """
    if e_type is Any:
        return

    origin_type = get_cached_origin(e_type)

    if origin_type is Union:
        _validate_union(key, value, e_type)
    elif origin_type is list or e_type is list: # e_type is list for plain list (Python 3.9+)
        _validate_list(key, value, e_type)
    elif origin_type is set or e_type is set:   # e_type is set for plain set (Python 3.9+)
        _validate_set(key, value, e_type)
    elif origin_type is dict or e_type is dict: # e_type is dict for plain dict (Python 3.9+)
        _validate_dict(key, value, e_type)
    elif origin_type is tuple or e_type is tuple: # e_type is tuple for plain tuple (Python 3.9+)
        _validate_tuple(key, value, e_type)
    elif is_dataclass(e_type): # Check before origin_type is None, as dataclasses are not generics from typing
        _validate_dataclass(key, value, e_type)
    elif HAS_PYDANTIC and is_pydantic_model(e_type): # Same, Pydantic models are not typing generics
        _validate_pydantic_model(key, value, e_type)
    elif isinstance(e_type, type) and issubclass(e_type, Enum): # Enums are classes, not typing generics
        _validate_enum(key, value, e_type)
    elif origin_type is not None:
        # Catches other `typing` generics like Deque, Callable, etc.
        # For these, we typically only validate the origin type (e.g., isinstance(value, collections.abc.Callable))
        # as detailed argument validation is complex and often not strictly necessary for serialization/deserialization.
        _validate_other_generic(key, value, e_type, origin_type)
    else: # Fallback for simple types (int, str, bool, etc.) or types not otherwise caught
        _validate_simple_type(key, value, e_type)
