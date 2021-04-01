# Generated by Django 2.0.5 on 2021-02-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210220_1919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='season',
            options={'ordering': ('season_index',)},
        ),
        migrations.RenameField(
            model_name='season',
            old_name='index',
            new_name='season_index',
        ),
        migrations.RemoveField(
            model_name='season',
            name='slug',
        ),
        migrations.AddField(
            model_name='season',
            name='season_slug',
            field=models.SlugField(default='spring', max_length=200, unique=True),
        ),
    ]
