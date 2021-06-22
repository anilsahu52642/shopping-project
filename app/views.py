from django.shortcuts import render,HttpResponseRedirect
from django.views import View
from app.models import customer,product,cart,orderplaced
from app.forms import myregistrationform,myloginform,mypasswordchangeform,mypasswordresetform,mysetpasswordform
from app.forms import myregistrationform,myloginform,mypasswordchangeform,mypasswordresetform,mysetpasswordform,addressform,signinuser1
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.views import LogoutView,LoginView,PasswordChangeDoneView,PasswordChangeView,PasswordResetDoneView,PasswordResetView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User,Group
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

class productdetailview(View):
 '''this contains code for home page'''
 def get(self,request):
  mobile=product.objects.filter(catagory='m')
  laptop=product.objects.filter(catagory='l')
  topwear=product.objects.filter(catagory='tw')
  bottomwear=product.objects.filter(catagory='bw')
  cartitemno=False
  user=request.user
  if user.is_authenticated:
      cartitemno=len(cart.objects.filter(user=request.user))
  return render(request,'app/home.html',{'allmobile':mobile,'alllaptop':laptop,'alltopwear':topwear,'allbottomwear':bottomwear,'no_of_cart_item':cartitemno})




class product_detail(View):
 '''this contains product detail page'''
 def get(self,request,pk):
  pr=product.objects.get(pk=pk)
  item_in_cart=False
  cartitemno=None
  if request.user.is_authenticated:
      item_in_cart=cart.objects.filter(Q(product=pr.id)&Q(user=request.user)).exists()
      cartitemno=len(cart.objects.filter(user=request.user))
  return render(request,'app/productdetail.html',{'partproduct':pr,'mycart':item_in_cart,'no_of_cart_item':cartitemno})



def add_to_cart(request):
    '''this will add product to cart'''
    if request.user.is_authenticated:
      user=request.user
      product_id=request.GET['anilproduct_id']
      productinstance=product.objects.get(id=product_id)
      cartitme=cart(user=user,product=productinstance).save()
      return HttpResponseRedirect('/mycart/')
    else:
        return HttpResponseRedirect('/accounts/login/')


@login_required
def buy_now(request):
    '''for buying product without adding to cart'''
    if request.user.is_authenticated:
        productid=request.GET['anilbuynow']
        user=request.user
        productobject=product.objects.get(id=productid)
        shippingamount=50.00
        quantity=1
        productamount=productobject.discount_price*quantity
        totalamount=productamount+shippingamount
    return render(request, 'app/buynow.html',{"product_obj":productobject,'quantity':quantity,'shippingamount':shippingamount,'totalamount':totalamount,'productamount':productamount})

def increasebuyitem(request):
    '''for increasing product quantity while buying'''
    user=request.user
    quantity=int(request.GET['anquantity2'])
    quantity+=1
    productid=request.GET['anilbuynow']
    productobject=product.objects.get(id=productid)
    shippingamount=50.00
    productamount=productobject.discount_price*quantity
    totalamount=productamount+shippingamount
    return render(request, 'app/buynow.html',{"product_obj":productobject,'productamount':productamount,'quantity':quantity,'shippingamount':shippingamount,'totalamount':totalamount,})


def decreasebuyitem(request):
    '''for decreasing product quantity while buying'''
    quantity=int(request.GET['anquantity1'])
    quantity-=1
    productid=request.GET['anilbuynow']
    productobject=product.objects.get(id=productid)
    shippingamount=50.00
    productamount=productobject.discount_price*quantity
    totalamount=productamount+shippingamount
    return render(request, 'app/buynow.html',{"product_obj":productobject,'productamount':productamount,'quantity':quantity,'shippingamount':shippingamount,'totalamount':totalamount,})



