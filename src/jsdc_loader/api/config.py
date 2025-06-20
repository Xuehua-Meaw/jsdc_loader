"""杂鱼♡～这是本喵借鉴dataclasses-json设计的字段配置系统喵～支持自定义编码解码器♡～"""

from dataclasses import field
from typing import Any, Callable, Dict, Optional, Union
from enum import Enum


class LetterCase(Enum):
    """杂鱼♡～字段命名格式枚举喵～支持不同的命名约定♡～"""
    CAMEL = "camelCase"      # firstName
    PASCAL = "PascalCase"    # FirstName  
    SNAKE = "snake_case"     # first_name
    KEBAB = "kebab-case"     # first-name


class UnhandledKeys(Enum):
    """杂鱼♡～未知字段处理策略喵～"""
    RAISE = "raise"      # 抛出异常
    EXCLUDE = "exclude"  # 忽略未知字段
    INCLUDE = "include"  # 包含在CatchAll字段中


def config(
    *,
    encoder: Optional[Callable[[Any], Any]] = None,
    decoder: Optional[Callable[[Any], Any]] = None,
    field_name: Optional[str] = None,
    letter_case: Optional[LetterCase] = None,
    exclude_if_none: bool = False,
    exclude_if_default: bool = False,
    description: Optional[str] = None,
    examples: Optional[list] = None,
    **kwargs
) -> Dict[str, Any]:
    """杂鱼♡～为dataclass字段配置自定义行为喵～
    
    Args:
        encoder: 自定义编码器函数，用于序列化
        decoder: 自定义解码器函数，用于反序列化
        field_name: 在JSON中使用的字段名（覆盖dataclass字段名）
        letter_case: 字段命名格式转换
        exclude_if_none: 如果值为None则从JSON中排除
        exclude_if_default: 如果值为默认值则从JSON中排除
        description: 字段描述（用于文档生成）
        examples: 示例值列表
        **kwargs: 其他自定义配置
        
    Returns:
        Dict[str, Any]: 配置字典，用于dataclass field的metadata
        
    Example:
        @dataclass
        class Person:
            name: str
            birth_date: datetime = field(
                metadata=config(
                    encoder=datetime.isoformat,
                    decoder=datetime.fromisoformat,
                    field_name="birthDate",
                    letter_case=LetterCase.CAMEL,
                    description="Person's birth date"
                )
            )
    """
    return {
        "jsdc_loader": {
            "encoder": encoder,
            "decoder": decoder, 
            "field_name": field_name,
            "letter_case": letter_case,
            "exclude_if_none": exclude_if_none,
            "exclude_if_default": exclude_if_default,
            "description": description,
            "examples": examples,
            **kwargs
        }
    }


def dataclass_config(
    *,
    letter_case: Optional[LetterCase] = None,
    unhandled_keys: UnhandledKeys = UnhandledKeys.EXCLUDE,
    exclude_none: bool = False,
    validate_schema: bool = False,
    **kwargs
) -> type:
    """杂鱼♡～为整个dataclass配置行为喵～用作类装饰器♡～
    
    Args:
        letter_case: 全局字段命名格式
        unhandled_keys: 未知字段处理策略
        exclude_none: 全局排除None值
        validate_schema: 启用Schema验证
        **kwargs: 其他配置
        
    Returns:
        type: 装饰器函数
        
    Example:
        @dataclass_config(letter_case=LetterCase.CAMEL, validate_schema=True)
        @dataclass
        class Person:
            first_name: str  # 在JSON中变为 "firstName"
    """
    def decorator(cls):
        # 杂鱼♡～将配置存储到类的特殊属性中喵～
        if not hasattr(cls, '__jsdc_config__'):
            cls.__jsdc_config__ = {}
        
        cls.__jsdc_config__.update({
            "letter_case": letter_case,
            "unhandled_keys": unhandled_keys,
            "exclude_none": exclude_none,
            "validate_schema": validate_schema,
            **kwargs
        })
        
        return cls
    
    return decorator


class CatchAll(dict):
    """杂鱼♡～用于捕获未知字段的特殊字典类型喵～"""
    pass


def get_field_config(field_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """杂鱼♡～从字段metadata中提取配置喵～
    
    Args:
        field_metadata: dataclass字段的metadata字典
        
    Returns:
        Dict[str, Any]: 提取的配置，如果没有配置则返回空字典
    """
    return field_metadata.get("jsdc_loader", {})


def get_dataclass_config(cls: type) -> Dict[str, Any]:
    """杂鱼♡～从dataclass中提取全局配置喵～
    
    Args:
        cls: dataclass类型
        
    Returns:
        Dict[str, Any]: 提取的配置，如果没有配置则返回空字典
    """
    return getattr(cls, "__jsdc_config__", {})


def transform_field_name(field_name: str, letter_case: LetterCase) -> str:
    """杂鱼♡～根据指定格式转换字段名喵～
    
    Args:
        field_name: 原始字段名（假设为snake_case）
        letter_case: 目标格式
        
    Returns:
        str: 转换后的字段名
    """
    if letter_case == LetterCase.SNAKE:
        return field_name
    
    # 杂鱼♡～将snake_case拆分为单词喵～
    words = field_name.split('_')
    
    if letter_case == LetterCase.CAMEL:
        # firstName
        return words[0] + ''.join(word.capitalize() for word in words[1:])
    elif letter_case == LetterCase.PASCAL:
        # FirstName
        return ''.join(word.capitalize() for word in words)
    elif letter_case == LetterCase.KEBAB:
        # first-name
        return '-'.join(words)
    
    return field_name 