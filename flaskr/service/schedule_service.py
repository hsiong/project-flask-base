from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import List, Any

from pydantic import BaseModel

from flaskr.constant import redis_constant

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
                data = redis_client.pop_queue(redis_constant.QUEUE_BUSSINESS)  # 获取识别队列
                None # 业务代码
            else:
                print("Failed to acquire lock. Task not executed.")
        except Exception as e:
            raise e
        finally:
            redis_client.release_lock(redis_constant.QUEUE_LOCK, identifier)
        
