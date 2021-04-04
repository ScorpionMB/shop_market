from django.db import models
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.conf import settings


class Order(models.Model):

    STATUS = [
        (None, 'Статусы'), 
        ('a', 'новый'),
        ('b', 'в обработке'),
        ('с', 'согласован'),
        ('d', 'ожидает оплаты'),
        ('e', 'ожидает товар'),
        ('f', 'собран'),
        ('g', 'отправлен'),
        ('h', 'доставлен'),
        ('i', 'в ожидании оплаты'),
        ('k', 'оплачен'),
        ('l', 'отменен'),
    ]

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Эл. почта')
    phone = models.CharField(max_length=50, null=True, verbose_name='Телефон')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    city = models.CharField(max_length=100, verbose_name='Город')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')
    status =  models.CharField(max_length=1, choices=STATUS, verbose_name='Статус')
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='orders')
    product = models.ManyToManyField(Product)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return round(total_cost - total_cost * self.discount / 100, 1)

    def order_big(self):
        return '10' + str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def order_num(self):
        return int(str(self.order)[6:])