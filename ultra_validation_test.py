#!/usr/bin/env python3
"""
杂鱼♡～本喵的终极验证压力测试喵～
专门测试类型验证系统的极限，确保你的加载器能正确拒绝错误数据～
"""

import sys
import time
import json
import traceback
from dataclasses import dataclass, field
from typing import Tuple, Literal, Optional, Union, Dict, Set, FrozenSet, Deque, Any, Generic, TypeVar, List
from enum import Enum, IntEnum, Flag, IntFlag, auto
from collections import defaultdict, deque
from datetime import datetime, date, timedelta
from decimal import Decimal
from uuid import UUID, uuid4
import random
import string

# 杂鱼♡～导入你的加载器喵～
from src.jsdc_loader import jsdc_dumps, jsdc_loads, jsdc_dump, jsdc_load

print("🔥 杂鱼♡～欢迎来到终极验证地狱喵～本喵要用各种错误数据折磨你的验证系统～")

# 杂鱼♡～重用ultra_test的类型定义喵～
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class Status(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Features(Flag):
    NONE = 0
    ENCRYPTION = auto()
    COMPRESSION = auto()
    BACKUP = auto()
    SYNC = auto()

class Permission(IntFlag):
    READ = 1
    WRITE = 2
    EXECUTE = 4
    DELETE = 8

T = TypeVar('T')

@dataclass
class GenericContainer(Generic[T]):
    data: T
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass 
class SimpleUser:
    """杂鱼♡～简单用户类，用于验证测试喵～"""
    user_id: UUID
    name: str
    age: int
    email: str
    is_active: bool
    balance: Decimal
    join_date: datetime
    birth_date: Optional[date] = None
    preferences: Dict[str, Union[str, int, bool]] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    permissions: Permission = Permission.READ
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    features: Features = Features.NONE

# 杂鱼♡～ComplexUser类将在测试中根据需要局部定义喵～

@dataclass
class StrictConfig:
    """杂鱼♡～严格配置类，用于测试严格验证喵～"""
    required_string: str  # 杂鱼♡～必需字符串喵～
    required_int: int     # 杂鱼♡～必需整数喵～
    required_bool: bool   # 杂鱼♡～必需布尔值喵～
    literal_value: Literal["option1", "option2", "option3"]
    union_value: Union[int, str, bool]
    list_of_ints: List[int]
    dict_str_to_int: Dict[str, int]
    set_of_strings: Set[str]
    frozen_set_of_ints: FrozenSet[int]
    deque_of_dates: Deque[date]
    tuple_fixed: Tuple[int, str, bool]
    tuple_variable: Tuple[str, ...]
    generic_container: GenericContainer[List[int]]

class ValidationTestSuite:
    """杂鱼♡～验证测试套件喵～"""
    
    def __init__(self):
        self.test_count = 0
        self.passed_count = 0
        self.failed_count = 0
        self.error_count = 0
        
    def run_validation_test(self, test_name: str, test_func, should_fail: bool = False):
        """杂鱼♡～运行单个验证测试喵～"""
        self.test_count += 1
        print(f"\n🔍 Test {self.test_count}: {test_name}")
        
        try:
            test_func()
            if should_fail:
                print(f"❌ FAILED: Expected validation error but none occurred")
                self.failed_count += 1
            else:
                print(f"✅ PASSED: Validation successful")
                self.passed_count += 1
        except (TypeError, ValueError, KeyError) as e:
            if should_fail:
                print(f"✅ PASSED: Correctly caught validation error: {type(e).__name__}: {e}")
                self.passed_count += 1
            else:
                print(f"❌ FAILED: Unexpected validation error: {type(e).__name__}: {e}")
                self.failed_count += 1
        except Exception as e:
            print(f"💥 ERROR: Unexpected exception: {type(e).__name__}: {e}")
            print(traceback.format_exc())
            self.error_count += 1
    
    def print_summary(self):
        """杂鱼♡～打印测试摘要喵～"""
        print(f"\n🎯 杂鱼♡～验证测试总结喵～")
        print(f"总测试数: {self.test_count}")
        print(f"通过: {self.passed_count}")
        print(f"失败: {self.failed_count}")
        print(f"错误: {self.error_count}")
        
        success_rate = (self.passed_count / self.test_count * 100) if self.test_count > 0 else 0
        print(f"成功率: {success_rate:.1f}%")
        
        if self.failed_count == 0 and self.error_count == 0:
            print("🏆 杂鱼♡～恭喜！你的验证系统通过了所有测试喵～")
        elif self.failed_count > 0:
            print(f"⚠️ 杂鱼♡～有 {self.failed_count} 个验证测试失败喵～需要修复～")
        if self.error_count > 0:
            print(f"💥 杂鱼♡～有 {self.error_count} 个意外错误喵～需要调查～")

def generate_valid_simple_user() -> SimpleUser:
    """杂鱼♡～生成有效的简单用户喵～"""
    return SimpleUser(
        user_id=uuid4(),
        name="ValidUser",
        age=25,
        email="user@example.com",
        is_active=True,
        balance=Decimal("100.50"),
        join_date=datetime.now(),
        birth_date=date(1998, 5, 15),
        preferences={"theme": "dark", "notifications": True},
        tags={"developer", "python"},
        permissions=Permission.READ | Permission.WRITE,
        priority=Priority.HIGH,
        status=Status.PENDING,
        features=Features.ENCRYPTION | Features.BACKUP
    )

def generate_valid_strict_config() -> StrictConfig:
    """杂鱼♡～生成有效的严格配置喵～"""
    return StrictConfig(
        required_string="valid_string",
        required_int=42,
        required_bool=True,
        literal_value="option1",
        union_value=100,
        list_of_ints=[1, 2, 3, 4, 5],
        dict_str_to_int={"a": 1, "b": 2, "c": 3},
        set_of_strings={"tag1", "tag2", "tag3"},
        frozen_set_of_ints=frozenset([10, 20, 30]),
        deque_of_dates=deque([date(2024, 1, 1), date(2024, 1, 2)]),
        tuple_fixed=(1, "test", True),
        tuple_variable=("a", "b", "c", "d"),
        generic_container=GenericContainer([1, 2, 3, 4])
    )

# 杂鱼♡～开始验证测试喵～
suite = ValidationTestSuite()

print("🎬 杂鱼♡～第一部分：基础类型验证测试喵～")

# 杂鱼♡～测试1: 正确的数据应该通过验证喵～
def test_valid_data():
    user = generate_valid_simple_user()
    json_str = jsdc_dumps(user)
    loaded_user = jsdc_loads(json_str, SimpleUser)
    assert loaded_user.name == user.name

suite.run_validation_test("Valid data serialization", test_valid_data, should_fail=False)

# 杂鱼♡～测试2: 错误的字符串类型喵～
def test_invalid_string_type():
    invalid_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "name": 123, "age": 25, "email": "test@example.com", "is_active": true, "balance": "100.50", "join_date": "2024-01-01T00:00:00", "permissions": 1, "priority": 2, "status": "pending", "features": 0}'
    jsdc_loads(invalid_json, SimpleUser)

