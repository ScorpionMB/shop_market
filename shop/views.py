from django.views.generic import ListView, DetailView, TemplateView
from .models import Product, Review
from cart.forms import CartAddProductForm
from .forms import ReviewForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class DostavkaView(TemplateView):
    template_name = 'dostavka_all.html'

class ReviewListView(ListView):
    model = Review
    # paginate_by = 10  
    template_name = 'reviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        return context

class ProductListView(ListView):
    model = Product  
    template_name = 'products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        get_params = self.request.GET.dict()

        # search
        if get_params.get('q'):
            qs = qs.filter(product_title__icontains=get_params.get('q'))

        # filter
        if get_params.get('filter'):
            qs = qs.filter(product_category=get_params.get('filter'))
        
        # all
        if get_params.get('all'):
            qs = qs.all
        return qs   

class ProductView(DetailView):
    model = Product
    template_name = 'product.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['review_form'] = ReviewForm()
        return context

def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    reviews = product.reviews.filter(active=True)
    products = Product.objects.all()
    cart_product_form = CartAddProductForm()
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.user = request.user
            new_review.product = product
            new_review.save()
            return HttpResponseRedirect(reverse("shop:product", args=pk))
    else:
        review_form = ReviewForm()
    return render(request,
                  'product.html',
                 {'reviews': reviews,
                  'products': products,
                  'product': product,
                  'review_form': review_form,
                  'cart_product_form': cart_product_form})