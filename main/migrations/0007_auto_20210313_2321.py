# Generated by Django 3.1 on 2021-03-13 17:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_remove_reply_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reply',
            new_name='Comments',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
