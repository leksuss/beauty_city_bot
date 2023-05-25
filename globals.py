import telebot

from datetime import date, timedelta
from telebot import types
from environs import Env
from telebot.util import quick_markup


env = Env()
env.read_env()
tg_bot_token = env('TG_CLIENTS_TOKEN')
agreement = env('AGREEMENT')
bot = telebot.TeleBot(token=tg_bot_token)

# others
INPUT_DUE_TIME = 60     # time (sec) to wait for user text input
BUTTONS_DUE_TIME = 30   # time (sec) to wait for user clicks button
ACCESS_DUE_TIME = 300   # if more time has passed since last main menu we should check access again

date_now = date.today()
date_end = date.today() + timedelta(days=14)

chats = {}

recording_time = [
    '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
    '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
    '19:00', '19:30', '20:00', '20:30', '21:00', '21:30'
]

# main menu callback buttons
time_buttons = {}

client_buttons = [
     {'Список услуг': {'callback_data': 'list_of_services'}},
     {'О нас': {'callback_data': 'information'}},
     {'Хочу записаться': {'callback_data': 'recording'}},
     {'Контактные данные': {'callback_data': 'contact_details'}},
     {'Оставить отзыв': {'callback_data': 'review'}}
]

# markup_client = quick_markup({
#     'Список услуг': {'callback_data': 'list_of_services'},
#     'О нас': {'callback_data': 'information'},
#     'Хочу записаться': {'callback_data': 'recording'},
#     'Контактные данные': {'callback_data': 'contact_details'},
#     'Оставить отзыв': {'callback_data': 'review'},
# })

markup_cancel_step = quick_markup({
    'Отмена': {'callback_data': 'cancel_step'},
  })





