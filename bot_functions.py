import datetime as dt
import json
import telebot


from telebot.util import quick_markup
from datetime import timedelta
from globals import (
    bot, agreement, ACCESS_DUE_TIME, markup_cancel_step, INPUT_DUE_TIME, chats, client_buttons, recording_time,

)



def get_markup_client(buttons):
    return quick_markup(buttons, row_width=1)


def get_client_buttons(buttons, key=None):
    client_buttons = {}
    for index, button in enumerate(buttons):
        if index != key:
            client_buttons.update(button)
    return client_buttons

def get_markup_time(recording_time):
    time_buttons = {}
    for time in recording_time:
        button = {time: {'callback_data': f'{time}'}}
        time_buttons.update(button)
    return quick_markup(time_buttons, row_width=6)

def start_bot(message: telebot.types.Message):
    tg_name = message.from_user.username
    msg = bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username}.')
    access_due = dt.datetime.now() + dt.timedelta(0, ACCESS_DUE_TIME)
    # access, group = db.check_user_access(tg_name=user_name)
    buttons = get_client_buttons(client_buttons)
    markup_client = get_markup_client(buttons)
    chats[message.chat.id] = {
        'callback': None,  # current callback button
        'last_msg': [],  # последние отправленные за один раз сообщения (для подчистки кнопок) -- перспектива
        'callback_source': [],  # если задан, колбэк кнопки будут обрабатываться только с этих сообщений
        'access_due': access_due,  # дата и время актуальности кэшированного статуса
        'msg_id_1': None,
        'msg_id_2': None,
        'agreement': None,  # для согласия на обработку данных
        'tg_name': tg_name,
        'text': None,  # для разных целей - перспектива
        'number': None,  # для разных целей - перспектива
        'step_due': None,  # срок актуальности ожидания ввода данных (используем в callback функциях)
    }
    chats[message.chat.id]['msg_id_1'] = msg.id
    msg = bot.send_message(message.chat.id, 'Вас приветствует онлайн-запись в сфере красоты и здоровья',
                           reply_markup=markup_client)
    chats[message.chat.id]['msg_id_2'] = msg.id


def check_user_in_cache(msg: telebot.types.Message):
    """проверят наличие user в кэше
    это на случай, если вдруг случился сбой/перезапуск скрипта на сервере
    и кэш приказал долго жить. В этом случае нужно отправлять пользователя в начало
    пути, чтобы избежать ошибок """
    user = chats.get(msg.chat.id)
    if not user:
        bot.send_message(msg.chat.id, 'Упс. Что то пошло не так.\n'
                                      'Начнем с главного меню')
        start_bot(msg)
        return None
    else:
        return user


def cancel_step(message: telebot.types.Message):
    """cancel current input process and show main menu"""
    bot.clear_step_handler(message)
    bot.send_message(message.chat.id, 'Действие отменено')
    chats[message.chat.id]['callback'] = None


def get_list_of_services(message: telebot.types.Message):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons, 0)
    markup_client = get_markup_client(buttons)
    text = 'Парикмахерские услуги - 1000 р. \n Наращивание ресниц - 1000 р.\n ' \
           'Педикюр (все виды) - 1000 р.\n Маникюр (все виды) - 1000 р.\n ' \
           'Наращивание ногтей - 1000 р.\n Услуги визажиста - 1000 р.'
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=text, reply_markup=markup_client)


def get_information(message: telebot.types.Message):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons, 1)
    markup_client = get_markup_client(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Что представляет собой BeautyCity. \n Это сервис онлайн записи в салон красоты. '
                               'С его помощью можно легко и удобно записываться на прием, не выходя из дома. '
                               'Не придется много раз звонить, если линии заняты, или долго ожидать ответа. '
                               'Запись проходит в онлайн режиме.', reply_markup=markup_client)


def get_recording(message: telebot.types.Message):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons, 2)
    markup_client = get_markup_client(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Кнопка не работает {message.chat.id}', reply_markup=markup_client)


def get_contact_details(message: telebot.types.Message):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons, 3)
    markup_client = get_markup_client(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Адрес: \n г. Алматы, пр. Жибек жолы 999, блок 9, этаж 9 \n '
                               'Товарищество с ограниченной ответственностью "BeautyCity" \n'
                               'Телефон: +74957777777 \n '
                               'Запись проходит в онлайн режиме.', reply_markup=markup_client)


def get_review(message: telebot.types.Message):
    user = chats[message.chat.id]
    # buttons = get_client_buttons(client_buttons, 4)
    markup_time = get_markup_time(recording_time)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Выберите время', reply_markup=markup_time)



def get_recording_time(message: telebot.types.Message):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons)
    markup_client = get_markup_client(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Кнопка пока не работает {message.chat.id}', reply_markup=markup_client)


def process_callback_time_button(message: telebot.types.Message, recording_time):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons)
    markup_client = get_markup_client(buttons)

    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выбранное время {recording_time}', reply_markup=markup_client)


