# Generated by Django 2.1.7 on 2019-03-20 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20181104_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='media/item'),
        ),
    ]
