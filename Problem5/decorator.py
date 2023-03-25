from functools import wraps
import httpx
from fastapi import HTTPException, Request, status
from schemas import UserInterface

async def get_country_code(client_ip: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            if(client_ip == "127.0.0.1"):
                client_ip = "39.109.234.23"
            response = await client.get(f"http://ip-api.com/json/{client_ip}")
            data = response.json()
            print(data)
            return data["countryCode"]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to fetch country code")


def check_country_code(fn):
    @wraps(fn)
    async def wrapper(request: Request, user: UserInterface, *args, **kwargs):
        country_code = await get_country_code(request.client.host)
        if not user.username.lower().startswith(country_code.lower()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad Request. User loggedin from another country",
            )
        return fn(request, user=user, *args, **kwargs)

    return wrapper
