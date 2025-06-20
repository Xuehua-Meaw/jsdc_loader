"""杂鱼♡～Python内置类型全面测试喵～"""

import array
import datetime
import fractions
import ipaddress
import pathlib
import re
import sys
import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List

from src.jsdc_loader import jsdc_dump, jsdc_load, jsdc_dumps, jsdc_loads

# 杂鱼♡～基本类型测试喵～
@dataclass
class BasicTypesTest:
    """杂鱼♡～测试基本内置类型喵～"""
    my_int: int = 42
    my_float: float = 3.14159
    my_str: str = "杂鱼♡～测试字符串喵～"
    my_bool: bool = True
    my_none: None = None

# 杂鱼♡～二进制类型测试喵～
@dataclass 
class BinaryTypesTest:
    """杂鱼♡～测试二进制类型喵～"""
    my_bytes: bytes = b"Hello World \x00\x01\x02"
    my_bytearray: bytearray = field(default_factory=lambda: bytearray(b"Mutable bytes \xff\xfe"))

# 杂鱼♡～数值类型测试喵～
@dataclass
class NumericTypesTest:
    """杂鱼♡～测试数值类型喵～"""
    my_complex: complex = complex(3.5, 4.2)
    my_decimal: Decimal = Decimal("123.456789012345678901234567890")
    my_fraction: fractions.Fraction = fractions.Fraction(355, 113)  # 近似π
    my_big_int: int = 12345678901234567890123456789
    my_negative_float: float = -3.14159e-10
    my_infinity: float = float('inf')
    my_neg_infinity: float = float('-inf')

# 杂鱼♡～集合和序列类型测试喵～
@dataclass
class CollectionTypesTest:
    """杂鱼♡～测试集合和序列类型喵～"""
    my_range: range = range(5, 20, 3)  # [5, 8, 11, 14, 17]
    my_slice_full: slice = slice(1, 10, 2)  # slice(1, 10, 2)
    my_slice_start_only: slice = slice(5)  # slice(None, 5, None)
    my_slice_negative: slice = slice(-5, -1)  # slice(-5, -1, None)

# 杂鱼♡～数组类型测试喵～
@dataclass
class ArrayTypesTest:
    """杂鱼♡～测试数组类型喵～"""
    my_int_array: array.array = field(default_factory=lambda: array.array('i', [1, -2, 3, -4, 5]))
    my_float_array: array.array = field(default_factory=lambda: array.array('f', [1.1, 2.2, 3.3]))
    my_double_array: array.array = field(default_factory=lambda: array.array('d', [1.11111, 2.22222, 3.33333]))
    my_byte_array: array.array = field(default_factory=lambda: array.array('b', [65, 66, 67, 68]))  # ABCD

# 杂鱼♡～路径类型测试喵～
@dataclass
class PathTypesTest:
    """杂鱼♡～测试路径类型喵～"""
    my_path: pathlib.Path = field(default_factory=lambda: pathlib.Path("/tmp/test/file.txt"))
    my_windows_path: pathlib.Path = field(default_factory=lambda: pathlib.Path(r"C:\Users\test\file.txt"))
    my_relative_path: pathlib.Path = field(default_factory=lambda: pathlib.Path("relative/path/file.txt"))
    my_pure_path: pathlib.PurePath = field(default_factory=lambda: pathlib.PurePath("pure/path/test"))

# 杂鱼♡～网络类型测试喵～
@dataclass
class NetworkTypesTest:
    """杂鱼♡～测试网络类型喵～"""
    my_ipv4: ipaddress.IPv4Address = ipaddress.IPv4Address("192.168.1.100")
    my_ipv6: ipaddress.IPv6Address = ipaddress.IPv6Address("2001:db8::1")
    my_ipv4_network: ipaddress.IPv4Network = ipaddress.IPv4Network("10.0.0.0/8")
    my_ipv6_network: ipaddress.IPv6Network = ipaddress.IPv6Network("2001:db8::/32")
    my_localhost_ipv4: ipaddress.IPv4Address = ipaddress.IPv4Address("127.0.0.1")
    my_localhost_ipv6: ipaddress.IPv6Address = ipaddress.IPv6Address("::1")

