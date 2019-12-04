# Generated by Django 2.2.6 on 2019-11-13 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_auto_20191031_1431'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objarea',
            options={'verbose_name': 'Район', 'verbose_name_plural': '02. Районы'},
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=15, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=15, verbose_name='Фамилия')),
                ('optional_name', models.CharField(max_length=15, verbose_name='Отчество')),
                ('worker_recruitment', models.DateTimeField(blank=True, null=True, verbose_name='Дата приема на работу')),
                ('phone_work', models.CharField(blank=True, max_length=11, null=True, verbose_name='Рабочий телефон')),
                ('phone_alt', models.CharField(blank=True, max_length=11, null=True, verbose_name='Дополнительный телефон')),
                ('worker_area', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='base.ObjArea', verbose_name='Район работы')),
            ],
            options={
                'verbose_name': 'Работник',
                'verbose_name_plural': '08. Работники',
            },
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='base.Worker', verbose_name='Работник'),
        ),
    ]