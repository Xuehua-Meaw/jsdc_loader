"""杂鱼♡～这是本喵测试容器类型转换器的脚本喵～"""

import sys
sys.path.insert(0, 'src')

from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional, Deque
from collections import deque
from jsdc_loader.pipeline.coordinator import convert_from_dict, convert_to_dict


@dataclass
class SimpleItem:
    """杂鱼♡～简单的项目类喵～"""
    name: str
    value: int


@dataclass
class ContainerTest:
    """杂鱼♡～容器类型测试dataclass喵～"""
    # 杂鱼♡～基础容器类型喵～
    string_list: List[str]
    int_set: Set[int]
    name_dict: Dict[str, str]
    coord_tuple: Tuple[int, int, int]
    
    # 杂鱼♡～复杂嵌套容器喵～
    nested_list: List[List[int]]
    nested_dict: Dict[str, List[int]]
    
    # 杂鱼♡～带对象的容器喵～
    item_list: List[SimpleItem]
    item_dict: Dict[str, SimpleItem]
    
    # 杂鱼♡～可选容器类型（必须放最后）喵～
    optional_list: Optional[List[str]] = None


@dataclass
class AdvancedContainerTest:
    """杂鱼♡～高级容器类型测试喵～"""
    # 杂鱼♡～deque类型喵～
    task_queue: Deque[str]
    
    # 杂鱼♡～超级复杂的嵌套喵～
    super_nested: Dict[str, List[Dict[str, int]]]
    
    # 杂鱼♡～元组变长喵～
    variable_tuple: Tuple[str, ...]


@dataclass
class NoneTypeTest:
    """杂鱼♡～测试NoneType的特殊情况喵～"""
    explicit_none: type(None)
    some_value: int


def test_basic_containers():
    """杂鱼♡～测试基础容器类型喵～"""
    print("杂鱼♡～测试基础容器类型喵～")
    
    test_data = {
        "string_list": ["hello", "world", "杂鱼"],
        "int_set": [1, 2, 3, 2, 1],  # 杂鱼♡～重复值将被过滤喵～
        "name_dict": {"first": "张三", "last": "李四"},
        "coord_tuple": [10, 20, 30],
        "nested_list": [[1, 2], [3, 4], [5]],
        "nested_dict": {
            "evens": [2, 4, 6],
            "odds": [1, 3, 5]
        },
        "item_list": [
            {"name": "item1", "value": 10},
            {"name": "item2", "value": 20}
        ],
        "item_dict": {
            "first": {"name": "first_item", "value": 100},
            "second": {"name": "second_item", "value": 200}
        }
    }
    
    try:
        print(f"  输入数据: {test_data}")
        
        # 杂鱼♡～字典转对象喵～
        result = convert_from_dict(test_data, ContainerTest)
        print(f"  转换成功: {result}")
        
        # 杂鱼♡～验证基础容器类型喵～
        assert isinstance(result.string_list, list)
        assert result.string_list == ["hello", "world", "杂鱼"]
        
        assert isinstance(result.int_set, set)
        assert result.int_set == {1, 2, 3}  # 杂鱼♡～重复值已过滤喵～
        
        assert isinstance(result.name_dict, dict)
        assert result.name_dict == {"first": "张三", "last": "李四"}
        
        assert isinstance(result.coord_tuple, tuple)
        assert result.coord_tuple == (10, 20, 30)
        
        # 杂鱼♡～验证嵌套容器喵～
        assert isinstance(result.nested_list, list)
        assert result.nested_list == [[1, 2], [3, 4], [5]]
        
        assert isinstance(result.nested_dict, dict)
        assert result.nested_dict == {"evens": [2, 4, 6], "odds": [1, 3, 5]}
        
        # 杂鱼♡～验证对象容器喵～
        assert isinstance(result.item_list, list)
        assert len(result.item_list) == 2
        
        assert isinstance(result.item_list[0], SimpleItem)
        assert result.item_list[0].name == "item1"
        assert result.item_list[0].value == 10
        
        assert isinstance(result.item_dict, dict)
        assert isinstance(result.item_dict["first"], SimpleItem)
        assert result.item_dict["first"].name == "first_item"
        
        print("    基础容器类型验证通过！")
        
    except Exception as e:
        print(f"    转换失败: {e}")
        import traceback
        traceback.print_exc()


