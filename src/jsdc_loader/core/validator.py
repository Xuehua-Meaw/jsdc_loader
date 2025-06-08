"""杂鱼♡～这是本喵的验证工具喵～本喵可是非常严格的，不会让杂鱼传入错误的类型呢～"""

from dataclasses import is_dataclass
from enum import Enum
from typing import Any, Dict, List, Set, Tuple, Type, Union, get_args, get_origin

from .compat import is_pydantic_model
from .types import _TYPE_HINTS_CACHE

# 杂鱼♡～本喵添加了类型验证缓存来提升性能喵～
_VALIDATION_CACHE = {}

def get_cached_type_hints(cls: Type) -> Dict[str, Any]:
    """杂鱼♡～本喵用缓存来获取类型提示，这样速度更快喵～"""
    if cls not in _TYPE_HINTS_CACHE:
        from typing import get_type_hints

        _TYPE_HINTS_CACHE[cls] = get_type_hints(cls)
    return _TYPE_HINTS_CACHE[cls]


def validate_dataclass(cls: Any) -> None:
    """杂鱼♡～本喵帮你验证提供的类是否为dataclass或BaseModel喵～杂鱼总是分不清这些～"""
    if not cls:
        raise TypeError("杂鱼♡～data_class不能为None喵！～")
    if not (is_dataclass(cls) or is_pydantic_model(cls)):
        raise TypeError("杂鱼♡～data_class必须是dataclass或Pydantic BaseModel喵！～")


