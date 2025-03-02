# JSDC Loader

JSDC Loader is a utility library for converting between JSON and Python dataclasses/Pydantic models.

## Features

- Convert JSON to Python dataclasses
- Convert Python dataclasses to JSON
- Support for nested dataclasses
- Support for Enum types
- Support for Pydantic BaseModel classes
- Type validation and error handling
- Proper handling of Optional/Union types

## Installation

```bash
pip install jsdc-loader
```

## Usage

### Basic Usage

```python
from dataclasses import dataclass, field
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class Config:
    name: str = "default"
    port: int = 8080
    debug: bool = False

# Serialize to JSON file
config = Config(name="myapp", port=5000)
jsdc_dump(config, "config.json")

# Deserialize from JSON file
loaded_config = jsdc_load("config.json", Config)
print(loaded_config.name)  # "myapp"
```

### Nested Dataclasses

```python
from dataclasses import dataclass, field
from typing import List, Dict
from jsdc_loader import jsdc_load, jsdc_loads, jsdc_dump

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = "password"

@dataclass
class AppConfig:
    name: str = "myapp"
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    debug: bool = False
    settings: Dict[str, str] = field(default_factory=dict)

# Create a config object
config = AppConfig(
    name="production-app",
    database=DatabaseConfig(host="db.example.com", port=5432),
    settings={"theme": "dark", "language": "en"}
)

# Serialize to JSON
jsdc_dump(config, "app_config.json")

# Deserialize from JSON string
json_str = '{"name": "test-app", "database": {"host": "localhost", "port": 3306, "user": "tester", "password": "test123"}, "debug": true, "settings": {"env": "test"}}'
test_config = jsdc_loads(json_str, AppConfig)
```

### Enums

```python
from dataclasses import dataclass, field
from enum import Enum, auto
from jsdc_loader import jsdc_load, jsdc_dump

class UserRole(Enum):
    ADMIN = auto()
    USER = auto()
    GUEST = auto()

@dataclass
class User:
    name: str
    role: UserRole = UserRole.USER

user = User(name="John", role=UserRole.ADMIN)
jsdc_dump(user, "user.json")

loaded_user = jsdc_load("user.json", User)
assert loaded_user.role == UserRole.ADMIN
```

### Pydantic Models

```python
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

# Create and serialize
api_config = ApiConfig()
api_config.servers.append(ServerConfig(name="backup", port=8081))
api_config.servers.append(ServerConfig(name="dev", port=8082, ssl=False))

jsdc_dump(api_config, "api_config.json")
loaded_api = jsdc_load("api_config.json", ApiConfig)
```

## Error Handling

JSDC Loader provides detailed error messages for various scenarios:

- FileNotFoundError: When the specified file doesn't exist
- ValueError: For invalid inputs, file sizes exceeding limits, encoding issues
- TypeError: For type validation errors
- OSError: For file system related errors

## License

MIT 