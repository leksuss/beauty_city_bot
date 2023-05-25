from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Master, Procedure, Appointment, Time, Client

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Master)
admin.site.register(Procedure)
admin.site.register(Appointment)
admin.site.register(Time)
admin.site.register(Client)