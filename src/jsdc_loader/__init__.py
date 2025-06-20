"""杂鱼♡～这是本喵的JSDC Loader v2.0喵～完全重构的架构♡～"""

# 杂鱼♡～从api层导入公共接口喵～
from .api.loader import jsdc_load, jsdc_loads
from .api.dumper import jsdc_dump, jsdc_dumps

# 杂鱼♡～初始化转换器系统喵～
from .converters import initialize_converters
initialize_converters()

__author__ = "Neko"
__version__ = "2.0.0"
__all__ = ["jsdc_load", "jsdc_loads", "jsdc_dump", "jsdc_dumps"]

# 杂鱼♡～新架构采用schema-first设计，不再有运行时类型猜测了喵～
# 本喵才不是因为担心杂鱼不理解新架构才写这么详细的注释的♡～ 