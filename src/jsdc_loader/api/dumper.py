"""杂鱼♡～这是本喵重新设计的dumper API喵～现在使用schema-first架构♡～"""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, TypeVar, Union

from .exceptions import ConversionError, ValidationError
from ..pipeline.coordinator import convert_to_dict

# 杂鱼♡～定义TypeVar喵～
T = TypeVar('T')


def jsdc_dumps(obj: T, indent: int = 4) -> str:
    """杂鱼♡～本喵重新设计的序列化为JSON字符串的函数喵～
    
    Args:
        obj: 要序列化的dataclass实例
        indent: JSON缩进空格数
        
    Returns:
        str: JSON字符串
        
    Raises:
        ConversionError: 转换失败时
        ValidationError: 验证失败时
    """
    if obj is None:
        raise ValidationError("杂鱼♡～不能序列化None值喵！～")
    
    if indent < 0:
        raise ValidationError("杂鱼♡～缩进必须是非负数喵！～")
    
    # 杂鱼♡～使用新的pipeline coordinator进行转换喵～
    try:
        data_dict = convert_to_dict(obj)
        return json.dumps(data_dict, ensure_ascii=False, indent=indent)
    except Exception as e:
        if isinstance(e, (ConversionError, ValidationError)):
            raise
        else:
            raise ConversionError(f"杂鱼♡～序列化过程中出错喵：{str(e)}～") from e


def jsdc_dump(obj: T, file_path: Union[str, Path], encoding: str = "utf-8", indent: int = 4) -> None:
    """杂鱼♡～本喵重新设计的序列化到JSON文件的函数喵～
    
    使用原子文件操作，保证数据安全♡～
    
    Args:
        obj: 要序列化的dataclass实例
        file_path: 输出文件路径
        encoding: 文件编码
        indent: JSON缩进空格数
        
    Raises:
        ConversionError: 转换失败时
        ValidationError: 验证失败时
        OSError: 文件操作失败时
    """
    if obj is None:
        raise ValidationError("杂鱼♡～不能序列化None值喵！～")
    
    path = Path(file_path)
    
    if not path or not str(path):
        raise ValidationError("杂鱼♡～输出路径无效喵！～")
    
    # 杂鱼♡～先序列化为字符串喵～
    json_str = jsdc_dumps(obj, indent)
    
    # 杂鱼♡～确保目录存在喵～
    abs_path = path.absolute()
    directory = abs_path.parent
    directory.mkdir(parents=True, exist_ok=True)
    
    # 杂鱼♡～使用原子文件操作进行安全写入喵～
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
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_file.close()
        
        # 杂鱼♡～原子操作替换目标文件喵～
        if abs_path.exists():
            abs_path.unlink()
        
        os.rename(temp_path, str(abs_path))
        
    except Exception as e:
        # 杂鱼♡～出错时清理临时文件喵～
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass  # 杂鱼♡～清理失败也没办法了喵～
        
        raise ConversionError(f"杂鱼♡～写入文件失败喵：{str(e)}～") from e 