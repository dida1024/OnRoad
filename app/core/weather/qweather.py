import asyncio
import time
import jwt
from cryptography.hazmat.primitives import serialization
import base64

from app.core.api_request import ApiRequest, MethodType
from app.core.config import settings

class Qweather:
    def __init__(self):
        self.url = settings.QWEATHER_URL
        self.project_id = settings.QWEATHER_PROJECT_ID
        self.key_id = settings.QWEATHER_KEY_ID
        self.key = settings.QWEATHER_KEY
    
    async def __aenter__(self):
        self.jwt_token = await self.get_token()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    async def get_token(self):
        private_key_bytes = base64.b64decode(self.key)
        private_key = serialization.load_der_private_key(private_key_bytes, password=None) # 加载私钥

        payload = {
            "sub": self.project_id,
            "iat": int(time.time()) - 30,
            "exp": int(time.time()) + 900
        }

        header = {
            "alg": "EdDSA",
            "kid": self.key_id
        }

        # 使用 PyJWT 生成 JWT
        jwt_token = jwt.encode(
            payload,
            private_key,
            algorithm="EdDSA",
            headers=header
        )
        return jwt_token


    # get请求天气
    async def get_weather(self, location):
        url = f"{self.url}/v7/weather/now?location={location}"
        headers = {
            "Authorization": f"Bearer {self.jwt_token}"
        }
        response = await ApiRequest(url, MethodType.GET, headers=headers).send()
        return response

    # get local
    async def get_location(self, location):
        url = f"{self.url}/geo/v2/city/lookup?location={location}"
        headers = {
            "Authorization": f"Bearer {self.jwt_token}"
        }
        response = await ApiRequest(url, MethodType.GET, headers=headers).send()
        return response
        
if __name__ == "__main__":
    async def main():
        async with Qweather() as qweather:
            location = await qweather.get_location("shenzhen")
            print(location.get("location")[0].get("id"))
            weather = await qweather.get_weather(location.get("location")[0].get("id"))
            print(weather)

    asyncio.run(main())