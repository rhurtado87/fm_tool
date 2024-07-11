# Generated by Django 5.0.6 on 2024-07-09 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_stockpick_delete_stockprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='StockPick',
        ),
    ]