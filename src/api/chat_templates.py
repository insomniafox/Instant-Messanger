from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from src.models.users.models import User
from src.services.users.dependencies import get_current_user
from src.services.templates.templates import TemplateService

router = APIRouter(prefix='')


@router.get('/chat', response_class=HTMLResponse)
async def chat_template(request: Request):
    response = await TemplateService.get_chat_template(
        request=request
    )
    return response


@router.get('/sign-up', response_class=HTMLResponse)
async def get_register_template(request: Request):
    response = await TemplateService.get_register_template(request)
    return response


@router.get('/sign-in', response_class=HTMLResponse)
async def get_register_template(request: Request):
    response = await TemplateService.get_login_template(request)
    return response
