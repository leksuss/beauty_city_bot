import telebot


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


# main menu callback buttons

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



chats = {}

