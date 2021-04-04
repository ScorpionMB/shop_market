from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail
# from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from tabulate import tabulate
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])          
            cart.clear() # очистка корзины
            order_created(request, order.id)
            order_created_shop(request, order.id)
            # запуск асинхронной задачи
            # order_created.delay(order.id)
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})

def order_created(request, order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа. 
    """
    order = Order.objects.get(id=order_id)
    subject = 'Заказ №10{}'.format(order_id)
    message = 'Добрый день, {}!\n\nВы успешно сформировали заказ.\
                \nВаш заказ №10{}.\n'.format(order.first_name,
                                             order.id)
    sum_order = 0                                         
    for item in OrderItem.objects.filter(order=order):
        sum_order += round(item.quantity*item.price, 1)
        message += '\n{}, кол-во: {} шт., сумма: {} руб.'\
            .format(item.product, item.quantity, round(item.quantity*item.price, 1))
        sum_order_coupon = round(sum_order - sum_order/100*order.discount, 1)
    message += '\n\nСтоимость заказа - {} руб.'.format(sum_order)
    if order.coupon is not None and order.coupon.code != 'SALE7' or order.coupon.code == 'SALE7' and len(request.user.orders.all()) == 0:
        message += '\n\nСкидка ("{}") - {} руб.'.format(order.coupon, round(sum_order/100*order.discount, 1))
        message += '\n\nОкончательная стоимость - {} руб.'.format(sum_order_coupon)
    mail_sent = send_mail(subject,
                          message,
                          settings.EMAIL_HOST_USER,
                          [order.email])
    return mail_sent

def order_created_shop(request, order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа на почту магазина. 
    """
    order = Order.objects.get(id=order_id)
    subject = 'Заказ №10{}'.format(order_id)
    message = 'Добрый день, заказ №10{} сформирован на сайте "kosmetica."\n'.format(order.id)
    sum_order = 0                                         
    for item in OrderItem.objects.filter(order=order):
        sum_order += round(item.quantity*item.price, 1)
        message += '\n{}, кол-во: {} шт., сумма: {} руб.'\
            .format(item.product, item.quantity, round(item.quantity*item.price, 1))
        sum_order_coupon = round(sum_order - sum_order/100*order.discount, 1)
    message += '\n\nСтоимость заказа - {} руб.'.format(sum_order)
    if order.coupon is not None and order.coupon.code != 'SALE7' or order.coupon.code == 'SALE7' and len(request.user.orders.all()) == 0:
        message += '\n\nСкидка ("{}") - {} руб.'.format(order.coupon, round(sum_order/100*order.discount, 1))
        message += '\n\nОкончательная стоимость - {} руб.'.format(sum_order_coupon)
    message += '\n\nЗаказчик:\n' 

    data = [
        ('Имя: ', f"{order.first_name}"),
        ('Фамилия: ', f"{order.last_name}"),
        ('Телефон: ', f"{order.phone}"),
        ('Email: ', f"{order.email}"),
        ('Город: ', f"{order.city}"),
        ('Индекс: ', f"{order.postal_code}"),
        ('Адрес: ', f"{order.address}"),
        ('Создан: ', f"{order.created}"[:19]),
        ]

    message += tabulate(data)

    # html = f'''
    # <!DOCTYPE html><html><head>
    # <meta charset="utf-8" /></head><body><table><tr>
    # <th>{order.first_name}</th>'
    # <th>Фамилия</th>
    # <th>Отчество</th>
    # </tr></table></body></html>
    # '''
    # message += html

    # mail_sent = EmailMessage(subject,
    #                         message,
    #                         settings.EMAIL_HOST_USER,
    #                         ['boleev@mail.ru'])
    # mail_sent.content_subtype = 'html'

    

    # mail_sent = EmailMultiAlternatives(subject,
    #                             message,
    #                             settings.EMAIL_HOST_USER,
    #                             ['boleev@mail.ru'])
    # mail_sent.attach_alternative(html, 'text/html')
    # mail_sent.send()

    mail_sent = send_mail(subject,
                                message,
                                settings.EMAIL_HOST_USER,
                                ['boleev@mail.ru'])
    return mail_sent


