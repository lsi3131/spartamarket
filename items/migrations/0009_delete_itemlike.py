# Generated by Django 4.2 on 2024-04-19 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_alter_itemlike_item_alter_itemlike_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ItemLike',
        ),
    ]