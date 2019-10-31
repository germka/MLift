from django.contrib import admin

from .models import Comments, Ticket, Object, ManageComp, ObjStr, ObjType, ObjManufacturer, FUReason, FUR_group

# Register your models here.


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
            ('ticket_str',
            'ticket_build',
            'ticket_build_housing',
            'ticket_par'),
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


class ObjectAdmin(admin.ModelAdmin):
    list_display = ('id','obj_number','obj_str','obj_build','obj_build_housing','obj_par','obj_in_service',)
    list_filter = ['obj_area','obj_type','obj_str','obj_build','obj_in_service',]
    search_fields = [
                'obj_number',
                'obj_area__area_name',
                'obj_str__street',
                'obj_build',
                'obj_build_housing',
    ]
    fieldsets = [
        ('Адрес', {'fields':
            [
            'obj_area',
            'obj_str',
            ('obj_build',
            'obj_build_housing',
            'obj_par'),
            ('manage_comp',
            'obj_in_service'),
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


class FUReasonAdmin(admin.ModelAdmin):
    list_display = ('reason_group','reason_text',)
    list_filter = ['reason_group',]
    search_fields = [
        'reason_group__group_name',
        'reason_text',
    ]
    fieldsets = [
    ('Группа', { 'fields':
        [
        'reason_group',
        ]
    }),
    ('Содержание', { 'fields':
        [
        'reason_text',
        ]
    }),
    ]


class FUReasonInLine(admin.TabularInline):
    model = FUReason
    extra = 0


class FUR_groupAdmin(admin.ModelAdmin):
    inlines = [FUReasonInLine]


admin.site.register(Comments)
admin.site.register(Object, ObjectAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(ManageComp)
admin.site.register(ObjStr)
admin.site.register(ObjType)
admin.site.register(ObjManufacturer)
admin.site.register(FUReason, FUReasonAdmin)
admin.site.register(FUR_group, FUR_groupAdmin)