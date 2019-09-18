import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class TicketStatus(models.Model):
    status = models.CharField(max_length=50)


class TicketType(models.Model):
    type_name = models.CharField(max_length=50)


class ManageComp(models.Model):
    comp_name = models.CharField(max_length=50)


class Object(models.Model):
    obj_str = models.CharField(max_length=50)
    obj_buid = models.IntegerField()
    obj_par = models.IntegerField()
    obj_number = models.IntegerField()
    manage_comp = models.ForeignKey(ManageComp, on_delete=models.CASCADE)
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

    def duration_save (self):
        if self.ticket_status == TicketStatus.objects.get(pk=3):
            Ticket.objects.filter(pk=self.id).update(ticket_duration=timezone.now() - self.ticket_date)
            return 'duration saved'

    def duration_get (self):
        ticket_duration=timezone.now() - self.ticket_date
        return ticket_duration

    def __str__(self):
        return '%s %s' % (self.ticket_date, self.ticket_status)


class Comments(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    comment_date =  models.DateTimeField('date published')
    comment_content = models.CharField(max_length=500)
    def __str__(self):
        return '%s %s' % (self.comment_date, self.comment_content)
