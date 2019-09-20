# Generated by Django 2.2.5 on 2019-09-20 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_ticket_ticket_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjBuild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ObjStr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ObjType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=15)),
            ],
        ),
        migrations.RemoveField(
            model_name='object',
            name='obj_buid',
        ),
        migrations.AlterField(
            model_name='object',
            name='manage_comp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ManageComp'),
        ),
        migrations.AlterField(
            model_name='object',
            name='obj_str',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ObjStr'),
        ),
        migrations.AddField(
            model_name='object',
            name='obj_build',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ObjBuild'),
        ),
        migrations.AddField(
            model_name='object',
            name='obj_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ObjType'),
        ),
    ]
