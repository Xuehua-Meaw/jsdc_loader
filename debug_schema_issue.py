"""杂鱼♡～精准调试schema构建过程喵～"""

from dataclasses import dataclass, field
from typing import Set, Dict
from uuid import uuid4, UUID

# 杂鱼♡～强制重置转换器初始化状态喵～
import src.jsdc_loader.converters
src.jsdc_loader.converters._initialized = False

@dataclass
class SimpleUser:
    user_id: UUID
    name: str
    friends: Set['SimpleUser'] = field(default_factory=set)  # 杂鱼♡～这里有循环引用喵～
    
    def __hash__(self):
        return hash(self.user_id)
    
    def __eq__(self, other):
        if isinstance(other, SimpleUser):
            return self.user_id == other.user_id
        return False

@dataclass
class Organization:
    org_id: UUID
    name: str
    employees: Set[SimpleUser]
    
@dataclass
class GlobalSystem:
    system_id: UUID
    organizations: Dict[UUID, Organization]

# 杂鱼♡～构建schema并检查喵～
from src.jsdc_loader.schema.schema_builder import build_schema

print("杂鱼♡～分析SimpleUser的schema喵～")
user_schema = build_schema(SimpleUser)
print(f"SimpleUser字段数: {len(user_schema.field_schemas)}")

for field_name, field_schema in user_schema.field_schemas.items():
    print(f"字段: {field_name}")
    print(f"  exact_type: {field_schema.exact_type}")
    print(f"  converter_type: {field_schema.converter_type}")
    if field_schema.sub_schema:
        print(f"  sub_schema keys: {list(field_schema.sub_schema.field_schemas.keys())}")
        for sub_key, sub_schema in field_schema.sub_schema.field_schemas.items():
            print(f"    {sub_key}: exact_type={sub_schema.exact_type}, converter_type={sub_schema.converter_type}")
    print()

print("杂鱼♡～分析Organization的schema喵～")
org_schema = build_schema(Organization)
print(f"Organization字段数: {len(org_schema.field_schemas)}")

for field_name, field_schema in org_schema.field_schemas.items():
    print(f"字段: {field_name}")
    print(f"  exact_type: {field_schema.exact_type}")
    print(f"  converter_type: {field_schema.converter_type}")
    if field_schema.sub_schema:
        print(f"  sub_schema keys: {list(field_schema.sub_schema.field_schemas.keys())}")
        for sub_key, sub_schema in field_schema.sub_schema.field_schemas.items():
            print(f"    {sub_key}: exact_type={sub_schema.exact_type}, converter_type={sub_schema.converter_type}")
            if sub_schema.sub_schema:
                print(f"      nested sub_schema keys: {list(sub_schema.sub_schema.field_schemas.keys())}")
    print()

# 杂鱼♡～创建测试数据喵～
user1 = SimpleUser(uuid4(), "Alice")
user2 = SimpleUser(uuid4(), "Bob")
user1.friends = {user2}  # 杂鱼♡～建立朋友关系喵～

org = Organization(uuid4(), "TestOrg", employees={user1, user2})
system = GlobalSystem(uuid4(), organizations={org.org_id: org})

print("杂鱼♡～开始序列化测试喵～")
from src.jsdc_loader.pipeline.coordinator import convert_to_dict

try:
    result = convert_to_dict(system)
    print("杂鱼♡～序列化成功喵～")
except Exception as e:
    print(f"杂鱼♡～序列化失败喵～: {e}")
    import traceback
    traceback.print_exc() 