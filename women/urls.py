"""coolsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.decorators.cache import cache_page


from women.views import about, WomenHome, WomenCategory, ShowPost, AddPage, RegisterUser, LoginUser, logout_user, ContactFormView

urlpatterns = [
# убрали путь admin, так как здесь он не нужен, он есть в coolsite.urls
    path('', WomenHome.as_view(), name='home'), # http://127.0.0.1:8000/
    # path('cats/<int:catid>/', categories), #http://127.0.0.1:8000/cats/1/
    # re_path(r'^archive/(?P<year>[0-9]{4})/', archive), # http://127.0.0.1:8000/archive/2019/
    path ('about/', about, name='about'), # http://127.0.0.1:8000/about/
    path ('addpage/', AddPage.as_view(), name='add_page'), # http://127.0.0.1:8000/addpage/
    path ('contact/', ContactFormView.as_view(), name='contact'), # http://127.0.0.1:8000/contact/
    path ('register/', RegisterUser.as_view(), name='register'), # http://127.0.0.1:8000/register/
    path ('login/', LoginUser.as_view(), name='login'), # http://127.0.0.1:8000/login/
    path ('logout/', logout_user, name='logout'),
    # path ('accounts/profile/', login_user, name='login'),
    path ('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path ('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
]
# можно ли по-другому прописывать catid, на языке питона, а не на html языке
# path ('cats/<int:...), где вместо int может быть
# str - любая не пустая строка, исключая символ '/'
# int - любое полож. число, не включая 0
# slug - слаг, то есть латиница ASCП таблицы, символы дефиса и подчеркивания
# uuid - цифры, малыет латинские символы ASCП, дефис
# path - любая не пустая строка, включая символ '/'
# 
# 
# В списке urlpatterns прописываем функцию re_path, чтобы задать нужную структуру - строго 4 цифры в url.
#
# Тема slug в URL - АДРЕСАХ
#