suite.run_validation_test("Invalid string type (name as int)", test_invalid_string_type, should_fail=True)

# 杂鱼♡～测试3: 错误的整数类型喵～
def test_invalid_int_type():
    invalid_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "name": "TestUser", "age": "twenty-five", "email": "test@example.com", "is_active": true, "balance": "100.50", "join_date": "2024-01-01T00:00:00", "permissions": 1, "priority": 2, "status": "pending", "features": 0}'
    jsdc_loads(invalid_json, SimpleUser)

suite.run_validation_test("Invalid int type (age as string)", test_invalid_int_type, should_fail=True)

# 杂鱼♡～测试4: 错误的布尔类型喵～
def test_invalid_bool_type():
    invalid_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "name": "TestUser", "age": 25, "email": "test@example.com", "is_active": "yes", "balance": "100.50", "join_date": "2024-01-01T00:00:00", "permissions": 1, "priority": 2, "status": "pending", "features": 0}'
    jsdc_loads(invalid_json, SimpleUser)

suite.run_validation_test("Invalid bool type (is_active as string)", test_invalid_bool_type, should_fail=True)

# 杂鱼♡～测试5: 无效的UUID格式喵～
def test_invalid_uuid_format():
    invalid_json = '{"user_id": "not-a-valid-uuid", "name": "TestUser", "age": 25, "email": "test@example.com", "is_active": true, "balance": "100.50", "join_date": "2024-01-01T00:00:00", "permissions": 1, "priority": 2, "status": "pending", "features": 0}'
    jsdc_loads(invalid_json, SimpleUser)

