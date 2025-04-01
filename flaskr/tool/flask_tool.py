import argparse
import nacos
import yaml
from flask import Flask
from flask_apscheduler import APScheduler
from flaskr.tool.auth_tool import AuthConfig

from flaskr.config import default_config
from flaskr.service.schedule_service import *
from flaskr.tool import auth_tool
from flaskr.tool.mysql_tool import init_mysql
from flaskr.tool.redis_tool import ProjectRedis


def _register_service(app):
    # 注册服务, 保证上下文中
    from flaskr.service.b_recognition_service import RecognitionService
    from flaskr.service.b_task_service import TaskService
    
    app.task_service = TaskService()  # 任务服务
    app.recognition_service = RecognitionService(app.task_service)  # 识别服务, 依赖任务服务

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
        # 'retry_on_timeout': True,  # 关闭自动重试, 本选项在网络异常时会导致线程无法释放
        'socket_keepalive': True,  # 启用 Keepalive 以保持长连接
    }
    app.config['REDIS_SOCKET_TIMEOUT'] = 10  # 增加 Redis 超时设置
    redis_client = ProjectRedis()
    redis_client.init_app(app)  # 在应用工厂中初始化 Redis 客户端
    
    # 提取端口
    args.port = nacos_config_dict.get('port')
    
    # 初始化 MySQL
    db = init_mysql(app, nacos_config_dict)
    
    # 初始化定时任务
    scheduler = APScheduler()
    scheduler.init_app(app)
    # scheduler.add_job(id='keep_mysql_connection_alive', func=scheduled_task, args=[app, db], trigger='interval', minutes=5) # mysql 连接
    scheduler.start()
    
    with app.app_context(): # 可以在没有实际请求的情况下使用 current_app、g 等与应用实例相关的变量与对象。
        # 注册事件监听器
        _register_service(app)  # 注册服务
    
    return app, args