@login_required
def checkout2(request):
    '''after hitting buy now where we have to go i.e. this page shows total price and more'''
    user=request.user
    address=customer.objects.filter(user=user)
    productid=request.GET['productid']
    pd=product.objects.get(id=productid)
    quant=int(request.GET['productquantity'])
    shippingamount=50.00
    quantity=1
    productobject=product.objects.get(id=productid)
    productamount=productobject.discount_price*quant
    totalamount=productamount+shippingamount
    return render(request,'app/checkout2.html',{'address':address,"prod":pd,'quant':quant,'totalamount':totalamount,'productamount':productamount})


@login_required
def payment_done2(request):
    '''after checkout page on this page we have to select address where prodcut to be deliver and it also creates object in orederplaced table'''
    prdid=request.GET['product_id']
    productobject=product.objects.get(id=prdid)
    productquantity=request.GET['quantity']
    user=request.user
    customerid=request.GET['addr_id']
    customerobject=customer.objects.get(id=customerid)
    orderplace=orderplaced(user=request.user,quantity=productquantity,customer=customerobject,product=productobject).save()
    return HttpResponseRedirect('/orders/')

@login_required
def cartproduct(request):
    '''this will display all the cart product present in the database'''
    if request.user.is_authenticated:
        cartitemno=len(cart.objects.filter(user=request.user))
        mycart=cart.objects.filter(user=request.user)
        shipping_charge=50.00
        total_amount=0.0
        if mycart:
            for cp in mycart:
                tempamount=cp.quantity*cp.product.discount_price
                total_amount+=tempamount
                alltotal=total_amount+shipping_charge
        else:
            print('no item in the cart')
            return render(request,'app/emptycart.html')
        return render(request,'app/addtocart.html',{'cartproduct':mycart,'totalamount':alltotal,'product_amount':total_amount,'no_of_cart_item':cartitemno})

def increasecartitem(request):
    '''for increasing product quantity to be order'''
    if request.user.is_authenticated:
        user=request.user
        product_quantity=int(request.GET['anil3cart_quantity'])
        product_quantity+=1
        product_id=request.GET['anil3cart_product_id']
        cart_object=cart.objects.filter(product=product_id).update(quantity=product_quantity)
    return HttpResponseRedirect('/mycart/')


def decreasecartitem(request):
    '''for decreasing product quantity to be order'''
    if request.user.is_authenticated:
        user=request.user
        product_quantity=int(request.GET['anil4cart_quantity'])
        product_quantity-=1
        product_id=request.GET['anil4cart_product_id']
        cart_object=cart.objects.filter(product=product_id).update(quantity=product_quantity)
    return HttpResponseRedirect('/mycart/')


def remove_cartitem(request):
    '''for romove an item from database of respecive user'''
    if request.user.is_authenticated:
        user=request.user
        mycart=cart.objects.filter(user=user)
        product_id=request.GET['anil2product_id']
        cart_object=cart.objects.filter(product=product_id)
        cart_object.delete()
    return HttpResponseRedirect('/mycart/')

