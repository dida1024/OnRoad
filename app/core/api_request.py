import httpx
from enum import Enum
from tenacity import retry, stop_after_attempt, wait_exponential


class MethodType(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class ApiRequest:
    """
    请求类，用于发送请求, 支持自动重试
    """
    def __init__(self, url: str, method: MethodType, headers: dict = None, data: dict = None, timeout: int = 10):
        """
        url: 请求url
        method: 请求方法 GET/POST/PUT/DELETE
        headers: 请求头
        data: 请求数据
        timeout: 请求超时时间 单位秒
        """

        self.url = url
        self.method = method.value
        self.headers = headers
        self.data = data
        self.timeout = timeout

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15))
    async def send(self):
        async with httpx.AsyncClient() as client:
            response = await client.request(self.method, self.url, headers=self.headers, data=self.data, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"请求失败，状态码：{response.status_code}")