def validate_type(key: str, value: Any, e_type: Any, _fast_mode: bool = False) -> None:
    """杂鱼♡～本喵帮你验证值是否匹配预期类型喵～本喵很擅长发现杂鱼的类型错误哦～优化版本～"""
    # 杂鱼♡～对于Any类型，本喵不做任何检查喵～它可以是任何类型～
    if e_type is Any:
        return

    # 杂鱼♡～在快速模式下，跳过复杂的类型检查喵～
    if _fast_mode:
        return

    # 杂鱼♡～本喵先检查缓存喵～
    value_type = type(value)
    cache_key = (value_type, e_type)
    if cache_key in _VALIDATION_CACHE:
        if not _VALIDATION_CACHE[cache_key]:
            raise TypeError(
                f"杂鱼♡～键{key}的类型无效喵：期望{e_type}，得到{value_type}～你连类型都搞不清楚吗？～"
            )
        return

    # 杂鱼♡～对于简单类型的快速检查喵～
    if e_type in (str, int, float, bool) and isinstance(value, e_type):
        _VALIDATION_CACHE[cache_key] = True
        return

    o_type = get_origin(e_type)

    try:
        # 杂鱼♡～对于Union类型，本喵需要特殊处理喵～
        if o_type is Union:
            # 如果值是None且Union包含Optional（即None类型），那么就是合法的喵～
            if value is None and type(None) in get_args(e_type):
                _VALIDATION_CACHE[cache_key] = True
                return

            # 对于非None值，我们需要检查它是否匹配Union中的任何类型喵～
            args = get_args(e_type)
            # 杂鱼♡～这里不使用isinstance检查，而是尝试递归验证每种可能的类型喵～
            valid = False
            for arg in args:
                if arg is type(None) and value is None:
                    valid = True
                    break
                try:
                    # 递归验证，如果没有抛出异常就是有效的喵～
                    validate_type(key, value, arg, True)  # 使用快速模式
                    valid = True
                    break
                except (TypeError, ValueError):
                    # 继续尝试下一个类型喵～
                    continue

            if not valid:
                _VALIDATION_CACHE[cache_key] = False
                raise TypeError(
                    f"杂鱼♡～键{key}的类型无效喵：期望{e_type}，得到{type(value)}～你连类型都搞不清楚吗？～"
                )

        # 杂鱼♡～对于列表类型，本喵需要检查容器类型和内容类型喵～
        elif o_type is list or o_type is List:
            if not isinstance(value, list):
                _VALIDATION_CACHE[cache_key] = False
                raise TypeError(
                    f"杂鱼♡～键{key}的类型无效喵：期望list，得到{type(value)}～真是个笨蛋呢～"
                )

            # 杂鱼♡～检查列表元素类型喵～但在快速模式下只检查前几个元素～
            args = get_args(e_type)
            if args:
                element_type = args[0]
                check_count = min(3, len(value)) if _fast_mode else len(value)  # 快速模式只检查前3个
                for i in range(check_count):
                    try:
                        validate_type(f"{key}[{i}]", value[i], element_type, True)
                    except (TypeError, ValueError) as e:
                        _VALIDATION_CACHE[cache_key] = False
                        raise TypeError(
                            f"杂鱼♡～列表{key}的第{i}个元素类型无效喵：{str(e)}"
                        )

        # 杂鱼♡～对于集合类型，本喵也需要检查内容类型喵～
        elif o_type is set or o_type is Set:
            if not isinstance(value, set):
                _VALIDATION_CACHE[cache_key] = False
                raise TypeError(
                    f"杂鱼♡～键{key}的类型无效喵：期望set，得到{type(value)}～真是个笨蛋呢～"
                )

            # 杂鱼♡～检查集合元素类型喵～但在快速模式下只检查前几个元素～
            args = get_args(e_type)
            if args:
                element_type = args[0]
                check_items = list(value)[:3] if _fast_mode else value  # 快速模式只检查前3个
                for i, item in enumerate(check_items):
                    try:
                        validate_type(f"{key}[{i}]", item, element_type, True)
                    except (TypeError, ValueError) as e:
                        _VALIDATION_CACHE[cache_key] = False
                        raise TypeError(f"杂鱼♡～集合{key}的某个元素类型无效喵：{str(e)}")

        # 杂鱼♡～对于字典类型，本喵需要检查键和值的类型喵～
        elif o_type is dict:
            if not isinstance(value, dict):
                _VALIDATION_CACHE[cache_key] = False
                raise TypeError(
                    f"杂鱼♡～键{key}的类型无效喵：期望dict，得到{type(value)}～真是个笨蛋呢～"
                )

            # 杂鱼♡～检查字典键和值的类型喵～但在快速模式下只检查前几个键值对～
            args = get_args(e_type)
            if len(args) == 2:
                key_type, val_type = args
                check_items = list(value.items())[:3] if _fast_mode else value.items()  # 快速模式只检查前3个
                for k, v in check_items:
                    try:
                        validate_type(f"{key}.key", k, key_type, True)
                    except (TypeError, ValueError) as e:
                        _VALIDATION_CACHE[cache_key] = False
                        raise TypeError(f"杂鱼♡～字典{key}的键类型无效喵：{str(e)}")

                    try:
                        validate_type(f"{key}[{k}]", v, val_type, True)
                    except (TypeError, ValueError) as e:
                        _VALIDATION_CACHE[cache_key] = False
                        raise TypeError(f"杂鱼♡～字典{key}的值类型无效喵：{str(e)}")

        # 杂鱼♡～对于元组类型，本喵也需要特殊处理喵～
        elif o_type is tuple or o_type is Tuple:
            if not isinstance(value, tuple):
                _VALIDATION_CACHE[cache_key] = False
                raise TypeError(
                    f"杂鱼♡～键{key}的类型无效喵：期望tuple，得到{type(value)}～真是个笨蛋呢～"
                )

            args = get_args(e_type)
            if not args:
                # 无类型参数的元组，只检查是否为元组类型
                pass
            elif len(args) == 2 and args[1] is Ellipsis:
                # Tuple[X, ...] 形式，所有元素都应该是同一类型
                element_type = args[0]
                check_count = min(3, len(value)) if _fast_mode else len(value)  # 快速模式只检查前3个
                for i in range(check_count):
                    try:
                        validate_type(f"{key}[{i}]", value[i], element_type, True)
                    except (TypeError, ValueError) as e:
                        _VALIDATION_CACHE[cache_key] = False
                        raise TypeError(
                            f"杂鱼♡～元组{key}的第{i}个元素类型无效喵：{str(e)}"
                        )
            else:
                # Tuple[X, Y, Z] 形式，长度和类型都固定
                if len(value) != len(args):
                    _VALIDATION_CACHE[cache_key] = False
                    raise TypeError(
                        f"杂鱼♡～元组{key}的长度无效喵：期望{len(args)}，得到{len(value)}～"
                    )

                for i, (item, arg_type) in enumerate(zip(value, args)):
                    try:
                        validate_type(f"{key}[{i}]", item, arg_type, True)
                    except (TypeError, ValueError) as e:
                        _VALIDATION_CACHE[cache_key] = False
                        raise TypeError(
                            f"杂鱼♡～元组{key}的第{i}个元素类型无效喵：{str(e)}"
                        )

        # 杂鱼♡～对于其他复杂类型，如List、Dict等，本喵需要检查origin喵～
        elif o_type is not None:
            # 对于列表、字典等容器类型，只需检查容器类型，不检查内容类型喵～
            if not isinstance(value, o_type):
                _VALIDATION_CACHE[cache_key] = False
                raise TypeError(
                    f"杂鱼♡～键{key}的类型无效喵：期望{o_type}，得到{type(value)}～真是个笨蛋呢～"
                )

        # 杂鱼♡～对于简单类型，直接使用isinstance喵～
        else:
            # 对于Enum类型，我们需要特殊处理喵～
            if isinstance(e_type, type) and issubclass(e_type, Enum):
                if not isinstance(value, e_type):
                    # 对于已经是枚举实例的验证喵～
                    if isinstance(value, str) and hasattr(e_type, value):
                        # 字符串值匹配枚举名，可以接受喵～
                        _VALIDATION_CACHE[cache_key] = True
                        return
                    _VALIDATION_CACHE[cache_key] = False
                    raise TypeError(
                        f"杂鱼♡～键{key}的类型无效喵：期望{e_type}，得到{type(value)}～"
                    )
            elif not isinstance(value, e_type) and e_type is not Any:
                # Any类型不做类型检查喵～
                _VALIDATION_CACHE[cache_key] = False
                raise TypeError(
                    f"杂鱼♡～键{key}的类型无效喵：期望{e_type}，得到{type(value)}～"
                )

        # 杂鱼♡～如果通过所有检查，就缓存为有效喵～
        _VALIDATION_CACHE[cache_key] = True

    except (TypeError, ValueError):
        _VALIDATION_CACHE[cache_key] = False
        raise
