from django.db import models


class Master(models.Model):
    name = models.CharField(
        'Имя мастера',
        max_length=100,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'мастер'
        verbose_name_plural = 'Мастера'


class Procedure(models.Model):
    name = models.CharField(
        'Название процедуры',
        max_length=100,
    )
    cost = models.IntegerField('Цена')
    master = models.ManyToManyField(
        Master,
        verbose_name='Мастер',
        related_name='procedures',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'процедура'
        verbose_name_plural = 'Процедуры'


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
    procedure = models.ForeignKey(
        Procedure,
        verbose_name='Процедура',
        related_name='appointments',
        on_delete=models.CASCADE,
    )
    master = models.ForeignKey(
        Master,
        verbose_name='Мастер',
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

    def __str__(self):
        return f'{self.procedure}, мастер {self.master} на {self.date} {self.time_slot}'

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'Записи на процедуры'