# 杂鱼♡～时间类型测试喵～
@dataclass
class TimeTypesTest:
    """杂鱼♡～测试时间类型喵～"""
    my_datetime: datetime.datetime = datetime.datetime(2024, 1, 15, 14, 30, 45, 123456)
    my_date: datetime.date = datetime.date(2024, 12, 25)
    my_time: datetime.time = datetime.time(23, 59, 59, 999999)
    my_timedelta: datetime.timedelta = datetime.timedelta(days=365, hours=12, minutes=30, seconds=45, microseconds=123456)
    my_timedelta_negative: datetime.timedelta = datetime.timedelta(days=-7, hours=-2)

# 杂鱼♡～UUID和正则表达式测试喵～
@dataclass
class MiscTypesTest:
    """杂鱼♡～测试UUID和正则表达式类型喵～"""
    my_uuid: uuid.UUID = uuid.UUID('12345678-1234-5678-1234-567812345678')
    my_random_uuid: uuid.UUID = field(default_factory=uuid.uuid4)
    my_pattern: re.Pattern = field(default_factory=lambda: re.compile(r'\d{3}-\d{2}-\d{4}', re.IGNORECASE))
    my_complex_pattern: re.Pattern = field(default_factory=lambda: re.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', re.MULTILINE))

# 杂鱼♡～综合测试数据类喵～
@dataclass
class BuiltinTypesComprehensiveTest:
    """杂鱼♡～所有内置类型的综合测试喵～"""
    basic_types: BasicTypesTest
    binary_types: BinaryTypesTest
    numeric_types: NumericTypesTest
    collection_types: CollectionTypesTest
    array_types: ArrayTypesTest
    path_types: PathTypesTest
    network_types: NetworkTypesTest
    time_types: TimeTypesTest
    misc_types: MiscTypesTest
    
    # 杂鱼♡～一些复杂的集合喵～
    mixed_list: List[object] = field(default_factory=lambda: [
        42, "string", True, 3.14, bytes([65, 66, 67])
    ])
    
    type_dict: Dict[str, object] = field(default_factory=lambda: {
        "integer": 42,
        "string": "test",
        "bytes": b"binary",
        "decimal": Decimal("123.45"),
        "complex": complex(1, 2)
    })

def create_test_data() -> BuiltinTypesComprehensiveTest:
    """杂鱼♡～创建全面的测试数据喵～"""
    return BuiltinTypesComprehensiveTest(
        basic_types=BasicTypesTest(),
        binary_types=BinaryTypesTest(),
        numeric_types=NumericTypesTest(),
        collection_types=CollectionTypesTest(),
        array_types=ArrayTypesTest(),
        path_types=PathTypesTest(),
        network_types=NetworkTypesTest(),
        time_types=TimeTypesTest(),
        misc_types=MiscTypesTest()
    )

def test_basic_types():
    """杂鱼♡～测试基本类型喵～"""
    print("🔧 测试基本类型...")
    
    original = BasicTypesTest()
    
    # 文件序列化测试
    jsdc_dump(original, "basic_types_test.json")
    loaded_file = jsdc_load("basic_types_test.json", BasicTypesTest)
    
    # 字符串序列化测试
    json_str = jsdc_dumps(original)
    loaded_str = jsdc_loads(json_str, BasicTypesTest)
    
    # 验证
    assert loaded_file.my_int == original.my_int
    assert loaded_file.my_float == original.my_float
    assert loaded_file.my_str == original.my_str
    assert loaded_file.my_bool == original.my_bool
    assert loaded_file.my_none == original.my_none
    
    assert loaded_str.my_int == original.my_int
    assert loaded_str.my_float == original.my_float
    assert loaded_str.my_str == original.my_str
    assert loaded_str.my_bool == original.my_bool
    assert loaded_str.my_none == original.my_none
    
    print("✅ 基本类型测试通过")

def test_binary_types():
    """杂鱼♡～测试二进制类型喵～"""
    print("💾 测试二进制类型...")
    
    original = BinaryTypesTest()
    
    # 序列化和反序列化
    json_str = jsdc_dumps(original)
    loaded = jsdc_loads(json_str, BinaryTypesTest)
    
    # 验证
    assert loaded.my_bytes == original.my_bytes
    assert loaded.my_bytearray == original.my_bytearray
    assert isinstance(loaded.my_bytes, bytes)
    assert isinstance(loaded.my_bytearray, bytearray)
    
    print("✅ 二进制类型测试通过")

def test_numeric_types():
    """杂鱼♡～测试数值类型喵～"""
    print("🔢 测试数值类型...")
    
    original = NumericTypesTest()
    
    # 序列化和反序列化
    json_str = jsdc_dumps(original)
    loaded = jsdc_loads(json_str, NumericTypesTest)
    
    # 验证
    assert loaded.my_complex == original.my_complex
    assert loaded.my_decimal == original.my_decimal
    assert loaded.my_fraction == original.my_fraction
    assert loaded.my_big_int == original.my_big_int
    assert loaded.my_negative_float == original.my_negative_float
    
    # 检查无穷大和NaN
    assert loaded.my_infinity == original.my_infinity
    assert loaded.my_neg_infinity == original.my_neg_infinity
    
    print("✅ 数值类型测试通过")

def test_collection_types():
    """杂鱼♡～测试集合类型喵～"""
    print("📦 测试集合类型...")
    
    original = CollectionTypesTest()
    
    # 序列化和反序列化
    json_str = jsdc_dumps(original)
    loaded = jsdc_loads(json_str, CollectionTypesTest)
    
    # 验证range
    assert list(loaded.my_range) == list(original.my_range)
    assert loaded.my_range.start == original.my_range.start
    assert loaded.my_range.stop == original.my_range.stop
    assert loaded.my_range.step == original.my_range.step
    
    # 验证slice
    assert loaded.my_slice_full == original.my_slice_full
    assert loaded.my_slice_start_only == original.my_slice_start_only
    assert loaded.my_slice_negative == original.my_slice_negative
    
    print("✅ 集合类型测试通过")

def test_array_types():
    """杂鱼♡～测试数组类型喵～"""
    print("🔢 测试数组类型...")
    
    original = ArrayTypesTest()
    
    # 序列化和反序列化
    json_str = jsdc_dumps(original)
    loaded = jsdc_loads(json_str, ArrayTypesTest)
    
    # 验证
    assert loaded.my_int_array.typecode == original.my_int_array.typecode
    assert list(loaded.my_int_array) == list(original.my_int_array)
    
    assert loaded.my_float_array.typecode == original.my_float_array.typecode
    assert list(loaded.my_float_array) == list(original.my_float_array)
    
    assert loaded.my_double_array.typecode == original.my_double_array.typecode
    assert list(loaded.my_double_array) == list(original.my_double_array)
    
    assert loaded.my_byte_array.typecode == original.my_byte_array.typecode
    assert list(loaded.my_byte_array) == list(original.my_byte_array)
    
    print("✅ 数组类型测试通过")

def test_path_types():
    """杂鱼♡～测试路径类型喵～"""
    print("📁 测试路径类型...")
    
    original = PathTypesTest()
    
    # 序列化和反序列化
    json_str = jsdc_dumps(original)
    loaded = jsdc_loads(json_str, PathTypesTest)
    
    # 验证
    assert loaded.my_path == original.my_path
    assert loaded.my_windows_path == original.my_windows_path
    assert loaded.my_relative_path == original.my_relative_path
    assert loaded.my_pure_path == original.my_pure_path
    
    # 验证类型
    assert isinstance(loaded.my_path, pathlib.Path)
    assert isinstance(loaded.my_pure_path, pathlib.PurePath)
    
    print("✅ 路径类型测试通过")

def test_network_types():
    """杂鱼♡～测试网络类型喵～"""
    print("🌐 测试网络类型...")
    
    original = NetworkTypesTest()
    
    # 序列化和反序列化
    json_str = jsdc_dumps(original)
    loaded = jsdc_loads(json_str, NetworkTypesTest)
    
    # 验证
    assert loaded.my_ipv4 == original.my_ipv4
    assert loaded.my_ipv6 == original.my_ipv6
    assert loaded.my_ipv4_network == original.my_ipv4_network
    assert loaded.my_ipv6_network == original.my_ipv6_network
    assert loaded.my_localhost_ipv4 == original.my_localhost_ipv4
    assert loaded.my_localhost_ipv6 == original.my_localhost_ipv6
    
    # 验证类型
    assert isinstance(loaded.my_ipv4, ipaddress.IPv4Address)
    assert isinstance(loaded.my_ipv6, ipaddress.IPv6Address)
    assert isinstance(loaded.my_ipv4_network, ipaddress.IPv4Network)
    assert isinstance(loaded.my_ipv6_network, ipaddress.IPv6Network)
    
    print("✅ 网络类型测试通过")

def test_time_types():
    """杂鱼♡～测试时间类型喵～"""
    print("⏰ 测试时间类型...")
    
    original = TimeTypesTest()
    
    # 序列化和反序列化
    json_str = jsdc_dumps(original)
    loaded = jsdc_loads(json_str, TimeTypesTest)
    
    # 验证
    assert loaded.my_datetime == original.my_datetime
    assert loaded.my_date == original.my_date
    assert loaded.my_time == original.my_time
    assert loaded.my_timedelta == original.my_timedelta
    assert loaded.my_timedelta_negative == original.my_timedelta_negative
    
    # 验证类型
    assert isinstance(loaded.my_datetime, datetime.datetime)
    assert isinstance(loaded.my_date, datetime.date)
    assert isinstance(loaded.my_time, datetime.time)
    assert isinstance(loaded.my_timedelta, datetime.timedelta)
    
    print("✅ 时间类型测试通过")

def test_misc_types():
    """杂鱼♡～测试UUID和正则表达式类型喵～"""
    print("🔧 测试杂项类型...")
    
    original = MiscTypesTest()
    
    # 序列化和反序列化
    json_str = jsdc_dumps(original)
    loaded = jsdc_loads(json_str, MiscTypesTest)
    
    # 验证UUID
    assert loaded.my_uuid == original.my_uuid
    assert loaded.my_random_uuid == original.my_random_uuid
    assert isinstance(loaded.my_uuid, uuid.UUID)
    assert isinstance(loaded.my_random_uuid, uuid.UUID)
    
    # 验证正则表达式
    assert loaded.my_pattern.pattern == original.my_pattern.pattern
    assert loaded.my_pattern.flags == original.my_pattern.flags
    assert loaded.my_complex_pattern.pattern == original.my_complex_pattern.pattern
    assert loaded.my_complex_pattern.flags == original.my_complex_pattern.flags
    
    print("✅ 杂项类型测试通过")

def test_comprehensive():
    """杂鱼♡～综合测试所有类型喵～"""
    print("🎯 综合测试所有内置类型...")
    
    original = create_test_data()
    
    # 文件序列化测试
    jsdc_dump(original, "builtin_comprehensive_test.json")
    loaded_file = jsdc_load("builtin_comprehensive_test.json", BuiltinTypesComprehensiveTest)
    
    # 字符串序列化测试
    json_str = jsdc_dumps(original)
    loaded_str = jsdc_loads(json_str, BuiltinTypesComprehensiveTest)
    
    # 验证基本完整性
    assert isinstance(loaded_file, BuiltinTypesComprehensiveTest)
    assert isinstance(loaded_str, BuiltinTypesComprehensiveTest)
    
    # 验证部分关键字段
    assert loaded_file.basic_types.my_int == original.basic_types.my_int
    assert loaded_file.numeric_types.my_complex == original.numeric_types.my_complex
    assert loaded_file.path_types.my_path == original.path_types.my_path
    assert loaded_file.network_types.my_ipv4 == original.network_types.my_ipv4
    
    assert loaded_str.basic_types.my_str == original.basic_types.my_str
    assert loaded_str.binary_types.my_bytes == original.binary_types.my_bytes
    assert loaded_str.time_types.my_datetime == original.time_types.my_datetime
    assert loaded_str.misc_types.my_uuid == original.misc_types.my_uuid
    
    print("✅ 综合测试通过")

def run_all_builtin_tests():
    """杂鱼♡～运行所有内置类型测试喵～"""
    print("🚀 开始Python内置类型全面测试...")
    print(f"Python版本: {sys.version}")
    print()
    
    try:
        test_basic_types()
        test_binary_types()
        test_numeric_types()
        test_collection_types()
        test_array_types()
        test_path_types()
        test_network_types()
        test_time_types()
        test_misc_types()
        test_comprehensive()
        
        print()
        print("🎉 所有Python内置类型测试全部通过！")
        print("✅ 基本类型: int, float, str, bool")
        print("✅ 二进制类型: bytes, bytearray")
        print("✅ 数值类型: complex, Decimal, Fraction")
        print("✅ 集合类型: range, slice")
        print("✅ 数组类型: array.array")
        print("✅ 路径类型: pathlib.Path, pathlib.PurePath")
        print("✅ 网络类型: ipaddress.IPv4Address, IPv6Address等")
        print("✅ 时间类型: datetime, date, time, timedelta")
        print("✅ 杂项类型: uuid.UUID, re.Pattern")
        print()
        print("杂鱼♡～本喵的内置类型支持完美无缺喵！～")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_builtin_tests()
    if success:
        print("杂鱼♡～所有内置类型测试完美通过！本喵太厉害了～")
    else:
        print("杂鱼♡～测试失败了，需要继续改进喵～")
        exit(1) 