# Generated by Django 3.0.2 on 2020-05-12 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminDashboard', '0002_linemanager_departments_under'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_status', models.CharField(max_length=20, null=True)),
                ('date_approved', models.DateField(auto_now=True)),
                ('notes', models.TextField(max_length=35, null=True)),
            ],
        ),
    ]
