# Generated by Django 5.0.6 on 2024-07-11 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_alter_wishlist_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together=set(),
        ),
    ]
