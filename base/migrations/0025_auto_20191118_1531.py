# Generated by Django 2.2.5 on 2019-11-18 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_auto_20191113_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='obj_in_service',
            field=models.BooleanField(verbose_name='Обслуживание'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='base.ObjType', verbose_name='Тип лифта'),
        ),
    ]