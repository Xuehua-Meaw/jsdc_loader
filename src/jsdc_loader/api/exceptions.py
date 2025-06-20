"""杂鱼♡～这是本喵定义的异常类喵～让错误消息更清晰♡～"""

from typing import Any, Optional, Type


class JSDCError(Exception):
    """杂鱼♡～JSDC Loader的基础异常类喵～"""
    pass


class ConversionError(JSDCError):
    """杂鱼♡～转换过程中的错误喵～包含详细的字段路径信息♡～"""
    
    def __init__(
        self, 
        message: str, 
        field_path: Optional[str] = None,
        expected_type: Optional[Type] = None,
        actual_value: Optional[Any] = None
    ):
        super().__init__(message)
        self.field_path = field_path
        self.expected_type = expected_type
        self.actual_value = actual_value


class SchemaError(JSDCError):
    """杂鱼♡～Schema构建过程中的错误喵～"""
    pass


class ValidationError(JSDCError):
    """杂鱼♡～类型验证错误喵～"""
    pass 