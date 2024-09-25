from typing import get_type_hints, TypeVar, Any
from enum import Enum
from dataclasses import dataclass, is_dataclass
import json

T = TypeVar('T', bound=dataclass) # type hinting for dataclass
def jsdc_load(data_path: str, data_class: T, encoding: str = 'utf-8') -> T:
    def __dict_to_dataclass(c_obj: Any, c_data: dict):
        t_hints: dict = get_type_hints(type(c_obj))
        for key, value in c_data.items():
            if hasattr(c_obj, key):
                e_type = t_hints.get(key)
                if isinstance(value, dict):
                    n_obj = getattr(c_obj, key)
                    __dict_to_dataclass(n_obj, value)
                else:
                    if e_type is not None:
                        try:
                            if issubclass(e_type, Enum):
                                value = e_type[value]
                            else:
                                value = e_type(value)
                        except (ValueError, KeyError):
                            raise ValueError(f'invalid type for key {key}, expected {e_type}, got {type(value)}')
                    if e_type is not None and not isinstance(value, e_type):
                        raise TypeError(f'Invalid type for key {key}: expected {e_type}, got {type(value)}')
                    setattr(c_obj, key, value)
            else:
                raise ValueError(f'unknown data key: {key}')

    with open(data_path, 'r', encoding=encoding) as f:
        try:
            data: dict = json.load(f)
        except json.JSONDecodeError:
            raise ValueError('not supported file format, only json is supported')
    if not is_dataclass(data_class):
        raise ValueError('data_class must be a dataclass')
    root_obj: T = data_class()
    __dict_to_dataclass(root_obj, data)

    return root_obj


def jsdc_dump(obj: T, output_path: str, encoding: str = 'utf-8', indent: int = 4) -> None:
    def __dataclass_to_dict(obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.name
        elif isinstance(obj, list):
            return [__dataclass_to_dict(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            result = {}
            t_hints = get_type_hints(type(obj))
            for key, value in vars(obj).items():
                e_type = t_hints.get(key)
                if e_type is not None and not isinstance(value, e_type):
                    raise TypeError(f'Invalid type for key {key}: expected {e_type}, got {type(value)}')
                result[key] = __dataclass_to_dict(value)
            return result
        return obj

    if not is_dataclass(obj):
        raise ValueError('obj must be a dataclass')
    data_dict = __dataclass_to_dict(obj)
    with open(output_path, 'w', encoding=encoding) as f:
        json.dump(obj=data_dict, fp=f, indent=indent)



if __name__ == '__main__':
    from dataclasses import field
    from enum import auto
    @dataclass
    class DatabaseConfig:
        host: str = 'localhost'
        port: int = 3306
        user: str = 'root'
        password: str = 'password'

    jsdc_dump(DatabaseConfig(), 'config.json')
    data = jsdc_load('config.json', DatabaseConfig)
    print(data.host)


    from dataclasses import dataclass, field
    from enum import Enum, auto

    data = DatabaseConfig()
    jsdc_dump(data, 'config.json')

    loaded_data = jsdc_load('config.json', DatabaseConfig)
    print(loaded_data.host)

    @dataclass
    class UserType(Enum):
        ADMIN = auto()
        USER = auto()

    @dataclass
    class UserConfig:
        name: str = 'John Doe'
        age: int = 30
        married: bool = False
        user_type: UserType = field(default_factory=lambda: UserType.USER)

    @dataclass
    class AppConfig:
        user: UserConfig = field(default_factory=lambda: UserConfig())
        database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())

    app_data = AppConfig()
    jsdc_dump(app_data, 'config.json')

    loaded_app_data = jsdc_load('config.json', AppConfig)
    print(loaded_app_data.user.name)

    loaded_app_data.user.name = 'Jane Doe'
    jsdc_dump(loaded_app_data, 'config.json')
    print(loaded_app_data.user.name)

    @dataclass
    class ControllerConfig:
        controller_id: str = 'controller_01'
        controller_type: str = 'controller_type_01'
        controller_version: str = 'controller_version_01'
        utc_offset: float = 0.0
        app: AppConfig = field(default_factory=lambda: AppConfig())

    controller_data = ControllerConfig()
    controller_data.utc_offset = 9.0
    jsdc_dump(controller_data, 'config.json')

    loaded_controller_data = jsdc_load('config.json', ControllerConfig)
    print(loaded_controller_data)

    try:
        loaded_controller_data = jsdc_load('config.json', AppConfig)
        print(loaded_controller_data)
    except Exception as e:
        print(e)

    import os
    os.remove('config.json')
