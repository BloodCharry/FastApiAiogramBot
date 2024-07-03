from aiogram import Router, types
from aiogram.filters import CommandStart
from telegram_bot.filters.chat_types import ChatTypeFilter

private_router = Router()
private_router.message.filter(ChatTypeFilter(["private"]))


@private_router.message(CommandStart())
async def guest_user(message: types.Message):
    await message.answer("Приветствуем вас на нашем ресурсе! "
                         "Для доступа к боту зарегестрируйтесь на "
                         "сайте https://checkpoint-manager.ru")
