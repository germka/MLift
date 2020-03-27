import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class TicketStatus(models.Model):
    status = models.CharField(max_length=50)
    def __str__(self):
        return '%s' % (self.status)
    class Meta:
        verbose_name = "Статус заявки"
        verbose_name_plural = "Статусы заявок"


class TicketType(models.Model):
    type_name = models.CharField(max_length=50)
    def __str__(self):
        return 'Тип заявки: %s' % (self.type_name)
    class Meta:
        verbose_name = "Тип заявки"
        verbose_name_plural = "07. Типы заявок"


class ManageComp(models.Model):
    comp_name = models.CharField('Обслуживающая компания', max_length=100)
    def __str__(self):
        return '%s' % (self.comp_name)
    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "02. Владельцы"


class ObjArea(models.Model):
    area_name = models.CharField('Район', max_length=50)
    def __str__(self):
        return '%s' % (self.area_name)
    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "02. Районы"

class ObjStr(models.Model):
    street = models.CharField('Улица', max_length=50)
    area = models.ForeignKey(ObjArea, on_delete=models.CASCADE, null=True, verbose_name='Район')
    def __str__(self):
        return '%s' % (self.street)
    class Meta:
        verbose_name = "Улица"
        verbose_name_plural = "02. Улицы"


class ObjType(models.Model):
    type_name = models.CharField('Тип лифта', max_length=20)
    def __str__(self):
        return '%s' % (self.type_name)
    class Meta:
        verbose_name = "Тип лифта"
        verbose_name_plural = "02. Типы лифтов"


class ObjManufacturer(models.Model):
    manufacturer = models.CharField('Завод производитель', max_length=50)
    def __str__(self):
        return '%s' % (self.manufacturer)
    class Meta:
        verbose_name = "Завод производитель"
        verbose_name_plural = "02. Заводы производители"


class ObjParField(models.IntegerField):
    def to_python(self, value, alter):
        if value is None:
            return value
        try:
            if alter:
                return chr(value+1039)
            else:
                return int(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )


class Object(models.Model):
    obj_area = models.ForeignKey(ObjArea, on_delete=models.DO_NOTHING, null=True, verbose_name='Район')
    obj_str = models.ForeignKey(ObjStr, on_delete=models.DO_NOTHING, verbose_name='Улица')
    obj_build = models.CharField('Дом', max_length=15, null=True)
    obj_build_housing = models.CharField('Корпус', max_length=10, null=True, blank=True)
    obj_par_alter = models.BooleanField('Литеральный номер парадной', default=False)
    obj_par = ObjParField('Номер парадной', null=True, blank=True)
    obj_number = models.CharField('Номер лифта', max_length=15, null=True, blank=True)
    obj_factory_number = models.CharField('Заводской номер', max_length=15, null=True, blank=True)
    obj_type = models.ForeignKey(ObjType, on_delete=models.DO_NOTHING, null=True, verbose_name='Тип лифта', blank=True)
    obj_carrying = models.IntegerField('Грузоподъемность', null=True, blank=True)
    obj_aperture = models.IntegerField('Этажность', null=True, blank=True)
    obj_manufacturer = models.ForeignKey(ObjManufacturer, on_delete=models.DO_NOTHING, null=True, verbose_name='Завод производитель', blank=True)
    manage_comp = models.ForeignKey(ManageComp, on_delete=models.DO_NOTHING, null=True, verbose_name='Управляющая компания', blank=True)
    obj_communication = models.BooleanField('Наличие связи', null=True)
    obj_manufacture = models.DateTimeField('Дата производства', null=True, blank=True)
    obj_exp_start = models.DateTimeField('Дата начала эксплуатации', null=True, blank=True)
    obj_inspection = models.DateTimeField('Дата последней инспекции', null=True, blank=True)
    obj_in_service = models.BooleanField('Обслуживание')
    def __str__(self):
        return '№ %s улица %s дом %s' % (self.obj_number, self.obj_str, self.obj_build)
    class Meta:
        verbose_name = "Лифт"
        verbose_name_plural = "01. Лифты"


