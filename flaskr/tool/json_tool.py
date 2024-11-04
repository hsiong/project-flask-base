import json
from enum import Enum
from typing import List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import Enum as SQLAlchemyEnum

from flaskr.tool.request_tool import ret_error, ret_success_data

T = TypeVar('T', bound=BaseModel)  # 定义泛型 T，要求继承自 BaseModel


def dict_to_json(data):
    """
    将 Python 字典转换为 JSON 字符串的通用函数。

    :param data: Python 字典
    :return: JSON 字符串
    """
    # 如果数据是列表，转换为 Pydantic 模型实例的列表
    if isinstance(data, list):
        return [sensor.dict() for sensor in data]
    
    return data.json()

def json_to_dict(data:str, model_class: Type[T]) -> Union[T, List[T]]:
    """
    将 JSON 字符串转换为 Pydantic 模型实例的通用函数，支持单个对象和对象列表。

    :param json_str: JSON 字符串
    :param model_class: Pydantic 模型类
    :return: Pydantic 模型实例或实例列表
    """
    # 如果数据是字符串，先将其转换为字典
    # 将 bytes 转换为字符串
    if isinstance(data, bytes):
        data = data.decode('utf-8')  # 或者 data.decode()，默认使用 'utf-8'
        
    if isinstance(data, str):
        data = json.loads(data) # 解析 JSON 字符串为 Python 字典或列表

    
    # 如果数据是列表，转换为 Pydantic 模型实例的列表
    if isinstance(data, list):
        return [model_class.parse_obj(item) for item in data]
    
    # 如果数据是单个对象，转换为 Pydantic 模型实例
    return model_class.parse_obj(data)


def dict_to_json_str(data: Union[BaseModel, List[BaseModel]]):
    '''
    将字典或包含 Pydantic 模型的列表转换为 JSON 字符串
    Args:
        data: 单个 Pydantic 模型实例或 Pydantic 模型实例的列表
    Returns:
        JSON 字符串
    '''
    if isinstance(data, list):
        # 对列表中的每个 BaseModel 对象调用 .json()
        return json.dumps([item.json() for item in data])
    else:
        # 直接将单个 BaseModel 对象转换为 JSON
        return data.json()


def _process_data(data, enum_columns):
    """
    处理数据，将枚举字段的字符串值转换为对应的枚举类型。
    """
    processed_data = {}
    for key, value in data.items():
        if key in enum_columns:  # 如果字段是枚举类型
            enum_class = enum_columns[key]
            processed_data[key] = enum_class[value]  # 使用 value 作为枚举的 name
        else:
            processed_data[key] = value
    return processed_data


def json_to_model(data, model_class):
    """
    将 JSON 字符串转换为 SQLAlchemy 模型实例的通用函数，支持枚举类型。
    Args:
        data: JSON 字符串或字典
        model_class: SQLAlchemy 模型类
    Returns:
        SQLAlchemy 模型实例
    """
    
    # 如果数据是字符串，先将其转换为字典
    if isinstance(data, str):
        data = json.loads(data)
    
    # 获取模型的所有枚举字段
    enum_columns = {column.name: column.type.enum_class for column in model_class.__table__.columns if
                    isinstance(column.type, SQLAlchemyEnum)}
    
    # 如果数据是列表，则返回模型实例列表
    if isinstance(data, list):
        return [model_class(**_process_data(item, enum_columns)) for item in data]
    
    # 如果数据是单个对象，则返回模型实例
    model_instance = model_class(**_process_data(data, enum_columns))
    
    return model_instance


def model_to_json_str(data):
    '''
    使用 SQLAlchemy 的内置方法转换为 JSON 字符串，支持单个模型和列表
    Args:
        data: SQLAlchemy 模型实例或 SQLAlchemy 模型实例的列表
    Returns:
        JSON 字符串
    '''
    return json.dumps(model_to_json_dict(data))


def model_to_json_dict(data):
    '''
    使用 SQLAlchemy 的内置方法转换为 JSON 字符串，支持单个模型和列表
    Args:
        data: SQLAlchemy 模型实例或 SQLAlchemy 模型实例的列表
    Returns:
        JSON 字符串
    '''
    
    def process_value(value):
        if isinstance(value,
                      Enum):  # SQLAlchemyEnum 是用于将枚举类（如 Python 的 enum.Enum）映射到数据库的字段类型。在实际的使用过程中，字段的值是枚举类的实例，而不是 
            # SQLAlchemyEnum 本身。
            return value.name
        return value
    
    # 如果传入的是列表，则对列表中的每个元素进行处理
    if isinstance(data, list):
        data_list = [{column.name: process_value(getattr(item, column.name)) for column in item.__table__.columns} for
                     item in data]
        return data_list
    
    # 如果传入的是单个 SQLAlchemy 模型实例
    data_dict = {column.name: process_value(getattr(data, column.name)) for column in data.__table__.columns}
    return data_dict


def _ret_json_success(data: Optional[dict] = None):
    return ret_success_data(data).json(), 200


def _ret_json_error(message):
    return ret_error(message).json(), 200


def return_success():
    '''
    返回成功
    Returns:

    '''
    return _ret_json_success()


def return_success_with_model(data):
    '''
    使用 SQLAlchemy 的内置方法返回成功
    Args:
        data: 

    Returns:

    '''
    return _ret_json_success(model_to_json_dict(data))


def return_success_data(data):
    '''
    返回成功
    Args:
        data: 数据

    Returns:

    '''
    return _ret_json_success(data)


def return_success_message(message):
    '''
    返回成功
    Args:
        message: 数据

    Returns:

    '''
    return message, 200


def return_error(exception):
    '''
    返回错误
    Returns:

    '''
    import traceback
    traceback.print_exc()  # 打印堆栈信息
    return json.dumps(str(exception)), 500


def return_error_message(message):
    '''
    使用 SQLAlchemy 的内置方法返回错误
    Args:
        message: 

    Returns:

    '''
    print(f'request error: {message}')
    return json.dumps(message), 500
