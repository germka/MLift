# Generated by Django 2.2.5 on 2019-11-18 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_auto_20191118_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='obj_factory_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Заводской номер'),
        ),
    ]
