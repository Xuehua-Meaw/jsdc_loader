"""杂鱼♡～这是本喵测试schema builder的脚本喵～"""

import sys
import os
sys.path.insert(0, 'src')

from jsdc_loader.schema.schema_builder import build_schema
from jsdc_loader.schema.field_schema import ConverterType

# 杂鱼♡～导入test.py中的GlobalSystem喵～
sys.path.insert(0, '.')
from test import GlobalSystem, User, Organization, Channel, Thread

def test_schema_analysis():
    """杂鱼♡～测试schema分析功能喵～"""
    print("杂鱼♡～开始分析GlobalSystem的schema喵～")
    
    try:
        # 杂鱼♡～构建GlobalSystem的schema喵～
        schema = build_schema(GlobalSystem)
        
        print(f"杂鱼♡～Schema构建成功喵！～")
        print(f"根类型: {schema.root_type.__name__}")
        print(f"缓存键值: {schema.cache_key}")
        print(f"字段数量: {len(schema.field_schemas)}")
        print()
        
        # 杂鱼♡～分析前10个字段的详细信息喵～
        print("杂鱼♡～前10个字段的详细分析喵～:")
        field_items = list(schema.field_schemas.items())[:10]
        
        for field_path, field_schema in field_items:
            print(f"  字段: {field_path}")
            print(f"    类型: {field_schema.exact_type}")
            print(f"    转换器: {field_schema.converter_type.value}")
            print(f"    可选: {field_schema.is_optional}")
            
            if field_schema.union_types:
                print(f"    Union类型: {[t.__name__ for t in field_schema.union_types]}")
            
            if field_schema.sub_schema:
                print(f"    子Schema: {field_schema.sub_schema.root_type.__name__} (包含{len(field_schema.sub_schema.field_schemas)}个字段)")
            
            print()
        
        # 杂鱼♡～测试几个特别复杂的字段喵～
        test_complex_fields(schema)
        
    except Exception as e:
        print(f"杂鱼♡～Schema构建失败喵～: {e}")
        import traceback
        traceback.print_exc()

def test_complex_fields(schema):
    """杂鱼♡～测试复杂字段的分析喵～"""
    print("杂鱼♡～测试复杂字段分析喵～:")
    
    # 杂鱼♡～测试Dict[UUID, Organization]类型喵～
    orgs_field = schema.field_schemas.get('organizations')
    if orgs_field:
        print(f"organizations字段:")
        print(f"  转换器类型: {orgs_field.converter_type.value}")
        print(f"  是否容器: {orgs_field.converter_type == ConverterType.CONTAINER}")
        if orgs_field.sub_schema:
            print(f"  子Schema字段数: {len(orgs_field.sub_schema.field_schemas)}")
            for sub_field in list(orgs_field.sub_schema.field_schemas.keys())[:3]:
                print(f"    子字段: {sub_field}")
        print()
    
    # 杂鱼♡～测试Deque[Tuple[datetime, User, str, Dict[str, Any]]]类型喵～
    audit_field = schema.field_schemas.get('audit_log')
    if audit_field:
        print(f"audit_log字段:")
        print(f"  转换器类型: {audit_field.converter_type.value}")
        if audit_field.sub_schema:
            print(f"  子Schema字段数: {len(audit_field.sub_schema.field_schemas)}")
            for sub_field in audit_field.sub_schema.field_schemas.keys():
                print(f"    子字段: {sub_field}")
        print()
    
    # 杂鱼♡～测试Dict[str, Features]类型喵～
    flags_field = schema.field_schemas.get('feature_flags')
    if flags_field:
        print(f"feature_flags字段:")
        print(f"  转换器类型: {flags_field.converter_type.value}")
        if flags_field.sub_schema:
            print(f"  子Schema字段数: {len(flags_field.sub_schema.field_schemas)}")
        print()

def test_user_schema():
    """杂鱼♡～单独测试User Schema喵～"""
    print("杂鱼♡～测试User Schema构建喵～:")
    
    try:
        user_schema = build_schema(User)
        print(f"User Schema构建成功！字段数: {len(user_schema.field_schemas)}")
        
        # 杂鱼♡～查看一些有趣的字段喵～
        interesting_fields = ['friends', 'profile', 'settings', 'login_history']
        
        for field_name in interesting_fields:
            if field_name in user_schema.field_schemas:
                field = user_schema.field_schemas[field_name]
                print(f"  {field_name}: {field.converter_type.value}, 可选={field.is_optional}")
                if field.sub_schema:
                    print(f"    子Schema: {field.sub_schema.root_type.__name__}")
        print()
        
    except Exception as e:
        print(f"杂鱼♡～User Schema构建失败喵～: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("杂鱼♡～本喵开始测试schema builder喵～")
    print("="*50)
    
    # 杂鱼♡～首先测试简单的User Schema喵～
    test_user_schema()
    
    print("="*50)
    
    # 杂鱼♡～然后测试复杂的GlobalSystem Schema喵～
    test_schema_analysis()
    
    print("杂鱼♡～Schema测试完成喵～") 