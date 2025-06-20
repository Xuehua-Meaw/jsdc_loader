"""杂鱼♡～这是本喵测试基础类型转换器的脚本喵～"""

import sys
sys.path.insert(0, 'src')

from dataclasses import dataclass
from typing import Optional
from jsdc_loader.pipeline.coordinator import convert_from_dict, convert_to_dict


@dataclass
class BasicTypesTest:
    """杂鱼♡～测试基础类型的dataclass喵～"""
    name: str
    age: int  
    height: float
    is_active: bool
    nickname: Optional[str] = None


def test_str_conversion():
    """杂鱼♡～测试字符串类型转换喵～"""
    print("杂鱼♡～测试字符串类型转换喵～")
    
    test_cases = [
        {"name": "TestUser"},           # 正常字符串
        {"name": 123},                  # 数字转字符串  
        {"name": 45.67},                # 浮点数转字符串
        {"name": True},                 # 布尔值转字符串
    ]
    
    for i, data in enumerate(test_cases):
        try:
            print(f"  测试用例{i+1}: {data}")
            # 杂鱼♡～添加其他必需字段喵～
            full_data = {**data, "age": 25, "height": 175.5, "is_active": True}
            result = convert_from_dict(full_data, BasicTypesTest)
            print(f"    转换成功: name='{result.name}' (类型: {type(result.name)})")
            
            # 杂鱼♡～验证转换结果喵～
            assert isinstance(result.name, str)
            
        except Exception as e:
            print(f"    转换失败: {e}")


def test_int_conversion():
    """杂鱼♡～测试整数类型转换喵～"""
    print("\n杂鱼♡～测试整数类型转换喵～")
    
    test_cases = [
        {"age": 25},                    # 正常整数
        {"age": "30"},                  # 字符串转整数
        {"age": 35.0},                  # 整数值浮点数
        {"age": True},                  # 布尔值转整数(True=1)
        {"age": False},                 # 布尔值转整数(False=0)
    ]
    
    for i, data in enumerate(test_cases):
        try:
            print(f"  测试用例{i+1}: {data}")
            full_data = {"name": "Test", **data, "height": 175.5, "is_active": True}
            result = convert_from_dict(full_data, BasicTypesTest)
            print(f"    转换成功: age={result.age} (类型: {type(result.age)})")
            
            # 杂鱼♡～验证转换结果喵～
            assert isinstance(result.age, int)
            
        except Exception as e:
            print(f"    转换失败: {e}")


def test_float_conversion():
    """杂鱼♡～测试浮点数类型转换喵～"""
    print("\n杂鱼♡～测试浮点数类型转换喵～")
    
    test_cases = [
        {"height": 175.5},              # 正常浮点数
        {"height": "180.0"},            # 字符串转浮点数  
        {"height": 170},                # 整数转浮点数
        {"height": True},               # 布尔值转浮点数
    ]
    
    for i, data in enumerate(test_cases):
        try:
            print(f"  测试用例{i+1}: {data}")
            full_data = {"name": "Test", "age": 25, **data, "is_active": True}
            result = convert_from_dict(full_data, BasicTypesTest)
            print(f"    转换成功: height={result.height} (类型: {type(result.height)})")
            
            # 杂鱼♡～验证转换结果喵～
            assert isinstance(result.height, float)
            
        except Exception as e:
            print(f"    转换失败: {e}")


def test_bool_conversion():
    """杂鱼♡～测试布尔类型转换喵～"""
    print("\n杂鱼♡～测试布尔类型转换喵～")
    
    test_cases = [
        {"is_active": True},            # 正常布尔值
        {"is_active": False},           # 正常布尔值
        {"is_active": "true"},          # 字符串转布尔值
        {"is_active": "false"},         # 字符串转布尔值
        {"is_active": "yes"},           # 字符串转布尔值
        {"is_active": "no"},            # 字符串转布尔值
        {"is_active": "1"},             # 字符串转布尔值
        {"is_active": "0"},             # 字符串转布尔值
        {"is_active": 1},               # 数字转布尔值
        {"is_active": 0},               # 数字转布尔值
        {"is_active": 42},              # 非零数字转布尔值
    ]
    
    for i, data in enumerate(test_cases):
        try:
            print(f"  测试用例{i+1}: {data}")
            full_data = {"name": "Test", "age": 25, "height": 175.5, **data}
            result = convert_from_dict(full_data, BasicTypesTest)
            print(f"    转换成功: is_active={result.is_active} (类型: {type(result.is_active)})")
            
            # 杂鱼♡～验证转换结果喵～
            assert isinstance(result.is_active, bool)
            
        except Exception as e:
            print(f"    转换失败: {e}")


def test_invalid_conversions():
    """杂鱼♡～测试无效转换的错误处理喵～"""
    print("\n杂鱼♡～测试无效转换的错误处理喵～")
    
    invalid_cases = [
        {"age": "not_a_number"},        # 无效字符串转整数
        {"age": 25.7},                  # 非整数值浮点数转整数
        {"height": "not_a_float"},      # 无效字符串转浮点数
        {"is_active": "maybe"},         # 无效字符串转布尔值
    ]
    
    for i, data in enumerate(invalid_cases):
        try:
            print(f"  无效测试用例{i+1}: {data}")
            full_data = {"name": "Test", "age": 25, "height": 175.5, "is_active": True, **data}
            result = convert_from_dict(full_data, BasicTypesTest)
            print(f"    意外成功: {result}")
            print("    错误：应该抛出异常！")
            
        except Exception as e:
            print(f"    正确抛出异常: {type(e).__name__}: {e}")


def test_round_trip_conversion():
    """杂鱼♡～测试往返转换（对象→字典→对象）喵～"""
    print("\n杂鱼♡～测试往返转换喵～")
    
    # 杂鱼♡～创建原始对象喵～
    original = BasicTypesTest(
        name="RoundTripTest",
        age=30,
        height=180.5,
        is_active=True,
        nickname="RT"
    )
    
    try:
        print(f"  原始对象: {original}")
        
        # 杂鱼♡～对象转字典喵～
        data_dict = convert_to_dict(original)
        print(f"  转换为字典: {data_dict}")
        
        # 杂鱼♡～字典转对象喵～
        restored = convert_from_dict(data_dict, BasicTypesTest)
        print(f"  恢复的对象: {restored}")
        
        # 杂鱼♡～验证数据一致性喵～
        assert original.name == restored.name
        assert original.age == restored.age
        assert original.height == restored.height
        assert original.is_active == restored.is_active
        assert original.nickname == restored.nickname
        
        print("    往返转换验证通过！")
        
    except Exception as e:
        print(f"    往返转换失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("杂鱼♡～本喵开始测试基础类型转换器喵～")
    print("="*60)
    
    # 杂鱼♡～运行各种测试喵～
    test_str_conversion()
    test_int_conversion()
    test_float_conversion()
    test_bool_conversion()
    test_invalid_conversions()
    test_round_trip_conversion()
    
    print("\n" + "="*60)
    print("杂鱼♡～基础类型转换器测试完成喵～") 