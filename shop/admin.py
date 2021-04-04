from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Product, Review, Slider

# Register your models here.
class ReviewAdmin(admin.StackedInline):
    model = Review
    fields = ('product', 'user', 'review_dt', 'review_text', 'active')
    readonly_fields = ('review_dt',)
    extra = 0

    admin.site.register(Review)


class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'css', 'get_img')
    list_display_links = ('title',)
    list_editable = ('css',)
    fields = ('title', 'text', 'css', 'img', 'get_img',)
    readonly_fields = ('get_img',)

    def get_img(self, obj):
        if obj.cms_img:
            return mark_safe(f'<img src="{obj.cms_img.url}" width="80px">')
        else:
            return 'нет картинки'

    get_img.short_description = 'Миниатюра'
    
admin.site.register(Slider, SliderAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title_capitalize', 'product_category', \
        'product_purchase_price', 'product_old_price', 'product_discount', \
            'product_new_price', 'product_copy', 'product_country', 'get_img')
    list_display_links = ('title_capitalize', 'get_img',)
    list_filter = ('product_category',)
    search_fields = ('product_title', 'product_description',)
    list_editable = ('product_old_price', 'product_discount', 'product_copy')
    fields = ('product_title', ('product_purchase_price', 'product_old_price', \
     'product_discount'), ('product_description', 'product_short_description'), \
         'product_copy', 'product_country', \
     'product_img', 'product_category', 'get_img')
    readonly_fields = ('get_img', 'product_new_price')
    #поле класса отзыв
    inlines = [ReviewAdmin,]

    def get_img(self, obj):
        if obj.product_img:
            return mark_safe(f'<img src="{obj.product_img.url}" width="60px">')
        else:
            return 'нет картинки'

    get_img.short_description = 'Миниатюра'

admin.site.register(Product, ProductAdmin)


