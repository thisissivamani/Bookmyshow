# Generated by Django 4.2.7 on 2024-12-27 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='theater',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=10),
        ),
    ]