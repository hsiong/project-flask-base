from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import List, Any

from pydantic import BaseModel

from flaskr.config import redis_constant


class CallbackRequestCow(BaseModel):
    class CameraResult(BaseModel):
        camera_id: str
        image_url: str
        recognition_url: str  # 识别图片url
        recognition_result: List[Any]  # 识别结果
        recognition_time: str  # 识别耗时 ms
        completion_time: str  # 完成时间，格式为YYYY-MM-DD HH:MM:SS
        error_msg: str  # 错误信息
    
    business_id: str  # 业务ID
    task_id: str  # 任务id
    task_num: int  # 识别总数
    cameras: List[CameraResult]


executor = ThreadPoolExecutor(max_workers=1)


def scheduled_task(app):
    '''
    定时任务 - 使用线程池并增加超时设置
    '''
    future = executor.submit(_recognize_queue_task, app)
    
    try:
        result = future.result(timeout=60)  # 设置任务超时时间为 30 秒
    except TimeoutError:
        print("Task took too long, terminating...")


# 定时任务函数
def _recognize_queue_task(app):
    '''
    定时任务
    :param app: # 手动推送应用上下文
    :return:

    '''
    with app.app_context():  # 手动推送应用上下文
        redis_client = app.extensions['redis']
        try:
            identifier = redis_client.acquire_lock(redis_constant.QUEUE_LOCK)  # 获取分布式锁, 这里也会产生连接异常
            if identifier:
                None # 业务代码
            else:
                print("Failed to acquire lock. Task not executed.")
        except Exception as e:
            raise e
        finally:
            redis_client.release_lock(redis_constant.QUEUE_COW_LOCK, identifier)
        
