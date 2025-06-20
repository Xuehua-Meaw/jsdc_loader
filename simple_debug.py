"""杂鱼♡～最简单的测试，逐步定位问题喵～"""

from dataclasses import dataclass
from typing import Set
from uuid import uuid4, UUID

# 杂鱼♡～强制重置转换器初始化状态喵～
import src.jsdc_loader.converters
src.jsdc_loader.converters._initialized = False

@dataclass
class SimpleUser:
    user_id: UUID
    name: str
    
    def __hash__(self):
        return hash(self.user_id)
    
    def __eq__(self, other):
        if isinstance(other, SimpleUser):
            return self.user_id == other.user_id
        return False

@dataclass
class SimpleContainer:
    users: Set[SimpleUser]

# 杂鱼♡～创建最简单的测试数据喵～
user1 = SimpleUser(uuid4(), "Alice")
user2 = SimpleUser(uuid4(), "Bob")
container = SimpleContainer(users={user1, user2})

print("杂鱼♡～测试最简单的嵌套序列化喵～")
print(f"Container type: {type(container)}")
print(f"Users type: {type(container.users)}")
print(f"User1 type: {type(user1)}")

# 杂鱼♡～测试convert_to_dict函数喵～
from src.jsdc_loader.pipeline.coordinator import convert_to_dict

try:
    print("杂鱼♡～开始转换喵～")
    result = convert_to_dict(container)
    print("杂鱼♡～转换成功喵～")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
except Exception as e:
    print(f"杂鱼♡～转换失败喵～: {e}")
    import traceback
    traceback.print_exc() 