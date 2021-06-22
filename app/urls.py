from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from app import views
from django.contrib.auth import views as myviews
from app.forms import mypasswordresetform,mysetpasswordform

urlpatterns = [
    path('',views.productdetailview.as_view(),name='home_page'),
    path('product-detail/<int:pk>/', views.product_detail.as_view(), name='product-detail'),

    #### for buying product after adding to cart...
    path('addtocart/', views.add_to_cart, name='add-to-cart'),
    path('mycart/',views.cartproduct,name='my_cart'),
    path('removeitem/',views.remove_cartitem,name='remove_item'),
    path('increaseitem/',views.increasecartitem,name='increase_cartitem'),
    path('decreaseitem/',views.decreasecartitem,name='decrease_cartitem'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    ### for buying product with out adding to cart....
    path('buy/', views.buy_now, name='buy-now'),
    path('increaseitem2/',views.increasebuyitem,name='increase_buyitem'),
    path('decreaseitem2/',views.decreasebuyitem,name='decrease_buyitem'),
    path('checkout2/', views.checkout2, name='checkout2'),
    path('paymentdone2/', views.payment_done2, name='paymentdone2'),

    path('profile/', views.profile.as_view(), name='profile'),
    path('address/', views.address.as_view(), name='address'),
    path('orders/', views.orders, name='orders'),

    # for password change of user
    path('changepassword/', views.change_password.as_view(), name='changepassword'),
    path('changepassworddone/', views.change_passworddone.as_view(), name='passwordchangedone'),

    # for password reset....
    path('passwordreset/', myviews.PasswordResetView.as_view(template_name='app/passwordreset.html',form_class=mypasswordresetform), name='reset_password'),
    path('passwordreset/done/', myviews.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'), name='password_reset_done'),
    path('passwordresetconform/<uidb64>/<token>/', myviews.PasswordResetConfirmView.as_view(template_name='app/passwordresetconform.html',form_class=mysetpasswordform), name='password_reset_confirm'),
    path('passwordresetcomplect/done/', myviews.PasswordResetCompleteView.as_view(template_name='app/passwordresetcomplete.html'), name='password_reset_complete'),

    path('mobile/', views.mobile.as_view(), name='mobile'),
    path('mobile/<slug:data>/', views.mobile.as_view(), name='mobile'),
    path('accounts/login/', views.login.as_view(), name='login'),
    path('accounts/logout/',views.logout.as_view(),name='logout'),
    path('registration/', views.customerregistration.as_view(), name='customerregistration'),


    path('searchitem/',views.searchitem,name='searchitem'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
