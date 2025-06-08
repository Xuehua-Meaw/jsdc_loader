"""
JSDC Loader: Functions for loading JSON data into dataclass or Pydantic model instances.
杂鱼♡～这是本喵为你写的JSDC Loader的加载函数喵～本喵可是很擅长把JSON变成对象呢～
"""

import orjson # 杂鱼♡～本喵现在用orjson了喵～更快更强喵～
import json # 杂鱼♡～保留json仅用于JSONDecodeError的类型提示，如果orjson的错误类型不同的话喵～
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
    """
    Loads data from a JSON file and converts it into an instance of the specified
    target class (dataclass or Pydantic model).
    杂鱼♡～本喵帮你从JSON文件加载数据并转换为指定的dataclass或Pydantic模型喵～

    Args:
        file_path (Union[str, Path]): Path to the JSON file.
            JSON文件的路径喵～杂鱼现在可以用字符串或Path对象了♡～
        target_class (Type[T]): The target dataclass or Pydantic model class.
            目标dataclass或Pydantic模型类喵～
        encoding (str, optional): File encoding. Defaults to "utf-8".
            Note: `orjson` primarily uses UTF-8; this parameter serves as a hint
            for error messages if decoding issues occur.
            文件编码，默认'utf-8'喵～
        max_file_size (Optional[int], optional): Maximum allowed file size in bytes.
            Defaults to None (no limit).
            最大文件大小（字节）喵～为None表示不限制～

    Returns:
        T: An instance of `target_class` created from the JSON data.
            从JSON数据创建的实例喵～杂鱼应该感谢本喵～

    Raises:
        FileNotFoundError: If the specified file does not exist.
            如果文件不存在喵～杂鱼肯定是路径搞错了～
        ValueError: If the file content is invalid JSON, too large, or if there's
            an issue during loading or conversion (e.g., encoding errors).
            如果文件内容无效或太大喵～杂鱼的数据有问题吧～
        TypeError: If `target_class` is not a valid dataclass or Pydantic model.
            如果target_class不是dataclass或BaseModel，杂鱼肯定传错类型了～
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
        # 杂鱼♡～orjson期望读取bytes，所以用 'rb' 模式喵～
        with path.open("rb") as f:
            file_bytes = f.read()
            # 杂鱼♡～直接将bytes传递给jsdc_loads喵～它会处理后续的解析和转换～
            # encoding参数现在主要用于提示用户文件应为UTF-8，因为orjson主要处理UTF-8喵～
            return jsdc_loads(file_bytes, target_class)

    except orjson.JSONDecodeError as e:
        # 杂鱼♡～如果orjson解析失败，可能文件不是有效的JSON或不是UTF-8编码喵～
        error_message = f"杂鱼♡～无效的JSON或UTF-8编码错误喵 (来自orjson)：{str(e)}～"
        if encoding.lower() != "utf-8":
            error_message += f" (文件期望编码: {encoding}, 但orjson主要使用UTF-8喵)"
        raise ValueError(error_message)
    except FileNotFoundError: # Re-raise specific error if path.open fails, though unlikely due to earlier check
        raise
    except Exception as e:
        # Catch other potential errors during file reading or jsdc_loads processing
        raise ValueError(f"杂鱼♡～加载或转换过程中出错喵：{str(e)}～")


def jsdc_loads(json_input: Union[str, bytes], target_class: Type[T]) -> T:
    """
    Loads data from a JSON string or bytes and converts it into an instance of the
    specified target class (dataclass or Pydantic model).
    杂鱼♡～本喵帮你从JSON字符串或字节串加载数据并转换为指定的dataclass或Pydantic模型喵～

    Args:
        json_input (Union[str, bytes]): The JSON string or UTF-8 encoded bytes to parse.
            JSON字符串或UTF-8编码的字节串喵～杂鱼提供的内容要合法哦～
        target_class (Type[T]): The target dataclass or Pydantic model class.
            目标dataclass或Pydantic模型类喵～

    Returns:
        T: An instance of `target_class` created from the JSON data.
            从JSON数据创建的实例喵～杂鱼应该感谢本喵～

    Raises:
        ValueError: If the input JSON is invalid, empty, or if there's an issue
            during conversion (e.g., data structure mismatch).
            如果输入内容无效或为空喵～杂鱼的数据有问题吧～
        TypeError: If `target_class` is not a valid dataclass/Pydantic model,
            or if `json_input` is not a string or bytes.
            如果target_class不是dataclass或BaseModel，或json_input类型不对，杂鱼肯定传错类型了～
    """
    data_to_parse: bytes
    if isinstance(json_input, str):
        if not json_input:
            raise ValueError("杂鱼♡～JSON字符串为空喵！～")
        data_to_parse = json_input.encode('utf-8')
    elif isinstance(json_input, bytes):
        if not json_input:
            raise ValueError("杂鱼♡～JSON字节串为空喵！～")
        data_to_parse = json_input
    else:
        raise TypeError(f"杂鱼♡～json_input必须是字符串或字节串喵，但得到了 {type(json_input).__name__}～")

    try:
        # 杂鱼♡～本喵现在用orjson.loads()了喵～它更快喵～
        json_data = orjson.loads(data_to_parse)

        origin = get_cached_origin(target_class)
        if origin is list or origin is TypingList: # Check for both list and typing.List
            if not isinstance(json_data, list):
                raise ValueError(
                    f"杂鱼♡～期望列表数据喵，但得到了 {type(json_data).__name__} 酱～"
                )

            args = get_cached_args(target_class)
            if not args: # Should have T from List[T]
                raise TypeError("杂鱼♡～List[T] 中的类型参数T未指定喵！～")
            item_class = args[0]
            validate_dataclass(item_class) # Validate the item_class (e.g., T in List[T])

            # 杂鱼♡～本喵要开始转换列表中的每个项目了喵～
            return [
                convert_dict_to_dataclass(item, item_class) for item in json_data
            ]
        else:
            # 杂鱼♡～对于单个对象，还是用老方法喵～
            validate_dataclass(target_class) # Validate the target_class itself

            # convert_dict_to_dataclass expects a dict.
            # If json_data is None, it implies an Optional[Dataclass] scenario,
            # which convert_dict_to_dataclass -> convert_value handles.
            # If json_data is not a dict and also not None, it's a type mismatch.
            if not isinstance(json_data, dict) and json_data is not None:
                 raise ValueError(
                    f"杂鱼♡～期望JSON对象来创建单个 {target_class.__name__} 实例喵，但得到了 {type(json_data).__name__}～"
                )
            # If json_data is an empty dict {}, convert_dict_to_dataclass will raise ValueError("Empty data dictionary").
            return convert_dict_to_dataclass(json_data, target_class)

    except orjson.JSONDecodeError as e:
        # Add context about UTF-8 if input was bytes
        error_message = f"杂鱼♡～无效的JSON喵 (来自orjson)：{str(e)}～"
        if isinstance(json_input, bytes):
            error_message += " (请确保字节串是有效的UTF-8编码JSON喵)"
        raise ValueError(error_message)
    except Exception as e: # Catch-all for other errors during conversion
        raise ValueError(f"杂鱼♡～加载或转换过程中出错喵：{str(e)}～")
