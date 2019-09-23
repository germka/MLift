import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class TicketStatus(models.Model):
    status = models.CharField(max_length=50)
    def __str__(self):
        return 'Заявка %s' % (self.status)


class TicketType(models.Model):
    type_name = models.CharField(max_length=50)
    def __str__(self):
        return 'Тип заявки: %s' % (self.type_name)


class ManageComp(models.Model):
    comp_name = models.CharField(max_length=50)
    def __str__(self):
        return 'УК %s' % (self.comp_name)

class ObjStr(models.Model):
    street = models.CharField(max_length=50)
    def __str__(self):
        return 'ул. %s' % (self.street)

class ObjType(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__(self):
        return 'тип лифта: %s' % (self.type_name)

class Object(models.Model):
    obj_str = models.ForeignKey(ObjStr, on_delete=models.CASCADE)
    obj_build = models.IntegerField(null=True)
    obj_par = models.IntegerField()
    obj_number = models.IntegerField()
    obj_type = models.ForeignKey(ObjType, on_delete=models.CASCADE, null=True)
    manage_comp = models.ForeignKey(ManageComp, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return '№ %s улица %s дом %s' % (self.obj_number, self.obj_str, self.obj_build)


class Ticket(models.Model):
    ticket_date = models.DateTimeField('date published')
    ticket_user = models.IntegerField()
    ticket_object = models.ForeignKey(Object, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    ticket_content = models.CharField(max_length=1000)
    ticket_status = models.ForeignKey(TicketStatus, on_delete=models.CASCADE, default=1)
    ticket_duration = models.DurationField()
    def close(self):
        Ticket.objects.filter(pk=self.id).update(ticket_status=TicketStatus.objects.get(pk=3))
        return 'ticket closed'

    def duration_save(self):
        if self.ticket_status == TicketStatus.objects.get(pk=3):
            Ticket.objects.filter(pk=self.id).update(ticket_duration=timezone.now() - self.ticket_date)
            return 'duration saved'

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


class Comments(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    comment_date =  models.DateTimeField('date published')
    comment_content = models.CharField(max_length=500)
    comment_user = models.CharField(max_length=50, null=True)
    def __str__(self):
        return '%s %s' % (self.comment_date.strftime("%Y/%m/%d %H:%M"), self.comment_content)
