from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
from . models import userProfile,loginTable

from  django .contrib import messages

# Create your views here.
def userRegistration(request):
    login_table=loginTable()
    userprofile=userProfile()

    if request.method=='POST':
        userprofile.username=request.POST['username']
        userprofile.password = request.POST['password']
        userprofile.password2 = request.POST['password1']

        login_table.username = request.POST['username']
        login_table.password = request.POST['password']
        login_table.password2 = request.POST['password1']
        login_table.type = 'user'

        if request.POST['password']==request.POST['password1']:
            userprofile.save()
            login_table.save()
            messages.info(request,'Registration success')
            return  redirect('login')

        else:
            messages.info(request,'password not matching')
            return redirect('register')
    return render(request,'register.html')

def loginPage(request):
    if request.method=='POST':
        username=request.POST['username']
        password = request.POST['password']

        user=loginTable.objects.filter(username=username,password=password,type='user').exists()

        try:
            if user is not None:
                user_details=loginTable.objects.get(username=username,password=password)
                user_name=user_details.username
                type=user_details.type

                if type=='user':
                    request.session['username']= user_name
                    return  redirect('user_view')
                elif type=='admin':
                    request.session['username']= user_name
                    return redirect('admin_view')
            else:
                messages.error(request,'Invalid username or password')
        except:
            messages.error(request,'Invalid role')
    return render(request,'login.html')

def admin_view(request):
    user_name=request.session['username']
    return  render(request,'admin_view.html',{'user_name':user_name})
def user_view(request):
    user_name = request.session['username']
    return render(request, 'user_view.html',{'user_name':user_name})

def logout_view(request):
    logout(request)
    return redirect('login')
