from enum import Enum

# 定义一个枚举类 HttpMethod
class HttpMethod(Enum):
	GET = "GET"
	DELETE = "DELETE"
	POST = "POST"
	PUT = "PUT"