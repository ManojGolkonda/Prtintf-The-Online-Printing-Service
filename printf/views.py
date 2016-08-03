from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import Context
from django.http import HttpResponse
from django.template import loader
from models import Customers
from models import Merchants
from django.contrib.auth.models import User
from forms import *
from django.contrib.auth import login
from django.http import HttpResponseRedirect


#
# # def (request):
# #     #template = loader.get_template('printf/sampleuser.html')
# #     return HttpResponse(zz)
# # def merchantview(request):
# #     template = loader.get_template('printf/samplemerchant.html')
# #     return HttpResponse(template.render(None))
#
# def index(request):
#     template=loader.get_template('printf/sampleuser.html')
#     return HttpResponse(template.render(None))
#
# def index1(request):
#     template=loader.get_template('printf/samplemerchant.html')
#     return HttpResponse(template.render(None))
#
# @login_required(login_url="/accounts/profile/")
# def GroupUser(request):
#     template=loader.get_template('printf/sampleuser.html')
#     return HttpResponse(template.render(None))
#
# @login_required(login_url="/accounts/login/")
# def GroupMerchant(request):
#     template=loader.get_template('printf/samplemerchant.html')
#     return HttpResponse(template.render(None))

from django.contrib.auth.models import Group

def testview(request):
    if "customerlogin" in str(request.path):
        if request.user in Group.objects.get(name="customer").user_set.all() :
            # id=User.objects.get(id=request.user.id)
            url='/printf/customerOrder/'
            return HttpResponseRedirect(url)
    elif "merchantlogin" in str(request.path):
        if request.user in Group.objects.get(name="merchant").user_set.all():
            #id = User.objects.get(id=request.user)
            url = '/printf/merchantOrder/'
            return HttpResponseRedirect(url)
    return HttpResponse("Its okay try again :)")


def homepageview(request):
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render(None))


def addcustomer(request,new_user):
    if request.method == "POST":
        customerform = CustomerForm(request.POST)
        if customerform.is_valid():
            data=customerform.cleaned_data
            new_user1=User.objects.get(id=new_user)
            new_user1.groups.add(Group.objects.get(name='customer'))
            new_customer = Customers(name=data['name'], location=data['location'], user=new_user1)
            new_customer.save()
            return HttpResponseRedirect('/homepage')
    else:
        customerform = CustomerForm()
    return render(request, 'printf/addcustomer.html', {'customerform': customerform})

def addmerchant(request,new_user):
    if request.method == "POST":
        merchantform = MerchantForm(request.POST)
        if merchantform.is_valid():
            data=merchantform.cleaned_data
            new_user1=User.objects.get(id=new_user)
            new_user1.groups.add(Group.objects.get(name='merchant'))
            new_customer = Merchants(name=data['name'], location=data['location'], user=new_user1,cost=data['cost'])
            new_customer.save()
            return HttpResponseRedirect('/homepage')
    else:
        merchantform = MerchantForm()
    return render(request, 'printf/addmerchant.html', {'customerform': merchantform})



def choose(request,id):
    template = loader.get_template('printf/choose.html')
    c = Context({'num': id})
    return HttpResponse(template.render(c))

def updateorder(request,order_id):
    myorder = Orders.objects.get(id=order_id)
    myorder.completed = True
    myorder.save()
    return HttpResponseRedirect('/printf/merchantOrder')

def adduser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            id=new_user.id
            if "customer" in str(request.path):
                s='/addcustomer/'+str(id)
                return HttpResponseRedirect(s)
            elif "merchant" in str(request.path):
                s = '/addmerchant/' + str(id)
                return HttpResponseRedirect(s)
    else:
        form = UserForm()
    return render(request, 'adduser.html', {'form': form})
