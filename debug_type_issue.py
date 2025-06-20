"""杂鱼♡～本喵要隔离类型信息丢失问题的测试喵～"""

from dataclasses import dataclass, field
from typing import Set, Dict, List
from src.jsdc_loader import jsdc_dump
from uuid import uuid4, UUID

# 杂鱼♡～强制重置转换器初始化状态喵～
import src.jsdc_loader.converters
src.jsdc_loader.converters._initialized = False

# 杂鱼♡～添加调试信息喵～
print("杂鱼♡～检查转换器初始化状态喵～")
from src.jsdc_loader.pipeline.registry import get_global_registry
from src.jsdc_loader.schema.field_schema import ConverterType

registry = get_global_registry()
print(f"测试SimpleUser dataclass转换器:")
try:
    from debug_type_issue import SimpleUser
except:
    pass

# 杂鱼♡～先定义类型再测试喵～
@dataclass
class SimpleUser:
    """杂鱼♡～简单的用户类型喵～"""
    user_id: UUID
    name: str
    age: int
    
    def __hash__(self):
        return hash(self.user_id)
    
    def __eq__(self, other):
        if isinstance(other, SimpleUser):
            return self.user_id == other.user_id
        return False

# 杂鱼♡～测试转换器喵～
for conv_type in ConverterType:
    try:
        converter = registry.get_converter(set, conv_type)
        print(f"找到 {conv_type} 转换器(set): {type(converter)}")
    except ValueError as e:
        print(f"没有找到 {conv_type} 转换器(set): {e}")

try:
    converter = registry.get_converter(SimpleUser, ConverterType.DATACLASS)
    print(f"找到 DATACLASS 转换器(SimpleUser): {type(converter)}")
except ValueError as e:
    print(f"没有找到 DATACLASS 转换器(SimpleUser): {e}")

@dataclass
class Organization:
    """杂鱼♡～组织类型，包含嵌套的Set喵～"""
    org_id: UUID
    name: str
    employees: Set[SimpleUser]
    departments: Dict[str, Set[SimpleUser]] = field(default_factory=dict)

@dataclass
class GlobalSystem:
    """杂鱼♡～全局系统，包含多层嵌套的Set喵～"""
    system_id: UUID
    organizations: Dict[UUID, Organization]
    global_admins: Set[SimpleUser]

# 杂鱼♡～创建测试数据喵～
users = [
    SimpleUser(uuid4(), "Alice", 25),
    SimpleUser(uuid4(), "Bob", 30),
    SimpleUser(uuid4(), "Charlie", 35),
    SimpleUser(uuid4(), "Diana", 28),
    SimpleUser(uuid4(), "Eve", 32)
]

# 杂鱼♡～创建组织喵～
org1 = Organization(
    org_id=uuid4(),
    name="TechCorp", 
    employees=set(users[:3]),
    departments={
        "Engineering": set(users[:2]),
        "Marketing": set(users[2:3])
    }
)

org2 = Organization(
    org_id=uuid4(),
    name="DataCorp",
    employees=set(users[3:]),
    departments={
        "Research": set(users[3:4]),
        "Analytics": set(users[4:])
    }
)

# 杂鱼♡～创建全局系统喵～
global_system = GlobalSystem(
    system_id=uuid4(),
    organizations={org1.org_id: org1, org2.org_id: org2},
    global_admins=set(users[:2])
)

print("杂鱼♡～开始测试复杂嵌套的Set序列化喵～")
print(f"全局管理员类型: {type(global_system.global_admins)}")
print(f"组织字典类型: {type(global_system.organizations)}")
print(f"第一个组织员工类型: {type(org1.employees)}")
print(f"第一个组织部门类型: {type(org1.departments)}")

try:
    result = jsdc_dump(global_system, "complex_test.json")
    print("杂鱼♡～复杂序列化成功喵～")
except Exception as e:
    print(f"杂鱼♡～复杂序列化失败喵～: {e}")
    import traceback
    traceback.print_exc() 