# Generated by Django 3.1 on 2021-03-13 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_comment_reply'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='problem',
            new_name='post',
        ),
    ]
