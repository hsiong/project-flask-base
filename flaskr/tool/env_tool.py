import os


def extract_config(model_cls, env_dict, prefix):
    '''
    从环境变量中提取配置
    Args:
        model_cls: 模型类
        env_dict: 环境变量字典
        prefix: 前缀
    Returns:
        dict
    '''
    
    # for k in model_cls.__fields__ 遍历模型类的字段
    # if f'{prefix}{k.upper()}' in env_dict: 如果环境变量中存在该字段
    # k: env_dict.get(f'{prefix}{k.upper()}') 从环境变量中获取该字段的值
    model_dict = {k: env_dict.get(f'{prefix}{k.upper()}')
                  for k in model_cls.__fields__
                  if f'{prefix}{k.upper()}' in env_dict
                  }
    return model_cls(**model_dict)


def smart_cast(val: str):
    val = val.strip()
    val_l = val.lower()
    if val_l == "true":
        return True
    if val_l == "false":
        return False
    if val_l == "none":
        return None
    if val.isdigit():
        return int(val)
    try:
        return float(val)
    except ValueError:
        return val


def load_env(filepath=".env"):
    '''
    加载环境变量
    '''
    os_env_dict = {}
    if not os.path.exists(filepath):
        return
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                os_env_dict[key.strip()] = value.strip()
    
    return os_env_dict
