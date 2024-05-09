from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
from . models import Book,Author,userProfile,loginTable
from  . forms import AuthorForm,BookForm
from  django .contrib import messages
from django.contrib import auth

# Create your views here.

def CreateBook(request):
    books=Book.objects.all()
    if request.method=='POST':
        form=BookForm(request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=BookForm()
    return render(request,'admin/book.html',{'form':form,'books':books})

def CreateAuthor (request):
    if request.method=='POST':
        form=AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=AuthorForm()
    return  render(request,'admin/author.html',{'form':form})

# def listBook(request):
#     books=Book.objects.all()
#     return render(request,'list.html',{'books':books})

# for pagination
def listBook(request):
    books=Book.objects.all()
    paginator=Paginator (books,4)
    page_number=request.GET.get('page')

    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number,num_pages)

    return render(request,'admin/list.html',{'books':books,'page':page})

def detailsView(request,book_id):
    book=Book.objects.get(id=book_id)
    return render(request,'admin/detailsview.html',{'book':book})

def updateBook(request,book_id):
    book=Book.objects.get(id=book_id)
    if request.method=='POST':
        form=BookForm(request.POST,files=request.FILES,instance=book)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=BookForm(instance=book)
    return render(request,'admin/updateview.html',{'form':form})

def deleteView(request,book_id):
    book=Book.objects.get(id=book_id)
    if request.method=='POST':
        book.delete()
        return  redirect('/')
    return render(request,'admin/deleteview.html',{'book':book})


# static file

def index(request):
    return  render(request,'admin/index.html')

# for saerch bar

def SearchBook(request):
    query=None
    books=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books=[]
    return  render(request,'admin/searchbook.html',{'books':books,'query':query})


# User authentication

# def Register_user(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         cpassword = request.POST.get('password1')
#
#         if password==cpassword:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request,'This username already exists')
#                 return  redirect('register')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request,'This email already exists')
#                 return  redirect('register')
#             else:
#                 user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
#                 user.save()
#                 return redirect('login')
#         else:
#             messages.info(request,'This password not matching')
#             return redirect('register')
#     return render(request,'register.html')
#
#    # login page
#
# def loginUser(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user=auth.authenticate(username=username,password=password)
#
#         if user is not None:
#             auth.login(request,user)
#             return  redirect('home')
#         else:
#             messages.info(request,'please provide correct details')
#             return redirect('login')
#     return render(request,'login.html')
#
#
#     # logout page
#
# def logout(request):
#     auth.logout(request)
#     return redirect('login')
#
#     # home page
#
# def Homepage(request):
#     return render(request,'home.html')

# role based Authentication

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


