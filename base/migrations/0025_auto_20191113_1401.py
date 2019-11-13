# Generated by Django 2.2.5 on 2019-11-13 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_auto_20191113_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='base.Worker', verbose_name='Работник'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='worker_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.ObjArea', verbose_name='Район работы'),
        ),
    ]
