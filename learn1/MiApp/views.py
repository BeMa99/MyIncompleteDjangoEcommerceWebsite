from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404#: it returns an object that
#corresponds to the filters specified, or raises a 404 exception
from MiApp import models
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from MiApp.forms import ContactForm
from MiApp import forms
import logging
logger = logging.getLogger(__name__)

def Contact_us(request):
    form = ContactForm()
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            print(form)
            form.save()
            return redirect('products.html')
    context={'form':form}
    return render(request, 'MiApp/aboutUs.html')

class ProductListView(ListView):
    template_name = "products.html"
    paginate_by = 4
    def get_queryset(self):
        tag = self.kwargs['tag']#this view is expecting to be called with
        #the tag specified in the URL path. 
        self.tag = None
        if tag != "all":
            self.tag = get_object_or_404(models.ProductTag, slug = tag)#tag as slug
        if self.tag:
            products = models.Products.objects.active().filter(tags=self.tag)
            #Depending on the content of kwargs,
            #it returns a list of active products belonging to that tag,
            #or simply all active ones if the tag all is specified
        else:
            products = models.Products.objects.active()
        return products.order_by("name")
        
class SignupView(FormView):
    template_name = "signup.html"
    form_class = forms.UserCreationForm
    success_url = '/thanks/'
    #def get_success_url(self):
        #redirect= self.request.GET.get("next","/")
        #return redirect
    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info("New Signup for email=%s through SignupView", email)
        user = authenticate(email=email, password = raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(self.request, "You signed up successfully")
        return response
    
class AddressListView(LoginRequiredMixin, ListView):
    model = models.Address
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class AddressCreateView(LoginRequiredMixin, CreateView):
    model=models.Address
    fields=["name","address1","address2","zip_code", "city", "country",]
    success_url = reverse_lazy("addess_list")
    def form_valid(self, form):
        obj=form.save(commit=False)
        obj.user=self.request.user
        obj.save()
        return super().form_valid(form)

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Address
    fields = ["name","address1","address2","zip_code","city","country",]
    success_url = reverse_lazy("address_list")
    def get_queryset(self):#Each user must be able to operate only on their own addresses
        return self.model.objects.filter(user=self.request.user)#The address creation
    #view needs the user to be set internally to the right value

class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Address
    success_url = reverse_lazy("address_list")
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
