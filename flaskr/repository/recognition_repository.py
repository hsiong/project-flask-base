from flaskr.entity.recognition_entity import Recognition
from flaskr.tool.mysql_tool import db



class RecognitionRepository:
    '''
    数据访问层 - 识别记录
    '''
    def save_recognition_repository(self, recognition):
        '''
        插入识别记录
        Args:
            recognition: 识别记录
        Returns:

        '''
        db.session.add(recognition)
        return recognition
    
    def update_recognition_repository(self, recognition):
        '''
        更新识别记录
        Args:
            recognition: 

        Returns:

        '''
        # 使用 merge() 合并记录
        recognition = db.session.merge(recognition)
        return recognition
    
    def delete_recognition_repository(self, id):
        '''
        删除识别记录
        Args:
            id: 识别记录id

        Returns:

        '''
        recognition = db.session.query(Recognition).filter_by(id=id).first()
        if recognition:
            db.session.delete(recognition)
        return recognition
    
    def query_by_id_repository(self, id):
        '''
        根据业务ID查询识别记录
        Args:
            id: 

        Returns:

        '''
        return db.session.query(Recognition).filter_by(id=id).first()
