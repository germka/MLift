from django.contrib import admin

from .models import Comments, Ticket, Object, ManageComp

# Register your models here.

admin.site.register(Comments)
admin.site.register(Ticket)
admin.site.register(Object)
admin.site.register(ManageComp)
