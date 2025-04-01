import time
import uuid

import redis
from flask_redis import FlaskRedis

from flaskr.config import default_config


def get_key(key):
    '''
    获取缓存key

    Args:
        key: 缓存key

    Returns:

    '''
    return f'{default_config.DATABASE_PREFIX}_{key}'


def get_key_object(key):
    '''
    获取缓存key

    Args:
        key: 缓存key

    Returns:

    '''
    return f'{key}_objects'


class ProjectRedis(FlaskRedis):
    '''
    Redis 工具类
    '''
    
    def cache_set(self, key: str, value: str):
        '''
        缓存数据

        Args:
            key: 缓存key
            value: 缓存数据

        Returns:

        '''
        key = get_key(key)
        self.set(get_key(key), value)
    
    def cache_get(self, key):
        '''
        获取缓存

        Args:
            key: 缓存key

        Returns:

        '''
        key = get_key(key)
        value = self.get(key)
        if value:
            value_decode = value.decode('utf-8')
            print(f"Redis Key {key} has value: {value_decode}.")
            return value_decode
        else:
            raise Exception(f"Key {key} does not exist.")
    
    def put_queue(self, key: str, task_id: str, task_object_json: object):
        '''
        将一个或多个值插入到队列中。 将 task_id 存储在 ZSET 中，而将实际的 task_object_json 存储在一个与 task_id 相关联的 HASH 中。
        用于实现查找 key 下 指定 id 的 排队数

        Args:
            key: 缓存key
            task_id: 任务id
            task_object_json: 任务对象

        Returns:

        '''
        score = time.time()
        key = get_key(key)
        object_key = get_key_object(key)
        
        # 添加任务到有序集合
        self.zadd(key, {task_id: score})
        self.hset(object_key, task_id, task_object_json)
    
    def get_queue_position(self, key: str, task_id: str):
        '''
        用于实现查找 key 下 指定 id 的 排队数

        Args:
            key: 缓存key
            task_id: 任务id
        Returns:

        '''
        key = get_key(key)
        position = self.zrank(key, task_id)
        if position is None:
            raise Exception(f"Key {key} does not exist.")
        return position + 1
    
    def remove_zset(self, key: str, task_id: str):
        '''
        从有序集合中删除一个元素
        Args:
            key:
            task_id:

        Returns:

        '''
        key = get_key(key)
        self.zrem(key, task_id)
    
    def remove_queue_object(self, key: str, task_id: str):
        '''
        从队列删除一个元素

        Args:
            task_id:
            key: 缓存key
        Returns:

        '''
        key = get_key(key)
        object_key = get_key_object(key)
        self.zrem(key, task_id)
        self.hdel(object_key, task_id)
    
    def get_queue(self, key: str):
        '''
        从队列中获取最新的元素,
        Raises UserWarning if the key is empty.
        Args:
            key: 缓存key
        Returns:

        '''
        key = get_key(key)
        object_key = get_key_object(key)
        # 从有序集合中获取第一个元素
        task_id = self.zrange(key, 0, 0)  # 获取分数最低的第一个元素
        if not task_id:
            raise UserWarning(f"Key {key} is empty.")
        task_id = task_id[0]
        task_object_json = self.hget(object_key, task_id)
        return task_object_json, task_id
    
    def pop_queue(self, key: str):
        '''
        从队列中弹出一个元素,
        Raises UserWarning if the key is empty.
        Args:
            key: 缓存key
        Returns:

        '''
        task_object_json, task_id = self.get_queue(key)
        self.remove_queue_object(key, task_id)
        return task_object_json
    
    def acquire_lock(self, lock_name, acquire_timeout=10, lock_timeout=10):
        '''
        获取锁（分布式锁）
        Args:
            acquire_timeout:
            lock_timeout:

        Returns:

        '''
        identifier = str(uuid.uuid4())  # 唯一标识符
        end = time.time() + acquire_timeout
        while time.time() < end:
            if self.set(lock_name, identifier, nx=True, px=lock_timeout * 1000):
                return identifier
            time.sleep(0.001)
        return False
    
    def release_lock(self, lock_name, identifier):
        '''
        释放锁（分布式锁）
        Args:
            identifier:

        Returns:

        '''
        pipe = self.pipeline(True)
        while True:
            try:
                pipe.watch(lock_name)
                lock_value = self.get(lock_name)
                if lock_value and lock_value.decode('utf-8') == identifier:
                    pipe.multi()
                    pipe.delete(lock_name)
                    pipe.execute()
                    return True
                pipe.unwatch()
                break
            except redis.exceptions.WatchError:
                pass
        return False
