from flask import Blueprint, current_app, request

from flaskr.config import default_config
from flaskr.schema.recognition_schema import RecognitionParam, RedisRecognitionSchema
from flaskr.tool.json_tool import *

api = Blueprint(default_config.CONTEXT_PATH, __name__)  # 注册蓝图


# 创建新的识别记录
@api.route('/recognition', methods=['POST'])
def create_recognition():
    try:
        redis_recognition_schema:RedisRecognitionSchema = RecognitionParam.parse_obj(request.get_json())  # 使用 Pydantic 进行验证
        data_task = current_app.recognition_service.insert_recognition(redis_recognition_schema)  # 插入新记录
    except Exception as e:
        return return_error(e) # todo 全局异常捕获
    return return_success_dict(data_task)  # 返回新记录的 JSON 响应


# 通过 ID 获取识别记录
@api.route('/recognition/<string:id>', methods=['GET'])
def get_recognition(id):
    recognition = current_app.recognition_service.get_recognition_by_id(id)
    if not recognition:
        return return_error_message('Recognition not found')
    return return_success_with_model(recognition)

# 
# # 更新识别记录通过业务 ID
# @api.route('/recognition/<string:business_id>', methods=['PUT'])
# def update_recognition(business_id):
#     try:
#         data = RecognitionSchema.parse_obj(request.get_json())  # 使用 Pydantic 进行验证
#     except ValidationError as e:
#         return return_error(e.errors())
# 
#     recognition = current_app.recognition_service.update_recognition({'business_id': business_id, **data.dict()})
#     if not recognition:
#         return return_error({'message': 'Recognition not found'})
#     return return_success_with_data(recognition)
# 
# 
# # 删除识别记录通过业务 ID
# @api.route('/recognition/<string:business_id>', methods=['DELETE'])
# def delete_recognition(business_id):
#     recognition = current_app.recognition_service.delete_recognition(business_id)
#     if not recognition:
#         return return_error({'message': 'Recognition not found'})
#     return return_success_with_data({'message': 'Recognition deleted successfully'})
