# Generated by Django 2.0.5 on 2021-02-20 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20210220_1945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='season',
            options={'ordering': ('index',)},
        ),
        migrations.RenameField(
            model_name='season',
            old_name='season_index',
            new_name='index',
        ),
    ]
