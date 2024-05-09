from  django.urls import path
from . import views

# urlpatterns=[
#     path('',views.CreateBook),
#     path('author/',views.CreateAuthor, name='author'),
#     path('listview/',views.listBook),
#     path('updateview/<int:book_id>/',views.updateBook,name='update'),
#     path('deleteview/<int:book_id>/',views.deleteView,name='delete'),
#     path('detailsview/<int:book_id>/',views.detailsView,name='details'),
#     path('index',views.index)
# ]


# ----template inheritance----

urlpatterns=[
    path('createbook/',views.CreateBook,name='createbook'),
    path('author/',views.CreateAuthor, name='author'),
    path('',views.listBook,name='booklist'),
    path('updateview/<int:book_id>/',views.updateBook,name='update'),
    path('deleteview/<int:book_id>/',views.deleteView,name='delete'),
    path('detailsview/<int:book_id>/',views.detailsView,name='details'),
    path('index',views.index),
    path('search/',views.SearchBook,name='search'),

    # path('register/',views.Register_user,name='register'),
    # path('login/',views.loginUser,name='login'),
    # path('logout/',views.logout,name='logout'),
    # path('home/',views.Homepage,name='home')

    # role based Authentication

    path('register/',views.userRegistration,name='register'),
    path('login/',views.loginPage,name='login'),
    path('admin_view/',views.admin_view,name='admin_view'),
    path('user_view/',views.user_view,name='user_view'),
    path('logout/',views.logout_view,name='logout')
]