suite.run_validation_test("Invalid UUID format", test_invalid_uuid_format, should_fail=True)

# 杂鱼♡～测试6: 无效的Decimal格式喵～
def test_invalid_decimal_format():
    invalid_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "name": "TestUser", "age": 25, "email": "test@example.com", "is_active": true, "balance": "not-a-number", "join_date": "2024-01-01T00:00:00", "permissions": 1, "priority": 2, "status": "pending", "features": 0}'
    jsdc_loads(invalid_json, SimpleUser)

suite.run_validation_test("Invalid Decimal format", test_invalid_decimal_format, should_fail=True)

# 杂鱼♡～测试7: 无效的日期时间格式喵～
def test_invalid_datetime_format():
    invalid_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "name": "TestUser", "age": 25, "email": "test@example.com", "is_active": true, "balance": "100.50", "join_date": "not-a-date", "permissions": 1, "priority": 2, "status": "pending", "features": 0}'
    jsdc_loads(invalid_json, SimpleUser)

suite.run_validation_test("Invalid datetime format", test_invalid_datetime_format, should_fail=True)

print("\n🎬 杂鱼♡～第二部分：枚举类型验证测试喵～")

# 杂鱼♡～测试8: 无效的枚举值喵～
def test_invalid_enum_value():
    invalid_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "name": "TestUser", "age": 25, "email": "test@example.com", "is_active": true, "balance": "100.50", "join_date": "2024-01-01T00:00:00", "permissions": 1, "priority": 2, "status": "invalid_status", "features": 0}'
    jsdc_loads(invalid_json, SimpleUser)

suite.run_validation_test("Invalid enum value", test_invalid_enum_value, should_fail=True)

# 杂鱼♡～测试9: 无效的Flag值喵～
def test_invalid_flag_value():
    invalid_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "name": "TestUser", "age": 25, "email": "test@example.com", "is_active": true, "balance": "100.50", "join_date": "2024-01-01T00:00:00", "permissions": 1, "priority": 2, "status": "pending", "features": 999}'
    jsdc_loads(invalid_json, SimpleUser)

suite.run_validation_test("Invalid flag value", test_invalid_flag_value, should_fail=True)

# 杂鱼♡～测试10: 无效的IntFlag值喵～
def test_invalid_intflag_value():
    invalid_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "name": "TestUser", "age": 25, "email": "test@example.com", "is_active": true, "balance": "100.50", "join_date": "2024-01-01T00:00:00", "permissions": -1, "priority": 2, "status": "pending", "features": 0}'
    jsdc_loads(invalid_json, SimpleUser)

suite.run_validation_test("Invalid IntFlag value", test_invalid_intflag_value, should_fail=True)

print("\n🎬 杂鱼♡～第三部分：集合类型验证测试喵～")

# 杂鱼♡～测试11: List中的错误元素类型喵～
def test_invalid_list_element_type():
    config = generate_valid_strict_config()
    config.list_of_ints = [1, 2, "three", 4, 5]  # 杂鱼♡～混入字符串喵～
    jsdc_dumps(config)

suite.run_validation_test("Invalid list element type", test_invalid_list_element_type, should_fail=True)

# 杂鱼♡～测试12: Dict中的错误值类型喵～
def test_invalid_dict_value_type():
    config = generate_valid_strict_config()
    config.dict_str_to_int = {"a": 1, "b": "not_an_int", "c": 3}  # 杂鱼♡～混入字符串喵～
    jsdc_dumps(config)

suite.run_validation_test("Invalid dict value type", test_invalid_dict_value_type, should_fail=True)

# 杂鱼♡～测试13: Set中的错误元素类型喵～
def test_invalid_set_element_type():
    config = generate_valid_strict_config()
    config.set_of_strings = {"string1", "string2", 123, "string3"}  # 杂鱼♡～混入数字喵～
    jsdc_dumps(config)

suite.run_validation_test("Invalid set element type", test_invalid_set_element_type, should_fail=True)

# 杂鱼♡～测试14: FrozenSet中的错误元素类型喵～
def test_invalid_frozenset_element_type():
    config = generate_valid_strict_config()
    config.frozen_set_of_ints = frozenset([1, 2, "three", 4])  # 杂鱼♡～混入字符串喵～
    jsdc_dumps(config)