def test_optional_containers():
    """杂鱼♡～测试可选容器类型喵～"""
    print("\n杂鱼♡～测试可选容器类型喵～")
    
    # 杂鱼♡～测试None值喵～
    test_data_none = {
        "string_list": ["test"],
        "int_set": [1],
        "name_dict": {"key": "value"},
        "coord_tuple": [1, 2, 3],
        "nested_list": [[1]],
        "nested_dict": {"test": [1]},
        "item_list": [{"name": "test", "value": 1}],
        "item_dict": {"test": {"name": "test", "value": 1}},
        "optional_list": None  # 杂鱼♡～None值喵～
    }
    
    # 杂鱼♡～测试有值的情况喵～
    test_data_value = {
        **test_data_none,
        "optional_list": ["optional", "value"]  # 杂鱼♡～有值喵～
    }
    
    try:
        print("  测试None值:")
        result_none = convert_from_dict(test_data_none, ContainerTest)
        assert result_none.optional_list is None
        print("    None值处理正确！")
        
        print("  测试有值:")
        result_value = convert_from_dict(test_data_value, ContainerTest)
        assert result_value.optional_list == ["optional", "value"]
        print("    有值处理正确！")
        
    except Exception as e:
        print(f"    转换失败: {e}")
        import traceback
        traceback.print_exc()


def test_deque_containers():
    """杂鱼♡～测试deque容器类型喵～"""
    print("\n杂鱼♡～测试deque容器类型喵～")
    
    test_data = {
        "task_queue": ["task1", "task2", "task3"],
        "super_nested": {
            "group1": [
                {"score": 100},
                {"score": 200}
            ],
            "group2": [
                {"score": 300}
            ]
        },
        "variable_tuple": ["var1", "var2", "var3", "var4"]
    }
    
    try:
        print(f"  输入数据: {test_data}")
        
        result = convert_from_dict(test_data, AdvancedContainerTest)
        print(f"  转换成功: {result}")
        
        # 杂鱼♡～验证deque类型喵～
        assert isinstance(result.task_queue, deque)
        assert list(result.task_queue) == ["task1", "task2", "task3"]
        
        # 杂鱼♡～验证超级复杂嵌套喵～
        assert isinstance(result.super_nested, dict)
        assert isinstance(result.super_nested["group1"], list)
        assert isinstance(result.super_nested["group1"][0], dict)
        assert result.super_nested["group1"][0]["score"] == 100
        
        # 杂鱼♡～验证变长元组喵～
        assert isinstance(result.variable_tuple, tuple)
        assert result.variable_tuple == ("var1", "var2", "var3", "var4")
        
        print("    高级容器类型验证通过！")
        
    except Exception as e:
        print(f"    转换失败: {e}")
        import traceback
        traceback.print_exc()


