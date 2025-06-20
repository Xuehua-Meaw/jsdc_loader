"""杂鱼♡～这是本喵重新设计的loader API喵～现在使用schema-first架构♡～"""

import json
from pathlib import Path
from typing import Type, TypeVar, Union

from .exceptions import ConversionError, ValidationError
from ..pipeline.coordinator import convert_from_dict

# 杂鱼♡～定义TypeVar喵～
T = TypeVar('T')


def jsdc_loads(json_str: str, target_class: Type[T]) -> T:
    """杂鱼♡～本喵重新设计的从JSON字符串加载数据的函数喵～
    
    Args:
        json_str: JSON字符串
        target_class: 目标dataclass类型
        
    Returns:
        T: 转换后的dataclass实例
        
    Raises:
        ConversionError: 转换失败时
        ValidationError: 验证失败时
    """
    if not json_str:
        raise ValidationError("杂鱼♡～JSON字符串为空喵！～")
    
    try:
        json_data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ConversionError(f"杂鱼♡～无效的JSON格式喵：{str(e)}～")
    
    # 杂鱼♡～使用新的pipeline coordinator进行转换喵～
    try:
        return convert_from_dict(json_data, target_class)
    except Exception as e:
        if isinstance(e, (ConversionError, ValidationError)):
            raise
        else:
            raise ConversionError(f"杂鱼♡～转换过程中出错喵：{str(e)}～") from e


def jsdc_load(file_path: Union[str, Path], target_class: Type[T], encoding: str = "utf-8") -> T:
    """杂鱼♡～本喵重新设计的从JSON文件加载数据的函数喵～
    
    Args:
        file_path: JSON文件路径
        target_class: 目标dataclass类型
        encoding: 文件编码
        
    Returns:
        T: 转换后的dataclass实例
        
    Raises:
        FileNotFoundError: 文件不存在时
        ConversionError: 转换失败时
        ValidationError: 验证失败时
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"杂鱼♡～文件不存在喵：{path}～")
    
    try:
        with path.open("r", encoding=encoding) as f:
            json_str = f.read()
    except UnicodeDecodeError as e:
        raise ConversionError(f"杂鱼♡～用{encoding}解码失败喵：{str(e)}～")
    except Exception as e:
        raise ConversionError(f"杂鱼♡～读取文件失败喵：{str(e)}～")
    
    return jsdc_loads(json_str, target_class) 