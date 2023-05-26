import os, sys
from datetime import datetime, timedelta
import django
DJANGO_PROJECT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.append(DJANGO_PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beauty_city_bot.settings")
django.setup()

from django.template.loader import render_to_string
from django.db.models import Count, Q

from salon.models import Master, Procedure, Appointment, Time, Client, MasterProcedure

# клиент  выбрал мастера
master_id = 1
# по его id получаем объект мастера
master = Master.objects.get(pk=master_id)

# задаем дату
date_string = '2023-05-26'
# конвертируем в datetime объект
date_object = datetime.strptime(date_string, '%Y-%m-%d').date()

# получаем свободные слоты для этого мастера
time_slots = master.get_empty_slots(date_object)

# Свободные слоты:
for slot in time_slots:
    print(slot.time_slot)