from django.db import models

# Create your models here.

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
    ticket_state = models.CharField(max_length=15)
    ticket_duration = models.DurationField()
    def __str__(self):
        return '%s %s' % (self.ticket_date, self.ticket_state)

class Comments(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    comment_date =  models.DateTimeField('date published')
    comment_content = models.CharField(max_length=500)
    def __str__(self):
        return '%s %s' % (self.comment_date, self.comment_content)
