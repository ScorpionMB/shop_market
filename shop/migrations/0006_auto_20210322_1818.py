# Generated by Django 3.1.4 on 2021-03-22 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210322_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('review_dt',), 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
    ]