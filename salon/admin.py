from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Master, Procedure, Appointment, Time, Client, MasterProcedure

admin.site.unregister(User)
admin.site.unregister(Group)

class MasterProcedureInline(admin.TabularInline):
    model = MasterProcedure
    extra = 1

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_procedures')
    inlines = (MasterProcedureInline,)

    @admin.display(description='Процедуры')
    def get_procedures(self, obj):
        return [procedure.name for procedure in obj.procedures.all()]


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_masters')
    inlines = (MasterProcedureInline,)

    @admin.display(description='Мастера')
    def get_masters(self, obj):
        return [master.name for master in obj.masters.all()]


admin.site.register(Appointment)
admin.site.register(Time)
admin.site.register(Client)