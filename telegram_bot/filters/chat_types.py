from aiogram.filters import Filter
from aiogram import types, Bot
from telegram_bot.database.config import session_maker
from telegram_bot.database.models import Users
from sqlalchemy import select


class ChatTypeFilter(Filter):
    """ этот класс позволяет создать фильтр, который пропускает только сообщения
    из чатов определенных типов."""

    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        user_id = message.from_user.id
        async with session_maker() as session:
            stmt = select(Users).where(Users.user_id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user and user.role == "admin":
                return True
            pass


class IsManager(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        user_id = message.from_user.id
        async with session_maker() as session:
            stmt = select(Users).where(Users.user_id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user and user.role == "manager":
                return True
            pass


class IsSecurity(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        user_id = message.from_user.id
        async with session_maker() as session:
            stmt = select(Users).where(Users.user_id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user and user.role == "security":
                return True
            pass


class IsUser(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        user_id = message.from_user.id
        async with session_maker() as session:
            stmt = select(Users).where(Users.user_id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user and user.role == "user":
                return True
            pass
