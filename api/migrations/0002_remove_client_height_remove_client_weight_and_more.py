# Generated by Django 5.1.3 on 2024-12-02 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='height',
        ),
        migrations.RemoveField(
            model_name='client',
            name='weight',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('client', 'client'), ('coach', 'coach')], max_length=10),
        ),
    ]
