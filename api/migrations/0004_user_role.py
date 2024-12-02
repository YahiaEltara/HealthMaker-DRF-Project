# Generated by Django 5.1.3 on 2024-12-02 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('client', 'client'), ('coach', 'coach')], default='admin', max_length=10),
            preserve_default=False,
        ),
    ]
