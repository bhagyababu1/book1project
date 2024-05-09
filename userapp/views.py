from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
from django .contrib import messages
from django.contrib import auth
from django.urls import reverse

from Bookapp.models import Book,Author,userProfile,loginTable
from . models import Cart,CartItem
import stripe
# Create your views here.

def UserlistBook(request):
    books=Book.objects.all()
    paginator=Paginator (books,4)
    page_number=request.GET.get('page')

    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number,num_pages)

    return render(request,'user/listuser.html',{'books':books,'page':page})

def UserdetailsView(request,book_id):
    book=Book.objects.get(id=book_id)
    return render(request,'user/userdetailsview.html',{'book':book})

def Userindex(request):
    return  render(request,'user/userindex.html')

# for search bar
def UserSearchBook(request):
    query=None
    books=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books=[]
    return  render(request,'user/usersearch.html',{'books':books,'query':query})


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
                    return redirect('/')
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

def add_to_cart(request,book_id):
    book=Book.objects.get(id=book_id)
    if book.quantity > 0:
        cart,created=Cart.objects.get_or_create(user=request.user)
        cart_item,item_created=CartItem.objects.get_or_create(cart=cart,book=book)

        if not item_created:
            cart_item.quantity+=1
            cart_item.save()
    return redirect('viewcart')

def view_cart(request):
    cart ,created=Cart.objects.get_or_create(user=request.user)
    cart_items=cart.cartitem_set.all()
    cart_item=CartItem.objects.all()
    total_price=sum(item.book.price*item.quantity for item in cart_items)
    total_items=cart_items.count()
    context={'cart_items':cart_items,'cart_item':cart_item,'total_price':total_price,'total_items':total_items}
    return render(request,'cart.html',context)

def increase_quantity(request,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    if cart_item.quantity < cart_item.book.quantity:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('viewcart')

def decrease_quantity(request,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    return redirect('viewcart')

def remove_from_cart(request,item_id):
    try:
        cart_item=CartItem.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoesNotExist:
        pass
    return redirect('viewcart')

# payment gateway

def create_checkout_session(request):
    cart_items=CartItem.objects.all()
    if cart_items:
        stripe.api_key=settings.STRIPE_SECRET_KEY
        if request.method=='POST':
            line_items = []
            for cart_item in cart_items:
                if cart_item.book:
                   line_item = {
                     'price_data':{
                        'currency':'INR',
                        'unit_amount':int(cart_item.book.price*100),
                        'product_data':{
                            'name':cart_item.book.title
                        },
                     },
                     'quantity':1
                   }
                   line_items.append(line_item)

            if line_items:
                checkout_session=stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel'))
                )
                return redirect(checkout_session.url,code=303)

def success(request):
    cart_items=CartItem.objects.all()
    for cart_item in cart_items:
        product=cart_item.book
        if product.quantity>=cart_item.quantity:
            product.quantity-=cart_item.quantity
            product.save()
    cart_item.delete()
    return render(request,'user/success.html')

def cancel(request):
    return render(request,'user/cancel.html')