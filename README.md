![CI/CD](https://github.com/Xuehua-Meaw/jsdc_loader/actions/workflows/jsdc_loader_CICD.yml/badge.svg)
# JSDC Loader 喵～

JSDC Loader是一个功能强大的库，用于在JSON和Python数据类（dataclasses）之间进行转换～～。杂鱼们会喜欢这个简单易用的工具喵♡～ 

## 项目核心理念～♡

JSDC Loader的主要目的是提供一个**面向类型的桥梁**，在JSON和数据类转换之间建立完美的类型安全通道喵～～

### "Trust No One" 安全策略 ♡～

本喵采用了严格的"信任无人"安全策略，确保所有数据在序列化和反序列化过程中都必须**完美对齐数据类模式**喵♡～：

- **严格类型验证**：每个写入JSON或从JSON读取的变量都必须严格按照数据类模式进行类型检查喵～
- **子类型支持**：完美处理嵌套类型、继承类型、泛型类型等复杂类型结构～
- **零容忍错误**：任何类型不匹配都会被本喵立即发现并报告，杂鱼想偷懒都不行喵♡～
- **模式一致性**：确保JSON结构与数据类定义100%一致，不允许任何偏差～

### 类型安全保障 ♡～

- **递归类型检查**：从根对象到最深层嵌套结构，本喵都会逐一验证喵～
- **继承链验证**：支持复杂的类继承关系，保证类型层次结构的完整性♡～
- **泛型类型处理**：List、Dict、Set、Tuple等泛型容器的内部类型也要严格检查喵～
- **联合类型智能解析**：Union类型会按照最佳匹配原则进行类型推导和验证～

杂鱼♡～本喵就是要让你的数据转换过程绝对安全可靠，一个类型错误都不放过喵～～

## 🚀 全面的Python类型支持

### 🔧 **内置类型** - 杂鱼♡～本喵支持所有Python内置类型喵～

```python
from dataclasses import dataclass
import array
import pathlib
import ipaddress
import fractions
from decimal import Decimal
from jsdc_loader import jsdc_dump, jsdc_load

@dataclass
class BuiltinTypesDemo:
    # 基本类型
    my_int: int = 42
    my_float: float = 3.14159
    my_str: str = "杂鱼字符串"
    my_bool: bool = True
    
    # 二进制类型 - 杂鱼♡～本喵新增支持喵～
    my_bytes: bytes = b"Hello Binary World"
    my_bytearray: bytearray = bytearray(b"Mutable bytes")
    
    # 数值类型 - 杂鱼♡～数学计算不是问题喵～
    my_complex: complex = complex(3, 4)  # 3+4j
    my_decimal: Decimal = Decimal("123.456789")
    my_fraction: fractions.Fraction = fractions.Fraction(22, 7)
    
    # 集合类型 - 杂鱼♡～Python特有的类型喵～
    my_range: range = range(5, 15, 2)  # [5, 7, 9, 11, 13]
    my_slice: slice = slice(1, 10, 2)  # slice(1, 10, 2)
    
    # 数组类型 - 杂鱼♡～高性能数组喵～
    my_array: array.array = array.array('i', [1, 2, 3, 4, 5])

# 杂鱼♡～序列化和反序列化，什么类型都不怕喵～
demo = BuiltinTypesDemo()
jsdc_dump(demo, "builtin_types.json")
loaded = jsdc_load("builtin_types.json", BuiltinTypesDemo)
```

### 📚 **标准库类型** - 杂鱼♡～标准库类型全面支持喵～

```python
import datetime
import uuid
import pathlib
import ipaddress
import re
from dataclasses import dataclass, field

@dataclass
class StandardLibTypesDemo:
    # 路径类型 - 杂鱼♡～跨平台路径处理喵～
    my_path: pathlib.Path = pathlib.Path("/tmp/test.txt")
    my_pure_path: pathlib.PurePath = pathlib.PurePath("relative/path")
    
    # 网络类型 - 杂鱼♡～IP地址和网络处理喵～
    my_ipv4: ipaddress.IPv4Address = ipaddress.IPv4Address("192.168.1.1")
    my_ipv6: ipaddress.IPv6Address = ipaddress.IPv6Address("::1")
    my_ipv4_network: ipaddress.IPv4Network = ipaddress.IPv4Network("192.168.0.0/24")
    my_ipv6_network: ipaddress.IPv6Network = ipaddress.IPv6Network("2001:db8::/32")
    
    # 时间类型 - 杂鱼♡～时间处理专家喵～
    my_datetime: datetime.datetime = field(default_factory=datetime.datetime.now)
    my_date: datetime.date = field(default_factory=datetime.date.today)
    my_time: datetime.time = datetime.time(14, 30, 0)
    my_timedelta: datetime.timedelta = datetime.timedelta(days=7, hours=2)
    
    # UUID类型 - 杂鱼♡～唯一标识符喵～
    my_uuid: uuid.UUID = field(default_factory=uuid.uuid4)
    
    # 正则表达式 - 杂鱼♡～模式匹配喵～
    my_pattern: re.Pattern = re.compile(r'\d+')

# 杂鱼♡～标准库类型也轻松搞定喵～
demo = StandardLibTypesDemo()
jsdc_dump(demo, "stdlib_types.json")
loaded = jsdc_load("stdlib_types.json", StandardLibTypesDemo)
```

### 🆕 **完整的Typing系统支持** - 杂鱼♡～typing高手就是本喵喵～

```python
from dataclasses import dataclass, field
from typing import (
    List, Dict, Set, Tuple, FrozenSet, Deque,
    Union, Optional, Literal, Annotated, 
    TypedDict, NamedTuple, NewType, Any
)
from collections import deque, ChainMap, Counter, OrderedDict, defaultdict

# 杂鱼♡～NewType自定义类型喵～
UserId = NewType('UserId', int)
UserName = NewType('UserName', str)

# 杂鱼♡～TypedDict结构化字典喵～
class PersonDict(TypedDict):
    name: str
    age: int
    email: Optional[str]

# 杂鱼♡～NamedTuple命名元组喵～
class Point(NamedTuple):
    x: float
    y: float
    name: str = "unknown"

@dataclass
class TypingSystemDemo:
    # 泛型容器 - 杂鱼♡～类型安全的容器喵～
    my_list: List[int] = field(default_factory=lambda: [1, 2, 3])
    my_dict: Dict[str, int] = field(default_factory=lambda: {"a": 1, "b": 2})
    my_set: Set[str] = field(default_factory=lambda: {"apple", "banana"})
    my_tuple: Tuple[int, str, bool] = (42, "answer", True)
    my_frozenset: FrozenSet[int] = frozenset([1, 2, 3])
    my_deque: Deque[str] = deque(["first", "second"])
    
    # 高级容器 - 杂鱼♡～Python高级数据结构喵～
    my_chainmap: ChainMap = ChainMap({'a': 1}, {'b': 2})
    my_counter: Counter = Counter(['apple', 'banana', 'apple'])
    my_ordered_dict: OrderedDict = OrderedDict([('first', 1), ('second', 2)])
    my_default_dict: defaultdict = field(default_factory=lambda: defaultdict(list))
    
    # 联合类型 - 杂鱼♡～灵活的类型组合喵～
    union_field: Union[int, str, bool] = 42
    optional_field: Optional[str] = "可选字符串"
    
    # 字面量类型 - 杂鱼♡～精确的值约束喵～
    literal_field: Literal["apple", "banana", "cherry"] = "apple"
    
    # 注解类型 - 杂鱼♡～带元数据的类型喵～
    annotated_field: Annotated[int, "这是一个带注解的整数"] = 100
    
    # 结构化类型 - 杂鱼♡～复杂结构轻松处理喵～
    typed_dict_field: PersonDict = field(default_factory=lambda: {
        "name": "杂鱼用户", "age": 25, "email": "user@example.com"
    })
    named_tuple_field: Point = Point(x=10.5, y=20.3, name="测试点")
    
    # 自定义类型 - 杂鱼♡～NewType也支持喵～
    user_id: UserId = UserId(12345)
    user_name: UserName = UserName("杂鱼昵称")
    
    # 任意类型 - 杂鱼♡～灵活处理喵～
    any_field: Any = {"anything": "goes here"}

# 杂鱼♡～typing系统全面支持，什么复杂类型都不怕喵～
demo = TypingSystemDemo()
jsdc_dump(demo, "typing_system.json")
loaded = jsdc_load("typing_system.json", TypingSystemDemo)
```

### 🔥 **增强的枚举类型支持** - 杂鱼♡～枚举专家就是本喵喵～

```python
from dataclasses import dataclass
from enum import Enum, IntEnum, Flag, IntFlag, auto

# 杂鱼♡～普通枚举喵～
class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

# 杂鱼♡～整数枚举喵～
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

# 杂鱼♡～标志枚举 - 支持组合值喵～
class Features(Flag):
    NONE = 0
    ENCRYPTION = auto()
    COMPRESSION = auto()
    BACKUP = auto()
    ALL = ENCRYPTION | COMPRESSION | BACKUP  # 组合值

# 杂鱼♡～整数标志枚举喵～
class Permission(IntFlag):
    READ = 1
    WRITE = 2
    EXECUTE = 4
    ADMIN = READ | WRITE | EXECUTE  # 组合权限

@dataclass
class EnumTypesDemo:
    my_status: Status = Status.PENDING
    my_priority: Priority = Priority.HIGH
    my_features: Features = Features.ALL  # 杂鱼♡～组合Flag值也支持喵～
    my_permission: Permission = Permission.ADMIN
    
    # 杂鱼♡～枚举作为字典键也完全支持喵～
    status_messages: Dict[Status, str] = field(default_factory=lambda: {
        Status.PENDING: "处理中",
        Status.COMPLETED: "已完成",
        Status.FAILED: "失败了"
    })

# 杂鱼♡～枚举类型和组合值都完美支持喵～
demo = EnumTypesDemo()
jsdc_dump(demo, "enum_types.json")
loaded = jsdc_load("enum_types.json", EnumTypesDemo)
```

### 🌟 **Python版本特性支持** - 杂鱼♡～与时俱进的本喵喵～

```python
# Python 3.9+ 内置泛型语法支持
from dataclasses import dataclass
from typing import Union, Optional

@dataclass 
class ModernPythonDemo:
    # 杂鱼♡～Python 3.9+ 可以直接用内置类型作为泛型喵～
    modern_list: list[int] = field(default_factory=lambda: [1, 2, 3])
    modern_dict: dict[str, int] = field(default_factory=lambda: {"key": 42})
    modern_set: set[str] = field(default_factory=lambda: {"item1", "item2"})
    modern_tuple: tuple[int, ...] = (1, 2, 3, 4, 5)
    
    # 杂鱼♡～传统语法当然也支持喵～
    classic_union: Union[int, str] = "classic"
    classic_optional: Optional[bool] = True

# Python 3.10+ Union语法 (如果可用的话)
if sys.version_info >= (3, 10):
    @dataclass
    class Python310Demo:
        # 杂鱼♡～Python 3.10+ 的新Union语法 int | str 喵～
        new_union: int | str = 42
        new_optional: str | None = "新语法"

# 杂鱼♡～无论什么Python版本，本喵都完美支持喵～
```

### 🔑 **复杂字典键类型支持** - 杂鱼♡～字典键类型专家喵～

```python
from dataclasses import dataclass, field
from typing import Dict, Literal
import uuid
from enum import Enum

class KeyEnum(Enum):
    KEY1 = "key1"
    KEY2 = "key2"

@dataclass
class ComplexKeyDemo:
    # 杂鱼♡～枚举作为字典键喵～
    enum_keys: Dict[KeyEnum, str] = field(default_factory=lambda: {
        KeyEnum.KEY1: "值1",
        KeyEnum.KEY2: "值2"
    })
    
    # 杂鱼♡～Literal作为字典键喵～
    literal_keys: Dict[Literal["apple", "banana"], int] = field(default_factory=lambda: {
        "apple": 100,
        "banana": 200
    })
    
    # 杂鱼♡～UUID作为字典键喵～
    uuid_keys: Dict[uuid.UUID, str] = field(default_factory=lambda: {
        uuid.uuid4(): "第一个",
        uuid.uuid4(): "第二个"
    })
    
    # 杂鱼♡～更多复杂键类型喵～
    int_keys: Dict[int, str] = field(default_factory=lambda: {1: "one", 2: "two"})
    bool_keys: Dict[bool, str] = field(default_factory=lambda: {True: "真", False: "假"})

# 杂鱼♡～复杂字典键类型都能处理喵～
demo = ComplexKeyDemo()
jsdc_dump(demo, "complex_keys.json")
loaded = jsdc_load("complex_keys.json", ComplexKeyDemo)
```

## 特点～♡

- **🎯 全面类型支持**：从Python内置类型到最新typing特性，本喵统统支持喵～
- **🔧 内置类型完整覆盖**：bytes、complex、range、slice、array等一个不落喵♡～
- **📚 标准库类型支持**：pathlib、ipaddress、fractions等现代Python类型～
- **🆕 最新Python特性**：Python 3.9+内置泛型、3.10+ Union语法、3.11+新特性～
- **🔥 增强枚举支持**：Enum、IntEnum、Flag、IntFlag，包括组合Flag值～
- **🌟 复杂嵌套结构**：无限深度的嵌套数据类、泛型、联合类型～
- **🚀 高性能优化**：缓存机制、批量验证、智能类型推导～
- **🛡️ 类型安全保障**：严格的类型验证，零容忍错误处理～
- **🔑 复杂字典键**：枚举、UUID、Literal等作为字典键完全支持～
- **💡 智能错误提示**：详细的类型错误信息，帮助杂鱼快速定位问题～

## 安装方法

```bash
pip install jsdc-loader
```

## 使用指南

### 基础用法

```python
# 杂鱼♡～这是最基本的用法喵～本喵教你序列化和反序列化～
from dataclasses import dataclass, field
from jsdc_loader import jsdc_load, jsdc_dump, jsdc_loads, jsdc_dumps

@dataclass
class Config:
    name: str = "default"
    port: int = 8080
    debug: bool = False

# 序列化到JSON文件，杂鱼看好了喵～
config = Config(name="myapp", port=5000)
jsdc_dump(config, "config.json")

# 从JSON文件反序列化，简单吧杂鱼～
loaded_config = jsdc_load("config.json", Config)
print(loaded_config.name)  # 输出 "myapp"

# 本喵还支持字符串序列化/反序列化喵～
json_str = jsdc_dumps(config)
loaded_from_str = jsdc_loads(json_str, Config)
```

### 嵌套数据类

```python
# 杂鱼♡～本喵来教你处理嵌套的数据类结构喵～
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from jsdc_loader import jsdc_load, jsdc_dumps, jsdc_dump

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = "password"
    ips: List[str] = field(default_factory=lambda: ["127.0.0.1"])
    primary_user: Optional[str] = None

@dataclass
class AppConfig:
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    version: str = "1.0.0"
    debug: bool = False
    settings: Dict[str, str] = field(default_factory=lambda: {"theme": "dark"})

# 创建配置并修改一些值，杂鱼看好了喵～
app = AppConfig()
app.database.ips.extend(["192.168.1.1", "10.0.0.1"])
app.settings["language"] = "en"

# 序列化到文件，简单吧杂鱼～
jsdc_dump(app, "app_config.json")

# 反序列化，一切都按照杂鱼的规则处理好了喵♡～
loaded_app = jsdc_load("app_config.json", AppConfig)
```

### 复杂类型支持

```python
# 杂鱼♡～本喵支持各种复杂类型喵～这些都不是问题～
import datetime
import uuid
from decimal import Decimal
from dataclasses import dataclass, field
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class ComplexConfig:
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now())
    expiry_date: datetime.date = field(default_factory=lambda: datetime.date.today())
    session_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4())
    amount: Decimal = Decimal('10.50')
    time_delta: datetime.timedelta = datetime.timedelta(days=7)
    
# 序列化和反序列化，杂鱼看好了喵～
config = ComplexConfig()
jsdc_dump(config, "complex.json")
loaded = jsdc_load("complex.json", ComplexConfig)

# 所有复杂类型都保持一致，本喵太厉害了喵♡～
assert loaded.created_at == config.created_at
assert loaded.session_id == config.session_id
assert loaded.amount == config.amount
```

### 集合类型与哈希支持

```python
# 杂鱼♡～本喵教你如何使用集合和哈希模型喵～
from dataclasses import dataclass, field
from typing import Set

@dataclass(frozen=True)  # 让数据类不可变以支持哈希
class Model:
    base_url: str = ""
    api_key: str = ""
    model: str = ""

    def __hash__(self):
        return hash((self.base_url, self.api_key, self.model))  # 本喵用元组哈希值

    def __eq__(self, other):
        if not isinstance(other, Model):
            return NotImplemented
        return (self.base_url, self.api_key, self.model) == (other.base_url, other.api_key, other.model)

@dataclass
class ModelList:
    models: Set[Model] = field(default_factory=set)
    
# 创建模型集合，杂鱼看本喵如何操作～
model1 = Model(base_url="https://api1.example.com", api_key="key1", model="gpt-4")
model2 = Model(base_url="https://api2.example.com", api_key="key2", model="gpt-3.5")

model_list = ModelList()
model_list.models.add(model1)
model_list.models.add(model2)

# 序列化和反序列化，本喵轻松搞定喵♡～
jsdc_dump(model_list, "models.json")
loaded_list = jsdc_load("models.json", ModelList)
```

### 联合类型

```python
# 杂鱼♡～本喵来展示如何处理联合类型喵～
from dataclasses import dataclass, field
from typing import Union, Dict, List
from jsdc_loader import jsdc_load, jsdc_dumps, jsdc_loads

@dataclass
class ConfigWithUnions:
    int_or_str: Union[int, str] = 42
    dict_or_list: Union[Dict[str, int], List[int]] = field(default_factory=lambda: {'a': 1})
    
# 两种不同的类型，本喵都能处理喵♡～
config1 = ConfigWithUnions(int_or_str=42, dict_or_list={'a': 1, 'b': 2})
config2 = ConfigWithUnions(int_or_str="string_value", dict_or_list=[1, 2, 3])

# 序列化为字符串，杂鱼看好了喵～
json_str1 = jsdc_dumps(config1)
json_str2 = jsdc_dumps(config2)

# 反序列化，联合类型完美支持，本喵太强了喵♡～
loaded1 = jsdc_loads(json_str1, ConfigWithUnions)
loaded2 = jsdc_loads(json_str2, ConfigWithUnions)
```

### 元组类型

```python
# 杂鱼♡～本喵来展示如何处理元组类型喵～
from dataclasses import dataclass, field
from typing import Tuple
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class ConfigWithTuples:
    simple_tuple: Tuple[int, str, bool] = field(default_factory=lambda: (1, "test", True))
    int_tuple: Tuple[int, ...] = field(default_factory=lambda: (1, 2, 3))
    nested_tuple: Tuple[Tuple[int, int], Tuple[str, str]] = field(
        default_factory=lambda: ((1, 2), ("a", "b"))
    )
    
# 序列化和反序列化，本喵轻松处理喵♡～
config = ConfigWithTuples()
jsdc_dump(config, "tuples.json")
loaded = jsdc_load("tuples.json", ConfigWithTuples)

# 元组类型保持一致，本喵太厉害了喵♡～
assert loaded.simple_tuple == (1, "test", True)
assert loaded.nested_tuple == ((1, 2), ("a", "b"))
```

### 特殊字符处理

```python
# 杂鱼♡～本喵来展示如何处理特殊字符喵～
from dataclasses import dataclass
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class SpecialCharsConfig:
    escaped_chars: str = "\n\t\r\b\f"
    quotes: str = '"quoted text"'
    unicode_chars: str = "你好，世界！😊🐱👍"
    backslashes: str = "C:\\path\\to\\file.txt"
    json_syntax: str = "{\"key\": [1, 2]}"
    
# 序列化和反序列化，杂鱼看本喵如何处理特殊字符喵♡～
config = SpecialCharsConfig()
jsdc_dump(config, "special.json")
loaded = jsdc_load("special.json", SpecialCharsConfig)

# 所有特殊字符都保持一致，本喵太强了喵♡～
assert loaded.unicode_chars == "你好，世界！😊🐱👍"
assert loaded.json_syntax == "{\"key\": [1, 2]}"
```

### 性能优化

JSDC Loader经过性能优化，即使处理大型结构也能保持高效喵♡～。杂鱼主人可以放心使用，本喵已经做了充分的性能测试喵～。

## 🎯 支持的Python类型总览

### ✅ **内置类型**
- 基本类型：`int`, `float`, `str`, `bool`
- 二进制类型：`bytes`, `bytearray`, `memoryview`
- 数值类型：`complex`, `Decimal`, `Fraction`
- 集合类型：`range`, `slice`, `list`, `dict`, `set`, `tuple`, `frozenset`
- 数组类型：`array.array`

### ✅ **标准库类型**
- 时间类型：`datetime`, `date`, `time`, `timedelta`
- 路径类型：`pathlib.Path`, `pathlib.PurePath`
- 网络类型：`ipaddress.IPv4Address`, `IPv6Address`, `IPv4Network`, `IPv6Network`
- 唯一标识：`uuid.UUID`
- 正则表达式：`re.Pattern`

### ✅ **Typing系统**
- 泛型容器：`List[T]`, `Dict[K,V]`, `Set[T]`, `Tuple[T,...]`, `FrozenSet[T]`, `Deque[T]`
- 高级容器：`ChainMap`, `Counter`, `OrderedDict`, `DefaultDict`
- 联合类型：`Union[T, U]`, `Optional[T]`, `T | U` (Python 3.10+)
- 字面量：`Literal["value1", "value2"]`
- 结构化：`TypedDict`, `NamedTuple`
- 特殊类型：`Any`, `ClassVar`, `Final`, `Annotated`, `NewType`

### ✅ **枚举类型**
- `Enum`, `IntEnum`, `Flag`, `IntFlag`
- 组合Flag值：`MyFlag.A | MyFlag.B`
- 枚举作为字典键完全支持

### ✅ **Python版本特性**
- Python 3.9+：内置泛型 `list[int]`, `dict[str, int]`
- Python 3.10+：Union语法 `int | str`
- Python 3.11+：`Self`, `Never`, `NotRequired`, `Required`, `TypeGuard`, `TypeIs`
- Python 3.13：`ReadOnly` TypedDict

### 🔄 **扩展支持**
- NumPy arrays (可选)
- Pandas DataFrames (可选)
- 异步类型 (Future等)

## 错误处理

本喵为各种情况提供了详细的错误信息喵～：

- FileNotFoundError：当指定的文件不存在时
- ValueError：无效输入、超过限制的文件大小、编码问题
- TypeError：类型验证错误，杂鱼给错类型了喵～
- OSError：文件系统相关错误

## 许可证

MIT 

杂鱼♡～本喵已经为你提供了最完整的说明文档，现在支持全面的Python类型系统！快去用起来喵～～
