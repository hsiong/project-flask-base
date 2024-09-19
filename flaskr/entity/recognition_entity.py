

from sqlalchemy import Column, String, JSON, BigInteger, Enum
from sqlalchemy.orm import declarative_base

from flaskr.config import default_config

from flaskr.config.prompt_enum import ModelType
from flaskr.tool import json_tool

_Base = declarative_base() # 创建一个 Alchemy 基类, 不是全局

class Recognition(_Base):
    '''
    实体-识别记录表
    '''
    __tablename__ = default_config.DATABASE_PREFIX + '_recognition'
    
    id = Column(String(64), primary_key=True)  # 不在此处插入id, 而是在json序列化生成id, 以满足全局事务的同时, 接口返回id
    create_time = Column(String(19), nullable=False, comment="创建时间，格式为YYYY-MM-DD HH:MM:SS")
    
    
    camera_id = Column(String(64), nullable=False, comment="摄像头ID")
    camera_size = Column(JSON, nullable=False, comment="摄像头尺寸，以JSON格式存储")
    monitor_areas = Column(JSON, nullable=False, comment="监控区域，以JSON格式存储")
    capture_time = Column(String(19), nullable=False, comment="捕获时间，格式为YYYY-MM-DD HH:MM:SS")
    image_url = Column(String(255), nullable=False, comment="图片URL")
    model = Column(Enum(ModelType), nullable=False, comment="模型")
    
    # 单张图片识别结果
    task_status = Column(String(32), nullable=False, comment="任务状态（pending, in_progress, completed, failed）")
    recognition_url = Column(String(255), nullable=False, default='', comment="识别图片url")
    recognition_result = Column(JSON, nullable=False, default={}, comment="识别结果，以JSON格式存储")
    recognition_time = Column(BigInteger, nullable=False, default=0, comment="识别耗时 ms")
    completion_time = Column(String(19), nullable=False, default='', comment="完成时间，格式为YYYY-MM-DD HH:MM:SS")
    error_msg = Column(String(1024), nullable=False, default='', comment="错误信息")
    
    
    def __repr__(self):
        '''
        自定义打印
        Returns:

        '''
        json_str = json_tool.model_to_json_str(self)
        return json_str 

