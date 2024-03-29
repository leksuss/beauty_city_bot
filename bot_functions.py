import datetime as dt
import telebot
import db


from telebot.util import quick_markup
from telebot.types import LabeledPrice, ShippingOption
from telegram_bot_calendar.base import DAY
from telegram_bot_calendar.detailed import DetailedTelegramCalendar
from db import procedure_id, master_id
from globals import (
bot, agreement, ACCESS_DUE_TIME, markup_cancel_step, INPUT_DUE_TIME, chats, client_buttons, markup_recording, date_now,
date_end, markup_accept, markup_user_data, markup_registration, pay_token
)


shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]


class WMonthTelegramCalendar(DetailedTelegramCalendar):
    first_step = DAY


def get_markup(buttons, row_width=1):
    return quick_markup(buttons, row_width=row_width)


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
    time_buttons.update({'Назад': {'callback_data': 'all_masters'}})
    return quick_markup(time_buttons, row_width=3)


def start_bot(message: telebot.types.Message):
    tg_name = message.from_user.username
    msg = bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.username}.')
    access_due = dt.datetime.now() + dt.timedelta(0, ACCESS_DUE_TIME)
    buttons = get_client_buttons(client_buttons)
    markup_client = get_markup(buttons)
    chats[message.chat.id] = {
        'callback': None,  # current callback button
        'last_msg': [],  # последние отправленные за один раз сообщения (для подчистки кнопок) -- перспектива
        'code_services': [],
        'code_masters': [],
        'callback_source': [],  # если задан, колбэк кнопки будут обрабатываться только с этих сообщений
        'access_due': access_due,  # дата и время актуальности кэшированного статуса
        'name': None,
        'date': None,
        'time': None,
        'master': None,
        'master_id': None,
        'service': None,
        'service_id': None,
        'cost': None,
        'msg_id_1': None,
        'msg_id_2': None,
        'agreement': None,  # для согласия на обработку данных
        'tg_name': tg_name,
        'text': None,  # для разных целей - перспектива
        'phone': None,
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
                                      'Нажмите /start')
        return None
    else:
        return user


def cancel_step(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons)
    markup_client = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Действие отменено', reply_markup=markup_client)


def cancel_step_accept(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    bot.delete_message(message.chat.id, message.message_id)
    buttons = get_client_buttons(client_buttons)
    markup_client = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Действие отменено', reply_markup=markup_client)


def get_list_of_services(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons, 0)
    markup_client = get_markup(buttons)
    service_text = db.get_data_procedures()[2]
    text = service_text
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=text, reply_markup=markup_client)


def get_information(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons, 1)
    markup_client = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Что представляет собой BeautyCity. \n Это сервис онлайн записи в салон красоты. '
                               'С его помощью можно легко и удобно записываться на прием, не выходя из дома. '
                               'Не придется много раз звонить, если линии заняты, или долго ожидать ответа. '
                               'Запись проходит в онлайн режиме.', reply_markup=markup_client)


def get_contact_details(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    buttons = get_client_buttons(client_buttons, 2)
    markup_client = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Адрес: \n г. Алматы, пр. Жибек жолы 999, блок 9, этаж 9 \n '
                               'Товарищество с ограниченной ответственностью "BeautyCity" \n'
                               'Телефон: +74957777777 \n '
                               'Запись проходит в онлайн режиме.', reply_markup=markup_client)


def get_review(message: telebot.types.Message, order_id, step=0):
    user = chats[message.chat.id]
    if step == 0:
        msg = bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                    text=f'Введите отзыв ', reply_markup=markup_cancel_step)
        user['callback_source'] = [msg.id]
        bot.register_next_step_handler(message, get_review, order_id, 1)
        user['step_due'] = dt.datetime.now() + dt.timedelta(0, INPUT_DUE_TIME)
    elif user['step_due'] < dt.datetime.now():
        bot.send_message(message.chat.id, 'Время ввода данных истекло. Нажмите /start')
        return
    elif step == 1:
        user['text'] = message.text
        buttons = get_client_buttons(client_buttons)
        markup_client = get_markup(buttons)
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                    text=f'Cпасибо за Ваш отзыв!',
                                    reply_markup=markup_client)
        db.add_comment(user['tg_name'], user['text'])
        user['callback'] = None
        user['callback_source'] = []


def get_recording(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    service_buttons = db.get_data_procedures()[1]
    markup_services = get_markup(service_buttons)
    code_services = db.get_data_procedures()[0]
    user['code_services'] = code_services
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
        text=f'Выберите услугу', reply_markup=markup_services)


