import argparse
import os

from flask import Flask
from flask_apscheduler import APScheduler

from flaskr.config import default_config
from flaskr.service.schedule_service import *
from flaskr.tool.mysql_tool import init_mysql
from flaskr.tool.redis_tool import ProjectRedis


def load_env(filepath=".env"):
	if not os.path.exists(filepath):
		return
	with open(filepath) as f:
		for line in f:
			line = line.strip()
			if not line or line.startswith("#"):
				continue
			if '=' in line:
				key, value = line.split('=', 1)
				os.environ[key.strip()] = value.strip()


def _register_service(app):
	# 注册服务, 保证上下文中
	from flaskr.service.b_recognition_service import RecognitionService
	from flaskr.service.b_task_service import TaskService
	
	app.task_service = TaskService()  # 任务服务
	app.recognition_service = RecognitionService(app.task_service)  # 识别服务, 依赖任务服务


def create_app():
	# 加载 .env 配置文件
	load_env()
	
	# 解析命令行参数
	parser = argparse.ArgumentParser(description="Flask with .env Configuration")
	parser.add_argument('--env', type=str, default=os.getenv("FLASK_ENV", "dev"), help='Set the environment: dev, test, prod')
	args = parser.parse_args()
	env = args.env
	
	# 初始化 Flask 应用
	app = Flask(__name__)
	app.config.from_object("config.default_config.DefaultConfig")
	
	# 提取 Redis 配置并应用到 Flask
	redis_url = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/{os.getenv('REDIS_DB')}"
	app.config['REDIS_URL'] = redis_url
	app.config['REDIS_OPTIONS'] = {
		'socket_keepalive': True,
	}
	app.config['REDIS_SOCKET_TIMEOUT'] = 10
	redis_client = ProjectRedis()
	redis_client.init_app(app)
	
	# 提取端口
	args.port = int(os.getenv("FLASK_PORT", 5000))
	
	# 初始化 MySQL 配置
	mysql_config = {
		"MYSQL_USER": os.getenv("MYSQL_USER"),
		"MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD"),
		"MYSQL_HOST": os.getenv("MYSQL_HOST"),
		"MYSQL_PORT": int(os.getenv("MYSQL_PORT", 3306)),
		"MYSQL_DB": os.getenv("MYSQL_DB")
	}
	db = init_mysql(app, mysql_config)
	
	# 初始化定时任务
	scheduler = APScheduler()
	scheduler.init_app(app)
	scheduler.start()
	
	# 注册服务
	with app.app_context():
		_register_service(app)
	
	return app, args
