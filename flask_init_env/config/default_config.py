import os

import shutil

CONTEXT_PATH = 'parse' # 替换为你的API上下文路径
DATABASE_PREFIX = 'ai_parse' # 替换为你的数据库前缀

class DefaultConfig:
    # flask 通用配置
    SECRET_KEY = 'supersecretkey' # 密钥
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 禁用 SQLALCHEMY 的追踪修改
    SCHEDULER_API_ENABLED = True # 启用 flask-scheduler