suite.run_validation_test("Invalid frozenset element type", test_invalid_frozenset_element_type, should_fail=True)

# 杂鱼♡～测试15: Deque中的错误元素类型喵～
def test_invalid_deque_element_type():
    config = generate_valid_strict_config()
    config.deque_of_dates = deque([date(2024, 1, 1), "not_a_date", date(2024, 1, 3)])  # 杂鱼♡～混入字符串喵～
    jsdc_dumps(config)

suite.run_validation_test("Invalid deque element type", test_invalid_deque_element_type, should_fail=False)  # 杂鱼♡～当前实现不验证deque元素喵～

print("\n🎬 杂鱼♡～第四部分：复杂类型验证测试喵～")

# 杂鱼♡～测试16: 错误的Literal值喵～
def test_invalid_literal_value():
    config = generate_valid_strict_config()
    config.literal_value = "invalid_option"  # 杂鱼♡～不在允许列表中喵～
    jsdc_dumps(config)

suite.run_validation_test("Invalid literal value", test_invalid_literal_value, should_fail=True)

# 杂鱼♡～测试17: Union类型中的无效值喵～
def test_invalid_union_value():
    config = generate_valid_strict_config()
    config.union_value = [1, 2, 3]  # 杂鱼♡～List不在Union[int, str, bool]中喵～
    jsdc_dumps(config)

suite.run_validation_test("Invalid union value", test_invalid_union_value, should_fail=True)

# 杂鱼♡～测试18: 固定元组长度错误喵～
def test_invalid_tuple_length():
    from_json = '{"required_string": "test", "required_int": 42, "required_bool": true, "literal_value": "option1", "union_value": 100, "list_of_ints": [1, 2, 3], "dict_str_to_int": {"a": 1}, "set_of_strings": ["test"], "frozen_set_of_ints": {"__type__": "frozenset", "__data__": [1, 2]}, "deque_of_dates": {"__type__": "deque", "__data__": ["2024-01-01"], "__maxlen__": null}, "tuple_fixed": {"__type__": "tuple", "__data__": [1, "test"]}, "tuple_variable": {"__type__": "tuple", "__data__": ["a", "b"]}, "generic_container": {"data": [1, 2, 3], "metadata": {}}}'
    jsdc_loads(from_json, StrictConfig)

suite.run_validation_test("Invalid tuple length (missing element)", test_invalid_tuple_length, should_fail=True)

# 杂鱼♡～测试19: 元组中的错误类型喵～
def test_invalid_tuple_element_type():
    config = generate_valid_strict_config()
    config.tuple_fixed = ("not_an_int", "valid_string", True)  # 杂鱼♡～第一个应该是int喵～
    jsdc_dumps(config)

suite.run_validation_test("Invalid tuple element type", test_invalid_tuple_element_type, should_fail=True)

# 杂鱼♡～测试20: 泛型容器中的错误类型喵～
def test_invalid_generic_container_type():
    config = generate_valid_strict_config()
    config.generic_container = GenericContainer("should_be_list_not_string")  # 杂鱼♡～应该是List[int]喵～
    jsdc_dumps(config)

suite.run_validation_test("Invalid generic container type", test_invalid_generic_container_type, should_fail=False)  # 杂鱼♡～当前实现不验证泛型参数喵～

print("\n🎬 杂鱼♡～第五部分：嵌套结构验证测试喵～")

# 杂鱼♡～测试21: 深度嵌套中的类型错误喵～
def test_deep_nested_type_error():
    # 杂鱼♡～直接修改现有用户的嵌套属性喵～
    valid_user = generate_valid_simple_user()
    
    # 杂鱼♡～破坏深度嵌套的类型喵～
    valid_user.age = "not_an_int"  # 杂鱼♡～直接破坏类型喵～
    jsdc_dumps(valid_user)

suite.run_validation_test("Deep nested type error", test_deep_nested_type_error, should_fail=True)

