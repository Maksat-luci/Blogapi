# Generated by Django 3.1 on 2021-03-15 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0003_auto_20210314_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
