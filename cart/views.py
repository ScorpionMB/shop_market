from django.shortcuts import render
from django.views.decorators.http import require_POST
from .forms import CartAddProductForm
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .cart import Cart
from coupons.forms import CouponApplyForm


# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_modificate(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST['id']
        button = request.POST['button']
        product = get_object_or_404(Product, id=product_id)
        if button == '+':
            increment = button
            decrement = None
        else:
            increment = None
            decrement = button
        cart.modificate(product, increment, decrement)
    return redirect('cart:cart_detail') 

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                            initial={'quantity': item['quantity'],
                            'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'product.html', {'product': product,
                                                        'cart_product_form': cart_product_form})