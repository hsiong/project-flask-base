import json
from datetime import time
from typing import List, Any, Optional

from pydantic import BaseModel

from flaskr.entity.recognition_entity import Recognition
from flaskr.entity.task_entity import Task
from flaskr.config import task_status_enum

from flaskr.tool import json_tool, time_tool
from flaskr.tool.mysql_tool import generator


class RedisRecognitionSchema(BaseModel):
    task: Optional[dict] = {}  # 任务 json，提供默认值为空字符串
    recognition_list: Optional[List] = []  # 待识别记录 json，提供默认值为空字符串
    
    def set_self(self, task: Task, recognition_list: List[Recognition]):
        self.task = json_tool.model_to_json_dict(task)
        self.recognition_list = json_tool.model_to_json_dict(recognition_list)
    
    def get_self(self):
        task = json_tool.json_to_model(self.task, Task)
        recognition_list = json_tool.json_to_model(self.recognition_list, Recognition)
        return task, recognition_list


class RecognitionParam(BaseModel):
    class CameraInfo(BaseModel):
        camera_id: str
        camera_size: List[int]  # 格式 [height, width]
        monitor_areas: str  # 三重数组定义监控区域 [[[x1, y1], [x2, y2], ...]]
        capture_time: str  # 格式 'yyyy-MM-dd HH:mm:ss'
        image_url: str  # 待识别图片地址
    
    business_id: str  # 业务ID, 必填
    system_code: str  # 业务系统编号枚举, 必填
    callback_url: str  # 异步响应回调地址, 必填
    prompt: str  # 检测内容枚举, 必填
    cameras: List[CameraInfo]  # 摄像头数据数组, 必填
    
    @classmethod
    def parse_obj(self, obj) -> RedisRecognitionSchema:
        '''
        自定义解析: 所有默认值在此处插入
        Args:
            obj: 

        Returns:

        '''
        super_obj = super().parse_obj(obj)
        
        prompt = super_obj.prompt
        
        
        parse_result = []
        task_id = next(generator)
        for camera in super_obj.cameras:
            
            capture_time = time_tool.str_to_datetime(camera.capture_time)
            capture_time_only = capture_time.time()  # 提取 capture_time 的时间部分
            
            # 定义每天的起始时间和结束时间
            start_time = time(8, 0)  # 8:00 AM
            end_time = time(18, 0)  # 6:00 PM
            
            # 推理
            if start_time <= capture_time_only <= end_time:
                model = ModelType.DAMOYOLO # 白天
            else:
                model = ModelType.GROUNDINGDINO # 晚上
            
            prompt = model.get_prompt(prompt)
            recognition = Recognition(id=next(generator),
                                      create_time=time_tool.get_datetime_str(),
                                      model = model,
                                      camera_id=camera.camera_id,
                                      camera_size=json.dumps(camera.camera_size),
                                      monitor_areas=json.dumps(camera.monitor_areas),
                                      capture_time=camera.capture_time,
                                      image_url=camera.image_url,
                                      task_status=task_status_enum.TaskStatusEnum.PENDING.value,
                                      recognition_url='',
                                      recognition_result={},
                                      recognition_time=0,
                                      completion_time='',
                                      error_msg='')
            parse_result.append(recognition)
        
        task = Task(id=task_id,
                    create_time=time_tool.get_datetime_str(),
                    business_id=super_obj.business_id,
                    system_code=super_obj.system_code,
                    callback_url=super_obj.callback_url,
                    prompt = prompt,
                    task_status=task_status_enum.TaskStatusEnum.PENDING.value,
                    task_num=0)
        redis_recognition_schema = RedisRecognitionSchema()
        redis_recognition_schema.set_self(task, parse_result)
        return redis_recognition_schema
