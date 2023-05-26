from django.db import models


class Procedure(models.Model):
    name = models.CharField(
        'Название процедуры',
        max_length=100,
    )
    cost = models.IntegerField('Цена')

    def get_empty_slots(self, date_obj):
        empty_slots = set()
        for master in self.masters.all():
            empty_slots.update(master.get_empty_slots(date_obj))
        return empty_slots

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'процедура'
        verbose_name_plural = 'Процедуры'

class Master(models.Model):
    name = models.CharField(
        'Имя мастера',
        max_length=100,
    )

    procedures = models.ManyToManyField(
        Procedure,
        related_name='masters',
        through='MasterProcedure'
    )

    def get_empty_slots(self, date_obj):
        appointments = Appointment.objects.filter(
            masterprocedure__master=self, date=date_obj
        ).values_list('time_slot')

        empty_slots = Time.objects.exclude(id__in=appointments)
        return empty_slots

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'мастер'
        verbose_name_plural = 'Мастера'


class MasterProcedure(models.Model):
    master = models.ForeignKey(
        Master,
        verbose_name='Мастер',
        on_delete=models.CASCADE,
    )
    procedure = models.ForeignKey(
        Procedure,
        verbose_name='Процедура',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.master}, {self.procedure}'

    class Meta:
        verbose_name = 'процедуры мастера'
        verbose_name_plural = 'процедуры мастеров'


class Client(models.Model):
    name = models.CharField(
        'Имя клиента',
        max_length=100,
    )
    phone_number = models.CharField(
        'Телефон',
        max_length=20
    )
    tg_username = models.CharField(
        'Ник в телеграм',
        max_length=30
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'


class Time(models.Model):
    time_slot = models.CharField(
        'Временной слот',
        max_length=20,
    )

    def __str__(self):
        return self.time_slot

    class Meta:
        verbose_name = 'слот'
        verbose_name_plural = 'Временные слоты'


class Appointment(models.Model):
    client = models.ForeignKey(
        Client,
        verbose_name='Клиент',
        related_name='appointments',
        on_delete=models.CASCADE,
    )
    masterprocedure = models.ForeignKey(
        MasterProcedure,
        verbose_name='Мастер с процедурой',
        related_name='appointments',
        on_delete=models.CASCADE,
    )
    date = models.DateField('Дата записи')
    time_slot = models.ForeignKey(
        Time,
        verbose_name='Время записи',
        related_name='appointments',
        on_delete=models.CASCADE,
    )

    @classmethod
    def add_with_master(cls, master, procedure, client, date_obj, time_slot):
        masterprocedure = MasterProcedure.objects.filter(
            master=master,
            procedure=procedure,
        ).first()

        appointment = cls(
            client=client,
            masterprocedure=masterprocedure,
            date=date_obj,
            time_slot=time_slot,
        )
        appointment.save()
        return appointment

    @classmethod
    def add_with_procedure(cls, procedure, client, date_obj, time_slot):
        master_procedures = MasterProcedure.objects.filter(
            procedure=procedure,
        )
        # get first master with suitable empty slot
        master_procedure = None
        for master_procedure in master_procedures:
            if time_slot in master_procedure.master.get_empty_slots(date_obj):
                break

        appointment = cls(
            client=client,
            masterprocedure=master_procedure,
            date=date_obj,
            time_slot=time_slot,
        )
        appointment.save()
        return appointment

    def __str__(self):
        return f'Мастер {self.masterprocedure} на {self.date}, ' \
               f'время {self.time_slot}'

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'Записи на процедуры'
