# Generated by Django 3.1 on 2021-03-12 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='moi_text',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
