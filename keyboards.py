from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

'''
класс клавиатур
'''
class Keyboard:
    @staticmethod
    def base_keyboard():
        '''
        клавиатура, появляющаяся в начале работы бота
        '''
        keyboard = ReplyKeyboardMarkup()
        keyboard.add(KeyboardButton("Посмотреть корзину"))
        keyboard.add(KeyboardButton("Посмотреть меню"))
        keyboard.add(KeyboardButton("Список заказов"))
        return keyboard
    

    @staticmethod
    def trash_keyboard():
        '''
        клавиатура, появляющаяся при переходе на просмотр корзины
        '''
        keyboard = ReplyKeyboardMarkup()
        keyboard.add(KeyboardButton("Очистить корзину"))
        keyboard.add(KeyboardButton("Посмотреть стоимость"))
        keyboard.add(KeyboardButton("Заказать"))
        keyboard.add(KeyboardButton("Назад"))
        return keyboard
    

    @staticmethod
    def product_inline_keyboard(product_id:str, user_id:str):
        '''
        клавиатура появляющаяся при просмотре меню, нужна чтобы добавить текущий товар в корзину
        '''
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Добавить в корзину", callback_data="add {} {}".format(product_id, user_id)))
        return keyboard
    
    @staticmethod
    def delete_inline_keyboard(product_id:str, user_id:str):
        '''
        клавиатура появляющаяся при просмотре корзины, нужна чтобы удалить текущий товар из корзины
        '''
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Удалить из корзины", callback_data="delete {} {} ".format(product_id, user_id)))
        return keyboard