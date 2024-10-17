from dataclasses import dataclass
from io import BytesIO

import cv2
import numpy as np
import requests

from flaskr.config import default_config


@dataclass
class FileInfo:
    name: str
    url: str
    size: int
    path: str
    id: str


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
