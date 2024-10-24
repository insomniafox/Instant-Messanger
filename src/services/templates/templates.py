from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from src.core.config import settings
from src.core.templates import templates


class TemplateService:
    # _BASE_URL = settings.MESSANGER_API_BASE_URL
    _BASE_URL = 'http://localhost:8009'
    _USERS_URL = '/api/users'
    _LOGIN_URL = f'{_USERS_URL}/login'
    _REGISTER_URL = f'{_USERS_URL}/register'
    _CHAT_URL = '/ws/chat'

    @classmethod
    async def get_chat_template(
        cls,
        request: Request
    ) -> HTMLResponse:
        response = templates.TemplateResponse(
            'index.html',
            {
                'request': request,
                'users_url': cls._build_absoulte_url(cls._USERS_URL),
                'chat_url': cls._build_absoulte_url(cls._CHAT_URL),
            }
        )
        return response

    @classmethod
    async def get_register_template(
        cls,
        request: Request,
    ) -> HTMLResponse:
        response = templates.TemplateResponse(
            '/register/register.html',
            {
                'request': request,
                'register_url': cls._build_absoulte_url(cls._REGISTER_URL)
            }
        )
        return response

    @classmethod
    async def get_login_template(
        cls,
        request: Request,
    ) -> HTMLResponse:
        response = templates.TemplateResponse(
            '/register/login.html',
            {
                'request': request,
                'login_url': cls._build_absoulte_url(cls._LOGIN_URL)
            }
        )
        return response

    @classmethod
    def _build_absoulte_url(cls, endpoint: str) -> str:
        return cls._BASE_URL + endpoint
