import telebot


from datetime import date, timedelta
from environs import Env
from telebot.util import quick_markup


env = Env()
env.read_env()
tg_bot_token = env('TG_CLIENTS_TOKEN')
pay_token = env('PAYMENTS_TOKEN')
agreement = env('AGREEMENT')
bot = telebot.TeleBot(token=tg_bot_token)

# others
INPUT_DUE_TIME = 60     # time (sec) to wait for user text input
BUTTONS_DUE_TIME = 30   # time (sec) to wait for user clicks button
ACCESS_DUE_TIME = 300   # if more time has passed since last main menu we should check access again


date_now = date.today()
date_end = date.today() + timedelta(days=14)

chats = {}
time_buttons = {}

# main menu callback buttons
client_buttons = [
    {'Список услуг': {'callback_data': 'list_of_services'}},
    {'О нас': {'callback_data': 'information'}},
    {'Контактные данные': {'callback_data': 'contact_details'}},
    {'Оставить отзыв': {'callback_data': 'review'}},
    {'Хочу записаться': {'callback_data': 'recording'}},

]

markup_cancel_step = quick_markup({
    'Отмена': {'callback_data': 'cancel_step'},
  })

markup_recording = quick_markup({
    'К свободному мастеру': {'callback_data': 'all_masters'},
    'Выбрать мастера': {'callback_data': 'master_choice'},
    'Отмена': {'callback_data': 'cancel_step'},
}, row_width=1)

markup_recording_time = quick_markup({
    'Выбрать время': {'callback_data': 'recording_time'},
    'Отмена': {'callback_data': 'cancel_step'},
}, row_width=1)

markup_user_data = quick_markup({
    'Введите ваши данные': {'callback_data': 'user_data_id'},
    'Отмена': {'callback_data': 'cancel_step'},
}, row_width=1)

markup_accept = quick_markup({
    'Принять': {'callback_data': 'accept'},
    'Отмена': {'callback_data': 'cancel_step_accept'},
}, row_width=1)

markup_registration = quick_markup({
    'Записаться и оплатить': {'callback_data': 'registration_pay', 'pay': True},
    'Записаться': {'callback_data': 'registration'},
    'Отмена': {'callback_data': 'cancel_step'},
}, row_width=1)
