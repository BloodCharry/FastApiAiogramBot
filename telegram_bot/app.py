import logging
import os

from fastapi import FastAPI, Request

from aiogram import types, Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats

from dotenv import load_dotenv, find_dotenv

from telegram_bot.handlers.group_private import user_group_router
from telegram_bot.filters.json_filter import CombinedModel, save_data
from telegram_bot.database.config import session_maker
from telegram_bot.middlewares.based_middlewares import DataBaseSession
from telegram_bot.common.qr_code import gererated_qr_code

load_dotenv((find_dotenv()))

from telegram_bot.handlers.user_private import user_private_router
from telegram_bot.handlers.admin_private import admin_private_router
from telegram_bot.handlers.manager_handler import manager_private_router
from telegram_bot.handlers.security_handler import security_private_router
from telegram_bot.handlers.common_handlers import private_router
from telegram_bot.common.bot_cmds import bot_commands

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

bot_app = FastAPI()
token = os.getenv("TOKEN")
ngrok_tunnel_url = os.getenv("NGROK_TUNNEL_URL")
chat_id = os.getenv('CHAT_ID')

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

dp.include_routers(
    user_group_router,
    admin_private_router,
    manager_private_router,
    security_private_router,
    user_private_router,
    private_router
)

WEBHOOK_PATH = f"/bot/{token}"
WEBHOOK_URL = f"{ngrok_tunnel_url}{WEBHOOK_PATH}"


@bot_app.on_event("startup")
async def on_startup():
    '''
     функция вызываемая при запуске бота,
     проверяет, соответствует ли текущий вебхук URL,
     который используется (WEBHOOK_URL),
     если нет,устанавливает новый вебхук с этим URL,
     а так же создаёт базу данных если её нету
     '''
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            allowed_updates=["message",
                             "edited_message",
                             "chat_member",
                             ],
        )


@bot_app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    '''
    функция обрабатывает обновления от Telegram, удаляет старые команды бота,
    устанавливает новые команды и передает обновления в диспетчер для обработки.
    '''
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
                                                   "(%(filename)s.%(funcName)s:%(lineno)d) - %(message)s")
    telegram_update = types.Update(**update)
    # нужно только если введены новые команды, для обновления списка команд
    # await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.set_my_commands(commands=bot_commands, scope=BotCommandScopeAllPrivateChats())
    await dp.feed_update(bot=bot, update=telegram_update)


@bot_app.post("/receive-json")
async def receive_json(combined_data: CombinedModel, request: Request):
    """
    функция прёма json данных, включает в себя вызов функций
     service_id, invite_link, generated_qr_code.
     А так же возращает ответ отправителю ввиде json с нужными данными

    :param combined_data:
    :param request:
    :return:
    """
    source_url = str(request.url)
    print(f"Получены JSON-данные из {source_url}:", combined_data.model_dump())
    service_id = await save_data(combined_data)
    invite_link = await bot.create_chat_invite_link(chat_id=chat_id, member_limit=1, name=str(service_id))
    qr_code_str = await gererated_qr_code(link=invite_link.invite_link)
    print(invite_link.invite_link)
    try:
        print("Данные успешно сохранены")
        print(f"service_id: {service_id},invite_link: {invite_link.invite_link} ,qr_code: {qr_code_str}")
        return {
            "data_qr_link": {
                "service_id": service_id,
                "invite_link": invite_link.invite_link,
                "qr_code": qr_code_str
            }
        }
    except Exception as e:
        print('Ошибка при сохранении данных:', e)
        return {"error": str(e)}


@bot_app.on_event("shutdown")
async def on_shutdown():
    '''
    функция вызываемая при остановке бота,
    закрывает сессию
    '''
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
