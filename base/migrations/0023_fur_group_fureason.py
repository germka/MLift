# Generated by Django 2.2.5 on 2019-10-31 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20191030_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='FUR_group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=50, verbose_name='Название группы')),
            ],
            options={
                'verbose_name': 'Группа причин заявок',
                'verbose_name_plural': 'Группы причин заявок',
            },
        ),
        migrations.CreateModel(
            name='FUReason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_text', models.TextField(max_length=2000, verbose_name='Содержание')),
                ('reason_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.FUR_group', verbose_name='Группа списка причин')),
            ],
            options={
                'verbose_name': 'Часто используемая причина',
                'verbose_name_plural': 'Часто используемые причины',
            },
        ),
    ]
