from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, DetailView
from MiApp import views, models, forms

app_name = "MiApp"

urlpatterns = [
    #path('aboutUs/', TemplateView.as_view(template_name="aboutUs.html")),
    path('address/create/',views.AddressCreateView.as_view(template_name = "MiApp/address_form.html"), name = 'address_create'),
    path('address/<int:pk>/',views.AddressUpdateView.as_view(), name = 'address_update'),
    path('address/<int:pk>/delete/',views.AddressDeleteView.as_view(),name='address_delete'),
    path('aboutUs/thanks/', TemplateView.as_view(template_name = "thanks.html"), name = 'thanks'),
    path('login/',auth_views.LoginView.as_view(template_name="login.html", form_class=forms.AuthenticationForm,),name='login'),
    #path('products/all/', TemplateView.as_view(template_name = "products.html")),
    path('products/<slug:tag>/', views.ProductListView.as_view(), name= 'products'),
    path('products/detail/<slug:slug>/', DetailView.as_view(model = models.Products), name = 'products/detail'),
    path('address/',views.AddressListView.as_view(),name = 'address_list'),
]
