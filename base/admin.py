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
            ('ticket_status',
            'ticket_type'),
            'ticket_object',
            ]}),
        ('Дата и Длительность', {'fields':
            [
            ('ticket_date',
            'ticket_duration'),
            ]}),
        ('Содержание', {'fields':
            [
            'ticket_content',
            ]}),
    ]
    inlines = [CommentsInLine]

admin.site.register(Ticket,TicketAdmin)

#admin.site.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('id','obj_number','obj_str', 'obj_build')
    list_filter = ['obj_area','obj_str','obj_build']
    search_fields = ['obj_number','obj_area','obj_str', 'obj_build']
    fieldsets = [
        ('Адрес', {'fields':
            [
            'obj_area',
            'obj_str',
            ('obj_build',
            'obj_build_housing',
            'obj_par'),
            'manage_comp',
            ]}),
        ('Характеристики', {'fields':
            [
            'obj_number',
            'obj_factory_number',
            ('obj_type',
            'obj_carrying',
            'obj_aperture'),
            'obj_manufacturer',
            'obj_communication',
            ]}),
        ('Даты', {'fields':
            [
            ('obj_manufacture',
            'obj_exp_start',
            'obj_inspection'),
            ]}),
    ]

admin.site.register(Object,ObjectAdmin)

admin.site.register(ManageComp)
admin.site.register(ObjStr)
admin.site.register(ObjType)
