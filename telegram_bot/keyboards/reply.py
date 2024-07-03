from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder


# функция для создания текстовой клавиатуры
def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,), ):
    '''
    Parameters request_contact and request_location must be as indexes of btns
    args for buttons you need.
    Example:
    get_keyboard(
    To request a contact or location, pass the button index to request_сontact or request_location
            "Бесплатные материалы",
            "Часто задаваемые вопросы",
            "Хочу записаться к вам на мок-бес",
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''

    # Создание экземпляра клавиатуры с помощью класса ReplyKeyboardBuilder.
    keyboard = ReplyKeyboardBuilder()

    # Цикл по всем кнопкам, которые были переданы в функцию. enumerate
    # используется для получения индекса каждой кнопки.
    for index, text in enumerate(btns, start=0):

        # Если текущий индекс кнопки совпадает с request_contact, то добавляется кнопка,
        # которая будет запрашивать контакт пользователя.
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        # Если текущий индекс кнопки совпадает с request_location, то добавляется кнопка,
        # которая будет запрашивать местоположение пользователя.
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            # Если текущий индекс кнопки не совпадает ни с request_contact, ни с request_location,
            # то добавляется обычная кнопка.
            keyboard.add(KeyboardButton(text=text))

    # Настройка размера клавиатуры с помощью метода adjust и преобразование ее в разметку с помощью метода as_markup.
    # Также устанавливается заполнитель поля ввода и включается опция resize_keyboard.
    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder)