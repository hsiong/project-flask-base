import threading
import time
from dataclasses import dataclass
from io import BytesIO
from typing import Optional

import numpy as np
import requests
from pydantic import BaseModel

from flaskr.config import default_config


@dataclass
class FileInfo:
    name: str
    url: str
    size: int
    path: str
    id: str


class ResponseModel(BaseModel):
    code: int
    data: Optional[dict] = None
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


async def async_post_request(url: str, data):
    # 使用协程进行异步请求，不影响主线程
    thread = threading.Thread(target=_send_post_request, args=(url, data, {}))
    thread.start()

def upload_image(image: np.ndarray, url: str, headers: dict):
    """
    上传图像到指定的接口

    Parameters:
    image (np.ndarray): 需要上传的图像。
    url (str): 接口的 URL。
    dir_name (str): 上传图像的目标目录。
    headers (dict): 可选的 HTTP headers。

    Returns:
    Response: 服务器的响应。
    """
    # 将图像编码为字节流
    import cv2
    _, buffer = cv2.imencode('.jpg', image)
    file_bytes = BytesIO(buffer)
    
    # 设置上传的文件和参数
    files = {'file': ('image.jpg', file_bytes, 'image/jpeg')}
    
    # 发送 POST 请求上传文件
    headers['projectName'] = default_config.DATABASE_PREFIX
    response = requests.post(url, files=files, headers=headers)
    
    # 查看返回的文本内容
    print("Response Text:", response.text)
    
    # 尝试解析并查看 JSON 内容
    try:
        json_response = response.json()
        data = Ret.parse_result(json_response, FileInfo)
        return data.url
    except ValueError as e:
        raise e
    
  


from pydantic import BaseModel
from typing import Optional, Type, TypeVar, Generic

T = TypeVar('T')


class FileInfo(BaseModel):
    name: str
    url: str
    size: int
    path: str
    id: str

def ret_success_data(data):
    return Ret(code=200, message='', data=data, success=True)


def ret_error(message):
    return Ret(code=500, message='', data=message, success=False)


class Ret(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None
    success: bool = False
    
    @classmethod
    def parse_result(cls: Type['Ret[T]'], result: str, data_type: Type[T]) -> T:
        # 如果 result 是字典，直接解析
        if isinstance(result, dict):
            r = cls.parse_obj(result)
        # 如果 result 是 JSON 字符串，先解析成字典
        else:
            r = cls.parse_raw(result)
        
        if not r.success:
            raise ValueError(r.message)
        # 用 data_type 来解析 data 字段
        return data_type.parse_obj(r.data)
