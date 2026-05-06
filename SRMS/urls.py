
from django.contrib import admin
from django.urls import path
from srmsapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('admin-login/', admin_login, name='admin-login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create-class/', create_class, name='create-class')

]
    