from pydantic import BaseModel
from typing import Union

from telegram_bot.database.config import session_maker
from telegram_bot.database.models import Users


class UserData(BaseModel):
    """базовая модель прёмки json от java-backend"""
    name: str
    mail: str
    role: str
    service_id: int


class SignalData(BaseModel):
    """Модель приёма json сигналов"""
    sigtnal: str
    event: str


# Объединение моделей
class CombinedModel(BaseModel):
    """комби модель для удобства обработки"""
    data: Union[UserData, SignalData]


async def save_user_data(user_data: UserData):
    """функция сохранения прнятых данных в нашу базу данных"""
    async with session_maker() as session:
        async with session.begin():
            user = Users(
                name=user_data.name,
                mail=user_data.mail,
                role=user_data.role,
                service_id=user_data.service_id
            )
            session.add(user)
        await session.commit()
        return user.service_id


async def save_signal_data(signal_data: SignalData):
    pass


async def save_data(data: CombinedModel):
    """функция проверки моделей и вызова нужного обработчика по принятому json"""
    if isinstance(data.data, UserData):
        return await save_user_data(data.data)

    elif isinstance(data.data, SignalData):
        await save_signal_data(data.data)
