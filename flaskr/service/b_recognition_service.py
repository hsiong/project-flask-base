from flask import current_app

from flaskr.config import redis_constant
from flaskr.repository.recognition_repository import RecognitionRepository
from flaskr.schema.recognition_schema import RedisRecognitionSchema
from flaskr.service.b_task_service import TaskService


class RecognitionService:
    '''
    service - 识别服务
    '''
    
    def __init__(self, task_service: TaskService):
        self.repo = RecognitionRepository()
        self.task_service = task_service  # 相关调用, 避免循环依赖
    
    def insert_recognition(self, data: RedisRecognitionSchema):
        data_task = data.task
        task, recognition_list = data.get_self()
        # 插入任务记录
        self.task_service.insert_task(task)
        
        # 插入识别记录
        for recognition in recognition_list:
            self.repo.save_recognition_repository(recognition)
            
        # 将识别内容放入队列
        ret_json = data.json()
        redis_client = current_app.extensions['redis']
        redis_client.put_queue(redis_constant.QUEUE_COW, task.id, ret_json)
        
        return data_task
    
    def update_recognition(self, recognition):
        return self.repo.update_recognition_repository(recognition)
    
    def delete_recognition(self, business_id):
        return self.repo.delete_recognition_repository(business_id)
    
    def get_recognition_by_id(self, business_id):
        return self.repo.query_by_id_repository(business_id)
