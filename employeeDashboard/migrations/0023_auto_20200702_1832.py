# Generated by Django 3.0.6 on 2020-07-02 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeDashboard', '0022_auto_20200628_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaves',
            name='Approval_by_Director',
            field=models.CharField(default='Pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='leaves',
            name='Approval_by_Executive_Director',
            field=models.CharField(default='Pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='leaves',
            name='Approval_by_Line_Manager',
            field=models.CharField(default='Pending', max_length=10),
        ),
    ]
