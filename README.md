# JSDC Loader 喵～
![CI/CD](https://github.com/Xuehua-Meaw/jsdc_loader/actions/workflows/python-app.yml/badge.svg)
JSDC Loader是一个功能强大的库，用于在JSON和Python数据类（dataclasses）/Pydantic模型之间进行转换～～。杂鱼们会喜欢这个简单易用的工具喵♡～ 

## 特点～♡

- 在JSON和Python数据类之间无缝转换喵～
- 完美支持嵌套的数据类结构～
- 枚举类型（Enum）支持，杂鱼都不用操心♡～
- 支持Pydantic的BaseModel类喵～
- 支持Set、Tuple等复杂容器类型～
- 支持复杂类型（datetime、UUID、Decimal等）～
- 高性能序列化和反序列化，内部使用 orjson 带来极致速度喵，即使对于大型JSON也很快喵♡～
- 更严格的序列化时类型检查，确保数据在转换前的类型正确性喵～ (完善的类型验证和错误处理，本喵帮杂鱼处理好了一切～)
- Optional/Union类型支持，杂鱼可以放心使用喵～
- 支持冻结（frozen）数据类，让杂鱼的数据不可变～
- 支持继承关系的数据类，层次结构也没问题喵♡～
- 支持UUID作为字典键，满足更多特殊需求喵～
- 直接支持顶层列表对象的序列化与反序列化喵～

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

### 枚举类型

```python
# 杂鱼♡～本喵来教你处理枚举类型喵～
from dataclasses import dataclass, field
from enum import Enum, auto
from jsdc_loader import jsdc_load, jsdc_dump

class UserType(Enum):
    ADMIN = auto()
    USER = auto()
    GUEST = auto()

@dataclass
class UserConfig:
    name: str = "John Doe"
    user_type: UserType = field(default_factory=lambda: UserType.USER)
    
# 创建并序列化，杂鱼看好了喵～
user = UserConfig(name="Admin", user_type=UserType.ADMIN)
jsdc_dump(user, "user.json")

# 反序列化后枚举值完全保持一致，本喵处理得很完美喵♡～
loaded_user = jsdc_load("user.json", UserConfig)
assert loaded_user.user_type == UserType.ADMIN
```

### Pydantic模型

```python
# 杂鱼♡～Pydantic模型也可以序列化/反序列化喵～
from pydantic import BaseModel
from typing import List, Dict
from jsdc_loader import jsdc_load, jsdc_dump

class ServerConfig(BaseModel):
    name: str = "main"
    port: int = 8080
    ssl: bool = True
    headers: Dict[str, str] = {"Content-Type": "application/json"}

class ApiConfig(BaseModel):
    servers: List[ServerConfig] = []
    timeout: int = 30
    retries: int = 3

# 创建并序列化，杂鱼看好了喵～
api_config = ApiConfig()
api_config.servers.append(ServerConfig(name="backup", port=8081))
api_config.servers.append(ServerConfig(name="dev", port=8082, ssl=False))

jsdc_dump(api_config, "api_config.json")
loaded_api = jsdc_load("api_config.json", ApiConfig)
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

### 处理顶层列表对象喵～

```python
# 杂鱼♡～本喵还能直接处理顶层是列表的数据对象喵～
from dataclasses import dataclass
from typing import List
from jsdc_loader import jsdc_dumps, jsdc_loads

@dataclass
class ListItem:
    id: int
    name: str

# 创建一个列表的实例喵～
list_of_items = [ListItem(id=1, name="item1"), ListItem(id=2, name="item2")]

# 序列化列表到JSON字符串，看本喵操作喵～
json_list_str = jsdc_dumps(list_of_items)
print(json_list_str)
# 输出会是: [{"id": 1, "name": "item1"}, {"id": 2, "name": "item2"}] (如果 indent=None 或紧凑模式)

# 从JSON字符串反序列化回列表对象，简单吧杂鱼～
loaded_list_of_items = jsdc_loads(json_list_str, List[ListItem])
assert len(loaded_list_of_items) == 2
assert loaded_list_of_items[0].name == "item1"
print(f"第一个项目名称: {loaded_list_of_items[0].name}喵～")
```

### 性能优化

JSDC Loader 内部使用 `orjson` 库进行核心JSON处理，带来了显著的性能提升喵♡～。杂鱼主人可以放心使用，本喵已经做了充分的性能测试喵～。

**关于缩进参数 `indent` 的小提示喵～：**
当使用 `jsdc_dumps` 或 `jsdc_dump` 并指定 `indent` 参数进行格式化输出时：
- 如果 `indent` 为 `None` 或 `0`，将输出紧凑的JSON喵～。
- 如果 `indent` 为一个正整数（例如 `2`, `4` 等），`jsdc_loader` 会利用 `orjson` 的 `OPT_INDENT_2` 选项，产生带有2个空格缩进的格式化JSON喵～。这意味着无论指定哪个正整数作为缩进级别，实际输出都会是2空格缩进喵～。这是为了兼顾格式化和 `orjson` 的性能优势所做的平衡喵～。

## 错误处理

本喵为各种情况提供了详细的错误信息喵～：

- FileNotFoundError：当指定的文件不存在时
- ValueError：无效输入、超过限制的文件大小、编码问题
- TypeError：类型验证错误，杂鱼给错类型了喵～
- OSError：文件系统相关错误

## 许可证

MIT 

杂鱼♡～本喵已经为你提供了最完整的说明文档，快去用起来喵～～ 