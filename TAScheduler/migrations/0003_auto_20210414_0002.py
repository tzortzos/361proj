# Generated by Django 3.2 on 2021-04-14 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TAScheduler', '0002_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='id',
            new_name='user_id',
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('A', 'Administrator'), ('P', 'Professor'), ('T', 'TA')], max_length=1, verbose_name='User Type'),
        ),
    ]
