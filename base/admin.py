from django.contrib import admin

from .models import Comments, Ticket, Object, ManageComp, ObjStr, ObjType

# Register your models here.

admin.site.register(Comments)
#admin.site.register(Ticket)
class CommentsInLine(admin.TabularInline):
    model = Comments
    extra = 0

class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_date','ticket_content', 'status')
    list_filter = ['ticket_date']
    search_fields = ['ticket_content']
    fieldsets = [
        (None, {'fields':
            [
            'ticket_user',
            'ticket_status',
            'ticket_object',
            'ticket_type',
            ]}),
        ('Дата и Длительность', {'fields':
            [
            'ticket_date',
            'ticket_duration',
            ]}),
        ('Содержание', {'fields':
            [
            'ticket_content',
            ]}),
    ]
    inlines = [CommentsInLine]

admin.site.register(Ticket,TicketAdmin)
admin.site.register(Object)
admin.site.register(ManageComp)
admin.site.register(ObjStr)
admin.site.register(ObjType)
