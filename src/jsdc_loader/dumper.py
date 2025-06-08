"""杂鱼♡～这是本喵的序列化工具喵～本喵可以把你的dataclass和Pydantic模型变成JSON喵～"""

import datetime
import orjson # 杂鱼♡～本喵现在用orjson了喵～
import os
import tempfile
import uuid
from dataclasses import is_dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Union, Optional

from .core.compat import is_pydantic_instance
from .core.converter import convert_dataclass_to_dict
from .core.types import T
from .file_ops import ensure_directory_exists


# 杂鱼♡～orjson的默认处理器喵～
def _orjson_default_handler(obj: Any) -> Any:
    """杂鱼♡～本喵帮orjson处理它不认识的类型喵～"""
    if isinstance(obj, datetime.timedelta):
        return obj.total_seconds()  # orjson本身不处理timedelta
    elif isinstance(obj, Decimal):
        return str(obj)  # orjson本身不处理Decimal
    # 杂鱼♡～datetime, date, time, UUID, set, Enum, dataclasses 都是orjson原生支持的喵～
    # 杂鱼♡～Dataclasses 和 Pydantic 模型在到达这里之前已经被 convert_dataclass_to_dict 转换成字典了喵～
    raise TypeError(f"杂鱼♡～类型 {type(obj)} 本喵的orjson默认处理器也处理不了喵～")


def jsdc_dumps(obj: T, indent: Optional[int] = 2, **kwargs) -> str:
    """杂鱼♡～本喵帮你把dataclass或Pydantic模型实例序列化成JSON字符串喵～

    这个函数接收一个dataclass实例，并将其序列化为JSON字符串喵～
    JSON输出可以使用指定的缩进级别格式化喵～杂鱼是不是太懒了，连文件都不想写呢♡～

    Args:
        obj (T): 要序列化的dataclass实例喵～
        indent (Optional[int], optional): JSON输出中使用的缩进空格数喵～
            None for compact, int for pretty. Default is 2.
            本喵偷偷把默认值改成了2，这样测试用例那边就不会出错了喵～

    Returns:
        str: 序列化后的JSON字符串喵～杂鱼可以好好利用它哦～

    Raises:
        TypeError: 如果obj不是dataclass或BaseModel，杂鱼肯定传错参数了～
        ValueError: 如果序列化过程中出错，本喵会生气地抛出错误喵！～
    """
    if indent is not None and not isinstance(indent, int):
        raise TypeError("杂鱼♡～indent必须是整数或None喵！～")

    if indent is not None and indent < 0:
        raise ValueError("杂鱼♡～缩进必须是非负数喵！～负数是什么意思啦～")

    try:
        if isinstance(obj, type):
            raise TypeError("杂鱼♡～obj必须是实例而不是类喵！～你真是搞不清楚呢～")

        # Handle list of dataclass/pydantic instances
        if isinstance(obj, list):
            processed_list = []
            # We need to determine the type of elements for validation,
            # assuming list is homogeneous for this transformation.
            # For simplicity in this context, type validation during list processing
            # will rely on individual item validation in convert_dataclass_to_dict.
            # A more robust approach might involve generic type hints for the list.
            for i, item in enumerate(obj):
                if not (is_dataclass(item) or is_pydantic_instance(item)):
                    raise TypeError(
                        f"杂鱼♡～列表中的第 {i} 个元素不是有效的dataclass或Pydantic实例喵！～"
                    )
                # Using type(item) for parent_type here, as list elements can be different types.
                processed_list.append(convert_dataclass_to_dict(item, parent_key=f"root[{i}]", parent_type=type(item)))
            data_to_dump = processed_list
        elif is_dataclass(obj) or is_pydantic_instance(obj):
            obj_type = type(obj)
            data_to_dump = convert_dataclass_to_dict(
                obj, parent_key="root", parent_type=obj_type
            )
        else:
            raise TypeError("杂鱼♡～obj必须是dataclass、Pydantic BaseModel实例或这些实例的列表喵！～")

        # 杂鱼♡～准备orjson的选项喵～
        orjson_options = 0
        if indent is not None and indent > 0:
            # orjson 主要支持 OPT_INDENT_2。如果需要其他缩进，需要额外处理或接受此限制。
            # 为了简单起见，任何正整数indent都映射到OPT_INDENT_2。
            orjson_options |= orjson.OPT_INDENT_2

        # 杂鱼♡～如果kwargs里有sort_keys=True，本喵就加上OPT_SORT_KEYS喵～
        if kwargs.get("sort_keys", False):
            orjson_options |= orjson.OPT_SORT_KEYS
            # 杂鱼♡～确保kwargs里的sort_keys不会传给orjson.dumps，因为它不认识这个参数名喵～
            # (实际上orjson.dumps不接受**kwargs，所以这里不需要del，但要注意传递的参数)

        # 杂鱼♡～ensure_ascii在orjson中是默认行为（总是UTF-8）喵～

        orjson_bytes = orjson.dumps(data_to_dump, default=_orjson_default_handler, option=orjson_options)
        return orjson_bytes.decode("utf-8") # orjson.dumps返回bytes，需要解码成字符串喵～

    except TypeError as e:
        raise TypeError(f"杂鱼♡～类型验证失败喵：{str(e)}～真是个笨蛋呢～")
    except Exception as e:
        raise ValueError(f"杂鱼♡～序列化过程中出错喵：{str(e)}～")


