# Generated by Django 3.2.2 on 2021-10-21 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_socialcomment_parent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='socialcomment',
            old_name='dislike',
            new_name='dislikes',
        ),
    ]
