from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings

# Create your models here.
class Slider(models.Model):
    img = models.ImageField(upload_to='sliderimg/', null=True, verbose_name='Изображение')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.CharField(max_length=200, verbose_name='Текст')
    css = models.CharField(max_length=200, default='-', verbose_name='CSS класс')


    def __str__(self):
        return self.cms_title

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return self.name     

class Product(models.Model):    
    COUNTRY = [
        (None, 'Страна'),
        ('RU', 'Россия'),
        ('KR', 'Корея'),
        ('FR', 'Франция'),
        ('QA', 'Катар'),
        ('IN', 'Индия'),
        ('CN', 'Китай'),
        ('IT', 'Италия'),
        ('EG', 'Египет'),
        ('VN', 'Вьетнам'),
        ('AE', 'ОАЭ'),
    ]

    CATEGORY = [
        (None, 'Категория'),
        ('a', 'Арабская'),
        ('b', 'Корейская'),
        ('c', 'Аюрведа'),
    ]

    product_title = models.CharField(max_length=200, verbose_name='Заголовок')
    product_img = models.ImageField(upload_to='productimg/', verbose_name='Изображение товара')
    product_purchase_price = models.IntegerField(blank=True, null=True, verbose_name='Закупочная цена')
    product_old_price = models.IntegerField(verbose_name='Старая цена')
    product_discount = models.IntegerField(verbose_name='Скидка (%)')
    product_copy = models.SmallIntegerField(verbose_name='Количество')
    product_country = models.CharField(max_length=2, choices=COUNTRY, verbose_name='Страна')
    product_description = models.TextField(verbose_name='Описание')
    product_short_description = models.TextField(verbose_name='Краткое описание')
    product_category = models.CharField(max_length=1, choices=CATEGORY, verbose_name='Категория')
    product_slug = models.SlugField(max_length=200, db_index=True)
    product_available = models.BooleanField(default=True)
    product_created = models.DateTimeField(auto_now_add=True)
    product_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'product_slug'),)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('shop:product', args=[str(self.id)])

    def title_capitalize(self):
        return self.product_title.capitalize()

    def __str__(self):
        return self.product_title

    def product_new_price(self):
        return int(self.product_old_price - self.product_old_price * 0.01 * self.product_discount)

    product_new_price.short_description = 'Цена'
    title_capitalize.short_description = 'Заголовок'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='товар')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='user_reviews')
    review_dt = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    review_text = models.TextField(verbose_name='Текст отзыва')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.review_text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('review_dt',)


