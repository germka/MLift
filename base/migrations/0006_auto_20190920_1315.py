# Generated by Django 2.2.5 on 2019-09-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20190920_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='obj_build',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='ObjBuild',
        ),
    ]