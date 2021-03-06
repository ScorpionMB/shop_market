# Generated by Django 3.1.4 on 2021-03-18 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Эл. почта')),
                ('address', models.CharField(max_length=250, verbose_name='Адрес')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Почтовый индекс')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('status', models.CharField(choices=[(None, 'Статусы'), ('a', 'новый'), ('b', 'в обработке'), ('с', 'согласован'), ('d', 'ожидает оплаты'), ('e', 'ожидает товар'), ('f', 'собран'), ('g', 'отправлен'), ('h', 'доставлен'), ('i', 'в ожидании оплаты'), ('k', 'оплачен'), ('l', 'отменен')], max_length=1, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.product', verbose_name='Товар')),
            ],
        ),
    ]
