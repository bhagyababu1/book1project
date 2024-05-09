from  django.urls import path
from . import views


urlpatterns=[



        path('',views.UserlistBook,name='booklist'),
        path('detailsview/<int:book_id>/',views.UserdetailsView,name='details'),
        path('index',views.Userindex),
        path('search/',views.UserSearchBook,name='search'),

        # path('register/', views.userRegistration, name='register'),
        # path('login/', views.loginPage, name='login'),
        # path('admin_view/', views.admin_view, name='admin_view'),
        # path('user_view/', views.user_view, name='user_view'),
        # path('logout/', views.logout_view, name='logout'),

        path('add_to_cart/<int:book_id>/',views.add_to_cart,name='addtocart'),
        path('view_cart/',views.view_cart,name='viewcart'),
        path('increase/<int:item_id>/',views.increase_quantity,name='increase_quantity'),
        path('decrease/<int:item_id>/',views.decrease_quantity,name='decrease_quantity'),
        path('remove_from_cart/<int:item_id>/',views.remove_from_cart,name='remove_cart'),
        # payment gateway
        path('create-checkout-session/',views.create_checkout_session,name='create-checkout-session'),
        path('success/',views.success,name='success'),
        path('cancel/',views.cancel,name='cancel')
]
