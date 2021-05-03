# Generated by Django 3.2 on 2021-05-03 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TAScheduler', '0009_auto_20210429_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='preferred_skills',
            field=models.ManyToManyField(help_text='Preferred Skills', to='TAScheduler.Skill'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Course Name'),
        ),
        migrations.AlterField(
            model_name='section',
            name='time',
            field=models.CharField(blank=True, max_length=12, verbose_name='Lecture Time'),
        ),
    ]
