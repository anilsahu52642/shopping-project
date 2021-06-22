from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from app.forms import myloginform,myregistrationform,productaddform
from django.views import View
from django.contrib.auth.models import Group
from django.contrib import messages




class seller_signup(View):
 '''for registering a new seller'''
 def get(self,request):
  form=myregistrationform()
  return render(request, 'app/sellersignup.html',{'myform':form})
 def post(self,request):
  form=myregistrationform(request.POST)
  if form.is_valid():
   x=form.save()
   group=Group.objects.get(name='seller')
   x.groups.add(group)
   messages.success(request,'succssfully regstered Now you can login to your account')
  return render(request, 'app/sellersignup.html',{'myform':form})


def seller_signin(request):
    '''for seller signin.. to account'''
    if request.method=='POST':
        form=myloginform(data=request.POST)
        if form.is_valid():
            n=form.cleaned_data['username']
            p=form.cleaned_data['password']
            x=authenticate(username=n,password=p)
            if x is None:
                print('sorry some data is incorrect')
            else:
                login(request,x)
                print('log in successful.....')
                print('user is:',request.user)
                return HttpResponseRedirect('/sellerprofile/')
    else:
        form=myloginform()
    return render(request,'app/sellersignin.html',{'form':form})




def seller_profile(request):
    '''for adding new product for selling by seller'''
    if request.method=='POST':
        form=productaddform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Added product for selling...')

        else:
            messages.error(request,'Some Filled data are incorrect....')
    form=productaddform()
    buttoncolor='primary'
    return render(request,'app/sellerprofile.html',{'form':form,'active':buttoncolor})
