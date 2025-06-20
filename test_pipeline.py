"""杂鱼♡～这是本喵测试pipeline编排功能的脚本喵～"""

import sys
sys.path.insert(0, 'src')

from dataclasses import dataclass
from typing import Optional
from jsdc_loader.pipeline.coordinator import convert_from_dict, convert_to_dict


@dataclass
class SimpleUser:
    """杂鱼♡～简单的用户类用于测试喵～"""
    name: str
    age: int
    email: Optional[str] = None


@dataclass
class SimpleProfile:
    """杂鱼♡～简单的档案类用于测试嵌套喵～"""
    bio: str
    user: SimpleUser


def test_simple_conversion():
    """杂鱼♡～测试简单的转换功能喵～"""
    print("杂鱼♡～测试简单dataclass转换喵～")
    
    # 杂鱼♡～创建测试数据喵～
    user_data = {
        "name": "TestUser",
        "age": 25,
        "email": "test@example.com"
    }
    
    try:
        # 杂鱼♡～测试从字典转换为dataclass喵～
        print("  测试 dict -> dataclass...")
        user = convert_from_dict(user_data, SimpleUser)
        print(f"    转换成功: {user}")
        
        # 杂鱼♡～测试从dataclass转换为字典喵～
        print("  测试 dataclass -> dict...")
        converted_data = convert_to_dict(user)
        print(f"    转换成功: {converted_data}")
        
        # 杂鱼♡～验证数据一致性喵～
        assert converted_data["name"] == user_data["name"]
        assert converted_data["age"] == user_data["age"]
        assert converted_data["email"] == user_data["email"]
        print("    数据一致性验证通过！")
        
    except Exception as e:
        print(f"    转换失败: {e}")
        import traceback
        traceback.print_exc()


def test_nested_conversion():
    """杂鱼♡～测试嵌套dataclass转换喵～"""
    print("\n杂鱼♡～测试嵌套dataclass转换喵～")
    
    # 杂鱼♡～创建嵌套测试数据喵～
    profile_data = {
        "bio": "这是一个测试用户",
        "user": {
            "name": "NestedUser",
            "age": 30,
            "email": "nested@example.com"
        }
    }
    
    try:
        # 杂鱼♡～测试嵌套转换喵～
        print("  测试 nested dict -> dataclass...")
        profile = convert_from_dict(profile_data, SimpleProfile)
        print(f"    转换成功: {profile}")
        print(f"    嵌套用户: {profile.user}")
        
        # 杂鱼♡～测试嵌套序列化喵～
        print("  测试 nested dataclass -> dict...")
        converted_data = convert_to_dict(profile)
        print(f"    转换成功: {converted_data}")
        
        # 杂鱼♡～验证嵌套数据一致性喵～
        assert converted_data["bio"] == profile_data["bio"]
        assert converted_data["user"]["name"] == profile_data["user"]["name"]
        assert converted_data["user"]["age"] == profile_data["user"]["age"]
        print("    嵌套数据一致性验证通过！")
        
    except Exception as e:
        print(f"    嵌套转换失败: {e}")
        import traceback
        traceback.print_exc()


def test_optional_fields():
    """杂鱼♡～测试可选字段处理喵～"""
    print("\n杂鱼♡～测试可选字段处理喵～")
    
    # 杂鱼♡～创建缺少可选字段的数据喵～
    user_data_no_email = {
        "name": "UserWithoutEmail",
        "age": 22
    }
    
    try:
        print("  测试缺少可选字段...")
        user = convert_from_dict(user_data_no_email, SimpleUser)
        print(f"    转换成功: {user}")
        print(f"    email字段: {user.email}")
        
        # 杂鱼♡～验证None值处理喵～
        converted_data = convert_to_dict(user)
        print(f"    反向转换: {converted_data}")
        
        assert user.email is None
        assert converted_data["email"] is None
        print("    可选字段处理验证通过！")
        
    except Exception as e:
        print(f"    可选字段测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_missing_required_field():
    """杂鱼♡～测试缺少必需字段的错误处理喵～"""
    print("\n杂鱼♡～测试缺少必需字段的错误处理喵～")
    
    # 杂鱼♡～创建缺少必需字段的数据喵～
    incomplete_data = {
        "name": "IncompleteUser"
        # 杂鱼♡～故意缺少age字段喵～
    }
    
    try:
        print("  测试缺少必需字段...")
        user = convert_from_dict(incomplete_data, SimpleUser)
        print(f"    转换意外成功: {user}")
        print("    错误：应该抛出异常！")
        
    except Exception as e:
        print(f"    正确抛出异常: {type(e).__name__}: {e}")
        print("    缺少必需字段处理验证通过！")


if __name__ == "__main__":
    print("杂鱼♡～本喵开始测试pipeline编排功能喵～")
    print("="*60)
    
    # 杂鱼♡～运行各种测试喵～
    test_simple_conversion()
    test_nested_conversion()
    test_optional_fields()
    test_missing_required_field()
    
    print("\n" + "="*60)
    print("杂鱼♡～Pipeline编排功能测试完成喵～") 