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
from django.urls import path
from coolsite import settings
from django.conf.urls.static import static

from django.urls import include # переносим страницу women.urls из women
from women.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls), # http://127.0.0.1:8000/
    path('', include ('women.urls')), # http://127.0.0.1:8000/
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG: # делается только в процессе отладки, при запуске сервера это уже автоматом настроено. Делается для того, чтобы реально было куда ссылаться на какой каталог для загрузки медиа
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = pageNotFound # функция-обработчик, с помощью которой формируется исключение, импортированная из файла women.views
# почему с помощью переменной прописывается исключение, а не через добавления path?
