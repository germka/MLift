# Generated by Django 2.2.5 on 2019-12-04 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_auto_20191203_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='optional_name',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Отчество'),
        ),
    ]
