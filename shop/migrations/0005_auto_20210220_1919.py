# Generated by Django 2.0.5 on 2021-02-20 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20210220_1906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='season',
            options={'ordering': ('index',)},
        ),
    ]
