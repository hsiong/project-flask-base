import os

import shutil

NACOS_SERVER = "http://url"  # 替换为你的 Nacos 服务器地址
NACOS_USERNAME = "nacos" # 替换为你的 Nacos 用户名
NACOS_PASSWORD = "pwd" # 替换为你的 Nacos 密码
NACOS_GROUP = "AI_COW"    # 替换为你的 Nacos Group

CONTEXT_PATH = 'context-path' # 替换为你的API上下文路径
CONTEXT_PATH_COW = CONTEXT_PATH + '/api' # 替换为你的API上下文路径
DATABASE_PREFIX = 'ai_db' # 替换为你的数据库前缀

class DefaultConfig:
    # flask 通用配置
    SECRET_KEY = 'supersecretkey' # 密钥
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 禁用 SQLALCHEMY 的追踪修改
    SCHEDULER_API_ENABLED = True # 启用 flask-scheduler


def delete_cache_file():
    '''

    删除缓存文件
    Returns:

    '''
    cache_dir = "nacos-data"

    # 检查文件夹是否存在，然后删除
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
    else:
        print(f"Cache directory not found: {cache_dir}")