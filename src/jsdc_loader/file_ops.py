"""
File operations utilities for JSDC Loader.
Includes helpers for directory creation, file size checking, and JSON file saving with custom type handling.
杂鱼♡～这是本喵为你写的文件操作辅助函数喵～才不是因为担心杂鱼不会处理文件呢～
"""

import datetime
import json
import uuid
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Union


def ensure_directory_exists(directory_path: Union[str, Path]) -> None:
    """
    Ensures that a directory exists, creating it if necessary.
    杂鱼♡～本喵帮你确保目录存在喵～如果不存在就创建它～

    Args:
        directory_path (Union[str, Path]): The path to the directory.
            要确保存在的目录路径喵～杂鱼现在可以用字符串或Path对象了♡～
    Raises:
        OSError: If directory creation fails (e.g., due to permission issues).
            如果创建目录失败喵～杂鱼的权限是不是有问题？～
    """
    # 杂鱼♡～本喵现在支持Path对象了喵～
    path = Path(directory_path)

    if path and not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"杂鱼♡～创建目录失败喵：{path}，错误：{str(e)}～")


# 杂鱼♡～本喵创建了一个支持复杂类型的JSON编码器喵～
class ComplexJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that extends `json.JSONEncoder` to support serialization
    of additional types like datetime objects, UUID, Decimal, and sets.
    自定义JSON编码器，支持datetime、UUID、Decimal等类型喵～
    """

    def default(self, obj: Any) -> Any:
        """
        Overrides the default method to handle serialization of types
        not natively supported by `json.JSONEncoder`.
        处理非标准类型的JSON序列化喵～
        """
        # Added type hints
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return obj.total_seconds()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, set):
            return list(obj)
        return super().default(obj)


def save_json_file(
    file_path: Union[str, Path],
    data: Dict[str, Any],
    encoding: str = "utf-8",
    indent: int = 4,
) -> None:
    """
    Saves the given data as a JSON file using the ComplexJSONEncoder for broad type support.
    杂鱼♡～本喵帮你把数据保存为JSON文件喵～

    Args:
        file_path (Union[str, Path]): The path where the file will be saved.
            要保存的文件路径喵～杂鱼现在可以用字符串或Path对象了♡～
        data (Dict[str, Any]): The data (as a dictionary) to save.
            要保存的数据（字典形式）喵～
        encoding (str, optional): The file encoding. Defaults to "utf-8".
            文件编码，默认utf-8喵～杂鱼应该不需要改这个～
        indent (int, optional): Number of spaces for JSON indentation. Defaults to 4.
            JSON缩进空格数，默认4喵～看起来整齐一点～

    Raises:
        OSError: If writing to the file fails.
            如果写入文件失败喵～
        TypeError: If the data cannot be serialized to JSON (should be rare with ComplexJSONEncoder).
            如果数据无法序列化成JSON喵～杂鱼提供的数据有问题！～
        UnicodeEncodeError: If encoding the data to the specified `encoding` fails.
    """
    # 杂鱼♡～本喵现在支持Path对象了喵～
    path = Path(file_path)

    try:
        with path.open("w", encoding=encoding) as f:
            json.dump(
                data, f, ensure_ascii=False, indent=indent, cls=ComplexJSONEncoder
            )
    except OSError as e:
        raise OSError(f"杂鱼♡～写入文件失败喵：{path}，错误：{str(e)}～")
    except TypeError as e:
        raise TypeError(f"杂鱼♡～无法将数据序列化为JSON喵，错误：{str(e)}～")
    except UnicodeEncodeError as e:
        raise UnicodeEncodeError(
            f"杂鱼♡～用{encoding}编码数据失败喵，错误：{str(e)}～",
            e.object,
            e.start,
            e.end,
            e.reason,
        )
    except Exception as e:
        raise ValueError(f"杂鱼♡～JSON序列化过程中出错喵：{str(e)}～")


def check_file_size(file_path: Union[str, Path], max_size: int) -> None:
    """
    Checks if the size of a file exceeds a specified maximum.
    杂鱼♡～本喵帮你检查文件大小是否超过限制喵～

    Raises an error if the file is too large, does not exist, or is not a file.
    如果文件大小超过max_size字节，本喵会生气地抛出ValueError喵！～
    如果文件不存在，本喵会抛出FileNotFoundError喵～杂鱼一定是路径搞错了～

    Args:
        file_path (Union[str, Path]): The path to the file to check.
            要检查的文件路径喵～杂鱼现在可以用字符串或Path对象了♡～
        max_size (int): The maximum allowed file size in bytes.
            允许的最大文件大小（字节）喵～

    Raises:
        ValueError: If the file size exceeds `max_size` or if `file_path` is not a file.
            如果文件太大喵～
        FileNotFoundError: If the file does not exist.
            如果文件不存在喵～
        PermissionError: If there's no permission to access the file.
            如果没有权限访问文件喵～杂鱼是不是忘记提升权限了？～
    """
    # 杂鱼♡～本喵现在支持Path对象了喵～
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"杂鱼♡～文件不存在喵：{path}～")

    if not path.is_file():
        raise ValueError(f"杂鱼♡～路径不是文件喵：{path}～")

    try:
        file_size = path.stat().st_size
        if file_size > max_size:
            raise ValueError(
                f"杂鱼♡～文件大小超过限制喵！当前大小：{file_size}字节，最大允许：{max_size}字节～"
            )
    except PermissionError:
        raise PermissionError(f"杂鱼♡～没有权限检查文件大小喵：{path}～")
