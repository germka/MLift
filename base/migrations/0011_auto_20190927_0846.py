# Generated by Django 2.2.5 on 2019-09-27 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20190924_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_content',
            field=models.CharField(max_length=500, verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_date',
            field=models.DateTimeField(verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_user',
            field=models.CharField(max_length=50, null=True, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Ticket', verbose_name='Номер заявки'),
        ),
        migrations.AlterField(
            model_name='managecomp',
            name='comp_name',
            field=models.CharField(max_length=100, verbose_name='Обслуживающая компания'),
        ),
        migrations.AlterField(
            model_name='objarea',
            name='area_name',
            field=models.CharField(max_length=50, verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='object',
            name='manage_comp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ManageComp', verbose_name='Управляющая компания'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_aperture',
            field=models.IntegerField(null=True, verbose_name='Пролет'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ObjArea', verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_build',
            field=models.CharField(max_length=15, null=True, verbose_name='Строение'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_build_housing',
            field=models.IntegerField(null=True, verbose_name='Корпус'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_carrying',
            field=models.IntegerField(null=True, verbose_name='Грузоподъемность'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_communication',
            field=models.BooleanField(null=True, verbose_name='Наличие связи'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_exp_start',
            field=models.DateTimeField(null=True, verbose_name='Дата начала эксплуатации'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_factory_number',
            field=models.CharField(max_length=15, null=True, verbose_name='Заводской номер'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_inspection',
            field=models.DateTimeField(null=True, verbose_name='Дата последней инспекции'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_manufacture',
            field=models.DateTimeField(null=True, verbose_name='Дата производства'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ObjManufacturer', verbose_name='Завод производитель'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_number',
            field=models.CharField(max_length=15, null=True, verbose_name='Номер объекта'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_par',
            field=models.IntegerField(null=True, verbose_name='Номер парадной'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_str',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ObjStr', verbose_name='Улица'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ObjType', verbose_name='Тип объекта'),
        ),
        migrations.AlterField(
            model_name='objmanufacturer',
            name='manufacturer',
            field=models.CharField(max_length=50, verbose_name='Завод производитель'),
        ),
        migrations.AlterField(
            model_name='objstr',
            name='street',
            field=models.CharField(max_length=50, verbose_name='Улица'),
        ),
        migrations.AlterField(
            model_name='objtype',
            name='type_name',
            field=models.CharField(max_length=20, verbose_name='Тип лифта'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_content',
            field=models.CharField(max_length=1000, verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_date',
            field=models.DateTimeField(verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_duration',
            field=models.DurationField(verbose_name='Время простоя'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Object', verbose_name='Объект заявки'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.TicketStatus', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.TicketType', verbose_name='Тип заявки'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_user',
            field=models.IntegerField(verbose_name='Автор'),
        ),
    ]
