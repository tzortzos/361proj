# Generated by Django 3.2 on 2021-04-29 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TAScheduler', '0007_alter_coursesection_ta_ids'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_labs', models.IntegerField(verbose_name='Maximum number of labs that this TA can be assigned')),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Lab Section ID')),
                ('code', models.CharField(max_length=3, verbose_name='Lab Section Code')),
                ('day', models.CharField(blank=True, max_length=1, verbose_name='Lab Day(s)')),
                ('time', models.CharField(blank=True, max_length=12, verbose_name='Lab Time')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Course Section ID')),
                ('code', models.CharField(max_length=3, verbose_name='Course Section Code')),
                ('days', models.CharField(blank=True, max_length=6, verbose_name='Lecture Day(s)')),
                ('time', models.TextField(blank=True, max_length=12, verbose_name='Lecture Time')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='labsection',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='labsection',
            name='course_section_id',
        ),
        migrations.RemoveField(
            model_name='labsection',
            name='ta_id',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='course_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='course_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='course_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='tmp_password',
            new_name='password_tmp',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='univ_id',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='course',
            name='admin_id',
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, default='', max_length=500, verbose_name='Extra skills and information'),
        ),
        migrations.DeleteModel(
            name='CourseSection',
        ),
        migrations.DeleteModel(
            name='LabSection',
        ),
        migrations.AddField(
            model_name='section',
            name='course',
            field=models.ForeignKey(help_text='Course ID', on_delete=django.db.models.deletion.CASCADE, to='TAScheduler.course'),
        ),
        migrations.AddField(
            model_name='section',
            name='prof',
            field=models.ForeignKey(blank=True, help_text='Instructor ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='TAScheduler.user'),
        ),
        migrations.AddField(
            model_name='section',
            name='tas',
            field=models.ManyToManyField(blank=True, help_text="Ta's Assigned to this Course Section", related_name='section_assign', through='TAScheduler.Assignment', to='TAScheduler.User'),
        ),
        migrations.AddField(
            model_name='lab',
            name='section',
            field=models.ForeignKey(help_text='Course Section ID', on_delete=django.db.models.deletion.CASCADE, to='TAScheduler.section'),
        ),
        migrations.AddField(
            model_name='lab',
            name='ta',
            field=models.ForeignKey(blank=True, help_text='TA ID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='TAScheduler.user'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TAScheduler.section'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='ta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TAScheduler.user'),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together={('code', 'course')},
        ),
        migrations.AlterUniqueTogether(
            name='lab',
            unique_together={('code', 'section')},
        ),
    ]
