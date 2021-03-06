# Generated by Django 3.1 on 2021-03-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text_ky',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_ky',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
