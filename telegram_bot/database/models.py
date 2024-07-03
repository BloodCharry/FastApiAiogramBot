from sqlalchemy import String, DateTime, func, MetaData

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()


class Base(DeclarativeBase):
    """
    Базовый класс моделей, содержащий поля created и updated
    которые будут присудствовать в каждой таблицые для отслеживания изменений в БД
    """
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class Users(Base):
    __tablename__ = "users"
    """
    Модель для хранения информации о пользователях
    """
    user_id: Mapped[int] = mapped_column(autoincrement=False, nullable=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    mail: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(String(150))
    invite_link: Mapped[str] = mapped_column(String(150), nullable=True)
    service_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
