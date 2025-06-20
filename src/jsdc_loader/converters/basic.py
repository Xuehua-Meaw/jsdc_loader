"""杂鱼♡～这是本喵的基础类型转换器喵～处理str、int、float、bool类型♡～"""

from typing import Any, Type

from .base import BaseConverter
from ..schema.field_schema import FieldSchema
from ..api.exceptions import ConversionError


class BasicConverter(BaseConverter):
    """杂鱼♡～基础类型转换器喵～处理基本的Python类型♡～"""
    
    # 杂鱼♡～支持的基础类型喵～
    SUPPORTED_TYPES = {str, int, float, bool}
    
    def can_convert(self, target_type: Type) -> bool:
        """杂鱼♡～检查是否可以转换指定类型喵～"""
        return target_type in self.SUPPORTED_TYPES
    
    def convert(self, value: Any, field_schema: FieldSchema) -> Any:
        """杂鱼♡～执行基础类型转换喵～
        
        Args:
            value: 要转换的值
            field_schema: 字段Schema信息
            
        Returns:
            Any: 转换后的值
            
        Raises:
            ConversionError: 转换失败时抛出
        """
        target_type = field_schema.exact_type
        field_path = field_schema.field_path
        
        if not self.can_convert(target_type):
            raise ConversionError(
                f"杂鱼♡～BasicConverter不支持类型{target_type}喵！～",
                field_path=field_path,
                expected_type=target_type,
                actual_value=value
            )
        
        # 杂鱼♡～如果值已经是目标类型，直接返回喵～
        # 注意：bool是int的子类，所以需要精确检查类型喵～
        if type(value) is target_type:
            return value
        
        # 杂鱼♡～根据目标类型进行转换喵～
        try:
            if target_type is str:
                return self._convert_to_str(value, field_path)
            elif target_type is int:
                return self._convert_to_int(value, field_path)
            elif target_type is float:
                return self._convert_to_float(value, field_path)
            elif target_type is bool:
                return self._convert_to_bool(value, field_path)
            else:
                raise ConversionError(
                    f"杂鱼♡～不支持的基础类型喵：{target_type}",
                    field_path=field_path,
                    expected_type=target_type,
                    actual_value=value
                )
                
        except Exception as e:
            if isinstance(e, ConversionError):
                raise
            else:
                raise ConversionError(
                    f"杂鱼♡～基础类型转换失败喵：{str(e)}",
                    field_path=field_path,
                    expected_type=target_type,
                    actual_value=value
                ) from e
    
    def _convert_to_str(self, value: Any, field_path: str) -> str:
        """杂鱼♡～转换为字符串类型喵～"""
        if isinstance(value, str):
            return value
        elif isinstance(value, (int, float, bool)):
            return str(value)
        elif value is None:
            raise ConversionError(
                f"杂鱼♡～不能将None转换为str喵：{field_path}",
                field_path=field_path,
                expected_type=str,
                actual_value=value
            )
        else:
            # 杂鱼♡～尝试转换其他类型喵～
            try:
                return str(value)
            except Exception as e:
                raise ConversionError(
                    f"杂鱼♡～无法将{type(value)}转换为str喵：{field_path}",
                    field_path=field_path,
                    expected_type=str,
                    actual_value=value
                ) from e
    
    def _convert_to_int(self, value: Any, field_path: str) -> int:
        """杂鱼♡～转换为整数类型喵～"""
        # 杂鱼♡～注意：bool是int的子类，但我们需要显式转换bool→int喵～
        if isinstance(value, bool):
            # 杂鱼♡～bool转int：True=1, False=0喵～
            return int(value)
        elif isinstance(value, int):
            return value
        elif isinstance(value, float):
            # 杂鱼♡～检查是否是整数值的浮点数喵～
            if value.is_integer():
                return int(value)
            else:
                raise ConversionError(
                    f"杂鱼♡～浮点数{value}不是整数值，无法转换为int喵：{field_path}",
                    field_path=field_path,
                    expected_type=int,
                    actual_value=value
                )
        elif isinstance(value, str):
            # 杂鱼♡～尝试解析字符串为整数喵～
            value = value.strip()
            if not value:
                raise ConversionError(
                    f"杂鱼♡～空字符串无法转换为int喵：{field_path}",
                    field_path=field_path,
                    expected_type=int,
                    actual_value=value
                )
            
            try:
                # 杂鱼♡～先尝试直接转换喵～
                return int(value)
            except ValueError:
                # 杂鱼♡～如果失败，尝试先转换为float再转换为int喵～
                try:
                    float_value = float(value)
                    if float_value.is_integer():
                        return int(float_value)
                    else:
                        raise ConversionError(
                            f"杂鱼♡～字符串'{value}'包含小数部分，无法转换为int喵：{field_path}",
                            field_path=field_path,
                            expected_type=int,
                            actual_value=value
                        )
                except ValueError as e:
                    raise ConversionError(
                        f"杂鱼♡～字符串'{value}'不是有效的数字格式喵：{field_path}",
                        field_path=field_path,
                        expected_type=int,
                        actual_value=value
                    ) from e
        else:
            raise ConversionError(
                f"杂鱼♡～无法将{type(value)}转换为int喵：{field_path}",
                field_path=field_path,
                expected_type=int,
                actual_value=value
            )
    
    def _convert_to_float(self, value: Any, field_path: str) -> float:
        """杂鱼♡～转换为浮点数类型喵～"""
        if isinstance(value, float):
            return value
        elif isinstance(value, (int, bool)):
            return float(value)
        elif isinstance(value, str):
            # 杂鱼♡～尝试解析字符串为浮点数喵～
            value = value.strip()
            if not value:
                raise ConversionError(
                    f"杂鱼♡～空字符串无法转换为float喵：{field_path}",
                    field_path=field_path,
                    expected_type=float,
                    actual_value=value
                )
            
            try:
                return float(value)
            except ValueError as e:
                raise ConversionError(
                    f"杂鱼♡～字符串'{value}'不是有效的浮点数格式喵：{field_path}",
                    field_path=field_path,
                    expected_type=float,
                    actual_value=value
                ) from e
        else:
            raise ConversionError(
                f"杂鱼♡～无法将{type(value)}转换为float喵：{field_path}",
                field_path=field_path,
                expected_type=float,
                actual_value=value
            )
    
    def _convert_to_bool(self, value: Any, field_path: str) -> bool:
        """杂鱼♡～转换为布尔类型喵～"""
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            # 杂鱼♡～数字转换：0为False，非0为True喵～
            return bool(value)
        elif isinstance(value, str):
            # 杂鱼♡～字符串转换：智能解析喵～
            value = value.strip().lower()
            
            # 杂鱼♡～True值喵～
            if value in ('true', 't', 'yes', 'y', '1', 'on', 'enabled'):
                return True
            # 杂鱼♡～False值喵～
            elif value in ('false', 'f', 'no', 'n', '0', 'off', 'disabled', ''):
                return False
            else:
                raise ConversionError(
                    f"杂鱼♡～字符串'{value}'无法解析为布尔值喵：{field_path}。"
                    f"支持的值：true/false, yes/no, 1/0, on/off等",
                    field_path=field_path,
                    expected_type=bool,
                    actual_value=value
                )
        elif value is None:
            raise ConversionError(
                f"杂鱼♡～None值无法转换为bool喵：{field_path}",
                field_path=field_path,
                expected_type=bool,
                actual_value=value
            )
        else:
            # 杂鱼♡～其他类型使用Python的bool()函数喵～
            try:
                return bool(value)
            except Exception as e:
                raise ConversionError(
                    f"杂鱼♡～无法将{type(value)}转换为bool喵：{field_path}",
                    field_path=field_path,
                    expected_type=bool,
                    actual_value=value
                ) from e
    
    def get_priority(self) -> int:
        """杂鱼♡～基础类型转换器优先级很高喵～"""
        return 10  # 杂鱼♡～优先级较高，数字越小优先级越高喵～


 