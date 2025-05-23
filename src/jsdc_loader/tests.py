"""杂鱼♡～这是本喵为JSDC Loader编写的测试用例喵～真是个杂鱼♡～"""

from dataclasses import dataclass, field, FrozenInstanceError
from enum import Enum, auto
from typing import Optional, List, Dict, Set, Any, Union, Tuple
import tempfile
import os
import unittest
import datetime
import uuid
from decimal import Decimal
import collections
import time

from pydantic import BaseModel

from .loader import jsdc_load, jsdc_loads
from .dumper import jsdc_dump, jsdc_dumps

class TestJSDCLoader(unittest.TestCase):
    """杂鱼♡～这是本喵为JSDC Loader编写的测试用例喵～"""
    
    def setUp(self):
        """杂鱼♡～本喵要设置测试环境喵～"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        
    def tearDown(self):
        """杂鱼♡～本喵要清理测试环境喵～"""
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)
    
    def test_basic_serialization(self):
        """杂鱼♡～本喵要测试最基础的序列化/反序列化喵～"""
        @dataclass 
        class DatabaseConfig:
            host: str = 'localhost'
            port: int = 3306
            user: str = 'root'
            password: str = 'password'
            ips: List[str] = field(default_factory=lambda: ['127.0.0.1'])
            primary_user: Optional[str] = field(default_factory=lambda: None)
        
        db = DatabaseConfig()
        jsdc_dump(db, self.temp_path)
        loaded_db = jsdc_load(self.temp_path, DatabaseConfig)
        
        self.assertEqual(db.host, loaded_db.host)
        self.assertEqual(db.port, loaded_db.port)
        self.assertEqual(db.ips, loaded_db.ips)
        print("杂鱼♡～本喵测试最基础的序列化/反序列化成功了喵～")
    
    def test_enum_serialization(self):
        """杂鱼♡～本喵要测试枚举的序列化/反序列化喵～"""
        class UserType(Enum):
            ADMIN = auto()
            USER = auto()
            GUEST = auto()

        @dataclass 
        class UserConfig:
            name: str = 'John Doe'
            age: int = 30
            married: bool = False
            user_type: UserType = field(default_factory=lambda: UserType.USER)
            roles: List[str] = field(default_factory=lambda: ['read'])
        
        user = UserConfig()
        jsdc_dump(user, self.temp_path)
        loaded_user = jsdc_load(self.temp_path, UserConfig)
        
        self.assertEqual(user.name, loaded_user.name)
        self.assertEqual(user.user_type, loaded_user.user_type)
        print("杂鱼♡～本喵测试枚举的序列化/反序列化成功了喵～")
    def test_nested_dataclasses(self):
        """杂鱼♡～本喵要测试嵌套的数据类了喵～"""
        class UserType(Enum):
            ADMIN = auto()
            USER = auto()
            GUEST = auto()

        @dataclass 
        class UserConfig:
            name: str = 'John Doe'
            age: int = 30
            married: bool = False
            user_type: UserType = field(default_factory=lambda: UserType.USER)
            roles: List[str] = field(default_factory=lambda: ['read'])

        @dataclass 
        class DatabaseConfig:
            host: str = 'localhost'
            port: int = 3306
            user: str = 'root'
            password: str = 'password'
            ips: List[str] = field(default_factory=lambda: ['127.0.0.1'])
            primary_user: Optional[str] = field(default_factory=lambda: None)

        @dataclass
        class AppConfig:
            user: UserConfig = field(default_factory=lambda: UserConfig())
            database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())
            version: str = '1.0.0'
            debug: bool = False
            settings: Dict[str, str] = field(default_factory=lambda: {'theme': 'dark'})
        
        app = AppConfig()
        app.user.roles.append('write')
        app.database.ips.extend(['192.168.1.1', '10.0.0.1'])
        app.settings['language'] = 'en'
        
        jsdc_dump(app, self.temp_path)
        loaded_app = jsdc_load(self.temp_path, AppConfig)
        
        self.assertEqual(loaded_app.user.roles, ['read', 'write'])
        self.assertEqual(loaded_app.database.ips, ['127.0.0.1', '192.168.1.1', '10.0.0.1'])
        self.assertEqual(loaded_app.settings, {'theme': 'dark', 'language': 'en'})
        print("杂鱼♡～本喵测试嵌套的数据类成功了喵～")
    def test_pydantic_models(self):
        """杂鱼♡～本喵要测试Pydantic模型了喵～"""
        class ServerConfig(BaseModel):
            name: str = "main"
            port: int = 8080
            ssl: bool = True
            headers: Dict[str, str] = {"Content-Type": "application/json"}

        class ApiConfig(BaseModel):
            servers: List[ServerConfig] = []
            timeout: int = 30
            retries: int = 3
        
        api_config = ApiConfig()
        api_config.servers.append(ServerConfig(name="backup", port=8081))
        api_config.servers.append(ServerConfig(name="dev", port=8082, ssl=False))
        
        jsdc_dump(api_config, self.temp_path)
        loaded_api = jsdc_load(self.temp_path, ApiConfig)
        
        self.assertEqual(len(loaded_api.servers), 2)
        self.assertEqual(loaded_api.servers[0].name, "backup")
        self.assertEqual(loaded_api.servers[1].port, 8082)
        self.assertFalse(loaded_api.servers[1].ssl)
        print("杂鱼♡～本喵测试Pydantic模型成功了喵～")
    def test_hashable_model_set(self):
        """杂鱼♡～为了让Model可哈希，本喵决定添加__hash__和__eq__方法喵～"""
        @dataclass(frozen=True)  # 让这个数据类不可变，以便可以哈希
        class Model:
            base_url: str = ""
            api_key: str = ""
            model: str = ""

            def __hash__(self):
                return hash((self.base_url, self.api_key, self.model))  # 使用元组的哈希值

            def __eq__(self, other):
                if not isinstance(other, Model):
                    return NotImplemented
                return (self.base_url, self.api_key, self.model) == (other.base_url, other.api_key, other.model)  # 比较内容

        @dataclass
        class ModelList:
            models: Set[Model] = field(default_factory=lambda: set()) 
            
        # 创建测试数据
        model1 = Model(base_url="https://api1.example.com", api_key="key1", model="gpt-4")
        model2 = Model(base_url="https://api2.example.com", api_key="key2", model="gpt-3.5")
        model3 = Model(base_url="https://api3.example.com", api_key="key3", model="llama-3")
        
        model_list = ModelList()
        model_list.models.add(model1)
        model_list.models.add(model2)
        model_list.models.add(model3)
        
        # 测试相同模型的哈希值和相等性
        duplicate_model = Model(base_url="https://api1.example.com", api_key="key1", model="gpt-4")
        model_list.models.add(duplicate_model)  # 这个不应该增加集合的大小
        
        self.assertEqual(len(model_list.models), 3)  # 验证重复模型没有被添加
        self.assertEqual(hash(model1), hash(duplicate_model))  # 验证哈希函数工作正常
        self.assertEqual(model1, duplicate_model)  # 验证相等性比较工作正常

        # 序列化和反序列化
        jsdc_dump(model_list, self.temp_path)
        loaded_model_list = jsdc_load(self.temp_path, ModelList)
        
        # 验证集合大小
        self.assertEqual(len(loaded_model_list.models), 3)
        
        # 验证所有模型都被正确反序列化
        loaded_models = sorted(loaded_model_list.models, key=lambda m: m.base_url)
        original_models = sorted(model_list.models, key=lambda m: m.base_url)
        
        for i in range(len(original_models)):
            self.assertEqual(loaded_models[i].base_url, original_models[i].base_url)
            self.assertEqual(loaded_models[i].api_key, original_models[i].api_key)
            self.assertEqual(loaded_models[i].model, original_models[i].model)
        
        # 验证集合操作仍然正常工作
        new_model = Model(base_url="https://api4.example.com", api_key="key4", model="claude-3")
        loaded_model_list.models.add(new_model)
        self.assertEqual(len(loaded_model_list.models), 4)
        
        # 验证重复模型仍然不会被添加
        duplicate_model_again = Model(base_url="https://api1.example.com", api_key="key1", model="gpt-4")
        loaded_model_list.models.add(duplicate_model_again)
        self.assertEqual(len(loaded_model_list.models), 4)
        print("杂鱼♡～本喵测试可哈希的模型成功了喵～")

    def test_error_handling(self):
        """杂鱼♡～本喵要测试错误处理了喵～"""
        @dataclass 
        class DatabaseConfig:
            host: str = 'localhost'
            port: int = 3306
        
        # Test nonexistent file
        with self.assertRaises(FileNotFoundError):
            jsdc_load("nonexistent.json", DatabaseConfig)
        
        # Test empty input
        with self.assertRaises(ValueError):
            jsdc_loads("", DatabaseConfig)
        
        # Test invalid JSON
        with self.assertRaises(ValueError):
            jsdc_loads("{invalid json}", DatabaseConfig)
        
        # Test invalid indent
        with self.assertRaises(ValueError):
            jsdc_dump(DatabaseConfig(), self.temp_path, indent=-1)
        print("杂鱼♡～本喵测试错误处理成功了喵～")
    def test_complex_types(self):
        """杂鱼♡～本喵要测试各种复杂类型了喵～准备好被本喵的测试震撼吧～"""
        @dataclass
        class ComplexConfig:
            created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now())
            updated_at: Optional[datetime.datetime] = None
            expiry_date: Optional[datetime.date] = field(default_factory=lambda: datetime.date.today())
            session_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4())
            amount: Decimal = Decimal('10.50')
            time_delta: datetime.timedelta = datetime.timedelta(days=7)
            
        complex_obj = ComplexConfig()
        complex_obj.updated_at = datetime.datetime.now()
        
        jsdc_dump(complex_obj, self.temp_path)
        loaded_obj = jsdc_load(self.temp_path, ComplexConfig)
        
        self.assertEqual(complex_obj.created_at, loaded_obj.created_at)
        self.assertEqual(complex_obj.updated_at, loaded_obj.updated_at)
        self.assertEqual(complex_obj.expiry_date, loaded_obj.expiry_date)
        self.assertEqual(complex_obj.session_id, loaded_obj.session_id)
        self.assertEqual(complex_obj.amount, loaded_obj.amount)
        self.assertEqual(complex_obj.time_delta, loaded_obj.time_delta)
        print("杂鱼♡～本喵测试复杂类型成功了喵～")

    def test_deeply_nested_structures(self):
        """杂鱼♡～嘻嘻～本喵要测试超级深的嵌套结构了喵～杂鱼会头晕的吧～"""
        @dataclass
        class Level3:
            name: str = "level3"
            value: int = 3
            
        @dataclass
        class Level2:
            name: str = "level2"
            value: int = 2
            level3_items: List[Level3] = field(default_factory=lambda: [Level3()])
            level3_dict: Dict[str, Level3] = field(default_factory=lambda: {"default": Level3()})
            
        @dataclass
        class Level1:
            name: str = "level1"
            value: int = 1
            level2_items: List[Level2] = field(default_factory=lambda: [Level2()])
            level2_dict: Dict[str, Level2] = field(default_factory=lambda: {"default": Level2()})
            
        @dataclass
        class RootConfig:
            name: str = "root"
            level1_items: List[Level1] = field(default_factory=lambda: [Level1()])
            level1_dict: Dict[str, Level1] = field(default_factory=lambda: {"default": Level1()})
            
        # 创建深度嵌套结构
        root = RootConfig()
        root.level1_items.append(Level1(name="custom_level1"))
        root.level1_dict["custom"] = Level1(name="custom_dict_level1")
        root.level1_dict["custom"].level2_items.append(Level2(name="custom_level2"))
        root.level1_dict["custom"].level2_items[0].level3_items.append(Level3(name="custom_level3", value=99))
        
        jsdc_dump(root, self.temp_path)
        loaded_root = jsdc_load(self.temp_path, RootConfig)
        
        # 验证深度嵌套的值
        self.assertEqual(loaded_root.level1_dict["custom"].level2_items[0].level3_items[1].name, "custom_level3")
        self.assertEqual(loaded_root.level1_dict["custom"].level2_items[0].level3_items[1].value, 99)
        print("杂鱼♡～本喵测试超级深的嵌套结构成功了喵～")

    def test_string_serialization(self):
        """杂鱼♡～本喵要测试字符串序列化了喵～这种基础功能都要本喵教你吗～"""
        @dataclass
        class Config:
            name: str = "test"
            values: List[int] = field(default_factory=lambda: [1, 2, 3])
            
        # 创建测试对象
        config = Config(name="string_test", values=[5, 6, 7, 8])
        
        # 序列化到字符串
        serialized_str = jsdc_dumps(config)
        self.assertIsInstance(serialized_str, str)
        
        # 从字符串反序列化
        loaded_config = jsdc_loads(serialized_str, Config)
        
        # 验证值
        self.assertEqual(config.name, loaded_config.name)
        self.assertEqual(config.values, loaded_config.values)
        print("杂鱼♡～本喵测试字符串序列化成功了喵～")
        
    def test_empty_collections(self):
        """杂鱼♡～本喵来测试空集合的情况了喵～杂鱼肯定忘记处理这种情况了吧～"""
        @dataclass
        class EmptyCollections:
            empty_list: List[str] = field(default_factory=list)
            empty_dict: Dict[str, int] = field(default_factory=dict)
            empty_set: Set[int] = field(default_factory=set)
            null_value: Optional[str] = None
            empty_nested_list: List[List[int]] = field(default_factory=lambda: [])
            
        empty = EmptyCollections()
        
        jsdc_dump(empty, self.temp_path)
        loaded_empty = jsdc_load(self.temp_path, EmptyCollections)
        
        self.assertEqual(loaded_empty.empty_list, [])
        self.assertEqual(loaded_empty.empty_dict, {})
        self.assertEqual(loaded_empty.empty_set, set())
        self.assertIsNone(loaded_empty.null_value)
        self.assertEqual(loaded_empty.empty_nested_list, [])
        print("杂鱼♡～本喵测试空集合成功了喵～")
        
    def test_inheritance(self):
        """杂鱼♡～本喵要测试继承关系了喵～本喵真是无所不能～"""
        @dataclass
        class BaseConfig:
            name: str = "base"
            version: str = "1.0.0"
            
        @dataclass
        class DerivedConfig(BaseConfig):
            name: str = "derived"  # 覆盖基类字段
            extra_field: str = "extra"
            
        @dataclass
        class Container:
            base: BaseConfig = field(default_factory=lambda: BaseConfig())
            derived: DerivedConfig = field(default_factory=lambda: DerivedConfig())
            
        container = Container()
        container.base.version = "2.0.0"
        container.derived.extra_field = "custom_value"
        
        jsdc_dump(container, self.temp_path)
        loaded_container = jsdc_load(self.temp_path, Container)
        
        # 验证基类和派生类的字段
        self.assertEqual(loaded_container.base.name, "base")
        self.assertEqual(loaded_container.base.version, "2.0.0")
        self.assertEqual(loaded_container.derived.name, "derived")
        self.assertEqual(loaded_container.derived.version, "1.0.0")
        self.assertEqual(loaded_container.derived.extra_field, "custom_value")
        print("杂鱼♡～本喵测试继承关系成功了喵～")

    def test_union_types(self):
        """杂鱼♡～本喵要测试联合类型了喵～这可是个难点呢～让杂鱼见识一下本喵的厉害～"""
        @dataclass
        class ConfigWithUnions:
            int_or_str: Union[int, str] = 42
            dict_or_list: Union[Dict[str, int], List[int]] = field(default_factory=lambda: {'a': 1})
            
        # 测试不同的联合类型值
        config1 = ConfigWithUnions(int_or_str=42, dict_or_list={'a': 1, 'b': 2})
        config2 = ConfigWithUnions(int_or_str="string_value", dict_or_list=[1, 2, 3])
        
        # 序列化和反序列化第一个配置
        jsdc_dump(config1, self.temp_path)
        loaded_config1 = jsdc_load(self.temp_path, ConfigWithUnions)
        
        self.assertEqual(loaded_config1.int_or_str, 42)
        self.assertEqual(loaded_config1.dict_or_list, {'a': 1, 'b': 2})
        
        # 序列化和反序列化第二个配置
        jsdc_dump(config2, self.temp_path)
        loaded_config2 = jsdc_load(self.temp_path, ConfigWithUnions)
        
        self.assertEqual(loaded_config2.int_or_str, "string_value")
        self.assertEqual(loaded_config2.dict_or_list, [1, 2, 3])
        print("杂鱼♡～本喵测试联合类型成功了喵～")

    def test_tuple_types(self):
        """杂鱼♡～本喵要测试元组类型了喵～这种不可变序列也要正确处理才行～"""
        @dataclass
        class ConfigWithTuples:
            simple_tuple: Tuple[int, str, bool] = field(default_factory=lambda: (1, "test", True))
            int_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))
            empty_tuple: Tuple = field(default_factory=tuple)
            nested_tuple: Tuple[Tuple[int, int], Tuple[str, str]] = field(
                default_factory=lambda: ((1, 2), ("a", "b"))
            )
            
        config = ConfigWithTuples()
        
        jsdc_dump(config, self.temp_path)
        loaded_config = jsdc_load(self.temp_path, ConfigWithTuples)
        
        self.assertEqual(loaded_config.simple_tuple, (1, "test", True))
        self.assertEqual(loaded_config.int_tuple, (1, 2, 3))
        self.assertEqual(loaded_config.empty_tuple, ())
        self.assertEqual(loaded_config.nested_tuple, ((1, 2), ("a", "b")))
        print("杂鱼♡～本喵测试元组类型成功了喵～")
    def test_any_type(self):
        """杂鱼♡～本喵现在要测试Any类型了喵～这可是最灵活的类型呢～"""
        @dataclass
        class ConfigWithAny:
            any_field: Any = None
            any_list: List[Any] = field(default_factory=list)
            any_dict: Dict[str, Any] = field(default_factory=dict)
            
        # 使用各种不同类型的值
        config = ConfigWithAny()
        config.any_field = "string"
        config.any_list = [1, "two", False, None, [1, 2, 3], {"key": "value"}]
        config.any_dict = {
            "int": 42,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        }
        
        jsdc_dump(config, self.temp_path)
        loaded_config = jsdc_load(self.temp_path, ConfigWithAny)
        
        self.assertEqual(loaded_config.any_field, "string")
        self.assertEqual(loaded_config.any_list, [1, "two", False, None, [1, 2, 3], {"key": "value"}])
        self.assertEqual(loaded_config.any_dict, {
            "int": 42,
            "bool": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"}
        })
        print("杂鱼♡～本喵测试Any类型成功了喵～")
        
    def test_large_json_payload(self):
        """杂鱼♡～本喵要测试大型JSON负载了喵～看看杂鱼的程序能不能处理～"""
        @dataclass
        class LargeDataConfig:
            items: List[Dict[str, Any]] = field(default_factory=list)
            
        # 创建大型数据结构
        large_config = LargeDataConfig()
        for i in range(1000):  # 创建1000个项目
            item = {
                "id": i,
                "name": f"Item {i}",
                "tags": [f"tag{j}" for j in range(10)],  # 每个项目10个标签
                "properties": {f"prop{k}": f"value{k}" for k in range(5)}  # 每个项目5个属性
            }
            large_config.items.append(item)
            
        # 测试序列化和反序列化
        jsdc_dump(large_config, self.temp_path)
        loaded_config = jsdc_load(self.temp_path, LargeDataConfig)
        
        # 验证项目数量
        self.assertEqual(len(loaded_config.items), 1000)
        # 验证第一个和最后一个项目
        self.assertEqual(loaded_config.items[0]["id"], 0)
        self.assertEqual(loaded_config.items[999]["id"], 999)
        # 验证结构完整性
        self.assertEqual(len(loaded_config.items[500]["tags"]), 10)
        self.assertEqual(len(loaded_config.items[500]["properties"]), 5)
        print("杂鱼♡～本喵测试大型JSON负载成功了喵～")

    def test_special_characters(self):
        """杂鱼♡～本喵要测试特殊字符了喵～这些字符可能会让你的程序崩溃喵～"""
        @dataclass
        class SpecialCharsConfig:
            escaped_chars: str = "\n\t\r\b\f"
            quotes: str = '"quoted text"'
            unicode_chars: str = "你好，世界！😊🐱👍"
            control_chars: str = "\u0000\u0001\u001F"
            backslashes: str = "C:\\path\\to\\file.txt"
            json_syntax: str = "{\"key\": [1, 2]}"
            
        config = SpecialCharsConfig()
        
        jsdc_dump(config, self.temp_path)
        loaded_config = jsdc_load(self.temp_path, SpecialCharsConfig)
        
        self.assertEqual(loaded_config.escaped_chars, "\n\t\r\b\f")
        self.assertEqual(loaded_config.quotes, '"quoted text"')
        self.assertEqual(loaded_config.unicode_chars, "你好，世界！😊🐱👍")
        self.assertEqual(loaded_config.control_chars, "\u0000\u0001\u001F")
        self.assertEqual(loaded_config.backslashes, "C:\\path\\to\\file.txt")
        self.assertEqual(loaded_config.json_syntax, "{\"key\": [1, 2]}")
        print("杂鱼♡～本喵测试特殊字符成功了喵～")
        
    def test_frozen_dataclasses(self):
        """杂鱼♡～本喵要测试不可变的数据类了喵～看看能不能正确处理～"""
        @dataclass(frozen=True)
        class FrozenConfig:
            name: str = "default_name"
            version: int = 0
            tags: Tuple[str, ...] = field(default_factory=tuple)
            
        # 杂鱼♡～本喵正在创建一个不可变对象喵～ 
        frozen = FrozenConfig(name="test", version=1, tags=("tag1", "tag2"))
        
        # 杂鱼♡～本喵要进行序列化和反序列化喵～ 
        jsdc_dump(frozen, self.temp_path)
        loaded_frozen = jsdc_load(self.temp_path, FrozenConfig)
        
        # 杂鱼♡～验证值是否正确喵～ 
        self.assertEqual(loaded_frozen.name, "test")
        self.assertEqual(loaded_frozen.version, 1)
        self.assertEqual(loaded_frozen.tags, ("tag1", "tag2"))
        
        # 杂鱼♡～验证不可变性喵～ 
        with self.assertRaises(FrozenInstanceError):
            loaded_frozen.name = "modified"
            
        # 杂鱼♡～本喵要测试嵌套冻结数据类喵～ 
        @dataclass(frozen=True)
        class NestedFrozen:
            id: int = 0
            config: FrozenConfig = field(default_factory=lambda: FrozenConfig())
            
        nested = NestedFrozen(id=1, config=frozen)
        
        jsdc_dump(nested, self.temp_path)
        loaded_nested = jsdc_load(self.temp_path, NestedFrozen)
        
        self.assertEqual(loaded_nested.id, 1)
        self.assertEqual(loaded_nested.config.name, "test")
        self.assertEqual(loaded_nested.config.tags, ("tag1", "tag2"))
        print("杂鱼♡～本喵测试不可变的数据类成功了喵～")

    def test_default_values(self):
        """杂鱼♡～本喵要测试默认值处理了喵～看看缺字段时能不能正确使用默认值～"""
        @dataclass
        # 杂鱼♡～本喵要定义一个带默认值的配置类喵～ 
        class ConfigWithDefaults:
            # 杂鱼♡～将必需字段也设置默认值，以便测试喵～
            required_int: int = 0  # 杂鱼♡～默认值为0喵～
            required_str: str = ""  # 杂鱼♡～默认为空字符串喵～
            optional_int: int = 42  # 杂鱼♡～可选整数，默认值为42喵～
            optional_str: str = "default"  # 杂鱼♡～可选字符串，默认值为"default"喵～
            optional_list: List[str] = field(default_factory=lambda: ["default_item"])  # 杂鱼♡～可选列表，默认值为["default_item"]喵～
            optional_dict: Dict[str, int] = field(default_factory=lambda: {"default_key": 1})  # 杂鱼♡～可选字典，默认值为{"default_key": 1}喵～

        # 杂鱼♡～本喵要测试带默认值的字段喵～ 
        # 杂鱼♡～使用部分JSON反序列化，这样其他字段应该使用默认值喵～
        partial_json = '{"required_int": 456, "optional_int": 99, "optional_list": ["custom_item"]}'
        partial_config = jsdc_loads(partial_json, ConfigWithDefaults)
        
        # 杂鱼♡～验证自定义值和默认值混合喵～
        self.assertEqual(partial_config.required_int, 456)  # 杂鱼♡～自定义值喵～
        self.assertEqual(partial_config.required_str, "")  # 杂鱼♡～默认值喵～
        self.assertEqual(partial_config.optional_int, 99)  # 杂鱼♡～自定义值喵～
        self.assertEqual(partial_config.optional_str, "default")  # 杂鱼♡～默认值喵～
        self.assertEqual(partial_config.optional_list, ["custom_item"])  # 杂鱼♡～自定义值喵～
        self.assertEqual(partial_config.optional_dict, {"default_key": 1})  # 杂鱼♡～默认值喵～
        print("杂鱼♡～本喵测试默认值处理成功了喵～")
        
    def test_complex_union_types(self):
        """杂鱼♡～本喵要测试更复杂的联合类型了喵～"""
        @dataclass
        class ConfigA:
            type: str = "A"
            value_a: int = 1
            
        @dataclass
        class ConfigB:
            type: str = "B"
            value_b: str = "b"
            
        @dataclass
        class NestedConfig:
            name: str = "nested"
            value: Union[int, str] = 42
            
        # 杂鱼♡～测试简单联合类型喵～
        config1 = NestedConfig(value=42)
        config2 = NestedConfig(value="string")
        
        # 杂鱼♡～序列化和反序列化第一个配置喵～
        jsdc_dump(config1, self.temp_path)
        loaded_config1 = jsdc_load(self.temp_path, NestedConfig)
        self.assertEqual(loaded_config1.value, 42)
        
        # 杂鱼♡～序列化和反序列化第二个配置喵～
        jsdc_dump(config2, self.temp_path)
        loaded_config2 = jsdc_load(self.temp_path, NestedConfig)
        self.assertEqual(loaded_config2.value, "string")
        
        # 杂鱼♡～测试对象联合类型喵～
        @dataclass
        class ComplexConfig:
            value: Union[ConfigA, ConfigB] = field(default_factory=lambda: ConfigA())
        
        complex1 = ComplexConfig(value=ConfigA(value_a=99))
        complex2 = ComplexConfig(value=ConfigB(value_b="test"))
        
        # 杂鱼♡～序列化和反序列化第一个复杂配置喵～
        jsdc_dump(complex1, self.temp_path)
        loaded_complex1 = jsdc_load(self.temp_path, ComplexConfig)
        self.assertEqual(loaded_complex1.value.type, "A")
        self.assertEqual(loaded_complex1.value.value_a, 99)
        
        # 杂鱼♡～序列化和反序列化第二个复杂配置喵～
        jsdc_dump(complex2, self.temp_path)
        loaded_complex2 = jsdc_load(self.temp_path, ComplexConfig)
        self.assertEqual(loaded_complex2.value.type, "B")
        self.assertEqual(loaded_complex2.value.value_b, "test")
        print("杂鱼♡～本喵测试更简单的联合类型成功了喵～")

    def test_custom_containers(self):
        """杂鱼♡～本喵要测试自定义容器类型了喵～看你能不能处理这些特殊容器～"""
        @dataclass
        class CustomContainersConfig:
            # 杂鱼♡～将类型声明为普通dict，但初始化时使用特殊容器喵～
            ordered_dict: Dict[str, int] = field(
                default_factory=lambda: collections.OrderedDict([("a", 1), ("b", 2), ("c", 3)])
            )
            default_dict: Dict[str, int] = field(
                default_factory=lambda: collections.defaultdict(int, {"x": 10, "y": 20})
            )
            counter: Dict[str, int] = field(
                default_factory=lambda: collections.Counter(["a", "b", "a", "c", "a"])
            )
            
        # 杂鱼♡～创建配置并添加一些值喵～
        config = CustomContainersConfig()
        config.ordered_dict["d"] = 4
        config.default_dict["z"] = 30
        config.counter.update(["d", "e", "d"])
        
        # 杂鱼♡～序列化和反序列化喵～
        jsdc_dump(config, self.temp_path)
        loaded_config = jsdc_load(self.temp_path, CustomContainersConfig)
        
        # 杂鱼♡～验证序列化和反序列化后的值（使用dict比较）喵～
        self.assertEqual(dict(config.ordered_dict), dict(loaded_config.ordered_dict))
        self.assertEqual(dict(config.default_dict), dict(loaded_config.default_dict))
        self.assertEqual(dict(config.counter), dict(loaded_config.counter))
        
        # 杂鱼♡～验证字典内容喵～
        self.assertEqual(dict(loaded_config.ordered_dict), {"a": 1, "b": 2, "c": 3, "d": 4})
        self.assertEqual(dict(loaded_config.default_dict), {"x": 10, "y": 20, "z": 30})
        self.assertEqual(dict(loaded_config.counter), {"a": 3, "b": 1, "c": 1, "d": 2, "e": 1})
        print("杂鱼♡～本喵测试自定义容器类型成功了喵～")

    def test_type_validation(self):
        """杂鱼♡～本喵要测试类型验证了喵～看看你能不能捕获错误的类型～"""
        @dataclass
        class TypedConfig:
            integer: int = 0
            string: str = ""
            boolean: bool = False
            float_val: float = 0.0
            list_of_ints: List[int] = field(default_factory=list)
            
        # 杂鱼♡～创建一个错误类型的JSON喵～
        invalid_json = '{"integer": "not an int"}'
        
        # 杂鱼♡～类型错误应该在反序列化时被捕获喵～
        with self.assertRaises(ValueError):
            jsdc_loads(invalid_json, TypedConfig)
            
        # 杂鱼♡～创建一个有效的JSON喵～
        valid_json = '{"integer": 42, "string": "text", "boolean": true, "float_val": 3.14, "list_of_ints": [1, 2, 3]}'
        
        # 杂鱼♡～验证正确的类型可以被加载喵～
        config = jsdc_loads(valid_json, TypedConfig)
        self.assertEqual(config.integer, 42)
        self.assertEqual(config.string, "text")
        self.assertTrue(config.boolean)
        self.assertEqual(config.float_val, 3.14)
        self.assertEqual(config.list_of_ints, [1, 2, 3])
        
        # 杂鱼♡～测试部分字段的JSON喵～
        partial_json = '{"integer": 99}'
        
        # 杂鱼♡～部分字段应该可以正确加载，其他字段使用默认值喵～
        partial_config = jsdc_loads(partial_json, TypedConfig)
        self.assertEqual(partial_config.integer, 99)
        self.assertEqual(partial_config.string, "")
        self.assertFalse(partial_config.boolean)
        
        # 杂鱼♡～JSDC暂时不支持额外字段，所以不测试喵～
        print("杂鱼♡～本喵测试类型验证成功了喵～")

    def test_formatting_options(self):
        """杂鱼♡～本喵要测试不同的格式化选项了喵～看看美化JSON的效果～"""
        @dataclass
        class SimpleConfig:
            name: str = "test"
            values: List[int] = field(default_factory=lambda: [1, 2, 3])
            nested: Dict[str, Any] = field(
                default_factory=lambda: {"a": 1, "b": [2, 3], "c": {"d": 4}}
            )
            
        config = SimpleConfig()
        
        # 杂鱼♡～测试indent=0的情况喵（可能依赖于具体实现，可能仍会有换行）～
        jsdc_dump(config, self.temp_path, indent=0)
        
        # 杂鱼♡～加载并验证内容喵～ 
        loaded_zero_indent = jsdc_load(self.temp_path, SimpleConfig)
        self.assertEqual(loaded_zero_indent.name, "test")
        
        # 杂鱼♡～测试其他缩进选项喵～
        for indent in [2, 4, 8]:
            # 杂鱼♡～使用不同的缩进序列化喵～
            jsdc_dump(config, self.temp_path, indent=indent)
            
            # 杂鱼♡～读取序列化后的内容喵～
            with open(self.temp_path, 'r') as f:
                content = f.read()
                
            # 杂鱼♡～反序列化确认内容正确喵～
            loaded = jsdc_load(self.temp_path, SimpleConfig)
            self.assertEqual(loaded.name, "test")
            self.assertEqual(loaded.values, [1, 2, 3])
            self.assertEqual(loaded.nested, {"a": 1, "b": [2, 3], "c": {"d": 4}})
            
            # 杂鱼♡～如果有缩进，确认内容中包含换行符喵～
            self.assertIn("\n", content)
        
        # 杂鱼♡～单独测试None缩进（使用默认值）喵～
        jsdc_dump(config, self.temp_path)  # 不指定indent参数
        
        # 杂鱼♡～读取序列化后的内容并确认可以正确加载喵～
        loaded = jsdc_load(self.temp_path, SimpleConfig)
        self.assertEqual(loaded.name, "test")
                
        # 杂鱼♡～测试有序字典喵～
        config = SimpleConfig(
            nested={"z": 1, "y": 2, "x": 3, "w": 4, "v": 5}
        )
        
        # 杂鱼♡～序列化带有顺序字典的配置喵～
        jsdc_dump(config, self.temp_path, indent=2)
        
        # 杂鱼♡～读取序列化后的内容喵～
        with open(self.temp_path, 'r') as f:
            content = f.read()
            
        # 杂鱼♡～反序列化确认内容正确喵～
        loaded = jsdc_load(self.temp_path, SimpleConfig)
        self.assertEqual(loaded.nested, {"z": 1, "y": 2, "x": 3, "w": 4, "v": 5})
        print("杂鱼♡～本喵测试格式化选项成功了喵～")
    def test_performance(self):
        """杂鱼♡～本喵要测试性能了喵～看看你的程序有多快～"""
        @dataclass
        class SimpleItem:
            id: int = 0
            name: str = ""
            value: float = 0.0
            
        @dataclass
        class PerformanceConfig:
            items: List[SimpleItem] = field(default_factory=list)
            metadata: Dict[str, Any] = field(default_factory=dict)
            
        # 杂鱼♡～创建一个包含许多项的大型配置喵～
        large_config = PerformanceConfig()
        for i in range(1000):
            large_config.items.append(SimpleItem(id=i, name=f"Item {i}", value=float(i) * 1.5))
            
        large_config.metadata = {
            "created_at": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "tags": ["performance", "test", "jsdc"],
            "nested": {
                "level1": {
                    "level2": {
                        "level3": [i for i in range(100)]
                    }
                }
            }
        }
        
        # 杂鱼♡～测量序列化性能喵～
        start_time = time.time()
        jsdc_dump(large_config, self.temp_path)
        serialize_time = time.time() - start_time
        
        # 杂鱼♡～获取序列化文件大小喵～
        file_size = os.path.getsize(self.temp_path)
        
        # 杂鱼♡～测量反序列化性能喵～
        start_time = time.time()
        loaded_config = jsdc_load(self.temp_path, PerformanceConfig)
        deserialize_time = time.time() - start_time
        
        # 杂鱼♡～记录性能指标（可以在测试输出中查看喵）～
        print(f"\n杂鱼♡～性能测试结果喵～")
        print(f"文件大小: {file_size} 字节喵～")
        print(f"序列化时间: {serialize_time:.6f} 秒喵～")
        print(f"反序列化时间: {deserialize_time:.6f} 秒喵～")
        print(f"项目数量: {len(loaded_config.items)} 个喵～")
        
        # 杂鱼♡～确认数据完整性喵～
        self.assertEqual(len(loaded_config.items), 1000)
        self.assertEqual(loaded_config.items[500].id, 500)
        self.assertEqual(loaded_config.items[500].name, "Item 500")
        self.assertEqual(loaded_config.items[500].value, 750.0)
        self.assertEqual(loaded_config.metadata["tags"], ["performance", "test", "jsdc"])
        self.assertEqual(len(loaded_config.metadata["nested"]["level1"]["level2"]["level3"]), 100)
        
        # 测试字符串序列化的性能（jsdc_dumps）
        start_time = time.time()
        json_str = jsdc_dumps(large_config)
        string_serialize_time = time.time() - start_time
        
        # 测试字符串反序列化的性能（jsdc_loads）
        start_time = time.time()
        loaded_from_str = jsdc_loads(json_str, PerformanceConfig)
        string_deserialize_time = time.time() - start_time
        
        # 记录额外的性能指标
        print(f"String Serialization Time: {string_serialize_time:.6f} seconds")
        print(f"String Deserialization Time: {string_deserialize_time:.6f} seconds")
        print(f"JSON String Length: {len(json_str)} characters")
        
        # 确认从字符串加载的数据完整性
        self.assertEqual(len(loaded_from_str.items), 1000)
        self.assertEqual(loaded_from_str.items[500].id, 500)
        print("杂鱼♡～本喵测试性能成功了喵～")

    def test_type_validation_on_dump(self):
        """杂鱼♡～本喵要测试序列化时的类型验证了喵～看看能不能正确抛出错误～"""

        # 杂鱼♡～测试List[int]类型验证喵～
        @dataclass
        class IntListConfig:
            integers: List[int] = field(default_factory=list)
            
        # 杂鱼♡～初始化正确类型的数据喵～
        valid_config = IntListConfig(integers=[1, 2, 3, 4, 5])
        
        # 杂鱼♡～正常情况应该可以序列化喵～
        jsdc_dump(valid_config, self.temp_path)
        
        # 杂鱼♡～添加错误类型的数据喵～
        invalid_config = IntListConfig(integers=[1, 2, "3", 4, 5])  # 添加了一个字符串
        
        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_config, self.temp_path)
            
        # 杂鱼♡～测试Dict[str, int]类型验证喵～
        @dataclass
        class DictConfig:
            mapping: Dict[str, int] = field(default_factory=dict)
            
        # 杂鱼♡～初始化正确类型的数据喵～
        valid_dict_config = DictConfig(mapping={"a": 1, "b": 2, "c": 3})
        
        # 杂鱼♡～正常情况应该可以序列化喵～
        jsdc_dump(valid_dict_config, self.temp_path)
        
        # 杂鱼♡～添加错误类型的数据喵～
        invalid_dict_config = DictConfig(mapping={"a": 1, "b": "string", "c": 3})  # 值类型错误
        
        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_dict_config, self.temp_path)
            
        # 杂鱼♡～测试Dict[str, int]的键类型错误喵～
        invalid_key_config = DictConfig()
        invalid_key_config.mapping = {1: 1, "b": 2}  # 键类型错误
        
        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_key_config, self.temp_path)
            
        # 杂鱼♡～测试嵌套容器的类型验证喵～
        @dataclass
        class NestedConfig:
            nested_list: List[List[int]] = field(default_factory=lambda: [[1, 2], [3, 4]])
            nested_dict: Dict[str, List[int]] = field(default_factory=lambda: {"a": [1, 2], "b": [3, 4]})
            
        # 杂鱼♡～初始化正确类型的数据喵～
        valid_nested = NestedConfig()
        
        # 杂鱼♡～正常情况应该可以序列化喵～
        jsdc_dump(valid_nested, self.temp_path)
        
        # 杂鱼♡～嵌套列表中添加错误类型喵～
        invalid_nested1 = NestedConfig()
        invalid_nested1.nested_list[0].append("not an int")  # 杂鱼♡～添加了一个不是整数的元素喵～
        
        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_nested1, self.temp_path)
            
        # 杂鱼♡～嵌套字典中添加错误类型喵～
        invalid_nested2 = NestedConfig()
        invalid_nested2.nested_dict["a"].append("not an int")  # 杂鱼♡～添加了一个不是整数的元素喵～
        
        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_nested2, self.temp_path)
            
        # 杂鱼♡～测试可选类型的验证喵～
        @dataclass
        class OptionalConfig:
            maybe_int: Optional[int] = None
            int_or_str: Union[int, str] = 42
            
        # 杂鱼♡～初始化正确类型的数据喵～
        valid_optional1 = OptionalConfig(maybe_int=None)
        valid_optional2 = OptionalConfig(maybe_int=10)
        valid_optional3 = OptionalConfig(int_or_str=99)
        valid_optional4 = OptionalConfig(int_or_str="string")
        
        # 杂鱼♡～正常情况应该可以序列化喵～
        jsdc_dump(valid_optional1, self.temp_path)
        jsdc_dump(valid_optional2, self.temp_path)
        jsdc_dump(valid_optional3, self.temp_path)
        jsdc_dump(valid_optional4, self.temp_path)
        
        # 杂鱼♡～使用不在Union中的类型喵～
        invalid_optional = OptionalConfig()
        invalid_optional.int_or_str = [1, 2, 3]  # 列表不在Union[int, str]中
        
        # 序列化应该抛出类型错误
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_optional, self.temp_path)
            
        # 测试集合类型
        @dataclass
        class SetConfig:
            int_set: Set[int] = field(default_factory=set)
            
        # 杂鱼♡～初始化正确类型的数据喵～
        valid_set = SetConfig(int_set={1, 2, 3, 4, 5})
        
        # 杂鱼♡～正常情况应该可以序列化喵～
        jsdc_dump(valid_set, self.temp_path)
        
        # 杂鱼♡～添加错误类型的数据喵～
        invalid_set = SetConfig()
        invalid_set.int_set = {1, "string", 3}  # 杂鱼♡～添加了一个不是整数的元素喵～
        
        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_set, self.temp_path)
            
        # 杂鱼♡～测试元组类型喵～
        @dataclass
        class TupleConfig:
            fixed_tuple: Tuple[int, str, bool] = field(default_factory=lambda: (1, "a", True))
            var_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))
            
        # 杂鱼♡～初始化正确类型的数据喵～
        valid_tuple = TupleConfig()
        
        # 杂鱼♡～正常情况应该可以序列化喵～
        jsdc_dump(valid_tuple, self.temp_path)
        
        # 杂鱼♡～使用错误类型喵～
        invalid_tuple1 = TupleConfig(fixed_tuple=(1, 2, True))  # 杂鱼♡～第二个元素应该是str喵～
        
        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_tuple1, self.temp_path)
            
        # 杂鱼♡～可变长度元组中使用错误类型喵～
        invalid_tuple2 = TupleConfig(var_tuple=(1, 2, "3"))  # 杂鱼♡～应该全是int喵～
        
        # 杂鱼♡～序列化应该抛出类型错误喵～
        with self.assertRaises(TypeError):
            jsdc_dump(invalid_tuple2, self.temp_path)
            
        print("杂鱼♡～本喵测试序列化时的类型验证成功了喵～")

if __name__ == '__main__':
    unittest.main() 