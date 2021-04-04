from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from crm.views import PersonalAccount, index, Registr, none_user
from orders.views import admin_order_detail
from django.contrib.sitemaps.views import sitemap
from shop.sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/orders/order/<order_id>/change/', admin_order_detail, name='admin_order_detail'),
    path('admin/', admin.site.urls),
    path('cabinet/None', none_user, name='none_user'),
    path('cabinet/<str:pk>', PersonalAccount.as_view(), name='pers_account'),
    path('registr/', Registr.as_view(), name='registr'),
    path('accounts/', include('allauth.urls')),
    path('product/', include('shop.urls', namespace='shop')),
    path('crm/', include('crm.urls', namespace='crm')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('coupons/', include('coupons.urls', namespace='coupon')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
