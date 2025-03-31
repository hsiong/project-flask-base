import hashlib
import hmac
import base64
import time

from enum import Enum

# 定义一个枚举类 HttpMethod
class HttpMethod(Enum):
    GET = "GET"
    DELETE = "DELETE"
    POST = "POST"
    PUT = "PUT"

class AuthConfig:
   url: str
   secret: str
   key: str
   oss_path: str
   
   def __init__(self, url=None, secret=None, key=None, oss_path=None):
       self.url = url
       self.secret = secret
       self.key = key
       self.oss_path = oss_path
   
auth_config = AuthConfig()
 
def sign(path, method: HttpMethod):
    '''
    Escher 鉴权
    Args:
        path: 路径
        method: 方法

    '''
    current_time = str(int(time.time() * 1000))  # 获取当前时间戳（毫秒）
    sign_str = f"{path}&{method.value}&{current_time}"
    sha256_hmac = _sha256_HMAC(sign_str, auth_config.secret)
    
    header = {
        "KEY":  auth_config.key,
        "TIME": current_time,
        "SIGN": sha256_hmac
    }
    
    return header


def _sha256_HMAC(message, secret):
    try:
        secret_key = secret.encode('utf-8')
        message_bytes = message.encode('utf-8')
        hmac_sha256 = hmac.new(secret_key, message_bytes, digestmod=hashlib.sha256)
        hash_bytes = hmac_sha256.digest()
        hash_str = base64.b64encode(hash_bytes).decode('utf-8')
        return hash_str
    except Exception as e:
        print(f"Error HmacSHA256 =========== {e}")
        return ""