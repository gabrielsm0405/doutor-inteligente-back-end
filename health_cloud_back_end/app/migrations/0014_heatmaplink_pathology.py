# Generated by Django 3.1 on 2021-12-01 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20211130_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='heatmaplink',
            name='pathology',
            field=models.CharField(default='memes', max_length=50),
            preserve_default=False,
        ),
    ]