def test_round_trip_containers():
    """杂鱼♡～测试容器类型往返转换喵～"""
    print("\n杂鱼♡～测试容器类型往返转换喵～")
    
    # 杂鱼♡～创建复杂的原始对象喵～
    original = ContainerTest(
        string_list=["转换", "测试", "杂鱼"],
        int_set={10, 20, 30},
        name_dict={"测试": "转换", "杂鱼": "喵"},
        coord_tuple=(100, 200, 300),
        nested_list=[[10, 20], [30, 40]],
        nested_dict={"数字": [1, 2, 3], "字母": [4, 5, 6]},
        item_list=[
            SimpleItem("项目1", 500),
            SimpleItem("项目2", 600)
        ],
        item_dict={
            "主要": SimpleItem("主要项目", 1000),
            "次要": SimpleItem("次要项目", 2000)
        },
        optional_list=["可选", "列表"]
    )
    
    try:
        print(f"  原始对象: {original}")
        
        # 杂鱼♡～对象→字典喵～
        data_dict = convert_to_dict(original)
        print(f"  转换为字典: {data_dict}")
        
        # 杂鱼♡～字典→对象喵～
        restored = convert_from_dict(data_dict, ContainerTest)
        print(f"  恢复的对象: {restored}")
        
        # 杂鱼♡～验证完整性喵～
        assert original.string_list == restored.string_list
        assert original.int_set == restored.int_set
        assert original.name_dict == restored.name_dict
        assert original.coord_tuple == restored.coord_tuple
        assert original.optional_list == restored.optional_list
        assert original.nested_list == restored.nested_list
        assert original.nested_dict == restored.nested_dict
        
        # 杂鱼♡～验证对象列表喵～
        assert len(original.item_list) == len(restored.item_list)
        for orig, rest in zip(original.item_list, restored.item_list):
            assert orig.name == rest.name
            assert orig.value == rest.value
        
        # 杂鱼♡～验证对象字典喵～
        for key in original.item_dict:
            assert original.item_dict[key].name == restored.item_dict[key].name
            assert original.item_dict[key].value == restored.item_dict[key].value
        
        print("    往返转换验证通过！")
        
    except Exception as e:
        print(f"    往返转换失败: {e}")
        import traceback
        traceback.print_exc()


def test_error_handling():
    """杂鱼♡～测试容器转换错误处理喵～"""
    print("\n杂鱼♡～测试容器转换错误处理喵～")
    
    invalid_cases = [
        {
            "desc": "string_list期望list，得到string",
            "data": {
                "string_list": "not_a_list",  # 杂鱼♡～错误类型喵～
                "int_set": [1],
                "name_dict": {"key": "value"},
                "coord_tuple": [1, 2, 3],
                "nested_list": [[1]],
                "nested_dict": {"test": [1]},
                "item_list": [{"name": "test", "value": 1}],
                "item_dict": {"test": {"name": "test", "value": 1}}
            }
        },
        {
            "desc": "item_list中的对象缺少字段",
            "data": {
                "string_list": ["test"],
                "int_set": [1],
                "name_dict": {"key": "value"},
                "coord_tuple": [1, 2, 3],
                "nested_list": [[1]],
                "nested_dict": {"test": [1]},
                "item_list": [{"name": "test"}],  # 杂鱼♡～缺少value字段喵～
                "item_dict": {"test": {"name": "test", "value": 1}}
            }
        }
    ]
    
    for case in invalid_cases:
        try:
            print(f"  测试: {case['desc']}")
            result = convert_from_dict(case["data"], ContainerTest)
            print(f"    意外成功: {result}")
            print("    错误：应该抛出异常！")
        except Exception as e:
            print(f"    正确抛出异常: {type(e).__name__}: {e}")


def test_none_type_field():
    """杂鱼♡～测试显式声明为None类型的字段喵～"""
    print("\n杂鱼♡～测试显式NoneType字段喵～")
    
    test_data = {
        "explicit_none": None,
        "some_value": 123
    }
    
    try:
        print(f"  输入数据: {test_data}")
        result = convert_from_dict(test_data, NoneTypeTest)
        print(f"  转换成功: {result}")
        
        assert result.explicit_none is None
        assert result.some_value == 123
        print("    显式NoneType字段验证通过！")

        # 往返测试
        data_dict = convert_to_dict(result)
        print(f"  转换为字典: {data_dict}")
        restored = convert_from_dict(data_dict, NoneTypeTest)
        print(f"  恢复的对象: {restored}")
        assert restored.explicit_none is None
        assert restored.some_value == 123
        print("    往返转换验证通过！")

    except Exception as e:
        print(f"    转换失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("杂鱼♡～本喵开始测试容器类型转换器喵～")
    print("="*60)
    
    # 杂鱼♡～运行各种测试喵～
    test_basic_containers()
    test_optional_containers()
    test_deque_containers()
    test_round_trip_containers()
    test_error_handling()
    test_none_type_field()
    
    print("\n" + "="*60)
    print("杂鱼♡～容器类型转换器测试完成喵～") 