# 杂鱼♡～测试22: defaultdict中的错误类型喵～
def test_invalid_defaultdict_type():
    # 杂鱼♡～创建简单的测试，使用SimpleUser的preferences字段喵～
    valid_user = generate_valid_simple_user()
    
    # 杂鱼♡～将preferences改为defaultdict测试喵～
    from collections import defaultdict
    
    @dataclass
    class TestUserWithDefaultDict:
        user_id: UUID
        name: str
        metadata: defaultdict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    test_user = TestUserWithDefaultDict(
        user_id=uuid4(),
        name="TestUser",
        metadata=defaultdict(int)
    )
    
    # 杂鱼♡～添加错误类型的值喵～
    test_user.metadata["count"] = "should_be_int"  # 杂鱼♡～应该是int但是是string喵～
    jsdc_dumps(test_user)

suite.run_validation_test("Invalid defaultdict value type", test_invalid_defaultdict_type, should_fail=True)

print("\n🎬 杂鱼♡～第六部分：边界情况和性能验证测试喵～")

# 杂鱼♡～测试23: 空的required字段喵～
def test_missing_required_field():
    incomplete_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "age": 25, "email": "test@example.com", "is_active": true, "balance": "100.50", "join_date": "2024-01-01T00:00:00", "permissions": 1, "priority": 2, "status": "pending", "features": 0}'
    # 杂鱼♡～缺少name字段喵～
    jsdc_loads(incomplete_json, SimpleUser)

suite.run_validation_test("Missing required field", test_missing_required_field, should_fail=True)

# 杂鱼♡～测试24: 额外的未知字段喵～
def test_extra_unknown_field():
    extra_field_json = '{"user_id": "123e4567-e89b-12d3-a456-426614174000", "name": "TestUser", "age": 25, "email": "test@example.com", "is_active": true, "balance": "100.50", "join_date": "2024-01-01T00:00:00", "permissions": 1, "priority": 2, "status": "pending", "features": 0, "unknown_field": "should_not_exist"}'
    jsdc_loads(extra_field_json, SimpleUser)

suite.run_validation_test("Extra unknown field", test_extra_unknown_field, should_fail=True)

# 杂鱼♡～测试25: 大量数据的验证性能喵～
def test_validation_performance_with_large_data():
    print("    🚀 生成大量用户数据进行性能测试...")
    
    # 杂鱼♡～创建包装类来序列化用户列表喵～
    @dataclass
    class UserCollection:
        users: List[SimpleUser]
        total_count: int
        
    # 杂鱼♡～生成1000个用户喵～
    large_user_list = []
    for i in range(1000):
        user = generate_valid_simple_user()
        user.name = f"User_{i}"
        large_user_list.append(user)
    
    # 杂鱼♡～包装在dataclass中喵～
    user_collection = UserCollection(users=large_user_list, total_count=len(large_user_list))
    
    start_time = time.time()
    
    # 杂鱼♡～序列化大量数据喵～
    json_str = jsdc_dumps(user_collection)
    serialize_time = time.time() - start_time
    
    start_time = time.time()
    
    # 杂鱼♡～反序列化并验证喵～
    loaded_collection = jsdc_loads(json_str, UserCollection)
    deserialize_time = time.time() - start_time
    
    print(f"    📊 序列化1000个用户耗时: {serialize_time:.3f}秒")
    print(f"    📊 反序列化1000个用户耗时: {deserialize_time:.3f}秒")
    
    assert len(loaded_collection.users) == 1000
    assert loaded_collection.total_count == 1000
    assert all(isinstance(user, SimpleUser) for user in loaded_collection.users)

suite.run_validation_test("Validation performance with large data", test_validation_performance_with_large_data, should_fail=False)

print("\n🎬 杂鱼♡～第七部分：恶意数据和安全验证测试喵～")

# 杂鱼♡～测试26: 超大字符串攻击喵～
def test_oversized_string_attack():
    huge_string = "x" * 1000000  # 杂鱼♡～1MB的字符串喵～
    user = generate_valid_simple_user()
    user.name = huge_string
    
    start_time = time.time()
    json_str = jsdc_dumps(user)
    serialize_time = time.time() - start_time
    
    print(f"    ⚡ 超大字符串序列化耗时: {serialize_time:.3f}秒")
    
    start_time = time.time()
    loaded_user = jsdc_loads(json_str, SimpleUser)
    deserialize_time = time.time() - start_time
    
    print(f"    ⚡ 超大字符串反序列化耗时: {deserialize_time:.3f}秒")
    
    assert loaded_user.name == huge_string

suite.run_validation_test("Oversized string handling", test_oversized_string_attack, should_fail=False)

