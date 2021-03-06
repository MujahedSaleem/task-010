# Generated by Django 3.0.4 on 2020-03-07 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EmployeeTracker', '0004_auto_20200306_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='vacations',
                                          to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
