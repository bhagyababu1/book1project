from django.contrib import admin
from  . models import Book,Author
from . models import userProfile,loginTable

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)

# role based Authentication

admin.site.register(userProfile)
admin.site.register(loginTable)