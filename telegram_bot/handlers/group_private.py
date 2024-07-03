from string import punctuation
from aiogram import Router, F, types
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER

from aiogram.types import ChatMemberUpdated

from sqlalchemy import update
from telegram_bot.database.models import Users
from telegram_bot.filters.chat_types import ChatTypeFilter

from telegram_bot.database.config import session_maker

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_group_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))


@user_group_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def user_added_to_group(event: ChatMemberUpdated):
    """
    Обработка новых пользователей,
     функция проверяет пришёл ли пользователь по инвайт ссылке,
     если пользователь пришёл по инвайт ссылке ищет его в базе
      данных по service_id спрятанном в инвайт ссылке и обновляет поле user_id
    :param event:
    :return:
    """
    user = event.new_chat_member.user
    await event.bot.send_message(user.id, "Приветствуем вас на нашем ресурсе! "
                                          "Для начала работы нажмите кнопку старт или напишите /start")
    invite_link = event.invite_link
    if invite_link is not None:
        async with session_maker() as session:
            async with session.begin():
                stmt = (
                    update(Users).
                    where(Users.service_id == int(invite_link.name)).
                    values(user_id=user.id)
                )
                await session.execute(stmt)
                await session.commit()
        print(f'Пользователь {user.full_name} ({user.id}) присоединился к группе по ссылке: {invite_link.invite_link}'
              f' и его service_id: {invite_link.name}')
    else:
        print(f'Пользователь {user.full_name} ({user.id}) присоединился к группе.')


@user_group_router.message(F.new_chat_members)
async def on_join_user(message: types.Message):
    """
    удаление системных сообщений о вступлении в группу
    """
    await message.delete()


@user_group_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def user_leave_group(event: ChatMemberUpdated):
    """
    функция для обработки пользователя
     который покинул группу
    """
    pass
    # await event.answer(f"Пользователь {event.from_user.first_name} покинул группу")


@user_group_router.message(F.left_chat_members)
async def left_join_user(message: types.Message):
    """
        удаление системных сообщений о выходе из группы
        """
    await message.delete()


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))
