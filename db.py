import os, sys

import django
DJANGO_PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(DJANGO_PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauty_city_bot.settings")
django.setup()

from salon.models import Master, Procedure, Appointment, Time, Client, Review


procedure_id = 100
master_id = 500


def get_procedures():
    procedures_db = Procedure.objects.all()
    procedures = {}
    for procedure in procedures_db:
        proc = {f'{procedure_id + procedure.id}':
            {
                'name': procedure.name,
                'cost': procedure.cost,
            }
        }
        procedures.update(proc)
    return procedures


def get_time_slot():
    time_slota_db = Time.objects.all()
    time_slots = {}
    for time in time_slota_db:
        time_slot = {time.time_slot:
            {
                'id': time.id
            }
        }
        time_slots.update(time_slot)
    return time_slots


def get_masters(call):
    procedure = Procedure.objects.get(pk=call)
    masters_db = procedure.masters.all()
    masters = {}
    code_masters = []
    for master_db in masters_db:
        master = {f'{master_id + master_db.id}':
           {
                'name': master_db.name,
           }
        }
        masters.update(master)
        code_masters.append(f'{master_id + master_db.id}')
    return masters, code_masters


def get_calls(var, func):
    calls = {}
    for id in var:
        calls.update({f'{id}': func})
    return calls


def get_data_procedures():
    procedures = get_procedures()
    code_service = []
    service_buttons = {}
    text = []
    for procedure_id in procedures:
        code_service.append(procedure_id)
        service_buttons.update({f'{procedures[f"{procedure_id}"]["name"]}': {'callback_data': f'{procedure_id}'}})
        text.append(f'{procedures[f"{procedure_id}"]["name"]} - {procedures[f"{procedure_id}"]["cost"]} руб.')
    service_buttons.update({'Отмена': {'callback_data': 'cancel_step'}})
    service_text = '\n'.join(text)
    return code_service, service_buttons, service_text


def get_time(procedure_id, date, master_id=None):
    if not master_id:
        procedure = Procedure.objects.get(pk=procedure_id)
        return procedure.get_empty_slots(date)
    else:
        master = Master.objects.get(pk=master_id)
        return master.get_empty_slots(date)


def add_new_user(tg_name, name, phone):
    client = Client.objects.filter(tg_username=tg_name)
    if not client:
        Client.objects.create(tg_username=tg_name, name=name, phone_number=phone)
    else:
        client.update(name=name, phone_number=phone)


def add_appointment(procedure_id, tg_name, date_object, time_slot, master=None):
    client = Client.objects.get(tg_username=tg_name)
    procedure = Procedure.objects.get(pk=procedure_id)
    time_slot = Time.objects.get(time_slot=time_slot)
    if master:
        master_obj = Master.objects.get(name=master)
        Appointment.add_with_master(master_obj, procedure, client, date_object, time_slot)
    else:
        Appointment.add_with_procedure(procedure, client, date_object, time_slot)


def add_comment(tg_name, text):
    client = Client.objects.get(tg_username=tg_name)
    Review.add_comment(client, text)
