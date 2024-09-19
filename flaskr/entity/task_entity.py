from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

from flaskr.config import default_config
from flaskr.tool import json_tool

_Base = declarative_base()  # 创建一个 Alchemy 基类, 不是全局


class Task(_Base):
    '''
    实体-识别记录表
    '''
    __tablename__ = default_config.DATABASE_PREFIX + '_task'
    
    id = Column(String(64), primary_key=True)  # 不在此处插入id, 而是在json序列化生成id, 以满足全局事务的同时, 接口返回id
    create_time = Column(String(19), nullable=False, comment="创建时间，格式为YYYY-MM-DD HH:MM:SS")
    
    business_id = Column(String(32), unique=False, nullable=False, comment="业务ID")
    system_code = Column(String(20), nullable=False, comment="系统编码")
    callback_url = Column(String(255), nullable=False, comment="回调地址")
    prompt = Column(String(255), nullable=False, comment="任务提示信息")
    
    # 任务结果
    task_status = Column(String(32), nullable=False, comment="任务状态（pending, in_progress, completed, failed）")
    task_num = Column(Integer, nullable=False, comment="识别总数")
    
    # task_id = None # 不会存储在数据库中
    
    def __repr__(self):
        '''
        自定义打印
        Returns:

        '''
        json_str = json_tool.model_to_json_str(self)
        return json_str
