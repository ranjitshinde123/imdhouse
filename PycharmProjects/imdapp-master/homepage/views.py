from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate, login as loginuser,logout

from imdapp.models import *
class HomeView(View):
    template_name = "home.html"
    def get(self, request):
        labels = []
        data = []
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'data'      : data,
            'sales'     : sales,
            'purchases' : purchases
        }
        return render(request, self.template_name, context)

def login(request):

   if request.method =='GET':
       form = AuthenticationForm()
       context = {
           "form": form
       }
       return render(request, 'login.html', context=context)
   else:
       form = AuthenticationForm(data=request.POST)
       print(form.is_valid())
       if form.is_valid():
           username = form.cleaned_data.get('username')
           password = form.cleaned_data.get('password')
           user= authenticate(username=username, password=password)
           if user is not None:
               loginuser(request,user)
               return redirect('home')
           return render(request,'index.html')

       else:
           context = {
               "form": form
           }
           return render(request, 'login.html', context=context)

class AboutView(TemplateView):
    template_name = "about.html"


