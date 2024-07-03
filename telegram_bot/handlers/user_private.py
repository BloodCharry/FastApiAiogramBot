from aiogram import Router, F, types

from aiogram.filters import CommandStart, Command, ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import ChatMemberUpdated

from telegram_bot.keyboards.reply import get_keyboard
from telegram_bot.filters.chat_types import ChatTypeFilter, IsUser

user_private_router = Router()

user_private_router.message.filter(ChatTypeFilter(['private']), IsUser())


@user_private_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def user_added_to_group(event: ChatMemberUpdated):
    user = event.new_chat_member.user
    await event.bot.send_message(user.id, "Приветствуем вас на нашем ресурсе! "
                                          "Для начала работы нажмите кнопку старт или напишите /start")


# Функция, вызываемая при запуске бота
@user_private_router.message(CommandStart())
async def on_startup(message: types.Message):
    await message.answer("Привет пользователь!",
                         reply_markup=get_keyboard("Пропуска",
                                                   "События",
                                                   "Территории",
                                                   placeholder="Выберите действие",
                                                   sizes=(1, 1, 1), ))
