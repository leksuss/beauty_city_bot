import telebot

from datetime import date, timedelta
from environs import Env
from telebot.util import quick_markup
from telebot.types import LabeledPrice, ShippingOption


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

PRICE = LabeledPrice(label='Услуги салона красоты', amount=1000*100)

shipping_options = [
    ShippingOption(id='instant', title='WorldWide Teleporter').add_price(LabeledPrice('Teleporter', 1000)),
    ShippingOption(id='pickup', title='Local pickup').add_price(LabeledPrice('Pickup', 300))]

date_now = date.today()
date_end = date.today() + timedelta(days=14)

chats = {}

recording_time = [
    '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
    '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
    '19:00', '19:30', '20:00', '20:30', '21:00', '21:30'
]

code_services = ['100', '101', '102', '103', '104', '105']

masters = { '500': {
    'name': 'Ольга',
    'code_services': ['100', '101', '102']
    },
    '501': {
    'name': 'Татьяна',
    'code_services': ['100', '101', '102', '104'],
    },
    '502': {
    'name': 'Валентина',
    'code_services': ['100', '101', '103', '105'],
    }
}

# main menu callback buttons
time_buttons = {}

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

markup_services = quick_markup({
    'Парикмахерские услуги': {'callback_data': '100'},
    'Наращивание ресниц': {'callback_data': '101'},
    'Педикюр (все виды)': {'callback_data': '102'},
    'Маникюр (все виды)': {'callback_data': '103'},
    'Наращивание ногтей': {'callback_data': '104'},
    'Услуги визажиста': {'callback_data': '105'},
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
