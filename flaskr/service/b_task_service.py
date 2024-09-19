from flaskr.entity.task_entity import Task
from flaskr.repository.task_repository import TaskRepository


class TaskService:
    '''
    service - 识别服务
    '''
    def __init__(self):
        self.repo = TaskRepository()

    def insert_task(self, task:Task):
        # 插入任务记录
        self.repo.save_task_repository(task)

    def update_task(self, task:Task):
        return self.repo.update_task_repository(task)

    def delete_task(self, business_id):
        return self.repo.delete_task_repository(business_id)

    def get_task_by_id(self, business_id):
        return self.repo.query_by_id_repository(business_id)