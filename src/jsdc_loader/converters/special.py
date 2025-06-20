"""杂鱼♡～这是本喵为特殊类型写的转换器喵～处理UUID、datetime、Enum等复杂类型♡～"""

import uuid
import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Type, get_origin, get_args

from .base import BaseConverter
from ..schema.field_schema import FieldSchema

# 杂鱼♡～尝试导入Literal类型喵～
try:
    from typing import Literal
except ImportError:
    Literal = None


class SpecialConverter(BaseConverter):
    """杂鱼♡～特殊类型转换器喵～处理各种特殊的Python类型♡～"""
    
    def get_priority(self) -> int:
        # 杂鱼♡～特殊类型优先级较高喵～
        return 20
    
    def can_convert(self, target_type: Type) -> bool:
        """杂鱼♡～检查是否能转换指定类型喵～"""
        # 杂鱼♡～UUID类型喵～
        if target_type is uuid.UUID:
            return True
        
        # 杂鱼♡～datetime相关类型喵～
        datetime_types = {
            datetime.datetime, datetime.date, datetime.time, datetime.timedelta
        }
        if target_type in datetime_types:
            return True
        
        # 杂鱼♡～Decimal类型喵～
        if target_type is Decimal:
            return True
        
        # 杂鱼♡～Enum类型喵～
        if isinstance(target_type, type) and issubclass(target_type, Enum):
            return True
        
        # 杂鱼♡～bytes和bytearray类型喵～
        if target_type in (bytes, bytearray):
            return True
        
        # 杂鱼♡～Literal类型喵～需要特殊检查origin喵～
        if Literal:
            origin = get_origin(target_type)
            if origin is Literal:
                return True
        
        # 杂鱼♡～处理typing.Any类型喵～
        import typing
        if target_type is typing.Any:
            return True
        
        return False
    
    def convert(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～执行特殊类型转换喵～
        
        Args:
            value: 要转换的值
            field_schema: 字段模式信息
            
        Returns:
            Any: 转换后的值
            
        Raises:
            ValueError: 转换失败时
        """
        target_type = field_schema.exact_type
        field_path = field_schema.field_path
        
        try:
            # 杂鱼♡～处理None值喵～
            if value is None:
                if field_schema.is_optional:
                    return None
                else:
                    raise ValueError(f"杂鱼♡～字段 '{field_path}' 不允许为None喵！～")
            
            # 杂鱼♡～优先使用自定义解码器喵～
            if field_schema.custom_decoder:
                try:
                    return self.apply_custom_decoder(value, field_schema)
                except Exception as e:
                    # 杂鱼♡～自定义解码器失败，继续使用默认处理喵～
                    pass
            
            # 杂鱼♡～UUID转换喵～
            if target_type is uuid.UUID:
                if isinstance(value, str):
                    return uuid.UUID(value)
                elif isinstance(value, uuid.UUID):
                    return value
                else:
                    raise ValueError(f"杂鱼♡～无法将 {type(value)} 转换为UUID喵！～")
            
            # 杂鱼♡～datetime转换喵～
            if target_type is datetime.datetime:
                if isinstance(value, str):
                    # 杂鱼♡～尝试多种datetime格式喵～
                    formats = [
                        "%Y-%m-%d %H:%M:%S.%f",
                        "%Y-%m-%d %H:%M:%S",
                        "%Y-%m-%dT%H:%M:%S.%f",
                        "%Y-%m-%dT%H:%M:%S",
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                        "%Y-%m-%dT%H:%M:%SZ"
                    ]
                    for fmt in formats:
                        try:
                            return datetime.datetime.strptime(value, fmt)
                        except ValueError:
                            continue
                    raise ValueError(f"杂鱼♡～无法解析datetime字符串 '{value}' 喵！～")
                elif isinstance(value, datetime.datetime):
                    return value
                elif isinstance(value, (int, float)):
                    return datetime.datetime.fromtimestamp(value)
                else:
                    raise ValueError(f"杂鱼♡～无法将 {type(value)} 转换为datetime喵！～")
            
            # 杂鱼♡～date转换喵～
            if target_type is datetime.date:
                if isinstance(value, str):
                    try:
                        return datetime.datetime.strptime(value, "%Y-%m-%d").date()
                    except ValueError:
                        raise ValueError(f"杂鱼♡～无法解析date字符串 '{value}' 喵！～")
                elif isinstance(value, datetime.date):
                    return value
                elif isinstance(value, datetime.datetime):
                    return value.date()
                else:
                    raise ValueError(f"杂鱼♡～无法将 {type(value)} 转换为date喵！～")
            
            # 杂鱼♡～time转换喵～
            if target_type is datetime.time:
                if isinstance(value, str):
                    formats = ["%H:%M:%S.%f", "%H:%M:%S", "%H:%M"]
                    for fmt in formats:
                        try:
                            return datetime.datetime.strptime(value, fmt).time()
                        except ValueError:
                            continue
                    raise ValueError(f"杂鱼♡～无法解析time字符串 '{value}' 喵！～")
                elif isinstance(value, datetime.time):
                    return value
                elif isinstance(value, datetime.datetime):
                    return value.time()
                else:
                    raise ValueError(f"杂鱼♡～无法将 {type(value)} 转换为time喵！～")
            
            # 杂鱼♡～timedelta转换喵～
            if target_type is datetime.timedelta:
                if isinstance(value, (int, float)):
                    return datetime.timedelta(seconds=value)
                elif isinstance(value, str):
                    # 杂鱼♡～简单的秒数字符串喵～
                    try:
                        return datetime.timedelta(seconds=float(value))
                    except ValueError:
                        raise ValueError(f"杂鱼♡～无法解析timedelta字符串 '{value}' 喵！～")
                elif isinstance(value, datetime.timedelta):
                    return value
                else:
                    raise ValueError(f"杂鱼♡～无法将 {type(value)} 转换为timedelta喵！～")
            
            # 杂鱼♡～Decimal转换喵～
            if target_type is Decimal:
                if isinstance(value, (str, int, float)):
                    return Decimal(str(value))
                elif isinstance(value, Decimal):
                    return value
                else:
                    raise ValueError(f"杂鱼♡～无法将 {type(value)} 转换为Decimal喵！～")
            
            # 杂鱼♡～Enum转换喵～
            if isinstance(target_type, type) and issubclass(target_type, Enum):
                # 杂鱼♡～尝试按值查找枚举喵～
                if isinstance(value, str):
                    # 杂鱼♡～先尝试按名称查找喵～
                    try:
                        return target_type[value]
                    except KeyError:
                        pass
                    
                    # 杂鱼♡～再尝试按值查找喵～
                    for enum_item in target_type:
                        if enum_item.value == value:
                            return enum_item
                    
                    raise ValueError(f"杂鱼♡～枚举 {target_type.__name__} 中没有值 '{value}' 喵！～")
                
                elif isinstance(value, (int, float)):
                    # 杂鱼♡～数值型枚举喵～
                    for enum_item in target_type:
                        if enum_item.value == value:
                            return enum_item
                    raise ValueError(f"杂鱼♡～枚举 {target_type.__name__} 中没有值 {value} 喵！～")
                
                elif isinstance(value, target_type):
                    return value
                else:
                    raise ValueError(f"杂鱼♡～无法将 {type(value)} 转换为枚举 {target_type.__name__} 喵！～")
            
            # 杂鱼♡～bytes转换喵～
            if target_type is bytes:
                if isinstance(value, str):
                    return value.encode('utf-8')
                elif isinstance(value, bytes):
                    return value
                elif isinstance(value, bytearray):
                    return bytes(value)
                elif isinstance(value, list):
                    # 杂鱼♡～字节数组喵～
                    return bytes(value)
                else:
                    raise ValueError(f"杂鱼♡～无法将 {type(value)} 转换为bytes喵！～")
            
            # 杂鱼♡～bytearray转换喵～
            if target_type is bytearray:
                if isinstance(value, str):
                    return bytearray(value.encode('utf-8'))
                elif isinstance(value, (bytes, bytearray)):
                    return bytearray(value)
                elif isinstance(value, list):
                    # 杂鱼♡～字节数组喵～
                    return bytearray(value)
                else:
                    raise ValueError(f"杂鱼♡～无法将 {type(value)} 转换为bytearray喵！～")
            
            # 杂鱼♡～Literal类型喵～
            if Literal and get_origin(target_type) is Literal:
                literal_values = get_args(target_type)
                if value in literal_values:
                    return value
                else:
                    raise ValueError(f"杂鱼♡～值 '{value}' 不在Literal {literal_values} 中喵！～")
            
            # 杂鱼♡～typing.Any类型喵～直接返回值
            import typing
            if target_type is typing.Any:
                return value
            
            raise ValueError(f"杂鱼♡～不支持的特殊类型 {target_type} 喵！～")
            
        except Exception as e:
            raise ValueError(f"杂鱼♡～字段 '{field_path}' 特殊类型转换失败喵！～ 错误: {str(e)}") from e
    
    def convert_to_dict(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～将特殊类型序列化为JSON兼容格式喵～
        
        Args:
            value: 要序列化的特殊类型值
            field_schema: 字段模式信息
            
        Returns:
            Any: 序列化后的值（通常是字符串或基础类型）
            
        Raises:
            ValueError: 序列化失败时
        """
        target_type = field_schema.exact_type
        field_path = field_schema.field_path
        
        try:
            # 杂鱼♡～处理None值喵～
            if value is None:
                return None
            
            # 杂鱼♡～优先使用自定义编码器喵～
            if field_schema.custom_encoder:
                try:
                    return self.apply_custom_encoder(value, field_schema)
                except Exception as e:
                    # 杂鱼♡～自定义编码器失败，继续使用默认处理喵～
                    pass
            
            # 杂鱼♡～UUID序列化喵～
            if target_type is uuid.UUID:
                if isinstance(value, uuid.UUID):
                    return str(value)
                else:
                    raise ValueError(f"杂鱼♡～期望UUID类型，得到{type(value)}喵！～")
            
            # 杂鱼♡～datetime序列化喵～
            if target_type is datetime.datetime:
                if isinstance(value, datetime.datetime):
                    return value.isoformat()
                else:
                    raise ValueError(f"杂鱼♡～期望datetime类型，得到{type(value)}喵！～")
            
            # 杂鱼♡～date序列化喵～
            if target_type is datetime.date:
                if isinstance(value, datetime.date):
                    return value.isoformat()
                else:
                    raise ValueError(f"杂鱼♡～期望date类型，得到{type(value)}喵！～")
            
            # 杂鱼♡～time序列化喵～
            if target_type is datetime.time:
                if isinstance(value, datetime.time):
                    return value.isoformat()
                else:
                    raise ValueError(f"杂鱼♡～期望time类型，得到{type(value)}喵！～")
            
            # 杂鱼♡～timedelta序列化喵～
            if target_type is datetime.timedelta:
                if isinstance(value, datetime.timedelta):
                    return value.total_seconds()
                else:
                    raise ValueError(f"杂鱼♡～期望timedelta类型，得到{type(value)}喵！～")
            
            # 杂鱼♡～Decimal序列化喵～
            if target_type is Decimal:
                if isinstance(value, Decimal):
                    return str(value)
                else:
                    raise ValueError(f"杂鱼♡～期望Decimal类型，得到{type(value)}喵！～")
            
            # 杂鱼♡～Enum序列化喵～
            if isinstance(target_type, type) and issubclass(target_type, Enum):
                if isinstance(value, target_type):
                    return value.value
                else:
                    raise ValueError(f"杂鱼♡～期望{target_type.__name__}类型，得到{type(value)}喵！～")
            
            # 杂鱼♡～bytes序列化喵～
            if target_type is bytes:
                if isinstance(value, bytes):
                    # 杂鱼♡～Base64编码喵～
                    import base64
                    return base64.b64encode(value).decode('ascii')
                else:
                    raise ValueError(f"杂鱼♡～期望bytes类型，得到{type(value)}喵！～")
            
            # 杂鱼♡～bytearray序列化喵～
            if target_type is bytearray:
                if isinstance(value, bytearray):
                    # 杂鱼♡～转换为bytes然后Base64编码喵～
                    import base64
                    return base64.b64encode(bytes(value)).decode('ascii')
                else:
                    raise ValueError(f"杂鱼♡～期望bytearray类型，得到{type(value)}喵！～")
            
            # 杂鱼♡～Literal类型序列化喵～
            if Literal and get_origin(target_type) is Literal:
                # 杂鱼♡～Literal值直接序列化喵～
                return value
            
            # 杂鱼♡～typing.Any类型序列化喵～根据实际值类型处理
            import typing
            if target_type is typing.Any:
                # 杂鱼♡～Any类型根据实际值的类型进行序列化喵～
                actual_type = type(value)
                if actual_type in (str, int, float, bool, type(None)):
                    # 杂鱼♡～基本JSON类型，直接返回喵～
                    return value
                elif actual_type in (list, dict):
                    # 杂鱼♡～容器类型，直接返回让JSON处理喵～
                    return value
                else:
                    # 杂鱼♡～其他类型转换为字符串喵～
                    return str(value)
            
            # 杂鱼♡～其他特殊类型，转换为字符串喵～
            return str(value)
            
        except Exception as e:
            raise ValueError(f"杂鱼♡～字段 '{field_path}' 特殊类型序列化失败喵！～ 错误: {str(e)}") from e 