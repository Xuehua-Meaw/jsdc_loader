# 杂鱼♡～本喵的可选依赖使用指南～

## 安装选项

杂鱼♡～本喵现在支持两种安装方式喵～

### 基础安装（仅支持 dataclass）
```bash
pip install jsdc_loader
```
杂鱼♡～这样安装只支持 Python 标准库的 dataclass 功能喵～已经够用了，不要太贪心哦～


## 使用示例

### 仅使用 dataclass（无需额外依赖）

```python
from dataclasses import dataclass
from jsdc_loader import jsdc_load, jsdc_dump

@dataclass
class User:
    name: str
    age: int

# 杂鱼♡～基础功能完全可用喵～
user = User(name="杂鱼", age=18)
jsdc_dump(user, "user.json")
loaded_user = jsdc_load("user.json", User)
```


## 优势

- 🐱 **轻量级**: 基础安装不依赖任何第三方库喵～
- 🐱 **渐进式**: 需要时才安装额外功能喵～  
- 🐱 **向后兼容**: 现有代码无需修改喵～
- 🐱 **清晰错误**: 缺失依赖时给出明确提示喵～

杂鱼♡～现在可以根据自己的需求选择安装方式了喵～本喵可是很贴心的呢～～ 