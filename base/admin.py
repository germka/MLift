from django.contrib import admin

from .models import Comments, Ticket, Object, ManageComp, ObjStr, ObjType

# Register your models here.

admin.site.register(Comments)
admin.site.register(Ticket)
admin.site.register(Object)
admin.site.register(ManageComp)
admin.site.register(ObjStr)
admin.site.register(ObjType)
