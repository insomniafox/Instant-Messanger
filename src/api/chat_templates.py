from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from src.services.templates.templates import TemplateService

router = APIRouter(prefix='')


@router.get('/chat', response_class=HTMLResponse)
async def chat_template(request: Request):
    response = await TemplateService.get_chat_template(request)
    return response


@router.get('/sign-up', response_class=HTMLResponse)
async def get_register_template(request: Request):
    response = await TemplateService.get_register_template(request)
    return response


@router.get('/sign-in', response_class=HTMLResponse)
async def get_register_template(request: Request):
    response = await TemplateService.get_login_template(request)
    return response
