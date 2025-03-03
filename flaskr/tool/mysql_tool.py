import importlib
import inspect
import os

from flask_sqlalchemy import SQLAlchemy
from snowflake.snowflake import SnowflakeGenerator
from sqlalchemy import MetaData, Table, text

db = None
generator = SnowflakeGenerator(instance=1)  # 创建一个 Snowflake ID 生成器实例


def _load_models_from_directory(directory):
    '''
    加载模型
    Args:
        directory: 模型目录


    '''
    models = []
    os_listdir = os.listdir(directory)
    for filename in os_listdir:
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # 去掉文件的后缀 .py
            module_path = f'{directory}.{module_name}'
            # 使用 importlib 动态导入模块
            module = importlib.import_module(module_path)
            for name, obj in inspect.getmembers(module):
                # 排除不属于用户定义模块的类，例如 SQLAlchemy 内部的类
                if inspect.isclass(obj) and hasattr(obj, '__tablename__'):
                    models.append(obj)
    return models


def _add_column_to_table(table_name, column):
    '''
    添加字段到表
    Args:
        table_name: 表名
        column: 字段
    '''
    column_type = column.type.compile(dialect=db.engine.dialect)
    nullable = "NULL" if column.nullable else "NOT NULL"
    # 根据列类型处理默认值
    if column.default is not None:
        default_value = column.default.arg
        # 根据不同的类型进行不同的处理
        if isinstance(column.type, (db.String, db.Text, db.Enum)):
            default = f"DEFAULT '{default_value}'"
        elif isinstance(column.type, db.Boolean):
            default = f"DEFAULT {int(default_value)}"  # Boolean 转换为整数 0 或 1
        else:
            default = f"DEFAULT {default_value}"
    else:
        default = ""
    
    alter_stmt = f'ALTER TABLE {table_name} ADD COLUMN {column.name} {column_type} {nullable} {default};'
    
    with db.engine.connect() as conn:
        conn.execute(text(alter_stmt))
        print(f"Added column {column.name} to table {table_name}.")


def _create_table_for_model(model):
    '''
    创建表
    Args:
        model: SQLAlchemy 模型
    '''
    table_name = model.__tablename__
    existing_columns = list(model.__table__.columns)
    metadata = MetaData()
    
    # 创建新的列定义，而不是使用已经存在的列对象
    from sqlalchemy import Column
    new_columns = [
        Column(name=col.name, type_=col.type, nullable=col.nullable, primary_key=col.primary_key, unique=col.unique)
        for col in existing_columns]
    
    table = Table(table_name, metadata, *new_columns)
    
    with db.engine.connect() as conn:
        table.create(conn)
        print(f"Created table {table_name}.")


def _check_and_update_tables():
    # 反射现有数据库表结构
    metadata = MetaData()
    metadata.reflect(bind=db.engine)
    
    # 动态加载所有模型
    models = _load_models_from_directory('entity')
    
    for model in models:
        print(f"Checking table {model.__tablename__}.")
        table_name = model.__tablename__
        if table_name in metadata.tables:
            table = metadata.tables[table_name]
            for column in model.__table__.columns:
                if column.name not in table.columns:
                    # 如果模型中的字段在数据库表中不存在，则添加该字段
                    _add_column_to_table(table_name, column)
                    print(f'Added column {column.name} to table {table_name}.')
        else:
            print(f"Table {table_name} does not exist, creating it.")
            _create_table_for_model(model)


def _register_service(app):
    # 注册服务, 保证上下文中
    from flaskr.service.b_recognition_service import RecognitionService
    from flaskr.service.b_task_service import TaskService
    
    app.task_service = TaskService()  # 任务服务
    app.recognition_service = RecognitionService(app.task_service)  # 识别服务
    


def init_mysql(app, nacos_config_dict):
    '''
    初始化 MySQL
    Args:
        app: Flask 应用
        nacos_config_dict: Nacos 配置字典

    '''
    
    # 提取 MySQL 配置并初始化 SQLAlchemy
    mysql_config = nacos_config_dict.get('datasource', {})
    mysql_url = f"mysql+pymysql://{mysql_config['username']}:{mysql_config['password']}@{mysql_config['url'].split('//')[1]}"
    app.config['SQLALCHEMY_DATABASE_URI'] = mysql_url
    # 当 pool_pre_ping 设置为 True 时，SQLAlchemy 会在每次获取连接之前发出一个轻量的 "ping" 请求（通常是 SELECT 1）。如果连接已经失效，SQLAlchemy 会丢弃该连接并从池中获取或创建一个新的连接。这样可以避免因为数据库连接长时间空闲后失效导致的错误。
    # 自动回收旧连接，防止连接被服务器关闭
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True,  'pool_recycle': 300}
    try:
        global db
        db = SQLAlchemy(app)
        # db.init_app(app)  # 在应用工厂中初始化
    except Exception as e:
        raise Exception(f"Can not connect MySQL Server: {mysql_config['url'].split('//')[1]}" + str(e))
    
    with app.app_context(): # 可以在没有实际请求的情况下使用 current_app、g 等与应用实例相关的变量与对象。
        # 注册事件监听器
        _check_and_update_tables()  # 检查并更新表结构
        _register_service(app)  # 注册服务
    
    # 自动提交或回滚事务: @app.teardown_appcontext 是 Flask 提供的一个装饰器，
    # 用来注册在应用上下文结束时自动执行的函数。这个机制的核心原理是管理在每个请求的生命周期内需要处理的任务，如数据库事务的提交、回滚、以及清理工作。
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if exception:
            db.session.rollback()  # 接口报错, 回滚
        else:
            db.session.commit()  # 接口正常返回, 提交
        db.session.remove()  # 关闭会话
        
    return db
