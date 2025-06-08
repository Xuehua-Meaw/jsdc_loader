"""杂鱼♡～这是本喵为你写的JSDC Loader的加载函数喵～本喵可是很擅长把JSON变成对象呢～"""

import json
from pathlib import Path
from typing import Optional, Type, Union, List as TypingList # Use TypingList to avoid conflict with list type

from .core import T, convert_dict_to_dataclass, validate_dataclass
from .core.compat import get_cached_origin, get_cached_args # For List[T] handling
from .file_ops import check_file_size


def jsdc_load(
    file_path: Union[str, Path],
    target_class: Type[T],
    encoding: str = "utf-8",
    max_file_size: Optional[int] = None,
) -> T:
    """杂鱼♡～本喵帮你从JSON文件加载数据并转换为指定的dataclass或Pydantic模型喵～

    Args:
        file_path (Union[str, Path]): JSON文件的路径喵～杂鱼现在可以用字符串或Path对象了♡～
        target_class (Type[T]): 目标dataclass或Pydantic模型类喵～
        encoding (str, optional): 文件编码，默认'utf-8'喵～
        max_file_size (Optional[int], optional): 最大文件大小（字节）喵～为None表示不限制～

    Returns:
        T: 从JSON数据创建的实例喵～杂鱼应该感谢本喵～

    Raises:
        FileNotFoundError: 如果文件不存在喵～杂鱼肯定是路径搞错了～
        ValueError: 如果文件内容无效或太大喵～杂鱼的数据有问题吧～
        TypeError: 如果target_class不是dataclass或BaseModel，杂鱼肯定传错类型了～
    """
    # 杂鱼♡～本喵现在支持Path对象了喵～
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"杂鱼♡～文件不存在喵：{path}～")

    # 检查文件大小喵～
    if max_file_size is not None:
        check_file_size(str(path), max_file_size)

    # 杂鱼♡～目标类验证现在移到 jsdc_loads 中了喵～

    try:
        with path.open("r", encoding=encoding) as f:
            # 杂鱼♡～直接调用 jsdc_loads 处理字符串内容喵～
            # 这样逻辑更统一，而且 jsdc_loads 会处理 List[T] 的情况喵～
            return jsdc_loads(f.read(), target_class)
    # 杂鱼♡～json.JSONDecodeError 和 ValueError (empty json_str) 已经在 jsdc_loads 中处理了喵～
    # 只需要处理文件相关的特定异常喵～
    except UnicodeDecodeError as e:
        raise ValueError(
            f"杂鱼♡～用{encoding}解码失败喵：{str(e)}～杂鱼是不是编码搞错了？～"
        )
    except Exception as e:
        raise ValueError(f"杂鱼♡～加载或转换过程中出错喵：{str(e)}～")


def jsdc_loads(json_str: str, target_class: Type[T]) -> T:
    """杂鱼♡～本喵帮你从JSON字符串加载数据并转换为指定的dataclass或Pydantic模型喵～

    Args:
        json_str (str): JSON字符串喵～杂鱼提供的内容要合法哦～
        target_class (Type[T]): 目标dataclass或Pydantic模型类喵～

    Returns:
        T: 从JSON数据创建的实例喵～杂鱼应该感谢本喵～

    Raises:
        ValueError: 如果字符串内容无效喵～杂鱼的数据有问题吧～
        TypeError: 如果target_class不是dataclass或BaseModel，杂鱼肯定传错类型了～
    """
    if not json_str:
        raise ValueError("杂鱼♡～JSON字符串为空喵！～")

    try:
        json_data = json.loads(json_str)

        # 如果数据为空 (例如 "null", "[]", "{}")，对于某些 target_class 这可能是有效的 (例如 Optional, List)
        # 但 convert_dict_to_dataclass 期望一个非空字典。
        # List[T] case will handle empty list naturally.
        # For single object, if json_data is not a dict (e.g. null from "null"), convert_dict_to_dataclass will fail.
        # Let's ensure json_data is not None if we are not expecting a list.

        origin = get_cached_origin(target_class)
        if origin is list or origin is TypingList: # Check for both list and typing.List
            if not isinstance(json_data, list):
                raise ValueError(
                    f"杂鱼♡～期望列表数据喵，但得到了 {type(json_data)} 酱～"
                )

            args = get_cached_args(target_class)
            if not args:
                raise TypeError("杂鱼♡～List[T] 中的类型参数T未指定喵！～")
            item_class = args[0]
            validate_dataclass(item_class) # Validate the item_class (e.g., T in List[T])

            # 杂鱼♡～本喵要开始转换列表中的每个项目了喵～
            # 如果json_data是空列表，这里会正确返回空列表喵～
            return [
                convert_dict_to_dataclass(item, item_class) for item in json_data
            ]
        else:
            # 杂鱼♡～对于单个对象，还是用老方法喵～
            validate_dataclass(target_class) # Validate the target_class itself
            if not json_data and json_data is not None : # Allow None to be handled by Union/Optional in convert_value
                 # convert_dict_to_dataclass expects a dict, so empty string "" -> json.loads("") error
                 # "null" -> None. "[]", "{}" are not suitable for single dataclass.
                 # This check might be too strict or needs refinement based on how convert_dict_to_dataclass handles non-dict.
                 # For now, if it's not a list and json_data is falsey (but not None), raise.
                raise ValueError("杂鱼♡～单个对象的JSON数据不能为空字典或空列表喵！～")
            return convert_dict_to_dataclass(json_data, target_class)

    except json.JSONDecodeError as e:
        raise ValueError(f"杂鱼♡～无效的JSON喵：{str(e)}～")
    except Exception as e:
        raise ValueError(f"杂鱼♡～加载或转换过程中出错喵：{str(e)}～")
