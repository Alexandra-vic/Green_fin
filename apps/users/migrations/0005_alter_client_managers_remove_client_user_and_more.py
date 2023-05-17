# Generated by Django 4.2.1 on 2023-05-17 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_username'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='client',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='client',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='company_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=100),
        ),
    ]
