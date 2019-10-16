# Generated by Django 2.2.5 on 2019-10-14 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_object_obj_in_service'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='managecomp',
            options={'verbose_name': 'Владелец', 'verbose_name_plural': 'Владельцы'},
        ),
        migrations.AlterModelOptions(
            name='objarea',
            options={'verbose_name': 'Район', 'verbose_name_plural': 'Районы'},
        ),
        migrations.AlterModelOptions(
            name='object',
            options={'verbose_name': 'Лифт', 'verbose_name_plural': 'Лифты'},
        ),
        migrations.AlterModelOptions(
            name='objmanufacturer',
            options={'verbose_name': 'Лифт', 'verbose_name_plural': 'Лифты'},
        ),
        migrations.AlterModelOptions(
            name='objstr',
            options={'verbose_name': 'Улица', 'verbose_name_plural': 'Улицы'},
        ),
        migrations.AlterModelOptions(
            name='objtype',
            options={'verbose_name': 'Тип лифта', 'verbose_name_plural': 'Типы лифтов'},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.AlterModelOptions(
            name='ticketstatus',
            options={'verbose_name': 'Статус заявки', 'verbose_name_plural': 'Статусы заявок'},
        ),
        migrations.AlterModelOptions(
            name='tickettype',
            options={'verbose_name': 'Лифт', 'verbose_name_plural': 'Лифты'},
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]