
from enum import Enum

class TaskStatusEnum(Enum):
    '''
    任务状态枚举 - .value 是字符串, 否则是枚举
    '''
    PENDING = "pending" # initial state
    IN_PROGRESS = "in_progress" # 处理中
    COMPLETED = "completed" # 已完成
    FAILED = "failed" # 失败