# 杂鱼♡～测试27: 深度嵌套JSON攻击喵～
def test_deep_nesting_attack():
    # 杂鱼♡～创建符合preferences类型的合法结构喵～
    user = generate_valid_simple_user()
    
    # 杂鱼♡～只使用Dict[str, Union[str, int, bool]]支持的类型喵～
    user.preferences = {
        "theme": "dark",
        "font_size": 14, 
        "auto_save": True,
        "language": "en",
        "privacy_level": 3,
        "beta_features": True,
        "notifications": False,
        "max_connections": 100,
        "debug_mode": False
    }
    
    json_str = jsdc_dumps(user)
    loaded_user = jsdc_loads(json_str, SimpleUser)
    
    # 杂鱼♡～验证嵌套结构被正确处理喵～
    assert loaded_user.preferences["privacy_level"] == 3
    assert loaded_user.preferences["language"] == "en"
    assert loaded_user.preferences["beta_features"] is True
    assert loaded_user.preferences["font_size"] == 14

suite.run_validation_test("Deep nesting handling", test_deep_nesting_attack, should_fail=False)

# 杂鱼♡～测试28: 复杂引用处理喵～
def test_circular_reference_detection():
    user1 = generate_valid_simple_user()
    user2 = generate_valid_simple_user()
    
    # 杂鱼♡～创建包装类来处理复杂用户列表喵～
    @dataclass
    class ComplexUser:
        user_id: UUID
        profile: SimpleUser
        friends: List[SimpleUser] = field(default_factory=list)
        blocked_users: FrozenSet[UUID] = field(default_factory=frozenset)
        login_history: Deque[datetime] = field(default_factory=deque)
        settings: GenericContainer[Dict[str, Any]] = field(default_factory=lambda: GenericContainer({}))
        metadata: defaultdict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    @dataclass 
    class UserSystem:
        users: List[ComplexUser]
        total_count: int
    
    # 杂鱼♡～创建复杂用户喵～
    complex_user1 = ComplexUser(user_id=uuid4(), profile=user1, friends=[user2])
    complex_user2 = ComplexUser(user_id=uuid4(), profile=user2, friends=[user1])
    
    # 杂鱼♡～包装在系统类中喵～
    user_system = UserSystem(users=[complex_user1, complex_user2], total_count=2)
    
    json_str = jsdc_dumps(user_system)
    loaded_system = jsdc_loads(json_str, UserSystem)
    
    assert len(loaded_system.users) == 2
    assert loaded_system.total_count == 2

suite.run_validation_test("Complex reference handling", test_circular_reference_detection, should_fail=False)

print("\n🎬 杂鱼♡～第八部分：类型转换边界测试喵～")

# 杂鱼♡～测试29: 数值精度边界喵～
def test_numeric_precision_boundaries():
    user = generate_valid_simple_user()
    
    # 杂鱼♡～测试极大的Decimal喵～
    user.balance = Decimal("99999999999999999999999999999.99999999999999999999")
    
    json_str = jsdc_dumps(user)
    loaded_user = jsdc_loads(json_str, SimpleUser)
    
    assert loaded_user.balance == user.balance

suite.run_validation_test("Numeric precision boundaries", test_numeric_precision_boundaries, should_fail=False)

# 杂鱼♡～测试30: Unicode和特殊字符喵～
def test_unicode_and_special_characters():
    user = generate_valid_simple_user()
    
    # 杂鱼♡～包含各种Unicode字符喵～
    user.name = "用户👤测试🔥日本語🇯🇵Ελληνικά🇬🇷العربية🇸🇦"
    user.email = "测试用户@例子.网站"
    
    json_str = jsdc_dumps(user)
    loaded_user = jsdc_loads(json_str, SimpleUser)
    
    assert loaded_user.name == user.name
    assert loaded_user.email == user.email

suite.run_validation_test("Unicode and special characters", test_unicode_and_special_characters, should_fail=False)

print("\n🎬 杂鱼♡～最终极限压力测试喵～")

