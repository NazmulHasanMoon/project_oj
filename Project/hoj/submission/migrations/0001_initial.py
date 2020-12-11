# Generated by Django 3.1.4 on 2020-12-09 04:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import submission.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('language', models.CharField(choices=[('C', 'C'), ('C++', 'C++'), ('Python', 'Python')], default='C++', max_length=10)),
                ('verdict', models.IntegerField(choices=[(0, 'Skipped'), (1, 'Accepted'), (2, 'Wrong Answer'), (3, 'Compilation Error'), (4, 'Time Limit Exceeded'), (5, 'Memory Limit Exceeded'), (6, 'Run Time Error')], default=0)),
                ('time', models.DecimalField(decimal_places=3, default=0.0, max_digits=5)),
                ('memory', models.IntegerField(default=0)),
                ('code', models.FileField(upload_to=submission.models.path_to_save)),
                ('problem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problem.problem')),
            ],
        ),
    ]