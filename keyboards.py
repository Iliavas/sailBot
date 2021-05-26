from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:
    @staticmethod
    def base_keyboard():
        keyboard = ReplyKeyboardMarkup()
        keyboard.add(KeyboardButton("Посмотреть корзину"))
        keyboard.add(KeyboardButton("Посмотреть меню"))
        keyboard.add(KeyboardButton("Список заказов"))
        return keyboard
    

    @staticmethod
    def trash_keyboard():
        keyboard = ReplyKeyboardMarkup()
        keyboard.add(KeyboardButton("Очистить корзину"))
        keyboard.add(KeyboardButton("Посмотреть стоимость"))
        keyboard.add(KeyboardButton("Заказать"))
        keyboard.add(KeyboardButton("Назад"))
        return keyboard
    

    @staticmethod
    def product_inline_keyboard(Type:str, user_id:str):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Добавить в корзину", callback_data="add {} {}".format(Type, user_id)))
        return keyboard
    
    @staticmethod
    def delete_inline_keyboard(Type:str, user_id:str):
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Удалить из корзины", callback_data="delete {} {} ".format(Type, user_id)))
        return keyboard