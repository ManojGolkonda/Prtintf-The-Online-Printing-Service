from django.db import models
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.template import loader

from printf.models import Customers
from printf.models import Merchants
from printf.models import Orders
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from printf.forms import *
from queries import display
from datetime import datetime,timedelta
@method_decorator(login_required,name='dispatch')
class CustomersCreateView(CreateView):
    model = Customers
    fields = ['id','name','location']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CustomersCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("Printf_createorder")

@method_decorator(login_required,name='dispatch')
class MerchantsCreateView(CreateView):
    model = Merchants
    fields = ['id','name','location','cost']

    def get_success_url(self):
        return reverse("MerchantsListView")

# @method_decorator(login_required,name='dispatch')
# class OrdersCreateView(CreateView):
#     model = Orders
#     fields = ['id','qty','date_of_order','date_of_delivery','customer','merchant']
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(OrdersCreateView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse("Printf_customerorder")


def list(request):
    if request.method=="POST":
        file = OrderForm(request.POST,request.FILES)

        if file.is_valid():
            customers=Customers.objects.get(user_id=request.user)
            order=file.save(commit=False)
            order.customer=customers
            order.date_of_order=date.today()
            order.date_of_delivery=datetime.now()+timedelta(days=3)
            order.save()
            return HttpResponseRedirect(reverse('Printf_customerorder'))
    else:
        file=OrderForm()
    return render(request,'printf/orders_form.html',{'myorders':Orders,'form':file})

def update_profile(request):
    if request.method=="POST":
        form=UpdateForm(request.POST)
        if form.is_valid():
            merchants=Merchants.objects.get(user_id=request.user)
            new_data=form.cleaned_data
            merchants.name=new_data['name']
            merchants.cost=new_data['cost']
            merchants.location=new_data['location']
            merchants.save()
            return HttpResponseRedirect(reverse('Printf_merchantorder'))
    else:
        form=UpdateForm()
    return render(request,'printf/merchants_update_form.html',{'merchant':Merchants,'form':form})

@method_decorator(login_required,name='dispatch')
class CustomersDetailView(DetailView):
    model = Orders
    context_object_name = 'myorders'

    def get_object(self, queryset=None):
        customer = Customers.objects.filter(pk=self.kwargs.get("customer_id"))
        if customer:
            return Orders.objects.all().filter(customer=customer)
        else:
            userid = self.request.user.id
            customer=Customers.objects.filter(user=userid)
            return Orders.objects.all().filter(customer=customer)

@method_decorator(login_required,name='dispatch')
class OrdersListView(ListView):
    model = Orders
    context_object_name = 'allorders'

    def get_object(self, queryset=None):
            return Orders.objects.all()

@method_decorator(login_required,name='dispatch')
class MerchantsListView(ListView):
    model = Merchants
    context_object_name = 'allmerchants'

    def get_object(self, queryset=None):
            return Merchants.objects.all()

@method_decorator(login_required,name='dispatch')
class MerchantsDetailView(DetailView):
    model = Orders
    template_name = 'printf/merchant_homepage.html'
    context_object_name = 'myorders'

    def get_object(self, queryset=None):
        merchant = Merchants.objects.filter(pk=self.kwargs.get("merchant_id"))
        if merchant:
            return Orders.objects.all().filter(merchant=merchant)
        else:
            userid = self.request.user.id
            merchant = Merchants.objects.filter(user=userid)
            return Orders.objects.all().filter(merchant=merchant)

@method_decorator(login_required,name='dispatch')
class MerchantsDetailViewCompleted(DetailView):
    model = Orders
    template_name = 'printf/merchant_homepage_completed.html'
    context_object_name = 'myorders'

    def get_object(self, queryset=None):
        merchant = Merchants.objects.filter(pk=self.kwargs.get("merchant_id"))
        if merchant:
            return Orders.objects.all().filter(merchant=merchant)
        else:
            userid = self.request.user.id
            merchant = Merchants.objects.filter(user=userid)
            return Orders.objects.all().filter(merchant=merchant)



@method_decorator(login_required,name='dispatch')
class MerchantsUpdate(UpdateView):
    model=Merchants
    fields = ['name','location','cost']
    template_name='printf/merchants_update_form.html'
    def get_success_url(self):
        return reverse('Printf_merchantorder')

