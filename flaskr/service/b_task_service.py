from flask import current_app

from flaskr.constant import redis_constant
from flaskr.entity.task_entity import Task
from flaskr.repository.task_repository import TaskRepository
from flaskr.schema.recognition_schema import RedisRecognitionSchema
from flaskr.service.b_recognition_service import RecognitionService


class TaskService:
    '''
    service - 识别服务
    '''
    def __init__(self, recognition_service: RecognitionService):
        self.repo = TaskRepository()
        self.recognition_service = recognition_service  # 相关调用, 避免循环依赖

    def insert_task(self, data: RedisRecognitionSchema):
        data_task = data.task
        task, recognition_list = data.get_self()
        
        # 插入任务记录
        self.repo.save_task_repository(task)
        # 将识别内容放入队列
        ret_json = data.json()
        redis_client = current_app.extensions['redis']
        redis_client.put_queue(redis_constant.QUEUE_BUSSINESS, task.id, ret_json)
        
        # 插入识别记录
        for recognition in recognition_list:
            self.repo.save_recognition_repository(recognition)
        

    def update_task(self, task:Task):
        return self.repo.update_task_repository(task)

    def delete_task(self, business_id):
        return self.repo.delete_task_repository(business_id)

    def get_task_by_id(self, business_id):
        return self.repo.query_by_id_repository(business_id)