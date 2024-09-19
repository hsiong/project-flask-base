import threading
import time

import requests
from pydantic import BaseModel


class ResponseModel(BaseModel):
    code: int
    data: dict
    message: str
    success: bool


def _send_post_request(url: str, data, headers: dict, retries: int = 2):
    '''
    发送 POST 请求
    Args:
        url (str): 请求 URL
        data : 请求数据
        headers (dict): 请求头

    Returns:

    '''
    attempt = 0
    while attempt <= retries:
        try:
            response = requests.post(url, json=data.dict(), headers=headers)
            response_data = ResponseModel(**response.json())  # 使用 pydantic 解析响应数据
            
            # 检查返回的code字段
            if response_data.code == 200:
                print(f"Request successful: {response_data}")
                return response_data
            else:
                print(f"Request failed with code {response_data.code}, retrying... ({attempt + 1}/{retries})")
                attempt += 1
                time.sleep(2)  # 等待2秒再重试
        except Exception as e:
            print(f"Error occurred: {e}")
            attempt += 1
            time.sleep(2)
    
    print("Max retries reached, exiting.")
    return None

def async_post_request(url: str, data):
    # 使用线程进行异步请求，不影响主线程
    thread = threading.Thread(target=_send_post_request, args=(url, data, {}))
    thread.start()