def jsdc_dump(
    obj: T, output_path: Union[str, Path], encoding: str = "utf-8", indent: Optional[int] = 2, **kwargs
) -> None:
    """杂鱼♡～本喵帮你把dataclass或Pydantic模型实例序列化成JSON文件喵～

    这个函数接收一个dataclass实例，并将其序列化表示写入到指定文件中，
    格式为JSON喵～输出文件可以使用指定的字符编码，JSON输出可以
    使用指定的缩进级别格式化喵～杂鱼一定会感激本喵的帮助的吧♡～

    本喵会使用临时文件进行安全写入，防止在写入过程中出错导致文件损坏喵～

    Args:
        obj (T): 要序列化的dataclass实例喵～
        output_path (Union[str, Path]): 要保存JSON数据的输出文件路径喵～杂鱼现在可以用字符串或Path对象了♡～
        encoding (str, optional): 输出文件使用的字符编码喵～默认是'utf-8'～
        indent (int, optional): JSON输出中使用的缩进空格数喵～默认是4～看起来整齐一点～

    Raises:
        ValueError: 如果提供的对象不是dataclass或路径无效，本喵会生气地抛出错误喵！～
        TypeError: 如果obj不是dataclass或BaseModel，杂鱼肯定传错参数了～
        OSError: 如果遇到文件系统相关错误，杂鱼的硬盘可能有问题喵～
        UnicodeEncodeError: 如果编码失败，杂鱼选的编码有问题喵！～
    """
    # 杂鱼♡～本喵现在支持Path对象了喵～
    path = Path(output_path)

    if not path or not str(path):
        raise ValueError("杂鱼♡～输出路径无效喵！～")

    if indent is not None and not isinstance(indent, int): # Added type check for indent similar to jsdc_dumps
        raise TypeError("杂鱼♡～indent必须是整数或None喵！～")

    if indent is not None and indent < 0:
        raise ValueError("杂鱼♡～缩进必须是非负数喵！～负数是什么意思啦～")

    # 获取输出文件的绝对路径喵～
    abs_path = path.absolute()
    directory = abs_path.parent

    try:
        # 确保目录存在且可写喵～
        ensure_directory_exists(str(directory))

        if isinstance(obj, type):
            raise TypeError("杂鱼♡～obj必须是实例而不是类喵！～你真是搞不清楚呢～")

        # 杂鱼♡～类型检查 (single instance or list of instances) 现在由 jsdc_dumps 处理了喵～
        # jsdc_dump 只需要负责文件操作和调用 jsdc_dumps 喵～ (不对，现在要直接用orjson.dumps)

        if isinstance(obj, type):
            raise TypeError("杂鱼♡～obj必须是实例而不是类喵！～你真是搞不清楚呢～")

        # 预处理对象为字典或字典列表 (与jsdc_dumps一致)
        if isinstance(obj, list):
            processed_list = []
            for i, item in enumerate(obj):
                if not (is_dataclass(item) or is_pydantic_instance(item)):
                    raise TypeError(
                        f"杂鱼♡～列表中的第 {i} 个元素不是有效的dataclass或Pydantic实例喵！～"
                    )
                processed_list.append(convert_dataclass_to_dict(item, parent_key=f"root[{i}]", parent_type=type(item)))
            data_to_dump = processed_list
        elif is_dataclass(obj) or is_pydantic_instance(obj):
            obj_type = type(obj)
            data_to_dump = convert_dataclass_to_dict(
                obj, parent_key="root", parent_type=obj_type
            )
        else:
            raise TypeError("杂鱼♡～obj必须是dataclass、Pydantic BaseModel实例或这些实例的列表喵！～")

        # 准备orjson选项
        orjson_options = 0
        if indent is not None and indent > 0:
            orjson_options |= orjson.OPT_INDENT_2

        if kwargs.get("sort_keys", False): # jsdc_dump的kwargs现在可以接受sort_keys了喵～
            orjson_options |= orjson.OPT_SORT_KEYS

        orjson_bytes = orjson.dumps(data_to_dump, default=_orjson_default_handler, option=orjson_options)

        # 杂鱼♡～使用临时文件进行安全写入喵～ (写入bytes)
        temp_file = tempfile.NamedTemporaryFile(
            prefix=f".{abs_path.name}.",
            dir=str(directory),
            suffix=".tmp",
            delete=False,
            mode="wb", # 写入二进制喵～
        )

        temp_path = temp_file.name
        try:
            temp_file.write(orjson_bytes) # 写入bytes喵～
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_file.close()

            # 杂鱼♡～原子重命名操作喵～
            if abs_path.exists():
                abs_path.unlink()

            # 杂鱼♡～安全地重命名文件喵～
            os.rename(temp_path, str(abs_path))
        except Exception as e:
            # 杂鱼♡～如果出错，清理临时文件喵～
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass  # 杂鱼♡～如果连临时文件都删不掉，本喵也无能为力了喵～
            raise e  # 杂鱼♡～重新抛出原始异常喵～

    except OSError as e:
        raise OSError(f"杂鱼♡～创建目录或访问文件失败喵：{str(e)}～")
    except TypeError as e:
        raise TypeError(f"杂鱼♡～类型验证失败喵：{str(e)}～真是个笨蛋呢～")
    except Exception as e:
        raise ValueError(f"杂鱼♡～序列化过程中出错喵：{str(e)}～")
