# Generated by Django 3.2.14 on 2022-07-22 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='submitted_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]