from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)
#     """
#     внешний Middleware для Проверки роли пользователя,
#     для предоставления функционала согласно его роли
#     """
#     def __init__(self) -> None:
#         pass
#
#     async def __call__(self,
#                        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#                        event: TelegramObject,
#                        data: Dict[str, Any]
#                        ) -> Any:
#         if event.from_user.id in role.admin:
#             return await handler(event)
