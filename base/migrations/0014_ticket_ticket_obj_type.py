# Generated by Django 2.2.5 on 2019-10-07 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20190927_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticket_obj_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ObjType', verbose_name='Тип лифта'),
        ),
    ]