def get_service(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    user['service_id'] = int(call) - procedure_id
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Услуга выбрана запишитесь к специалисту', reply_markup=markup_recording)


def get_master_buttons(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    id = int(user['service_id'])
    buttons = {}
    masters = db.get_masters(id)[0]
    user['code_masters'] = db.get_masters(id)[1]
    for master_id in masters:
        name = masters[master_id]['name']
        buttons.update({name: {'callback_data': master_id}})
    buttons.update({'Отмена': {'callback_data': 'cancel_step'}})
    markup_masters = get_markup(buttons)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выберите мастера', reply_markup=markup_masters)


def get_date_of_visit(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    if call != 'all_masters':
        user['master_id'] = int(call) - master_id
    calendar, step = WMonthTelegramCalendar(locale='ru', min_date=date_now, max_date=date_end).build()
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выберите день', reply_markup=calendar)


def get_recording_time(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    date = user['date']
    master = user['master_id']
    procedure = user['service_id']
    recording_time = []
    time_slots = db.get_time(procedure, date, master)
    for time in time_slots:
        recording_time.append(str(time))
    user['last_msg'] = recording_time
    markup_time = get_markup_time(recording_time)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text='Выберите время', reply_markup=markup_time)


def process_callback_time_button(message: telebot.types.Message, recording_time):
    user = chats[message.chat.id]
    user['time'] = recording_time
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'Выбранное время {recording_time}', reply_markup=markup_user_data)


def get_user_data_id(message: telebot.types.Message, order_id, step=0):
    user = chats[message.chat.id]
    if step == 0:
        msg = bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                              text=f'Введите имя ', reply_markup=markup_cancel_step)
        user['callback_source'] = [msg.id]
        bot.register_next_step_handler(message, get_user_data_id, order_id, 1)
        user['step_due'] = dt.datetime.now() + dt.timedelta(0, INPUT_DUE_TIME)
    elif user['step_due'] < dt.datetime.now():
        bot.send_message(message.chat.id, 'Время ввода данных истекло. Нажмите /start')
        return
    elif step == 1:
        user['name'] = message.text
        bot.delete_message(message.chat.id, message.message_id)
        msg = bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                    text=f'Ваше имя {user["name"]}. Введите номер телефона', reply_markup=markup_cancel_step)
        user['callback_source'] = [msg.id]
        bot.register_next_step_handler(message, get_user_data_id, order_id, 2)
        user['step_due'] = dt.datetime.now() + dt.timedelta(0, INPUT_DUE_TIME)
    elif step == 2:
        user['phone'] = message.text
        bot.delete_message(message.chat.id, message.message_id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                                    text='Ознакомьтесь с согласием на обработку персональных данных. '
                                         'При согласии нажмите "Принять" или кнопку отмены.',
                                    )
        bot.send_document(message.chat.id, open(agreement, 'rb'), reply_markup=markup_accept)
        user['callback'] = None
        user['callback_source'] = []


def get_accept(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    user['agreement'] = True
    masters = db.get_masters(user['service_id'])[0]
    procedures = db.get_procedures()
    if user['master_id']:
        id = master_id + int(user['master_id'])
        print(masters[f'{id}']['name'])
        print(masters)
        user['master'] = masters[f'{id}']['name']
    else:
        user['master'] = 'Свободному'
    user['service'] = procedures[f'{procedure_id+int(user["service_id"])}']['name']
    user['cost'] = procedures[f'{procedure_id+int(user["service_id"])}']['cost']
    bot.delete_message(message.chat.id, message.message_id)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text=f'*Запись к мастеру {user["master"]}*\n---\n' \
                               f'Услуга {user["service"]}\n---\n' \
                               f'Стоимость {user["cost"]} руб.\n---\n' \
                               f'Дата посещения салона: {user["date"]}\n' \
                               f'Время посещения: {user["time"]}\n --- \n', reply_markup=markup_registration)
    user['master'] = None


def get_registration(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    user['agreement'] = True
    buttons = get_client_buttons(client_buttons)
    markup_client = get_markup(buttons)
    db.add_new_user(user['tg_name'], user['name'], user['phone'])
    bot.send_message(chat_id=message.chat.id,
                          text=f'*Запись подтверждена*\n---\n' \
                               f'Услуга {user["service"]}\n---\n' \
                               f'Стоимость {user["cost"]} руб.\n---\n' \
                               f'Дата посещения салона: {user["date"]}\n' \
                               f'Время посещения: {user["time"]}\n --- \n'
                               f'Адрес: \n г. Алматы, пр. Жибек жолы 999, блок 9, этаж 9 \n '
                               f'Телефон: +74957777777 \n ')
    msg = bot.send_message(chat_id=message.chat.id,
                     text='Ура! Спасибо за запись! Ждем Вас в условленное время!',
                     parse_mode='Markdown', reply_markup=markup_client)
    chats[message.chat.id]['msg_id_2'] = msg.id
    db.add_appointment(user["service_id"], user['tg_name'], user["date"], user["time"], user["master"])


def get_registration_pay(message: telebot.types.Message, call):
    user = chats[message.chat.id]
    user['agreement'] = True
    price = LabeledPrice(label='Услуги салона красоты', amount=int(user['cost']) * 100)
    bot.edit_message_text(chat_id=message.chat.id, message_id=user['msg_id_2'],
                          text="Со мной не будут работать настоящие карты, никакие деньги не будут списаны с вашего счета."
                     " Используйте этот номер тестовой карты для оплаты: `4242 4242 4242 4242`"
                     "\n\nДля отмены платежа нажмите кнопку /start"
                     "\n\nЭто ваш демонстрационный счет:", parse_mode='Markdown')
    bot.send_invoice(
        message.chat.id,
        title='Услуги салона красоты',
        description='Оплата услуги салона красоты',
        provider_token=pay_token,
        invoice_payload='Оплата услуги салона красоты',
        currency='rub',
        prices=[price],
        photo_url='https://kartinkof.club/uploads/posts/2022-04/1649916854_1-kartinkof-club-p-rzhachnie-kartinki-pricheski-zhenskie-1.jpg',
        photo_height=512,
        photo_width=512,
        photo_size=512,
        is_flexible=False,  # True If you need to set up Shipping Fee
        start_parameter='test-invoice-payload')
