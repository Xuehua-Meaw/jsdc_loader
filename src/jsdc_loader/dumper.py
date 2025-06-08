"""杂鱼♡～这是本喵的序列化工具喵～本喵可以把你的dataclass和Pydantic模型变成JSON喵～"""

import datetime
import json
import os
import tempfile
import uuid
from dataclasses import is_dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Union, Optional, Tuple

from .core.compat import is_pydantic_instance
from .core.converter import convert_dataclass_to_dict
from .core.validator import validate_dataclass
from .core.types import T
from .file_ops import ensure_directory_exists


# 杂鱼♡～本喵创建了一个自定义JSON编码器，这样就可以处理各种复杂类型喵～
class JSDCJSONEncoder(json.JSONEncoder):
    """杂鱼♡～这是本喵为你特制的JSON编码器喵～可以处理各种特殊类型哦～"""

    def default(self, obj: Any) -> Any:
        """杂鱼♡～本喵会把这些特殊类型转换成JSON兼容的格式喵～"""
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
        elif is_dataclass(obj):
            return convert_dataclass_to_dict(obj)
        # 杂鱼♡～其他类型就交给父类处理喵～
        return super().default(obj)


def jsdc_dumps(
    obj,
    *,
    indent: Optional[Union[int, str]] = None,
    separators: Optional[Tuple[str, str]] = None,
    sort_keys: bool = False,
    ensure_ascii: bool = True,
    performance_mode: bool = False,  # 杂鱼♡～本喵添加了性能模式选项喵～
) -> str:
    """
    杂鱼♡～这是本喵为你写的序列化函数喵～

    Args:
        obj: 要序列化的对象，必须是dataclass或Pydantic BaseModel实例
        indent: JSON缩进，默认为None（不缩进）
        separators: JSON分隔符，默认为None
        sort_keys: 是否对字典键排序，默认为False
        ensure_ascii: 是否确保ASCII编码，默认为True
        performance_mode: 是否启用性能模式（减少类型验证），默认为False
    
    Returns:
        JSON字符串
        
    Raises:
        TypeError: 杂鱼♡～如果对象不是dataclass或BaseModel实例就会报错喵～
        ValueError: 杂鱼♡～如果对象无法序列化就会报错喵～
    """
    if obj is None:
        raise ValueError("杂鱼♡～不能序列化None对象喵！～")

    try:
        # 杂鱼♡～本喵先验证对象类型喵～
        validate_dataclass(obj.__class__)
        
        # 杂鱼♡～然后把dataclass转换为字典喵～
        if performance_mode:
            # 杂鱼♡～性能模式：跳过大部分类型验证，加快序列化速度喵～
            dict_obj = convert_dataclass_to_dict(obj, _skip_validation=True)
        else:
            # 杂鱼♡～普通模式：完整的类型验证喵～
            dict_obj = convert_dataclass_to_dict(obj)
        
        # 杂鱼♡～最后序列化为JSON字符串喵～
        return json.dumps(
            dict_obj,
            indent=indent,
            separators=separators,
            sort_keys=sort_keys,
            ensure_ascii=ensure_ascii,
        )
    except Exception as e:
        raise ValueError(f"杂鱼♡～序列化失败喵：{str(e)}～") from e


def jsdc_dump(
    obj: T, output_path: Union[str, Path], encoding: str = "utf-8", indent: int = 4
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

    if indent < 0:
        raise ValueError("杂鱼♡～缩进必须是非负数喵！～负数是什么意思啦～")

    # 获取输出文件的绝对路径喵～
    abs_path = path.absolute()
    directory = abs_path.parent

    try:
        # 确保目录存在且可写喵～
        ensure_directory_exists(str(directory))

        if isinstance(obj, type):
            raise TypeError("杂鱼♡～obj必须是实例而不是类喵！～你真是搞不清楚呢～")

        if not (is_dataclass(obj) or is_pydantic_instance(obj)):
            raise TypeError("杂鱼♡～obj必须是dataclass或Pydantic BaseModel实例喵！～")

        # 杂鱼♡～先序列化为字符串喵～
        json_str = jsdc_dumps(obj, indent)

        # 杂鱼♡～使用临时文件进行安全写入喵～
        # 在同一目录创建临时文件，确保重命名操作在同一文件系统内执行喵～
        temp_file = tempfile.NamedTemporaryFile(
            prefix=f".{abs_path.name}.",
            dir=str(directory),
            suffix=".tmp",
            delete=False,
            mode="w",
            encoding=encoding,
        )

        temp_path = temp_file.name
        try:
            # 杂鱼♡～写入临时文件喵～
            temp_file.write(json_str)
            # 必须先刷新缓冲区喵～
            temp_file.flush()
            # 确保文件内容已完全写入磁盘喵～然后再关闭文件～
            os.fsync(temp_file.fileno())
            temp_file.close()

            # 杂鱼♡～使用原子操作将临时文件重命名为目标文件喵～
            # 在Windows上，如果目标文件已存在，可能会失败，所以先尝试删除喵～
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
