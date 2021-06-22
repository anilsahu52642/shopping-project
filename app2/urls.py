from django.contrib import admin
from django.urls import path
from app2 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sellersignin/',views.seller_signin,name='sellersignin'),

    path('sellersignup/',views.seller_signup.as_view(),name='sellersignup'),
    path('sellerprofile/',views.seller_profile,name='sellerprofile'),


]