class Worker(models.Model):
    last_name = models.CharField('Фамилия', max_length=15)
    first_name = models.CharField('Имя', max_length=15)
    optional_name = models.CharField('Отчество', max_length=15, null=True, blank=True)
    worker_area = models.ForeignKey(ObjArea, on_delete=models.DO_NOTHING, verbose_name='Район работы')
    worker_recruitment = models.DateField('Дата приема на работу', null=True, blank=True)
    phone_work = models.CharField('Рабочий телефон', max_length=11, null=True, blank=True)
    phone_alt = models.CharField('Дополнительный телефон', max_length=11, null=True, blank=True)
    def __str__(self):
        return '%s %s %s' % (self.last_name, self.first_name, self.optional_name)
    @property
    def full_name(self):
        return '%s %s' % (self.last_name, self.first_name)
    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "08. Работники"


class Ticket(models.Model):
    ticket_date = models.DateTimeField('Дата публикации')
    ticket_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Автор')
    ticket_object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Объект заявки', null=True)
    ticket_str = models.ForeignKey(ObjStr, on_delete=models.DO_NOTHING, verbose_name='Улица')
    ticket_build = models.CharField('Дом', max_length=15, default='-')
    ticket_build_housing = models.CharField('Корпус', max_length=10, null=True)
    ticket_par = models.IntegerField('Парадная',null=True)
    ticket_obj_type = models.ForeignKey(ObjType, on_delete=models.DO_NOTHING, verbose_name='Тип лифта', null=True)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.DO_NOTHING, verbose_name='Тип заявки', null=True)
    ticket_content = models.CharField('Содержание' ,max_length=1000)
    ticket_status = models.ForeignKey(TicketStatus, on_delete=models.DO_NOTHING, default=1, verbose_name='Статус')
    ticket_duration = models.DurationField('Время простоя', null=True)
    ticket_worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING, verbose_name='Работник', blank=True, null=True)
    ticket_sender = models.CharField('Заявитель', max_length=50, null=True, blank=True)
    def close(self):
        self.ticket_status_id = 2
        self.save()

    def duration_save(self):
        if self.ticket_status_id == 2:
            self.ticket_duration = (timezone.now().astimezone() - self.ticket_date)
            self.save()

    def duration_get(self):
        ticket_duration=timezone.now().astimezone() - self.ticket_date
        if ticket_duration.days > 7:
            return str(ticket_duration).split(".")[0].replace("days", "Дней").replace("day", "День")

    @property
    def duration_time(self):
        return str(self.ticket_duration).split(".")[0].replace("days", "Дней").replace("day", "День")

    @property
    def close_time(self):
        if self.ticket_duration:
            closed = self.ticket_date + self.ticket_duration
            return closed
    @property
    def ticket_date_tz(self):
        return self.ticket_date.astimezone()

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
        verbose_name_plural = "07. Заявки"


class Comments(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='Номер заявки')
    comment_date =  models.DateTimeField('Дата публикации')
    comment_content = models.CharField('Содержание', max_length=500)
    comment_user = models.CharField('Пользователь', max_length=50, null=True)
    def __str__(self):
        return '%s %s' % (self.comment_date.strftime("%Y/%m/%d %H:%M"), self.comment_content)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "07. Комментарии"


class FUR_group(models.Model):
    group_name = models.CharField('Название группы', max_length=50)
    def __str__(self):
        return '%s' % (self.group_name)
    class Meta:
        verbose_name = "Группа причин заявок"
        verbose_name_plural = "09. Группы причин заявок"


class FUReason(models.Model):
    reason_group = models.ForeignKey(FUR_group, on_delete=models.CASCADE, verbose_name='Группа списка причин')
    reason_text = models.TextField('Содержание', max_length=2000)
    def __str__(self):
        return '%s' % (self.reason_text)
    class Meta:
        verbose_name = "Часто используемая причина"
        verbose_name_plural = "09. Часто используемые причины"
