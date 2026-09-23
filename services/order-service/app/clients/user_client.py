import httpx
form app.core.config import config


class UserClient:

    async def get_user(self,user_id:str,)->dict | None:
        url=(
            f"{config.USER_SERVICE_URL}"
            f"/api/v1/users/{user_id}"
        )



        async with httpx.AsyncClient(timeout=5.0) as client:
            response=await client.get(url)  

        if response.status_code==400:
            return None

        response.raise_for_status()
        return response.json()


user_client=UserClient()
