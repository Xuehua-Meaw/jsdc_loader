"""杂鱼♡～这是本喵定义的Schema数据结构喵～让类型转换更有条理♡～"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, Callable
from enum import Enum


class ConverterType(Enum):
    """杂鱼♡～转换器类型枚举喵～"""
    BASIC = "basic"          # str, int, float, bool
    CONTAINER = "container"  # List, Dict, Set, Tuple, Deque  
    SPECIAL = "special"      # UUID, datetime, Enum, Decimal
    DATACLASS = "dataclass"  # 嵌套dataclass
    UNION = "union"          # Union类型


@dataclass
class FieldSchema:
    """杂鱼♡～字段Schema定义喵～包含转换所需的所有信息♡～"""
    field_path: str                           # 字段路径，如 "user.settings.theme"
    exact_type: Type                          # 精确的类型
    converter_type: ConverterType             # 使用的转换器类型
    sub_schema: Optional['TypeSchema'] = None # 嵌套类型的子Schema
    is_optional: bool = False                 # 是否可选（包含None）
    union_types: Optional[List[Type]] = None  # Union类型的所有选项
    
    # 杂鱼♡～新增字段配置支持喵～
    custom_encoder: Optional[Callable[[Any], Any]] = None     # 自定义编码器
    custom_decoder: Optional[Callable[[Any], Any]] = None     # 自定义解码器  
    json_field_name: Optional[str] = None                     # JSON中的字段名
    exclude_if_none: bool = False                             # None时排除
    exclude_if_default: bool = False                          # 默认值时排除
    description: Optional[str] = None                         # 字段描述
    examples: Optional[List[Any]] = None                      # 示例值


@dataclass  
class TypeSchema:
    """杂鱼♡～完整的类型Schema喵～包含所有字段的转换信息♡～"""
    root_type: Type                           # 根类型
    field_schemas: Dict[str, FieldSchema]     # 字段路径 -> 字段Schema映射
    cache_key: str                            # 缓存键值
    
    # 杂鱼♡～新增类级别配置支持喵～
    global_letter_case: Optional[str] = None         # 全局命名格式
    unhandled_keys_strategy: str = "exclude"         # 未知字段处理策略
    exclude_none_globally: bool = False              # 全局排除None值
    validate_schema: bool = False                    # 启用Schema验证 