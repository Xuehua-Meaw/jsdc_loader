"""杂鱼♡～这是本喵为你写的文件操作辅助函数喵～才不是因为担心杂鱼不会处理文件呢～"""

import os
import json
from typing import Dict, Any
import datetime
import uuid
from decimal import Decimal

def ensure_directory_exists(directory_path: str) -> None:
    """
    杂鱼♡～本喵帮你确保目录存在喵～如果不存在就创建它～

    :param directory_path: 要确保存在的目录路径喵～
    :raises: OSError 如果创建目录失败喵～杂鱼的权限是不是有问题？～
    """
    if directory_path:
        if not os.path.exists(directory_path):
            try:
                os.makedirs(directory_path)
            except OSError as e:
                raise OSError(f"杂鱼♡～创建目录失败喵：{directory_path}，错误：{str(e)}～")

# 杂鱼♡～本喵创建了一个支持复杂类型的JSON编码器喵～
class ComplexJSONEncoder(json.JSONEncoder):
    """自定义JSON编码器，支持datetime、UUID、Decimal等类型喵～"""
    
    def default(self, obj):
        """处理非标准类型的JSON序列化喵～"""
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

def save_json_file(file_path: str, data: Dict[str, Any], encoding: str = 'utf-8', indent: int = 4) -> None:
    """
    杂鱼♡～本喵帮你把数据保存为JSON文件喵～

    :param file_path: 要保存的文件路径喵～
    :param data: 要保存的数据（字典形式）喵～
    :param encoding: 文件编码，默认utf-8喵～杂鱼应该不需要改这个～
    :param indent: JSON缩进空格数，默认4喵～看起来整齐一点～
    :raises: OSError 如果写入文件失败喵～
    :raises: TypeError 如果数据无法序列化成JSON喵～杂鱼提供的数据有问题！～
    """
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=indent, cls=ComplexJSONEncoder)
    except OSError as e:
        raise OSError(f"杂鱼♡～写入文件失败喵：{file_path}，错误：{str(e)}～")
    except TypeError as e:
        raise TypeError(f"杂鱼♡～无法将数据序列化为JSON喵，错误：{str(e)}～")
    except UnicodeEncodeError as e:
        raise UnicodeEncodeError(f"杂鱼♡～用{encoding}编码数据失败喵，错误：{str(e)}～", e.object, e.start, e.end, e.reason)
    except Exception as e:
        raise ValueError(f"杂鱼♡～JSON序列化过程中出错喵：{str(e)}～")

def check_file_size(file_path: str, max_size: int) -> None:
    """
    杂鱼♡～本喵帮你检查文件大小是否超过限制喵～

    如果文件大小超过max_size字节，本喵会生气地抛出ValueError喵！～
    如果文件不存在，本喵会抛出FileNotFoundError喵～杂鱼一定是路径搞错了～

    :param file_path: 要检查的文件路径喵～
    :param max_size: 允许的最大文件大小（字节）喵～
    :raises: ValueError 如果文件太大喵～
    :raises: FileNotFoundError 如果文件不存在喵～
    :raises: PermissionError 如果没有权限访问文件喵～杂鱼是不是忘记提升权限了？～
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"杂鱼♡～文件不存在喵：{file_path}～")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"杂鱼♡～路径不是文件喵：{file_path}～")
    
    try:
        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            raise ValueError(f"杂鱼♡～文件大小超过限制喵！当前大小：{file_size}字节，最大允许：{max_size}字节～")
    except PermissionError:
        raise PermissionError(f"杂鱼♡～没有权限检查文件大小喵：{file_path}～") 