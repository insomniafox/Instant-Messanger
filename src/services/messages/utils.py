from fastapi import WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_sqlalchemy_session
from src.services.auth.exceptions import NotAuthorizedException
from src.services.auth.auth import get_user_from_token
from src.models.users.models import User


async def get_ws_current_user(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_sqlalchemy_session)
) -> User:
    token = websocket.query_params.get('token')
    # headers = websocket.scope.get("headers")
    #
    # for header in headers:
    #     header_name = header[0].decode("utf-8")
    #     header_value = header[1].decode("utf-8")
    #     if header_name == "authorization":
    #         token = header_value.split(" ")[1]

    if not token:
        await websocket.close(code=1008)  # Закрываем WebSocket при отсутствии токена
        raise NotAuthorizedException("Token missing")

    user = await get_user_from_token(token, db=db)
    return user
