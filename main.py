import datetime as dt

import bot_functions as calls
from globals import *


# general callback functions mapping to callback buttons
# all of these buttons are from main user menus
calls_map = {
    'list_of_services': calls.get_list_of_services,
    'information': calls.get_information,
    'contact_details': calls.get_contact_details,
    'recording': calls.get_recording,
    'review': calls.get_review

}

# callback functions mapping to callback buttons
# for handling particular entity by ID
# all of these buttons are attached to particular messages
calls_id_map = {

}

@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    calls.start_bot(message)


@bot.message_handler()
def get_text(message):
    if calls.check_user_in_cache(message):
        bot.send_message(message.chat.id, 'Для работы с ботом пользуйтесь кнопками')
        calls.start_bot(message)



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
    current_command = user['callback']
    if btn_command == 'cancel_step':
        if current_command:
            calls.cancel_step(call.message)
        return
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
    else:
        calls_map[call.data](call.message)


bot.polling(none_stop=True, interval=0)