import os, sys
from datetime import datetime, timedelta
import django
DJANGO_PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(DJANGO_PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauty_city_bot.settings")
django.setup()


from salon.models import Master, Procedure, Appointment, Time, Client, MasterProcedure

####
# Список процедур
procedures = Procedure.objects.all()
####

####
# Список мастеров
masters = Master.objects.all()
####

####
# Список свободных слотов для мастера на конкретный день
####
# клиент выбрал мастера
master_id = 1
master = Master.objects.get(pk=master_id)
# клиент выбрал дату
date_string = '2023-05-26'
# конвертируем в datetime объект
date_object = datetime.strptime(date_string, '%Y-%m-%d').date()
empty_slots_for_master = master.get_empty_slots(date_object)


####
# Список свободных слотов для процедуры на конкретный день
####
# клиент выбрал мастера
procedure_id = 1
procedure = Procedure.objects.get(pk=procedure_id)
# клиент выбрал дату
date_string = '2023-05-26'
# конвертируем в datetime объект
date_object = datetime.strptime(date_string, '%Y-%m-%d').date()
empty_slots_for_procedure = procedure.get_empty_slots(date_object)


####
# Записываемся к мастеру
####
# получаем юзернейм в телеге
username = 'imleksus'
client = Client.objects.get(tg_username=username)
# клиент выбрал процедуру
procedure_id = 2
# по его id получаем объект процедуры
procedure = Procedure.objects.get(pk=procedure_id)
# клиент  выбрал мастера
master_id = 1
# по его id получаем объект мастера
master = Master.objects.get(pk=master_id)
# клиент выбрал дату
date_string = '2023-05-26'
# конвертируем в datetime объект
date_object = datetime.strptime(date_string, '%Y-%m-%d').date()
# клиент выбрал id слота
time_slot_id = 2
time_slot = Time.objects.get(pk=time_slot_id)
# добавляем запись на определенную процедуру к определенному мастеру
appointment_with_master = Appointment.add_with_master(master, procedure, client, date_object, time_slot)


####
# Записываемся на процедуру
####
# получаем юзернейм в телеге
username = 'imleksus'
client = Client.objects.get(tg_username=username)
# клиент выбрал процедуру
procedure_id = 2
# по его id получаем объект процедуры
procedure = Procedure.objects.get(pk=procedure_id)
# клиент выбрал дату
date_string = '2023-05-26'
# конвертируем в datetime объект
date_object = datetime.strptime(date_string, '%Y-%m-%d').date()
# клиент выбрал id слота
time_slot_id = 2
time_slot = Time.objects.get(pk=time_slot_id)
# добавляем запись на определенную процедуру к любому свободному мастеру
# при этом у нас не может быть, что на это время нет свободных мастеров,
# т.к. мы до этого выбрали свободный слот, где точно есть запись.
appointment_with_procedure = Appointment.add_with_procedure(procedure, client, date_object, time_slot)
