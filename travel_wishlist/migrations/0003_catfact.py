# Generated by Django 3.2.8 on 2021-11-19 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_wishlist', '0002_auto_20211103_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatFact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fact', models.CharField(max_length=500)),
            ],
        ),
    ]
