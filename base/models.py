import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class TicketStatus(models.Model):
    status = models.CharField(max_length=50)
    def __str__(self):
        return 'Заявка %sа' % (self.status)
    class Meta:
        verbose_name = "Статус заявки"
        verbose_name_plural = "Статусы заявок"


class TicketType(models.Model):
    type_name = models.CharField(max_length=50)
    def __str__(self):
        return 'Тип заявки: %s' % (self.type_name)
    class Meta:
        verbose_name = "Лифт"
        verbose_name_plural = "Лифты"


class ManageComp(models.Model):
    comp_name = models.CharField('Обслуживающая компания', max_length=100)
    def __str__(self):
        return '%s' % (self.comp_name)
    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"


class ObjArea(models.Model):
    area_name = models.CharField('Район', max_length=50)
    def __str__(self):
        return '%s' % (self.area_name)
    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"

class ObjStr(models.Model):
    street = models.CharField('Улица', max_length=50)
    def __str__(self):
        return '%s' % (self.street)
    class Meta:
        verbose_name = "Улица"
        verbose_name_plural = "Улицы"


class ObjType(models.Model):
    type_name = models.CharField('Тип лифта', max_length=20)
    def __str__(self):
        return '%s' % (self.type_name)
    class Meta:
        verbose_name = "Тип лифта"
        verbose_name_plural = "Типы лифтов"


class ObjManufacturer(models.Model):
    manufacturer = models.CharField('Завод производитель', max_length=50)
    def __str__(self):
        return '%s' % (self.manufacturer)
    class Meta:
        verbose_name = "Лифт"
        verbose_name_plural = "Лифты"


class Object(models.Model):
    obj_area = models.ForeignKey(ObjArea, on_delete=models.CASCADE, null=True, verbose_name='Район')
    obj_str = models.ForeignKey(ObjStr, on_delete=models.CASCADE, verbose_name='Улица')
    obj_build = models.CharField('Дом', max_length=15, null=True)
    obj_build_housing = models.CharField('Корпус', max_length=2, null=True)
    obj_par = models.IntegerField('Номер парадной', null=True)
    obj_number = models.CharField('Номер лифта', max_length=15, null=True)
    obj_factory_number = models.CharField('Заводской номер', max_length=15, null=True)
    obj_type = models.ForeignKey(ObjType, on_delete=models.CASCADE, null=True, verbose_name='Тип объекта')
    obj_carrying = models.IntegerField('Грузоподъемность', null=True)
    obj_aperture = models.IntegerField('Пролет', null=True)
    obj_manufacturer = models.ForeignKey(ObjManufacturer, on_delete=models.CASCADE, null=True,verbose_name='Завод производитель')
    manage_comp = models.ForeignKey(ManageComp, on_delete=models.CASCADE, null=True, verbose_name='Управляющая компания')
    obj_communication = models.BooleanField('Наличие связи', null=True)
    obj_manufacture = models.DateTimeField('Дата производства', null=True)
    obj_exp_start = models.DateTimeField('Дата начала эксплуатации', null=True)
    obj_inspection = models.DateTimeField('Дата последней инспекции', null=True)
    obj_in_service = models.BooleanField('Находится на обслуживании')
    def __str__(self):
        return '№ %s улица %s дом %s' % (self.obj_number, self.obj_str, self.obj_build)
    class Meta:
        verbose_name = "Лифт"
        verbose_name_plural = "Лифты"

class Ticket(models.Model):
    ticket_date = models.DateTimeField('Дата публикации')
    ticket_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    ticket_object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Объект заявки', null=True)
    ticket_str = models.ForeignKey(ObjStr, on_delete=models.CASCADE, verbose_name='Улица')
    ticket_build = models.CharField('Дом', max_length=15, default='-')
    ticket_build_housing = models.CharField('Корпус', max_length=2, null=True)
    ticket_par = models.IntegerField('Парадная')
    ticket_obj_type = models.ForeignKey(ObjType, on_delete=models.CASCADE, verbose_name='Тип лифта', null=True)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, verbose_name='Тип заявки', null=True)
    ticket_content = models.CharField('Содержание' ,max_length=1000)
    ticket_status = models.ForeignKey(TicketStatus, on_delete=models.CASCADE, default=1, verbose_name='Статус')
    ticket_duration = models.DurationField('Время простоя', null=True)
    def close(self):
        Ticket.objects.filter(pk=self.id).update(ticket_status=TicketStatus.objects.get(pk=2))

    def duration_save(self):
        if self.ticket_status == TicketStatus.objects.get(pk=2):
            Ticket.objects.filter(pk=self.id).update(ticket_duration=timezone.now() - self.ticket_date)

    def duration_get(self):
        ticket_duration=timezone.now() - self.ticket_date
        return ticket_duration

    def status(self):
        status = TicketStatus.objects.get(pk=self.ticket_status.id)
        return status

    status.admin_order_field = 'ticket_status'
    status.boolean = False
    status.short_description = 'Статус заявки'

    def __str__(self):
        return 'Открыта: %s, статус: %s' % (self.ticket_date.strftime("%Y/%m/%d %H:%M"), self.ticket_status)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class Comments(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Номер заявки')
    comment_date =  models.DateTimeField('Дата публикации')
    comment_content = models.CharField('Содержание', max_length=500)
    comment_user = models.CharField('Пользователь', max_length=50, null=True)
    def __str__(self):
        return '%s %s' % (self.comment_date.strftime("%Y/%m/%d %H:%M"), self.comment_content)


    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"