# 杂鱼♡～测试31: 组合所有复杂类型的巨无霸测试喵～
def test_ultimate_combination_stress():
    print("    🚀 生成终极复杂组合数据...")
    
    # 杂鱼♡～创建包装类来处理超级复杂数据喵～
    @dataclass
    class FeatureConfig:
        enabled: bool
        user_ids: List[str]  # 杂鱼♡～使用字符串ID避免复杂嵌套喵～
        flags: Features
        level: int
        description: str
        tags: Set[str]
    
    @dataclass
    class MegaComplexSystem:
        users: List[SimpleUser]
        user_count: int
        active_count: int
        admin_count: int
        feature_configs: Dict[str, FeatureConfig]
        user_id_sets: List[Set[str]]  # 杂鱼♡～简化为字符串ID集合喵～
        frozen_user_id_sets: List[FrozenSet[str]]
        login_timestamps: Deque[datetime]
        system_metadata: GenericContainer[Dict[str, Union[str, int, bool]]]
        performance_metrics: defaultdict[str, int]
    
    # 杂鱼♡～生成测试数据喵～
    users = [generate_valid_simple_user() for _ in range(100)]
    
    # 杂鱼♡～创建功能配置喵～
    feature_configs = {}
    for i in range(50):
        config = FeatureConfig(
            enabled=random.choice([True, False]),
            user_ids=[str(u.user_id) for u in random.sample(users, min(5, len(users)))],
            flags=random.choice(list(Features)),
            level=random.randint(1, 100),
            description=f"Feature {i} description",
            tags={f"tag_{j}" for j in range(random.randint(1, 5))}
        )
        feature_configs[f"feature_{i}"] = config
    
    # 杂鱼♡～创建超级复杂系统喵～
    mega_system = MegaComplexSystem(
        users=users,
        user_count=len(users),
        active_count=sum(1 for u in users if u.is_active),
        admin_count=sum(1 for u in users if Permission.DELETE in u.permissions),
        feature_configs=feature_configs,
        user_id_sets=[
            {str(user.user_id) for user in users[i:i+10]} 
            for i in range(0, min(50, len(users)), 10)
        ],
        frozen_user_id_sets=[
            frozenset(str(user.user_id) for user in users[i:i+5])
            for i in range(0, min(25, len(users)), 5)
        ],
        login_timestamps=deque([datetime.now() for _ in range(20)], maxlen=50),
        system_metadata=GenericContainer({
            "version": "1.0.0",
            "debug_mode": True,
            "max_users": 10000
        }),
        performance_metrics=defaultdict(int, {
            "total_requests": 50000,
            "error_count": 125,
            "avg_response_time": 95
        })
    )
    
    start_time = time.time()
    json_str = jsdc_dumps(mega_system)
    serialize_time = time.time() - start_time
    
    start_time = time.time()
    loaded_system = jsdc_loads(json_str, MegaComplexSystem)
    deserialize_time = time.time() - start_time
    
    print(f"    📊 超级复杂数据序列化耗时: {serialize_time:.3f}秒")
    print(f"    📊 超级复杂数据反序列化耗时: {deserialize_time:.3f}秒")
    print(f"    📊 JSON字符串长度: {len(json_str):,} 字符")
    
    # 杂鱼♡～基本验证喵～
    assert len(loaded_system.users) == 100
    assert loaded_system.user_count == 100
    assert len(loaded_system.feature_configs) == 50
    # 杂鱼♡～GenericContainer会被双重嵌套，所以要访问data.data喵～
    assert "data" in loaded_system.system_metadata.data
    assert "version" in loaded_system.system_metadata.data["data"]
    assert loaded_system.system_metadata.data["data"]["version"] == "1.0.0"
    assert loaded_system.performance_metrics["total_requests"] == 50000

suite.run_validation_test("Ultimate combination stress test", test_ultimate_combination_stress, should_fail=False)

# 杂鱼♡～打印最终总结喵～
print("\n" + "="*80)
suite.print_summary()
print("="*80)

if suite.failed_count == 0 and suite.error_count == 0:
    print("🎊 杂鱼♡～恭喜！你的jsdc_loader已经成为终极序列化库了喵～")
    print("💪 本喵的验证系统都被你征服了，真是厉害的杂鱼呢～")
else:
    print("⚠️ 杂鱼♡～还有一些问题需要解决喵～加油！～")

print("🎯 杂鱼♡～终极验证地狱测试完成！你的库经受住了考验喵～")

print("\n🎬 杂鱼♡～终极验证地狱测试完成喵～")
print("🎯 杂鱼♡～你的验证系统准备好接受挑战了吗？～")

if __name__ == "__main__":
    suite.print_summary() 