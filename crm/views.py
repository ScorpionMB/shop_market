from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from shop.models import Product
from .models import CustomUser
from orders.models import OrderItem, Order
from django.http import HttpResponse
from .forms import LoginForm


# Create your views here.
def index(request):
#    slider_list = CmsSlider.objects.all()
    products = Product.objects.all()
    dict_obj = {'products': products}
    return render(request, './index.html', dict_obj)

def none_user(request):
    return render(request, './none_user.html')

class PersonalAccount(DetailView):
    model = CustomUser 
    template_name = 'pers_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItem.objects.all()
        context['products'] = Product.objects.all()
        return context 


class Registr(FormView):
    form_class = CustomUserCreationForm   
    template_name = 'registr.html'  
    success_url = reverse_lazy('index')  
  
    def form_valid(self, form):  
        form.save()  
        username = form.cleaned_data.get('username')  
        raw_password = form.cleaned_data.get('password1')  
        login(self.request, authenticate(username=username, password=raw_password))  
        return super(Registr, self).form_valid(form)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})