@method_decorator(login_required,name='dispatch')
class profile(View):
 '''for adding user a address to database'''
 def get(self,request):
  myform=addressform()
  return render(request,'app/profile.html',{'form':myform,'active':'primary'})
 def post(self,request):
  mf=addressform(request.POST)
  if mf.is_valid():
   user=request.user
   name=mf.cleaned_data['name']
   locality=mf.cleaned_data['locality']
   city=mf.cleaned_data['city']
   zipcode=mf.cleaned_data['zipcode']
   state=mf.cleaned_data['state']
   mf2=customer(user=user,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
   mf2.save()
   messages.success(request,'address added successfully')
  else:
   messages.error(request,'some data is not with proper format')
  myform=addressform()
  cartitemno=len(cart.objects.filter(user=request.user))
  return render(request,'app/profile.html',{'form':myform,'active':'primary','no_of_cart_item':cartitemno})


@method_decorator(login_required,name='dispatch')
class address(View):
 '''for adding address'''
 def get(self,request):
  name1=request.user
  cartitemno=len(cart.objects.filter(user=request.user))
  customeraddress=customer.objects.filter(user=name1)
  return render(request,'app/address.html',{'address':customeraddress,'active':'primary','no_of_cart_item':cartitemno,'no_of_cart_item':cartitemno})


@login_required
def orders(request):
    '''for showing which items are successfully order placed'''
    user=request.user
    orderplaced_object=orderplaced.objects.filter(user=user)
    return render(request, 'app/orders.html',{'orders':orderplaced_object})





class change_password(PasswordChangeView):
 '''for change password of user'''
 template_name = 'app/changepassword.html'
 form_class = mypasswordchangeform
 success_url = reverse_lazy('passwordchangedone')


class change_passworddone(PasswordChangeDoneView):
 template_name='app/passwordchangedone.html'



class mobile(View):
 '''this is for mobile page'''
 def get(self,request,data=None):
  if data==None:
   mobiles = product.objects.filter(catagory='m')
  elif data=='samsung':
   mobiles = product.objects.filter(catagory='m').filter(brand=data)
  elif data=='oppo':
   mobiles = product.objects.filter(catagory='m').filter(brand=data)
  elif data=='below':
   mobiles = product.objects.filter(catagory='m').filter(discount_price__lte=15000)
  elif data=='above':
   mobiles=product.objects.filter(catagory='m').filter(discount_price__gte=15000)
  cartitemno=None
  user=request.user
  if request.user.is_authenticated:
      cartitemno=len(cart.objects.filter(user=request.user))
  return render(request,'app/mobile.html',{'allmobile':mobiles,'no_of_cart_item':cartitemno})



class login(LoginView):
 '''for login to accounts'''
 template_name = 'app/login.html'
 authentication_form = myloginform


class logout(LogoutView):
 '''for log out page'''
 template_name = 'app/base.html'
 next_page = 'home_page'



class customerregistration(View):
 '''for registering a new user'''
 def get(self,request):
  myform=myregistrationform()
  return render(request, 'app/customerregistration.html',{'form':myform})
 def post(self,request):
  myform=myregistrationform(request.POST)
  if myform.is_valid():
   myform.save()
   messages.info(request,'succssfully regstered Now you can login to your account')
  return render(request, 'app/customerregistration.html',{'form':myform})

@login_required
def checkout(request):
    '''for after selecting product from cart selecing address for placing order'''
    user=request.user
    address=customer.objects.filter(user=user)
    mycart=cart.objects.filter(user=user)
    shipping_charge=50.00
    total_amount=0.0
    alltotal=0.0
    if mycart:
        for cp in mycart:
            tempamount=cp.quantity*cp.product.discount_price
            total_amount+=tempamount
            alltotal=total_amount+shipping_charge
    return render(request, 'app/checkout.html',{'address':address,'total':alltotal,'cartitem':mycart})


def payment_done(request):
    '''for placing order and deleting cart object from database after it is added to orderplaced model'''
    user=request.user
    customer_objectid=request.GET['addr_id']
    customer_object=customer.objects.get(id=customer_objectid)
    cart_object=cart.objects.filter(user=user)
    for co in cart_object:
        orderplaced(user=user,customer=customer_object,product=co.product,quantity=co.quantity).save()
        co.delete()
    return HttpResponseRedirect('/orders/')



def searchitem(request):
    searchcontent=request.GET['productsearchitem2']
    searchtitle=product.objects.filter(title__icontains=searchcontent)
    searchdescription=product.objects.filter(description__contains=searchcontent)
    searchitem=searchtitle.union(searchdescription)
    searchbrand=product.objects.filter(brand__icontains=searchcontent)
    searchitem2=searchitem.union(searchbrand)
    context={'searchcontent':searchcontent,'searchitem':searchitem2}
    return render(request,'app/searchitem.html',context)
