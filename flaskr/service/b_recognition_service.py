from flaskr.repository.recognition_repository import RecognitionRepository


class RecognitionService:
    '''
    service - 识别服务
    '''
    
    def __init__(self):
        self.repo = RecognitionRepository()
    
    def insert_recognition(self, recognition):
        self.repo.save_recognition_repository(recognition)
    
    def update_recognition(self, recognition):
        return self.repo.update_recognition_repository(recognition)
    
    def delete_recognition(self, business_id):
        return self.repo.delete_recognition_repository(business_id)
    
    def get_recognition_by_id(self, business_id):
        return self.repo.query_by_id_repository(business_id)
