import datetime as dt

import bot_functions as calls


from globals import (
    bot, agreement, ACCESS_DUE_TIME, markup_cancel_step, INPUT_DUE_TIME, chats, client_buttons, telebot, date_now,
    date_end, recording_time, chats, markup_recording_time, shipping_options,
)
from telegram_bot_calendar import LSTEP
from telegram_bot_calendar.base import DAY
from telegram_bot_calendar.detailed import DetailedTelegramCalendar



# general callback functions mapping to callback buttons
# all of these buttons are from main user menus

calls_map = {
    'accept': calls.get_accept,
    'list_of_services': calls.get_list_of_services,
    'information': calls.get_information,
    'contact_details': calls.get_contact_details,
    'recording': calls.get_recording,
    'review': calls.get_review,
    'all_masters': calls.get_date_of_visit,
    'master_choice': calls.get_masters,
    'cancel_step': calls.cancel_step,
    'cancel_step_accept': calls.cancel_step_accept,
    'recording_time': calls.get_recording_time,
    'registration': calls.get_registration,
    'registration_pay': calls.get_registration_pay,
    '100': calls.get_service,
    '101': calls.get_service,
    '102': calls.get_service,
    '103': calls.get_service,
    '104': calls.get_service,
    '105': calls.get_service,
    '500': calls.get_date_of_visit,
    '501': calls.get_date_of_visit,
    '502': calls.get_date_of_visit,
}

calls_time_map = {
    '10:00': calls.process_callback_time_button,
    '10:30': calls.process_callback_time_button,
    '11:00': calls.process_callback_time_button,
    '11:30': calls.process_callback_time_button,
    '12:00': calls.process_callback_time_button,
    '12:30': calls.process_callback_time_button,
    '13:00': calls.process_callback_time_button,
    '13:30': calls.process_callback_time_button,
    '14:00': calls.process_callback_time_button,
    '14:30': calls.process_callback_time_button,
    '15:00': calls.process_callback_time_button,
    '15:30': calls.process_callback_time_button,
    '16:00': calls.process_callback_time_button,
    '16:30': calls.process_callback_time_button,
    '17:00': calls.process_callback_time_button,
    '17:30': calls.process_callback_time_button,
    '18:00': calls.process_callback_time_button,
    '18:30': calls.process_callback_time_button,
    '19:00': calls.process_callback_time_button,
    '19:30': calls.process_callback_time_button,
    '20:00': calls.process_callback_time_button,
    '20:30': calls.process_callback_time_button,
    '21:00': calls.process_callback_time_button,
    '21:30': calls.process_callback_time_button,
}

# callback functions mapping to callback buttons
# for handling particular entity by ID
# all of these buttons are attached to particular messages

calls_id_map = {
    'user_data_id': calls.get_user_data_id,
}


class WMonthTelegramCalendar(DetailedTelegramCalendar):
    first_step = DAY



@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    calls.start_bot(message)


@bot.message_handler()
def get_text(message):
    if calls.check_user_in_cache(message):
        bot.delete_message(message.chat.id, message.message_id)


@bot.callback_query_handler(func=WMonthTelegramCalendar.func())
def cal(c):
    result, key, step = WMonthTelegramCalendar(locale='ru', min_date=date_now, max_date=date_end).process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали {result}",
                              c.message.chat.id,
                              c.message.message_id, reply_markup=markup_recording_time)
    user = chats[c.message.chat.id]
    user['date'] = result




@bot.callback_query_handler(func=lambda call: call.data)
def handle_buttons(call):
    user = calls.check_user_in_cache(call.message)
    if not user:
        return
    source = user['callback_source']
    if source and not call.message.id in user['callback_source']:
        bot.send_message(call.message.chat.id, 'Кнопка не актуальна')
        return
    elif (dt.datetime.now()-dt.timedelta(0, 180)) > dt.datetime.fromtimestamp(call.message.date):
        bot.send_message(call.message.chat.id, 'Срок действия кнопки истек')
        return
    btn_command: str = call.data
    if user['callback']:
        bot.send_message(call.message.chat.id,
                         f'Вы находитесь в режиме '
                         f'ввода данных другой команды.\n'
                         f'Сначала завершите ее или отмените')
        return
    if 'id' in btn_command:
        parts = btn_command.split(':')
        key_func = parts[-1]
        func_name = parts[0]
        calls_id_map[func_name](call.message, key_func)
        return
    elif call.data in recording_time:
        calls_time_map[call.data](call.message, call.data)
    else:
        calls_map[call.data](call.message, call.data)


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Повторите попытку позже!')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message='Инопланетяне пытались украсть CVV вашей карты, но мы успешно защитили '
                                                'ваши учетные данные. Попробуй заплатить еще раз через несколько минут, '
                                                'нам нужен небольшой отдых.')


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Ура! Спасибо за оплату услуги! Ждем Вас в условленное время!',
                     parse_mode='Markdown')
    calls.start_bot(message)


bot.polling(none_stop=True, interval=0)