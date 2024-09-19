import argparse

import nacos
import onnxruntime
import yaml
from flask import Flask
from flask_apscheduler import APScheduler

from flaskr.config import default_config
from flaskr.service import inference_grounding_dino_service, inference_damoyolo_service
from flaskr.service.schedule_service import *
from flaskr.tool import auth_tool
from flaskr.tool.auth_tool import AuthConfig
from flaskr.tool.mysql_tool import init_mysql, keep_mysql_connection_alive
from flaskr.tool.redis_tool import ProjectRedis


def create_app():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Flask with Nacos Configuration")
    parser.add_argument('--env', type=str, default='dev', help='Set the environment: dev, test, prod')
    args = parser.parse_args()
    env = args.env
    # 根据命令行参数或默认配置选择环境
    
    # 初始化 Flask 应用
    app = Flask(__name__)
    app.config.from_object("config.default_config.DefaultConfig")
    
    # 从 Nacos 获取环境特定的配置
    try:
        nacos_client = nacos.NacosClient(default_config.NACOS_SERVER,
                                         namespace=env,
                                         username=default_config.NACOS_USERNAME,
                                         password=default_config.NACOS_PASSWORD)
    except Exception as e:
        raise Exception(f"Can not connect Nacos Server: {default_config.NACOS_SERVER} " + str(e))
    nacos_context_id = default_config.CONTEXT_PATH + "-" + env + ".yml"
    nacos_config = nacos_client.get_config(nacos_context_id, default_config.NACOS_GROUP)
    nacos_config_dict = yaml.safe_load(nacos_config)  # 解析 YAML 配置
    default_config.delete_cache_file()
    
    # 提取 Redis 配置并应用到 Flask
    redis_config = nacos_config_dict.get('redis', {})
    redis_password = redis_config.get('password')
    redis_host = redis_config.get('host')
    redis_port = redis_config.get('port')
    redis_db = redis_config.get('database')
    redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/{redis_db}"
    app.config['REDIS_URL'] = redis_url
    app.config['REDIS_OPTIONS'] = {
        'retry_on_timeout': True,  # 重试
        'socket_keepalive': True,  # 启用 Keepalive 以保持长连接
    }
    app.config['REDIS_SOCKET_TIMEOUT'] = 10  # 增加 Redis 超时设置
    redis_client = ProjectRedis()
    redis_client.init_app(app)  # 在应用工厂中初始化 Redis 客户端
    
    # 提取端口
    args.port = nacos_config_dict.get('port')
    
    # 提取认证配置
    auth_config_dict = nacos_config_dict.get('auth')
    auth_tool.auth_config = AuthConfig(**auth_config_dict)  # 使用解包的方式将字典的键值对传入类
    
    # 初始化 MySQL
    db = init_mysql(app, nacos_config_dict)
    
    # 初始化定时任务
    scheduler = APScheduler()
    scheduler.init_app(app)
    # scheduler.add_job(id='keep_mysql_connection_alive', func=keep_mysql_connection_alive, args=[app, db], trigger='interval', minutes=5) # mysql 连接
    scheduler.start()
    
    return app, args

