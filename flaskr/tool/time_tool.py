from datetime import datetime


def datetime_to_str(timestamp):
    # 将时间戳转换为 'yyyy-MM-dd HH:MM:SS' 格式的字符串
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_completion_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_completion_time


def str_to_datetime(date_str):
    # 将'yyyy-MM-dd HH'格式转换为时间戳
    time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return time
    
def get_time_str():
    time = datetime.now()
    return time.strftime('%Y-%m-%d %H:%M:%S')