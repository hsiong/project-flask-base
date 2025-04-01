import argparse
import os

from flask import Flask
from flask_apscheduler import APScheduler

from flaskr.tool import env_tool
from flaskr.tool.mysql_tool import init_mysql
from flaskr.tool.redis_tool import ProjectRedis



def _register_service(app):
    # 注册服务, 保证上下文中
    from flaskr.service.b_recognition_service import RecognitionService
    from flaskr.service.b_task_service import TaskService
    
    app.recognition_service = RecognitionService()  # 识别服务
    app.task_service = TaskService(app.recognition_service)  # 任务服务, 依赖识别服务


def create_app():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Flask with .env.dev Configuration")
    parser.add_argument('--env', type=str, default='dev', help='Set the environment: dev, test, prod')

    args = parser.parse_args()
    env = args.env
    # 加载 .env.dev 配置文件
    os_env_dict = env_tool.load_env(filepath=f".env.{env}")
    
    # 初始化 Flask 应用
    app = Flask(__name__)
    app.config.from_object("config.default_config.DefaultConfig")
    
    # 提取 Redis 配置并应用到 Flask
    redis_url = f"redis://:{os_env_dict.get('REDIS_PASSWORD')}@{os_env_dict.get('REDIS_HOST')}:{os_env_dict.get('REDIS_PORT')}/{os_env_dict.get('REDIS_DB')}"
    app.config['REDIS_URL'] = redis_url
    app.config['REDIS_OPTIONS'] = {
        'socket_keepalive': True,
    }
    app.config['REDIS_SOCKET_TIMEOUT'] = 10
    redis_client = ProjectRedis()
    redis_client.init_app(app)
    
    # 提取端口
    args.port = int(os_env_dict.get("FLASK_PORT", 5000))
    
    # 初始化 MySQL 配置
    mysql_config = {
        "username": os_env_dict.get("MYSQL_USER"),
        "password": os_env_dict.get("MYSQL_PASSWORD"),
        "url": f"{os_env_dict.get("MYSQL_HOST")}:{int(os_env_dict.get("MYSQL_PORT", 3306))}/{os_env_dict.get("MYSQL_DB")}",
        "sql_flag": os_env_dict.get("SQL_LOG", False)
    }
    db = init_mysql(app, mysql_config)
    app.db = db
    
    # 初始化定时任务
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    
    # 注册服务
    with app.app_context():
        _register_service(app)
    
    return app, args
