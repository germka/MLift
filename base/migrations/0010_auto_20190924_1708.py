# Generated by Django 2.2.5 on 2019-09-24 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20190924_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='objarea',
            name='area_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ObjManufacturer'),
        ),
    ]
