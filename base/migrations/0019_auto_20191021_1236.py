# Generated by Django 2.2.5 on 2019-10-21 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_auto_20191021_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_par',
            field=models.IntegerField(null=True, verbose_name='Парадная'),
        ),
    ]
