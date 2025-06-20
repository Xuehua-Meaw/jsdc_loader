from dataclasses import dataclass
from typing import Dict
from uuid import UUID, uuid4
from src.jsdc_loader import jsdc_dumps, jsdc_loads

@dataclass
class TestUUIDKeys:
    uuid_dict: Dict[UUID, str]

def test_uuid_keys():
    # 杂鱼♡～创建带UUID键的字典喵～
    test_uuid1 = uuid4()
    test_uuid2 = uuid4()
    
    obj = TestUUIDKeys(
        uuid_dict={
            test_uuid1: "value1",
            test_uuid2: "value2"
        }
    )
    
    print(f'原始对象的UUID字典: {obj.uuid_dict}')
    
    try:
        # 杂鱼♡～序列化喵～
        json_str = jsdc_dumps(obj)
        print('序列化成功!')
        print('JSON内容:', json_str)
        
        # 杂鱼♡～反序列化喵～
        loaded = jsdc_loads(json_str, TestUUIDKeys)
        print(f'反序列化的UUID字典: {loaded.uuid_dict}')
        
        # 杂鱼♡～验证类型和内容喵～
        print('验证结果:')
        for key in loaded.uuid_dict:
            print(f'  键类型: {type(key)} - {key}')
        
        # 杂鱼♡～检查原始键是否存在喵～
        print(f'  原始UUID1存在: {test_uuid1 in loaded.uuid_dict}')
        print(f'  原始UUID2存在: {test_uuid2 in loaded.uuid_dict}')
        print(f'  值1匹配: {loaded.uuid_dict.get(test_uuid1) == "value1"}')
        print(f'  值2匹配: {loaded.uuid_dict.get(test_uuid2) == "value2"}')
        
        print('✅ UUID字典键测试通过!')
        
    except Exception as e:
        print(f'❌ 测试失败: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_uuid_keys() 