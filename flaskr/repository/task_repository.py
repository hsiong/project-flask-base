from flaskr.entity.task_entity import Task
from flaskr.tool.mysql_tool import db



class TaskRepository:
    '''
    数据访问层 - 识别记录
    '''
    def save_task_repository(self, task):
        '''
        插入识别记录
        Args:
            task: 识别记录
        Returns:

        '''
        db.session.add(task)
        return task
    
    def update_task_repository(self, task):
        '''
        更新识别记录
        Args:
            task: 
            data: 识别记录

        Returns:

        '''
        # 使用 merge() 合并记录
        task = db.session.merge(task)
        return task
    
    def delete_task_repository(self, id):
        '''
        删除识别记录
        Args:
            id: 识别记录id

        Returns:

        '''
        task = db.session.query(Task).filter_by(id=id).first()
        if task:
            db.session.delete(task)
        return task
    
    def query_by_id_repository(self, id):
        '''
        根据业务ID查询识别记录
        Args:
            id: 

        Returns:

        '''
        return db.session.query(Task).filter_by(id=id).first()
