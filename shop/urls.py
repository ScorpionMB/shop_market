from django.urls import path
from .views import ProductListView, AboutView, ReviewListView, DostavkaView, product_detail


app_name = 'shop'

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('dostavka/', DostavkaView.as_view(), name='dostavka'),
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('<pk>/', product_detail, name='product'),
    path('', ProductListView.as_view(), name='products'),
]
    
    