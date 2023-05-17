
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


# ListView - отображение списка
# DetailView - отображение поста
# CreateView - формирование нового поста через форму


from women.models import *
from women.forms import *
from women.utils import *
# Create your views here.

# ссылка на class HttpRequest, где содержится информация о сессии, о куках, о запросе. 
# через переменную request нам доступна вся возможная информация в рамках текущего запроса  
# 
## menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]  - предыдущий вариант

menu = [{'title': "О сайте", 'url_name': 'about'}, # список из словарей
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]


#def index(request): # предыдущий вариант
 #  posts = Women.objects.all()
 #  return render (request, 'women/index.html', {'posts': posts, 'menu': menu, 'title': 'Главная страница'}) # render отвечает за обработку шаблонов, templates уже указан в settings.py, поэтому прописываем только короткий путь 
# HttpResponse не получится выводить много даных приложения, поэтому используют функцию render. Она подключает шаблон

class WomenHome(DataMixin, ListView): # отвечает за главную страницу нашего сайта. Основывается на классе  ListView

    model = Women # ссылка на модель Women,связанной с этим списком, отображает список статей, которые находятся в модели Women
    
# по умолчанию ищет шаблон по такому пути <имя приложения>/<имя модели>_list.html
# далее подключаем к urls.py, прописываем вместо функции index, только вызываем функцию (as_view()), получаем WomenHome.as_view()
    template_name = 'women/index.html' # если уже есть шаблон, но назван по-другому, то прописываем такой атрибут
    context_object_name = 'posts' # в шаблоне прописана именно posts
    # extra_context = {'title': 'Главная страница'} # в extra_context передаются в словаре статические параметры (в данном случае title) - списки передавать нельзя (только строки или числа). Например nmenu - динамаческий список

    def get_context_data(self, object_list=None, **kwargs): # для передачи динамических данных создают специальную функцию, куда передают все имеющиеся данные путем наследования от суперкласса. Они формируют динамический и статический контекст, которые передаются затем в шаблон index.html
        context = super().get_context_data(**kwargs) # получаем контекст, который уже сформирован для шаблона (posts, menu). Обращение к базовому классу, распаковываем словарь **kwargs и передаем все именованные параметры
        c_def = self.get_user_context(title="Главная страница") # передаем значение title, так как остальные menu, cats, cat_selected уже существуют
        # return context # возвращаем переменную
        # print (dict(list(context.items()) + list(c_def.items())))
        return dict(list(context.items()) + list(c_def.items())) # формируем общий словарь на основе двух словарей: context верхний на основе ListView, c_def - на основе DataMixin
    
    def get_queryset2(self): # название может быть любое
        return Women.objects.filter(is_published=True).select_related('cat') # отображаем только публикации с полем is_piblished = True. Делаем жадный запрос по ключу cat, так как в моделях именно cat является внешним ключом.
        
# def index(request):  # функция index использует шаблон через render, поэтому чтобы прочитать из БД, прикрепляем списки из БД в нее
#     posts = Women.objects.all() # сохраняем в переменные все данные из БД
#     # cats = Category.objects.all() # в шаблоне они идут в виде списка. Закомментили, так как список вернули через простой тег {# get_categories as categories #}
#     context = {
#         'posts': posts, 
#         'menu': menu,
#         'title': 'Главная страница',
#       #  'cats': cats, # заменили простым пользовательским тегом
#         'cat_selected': 0,
#         }
#     return render (request, 'women/index.html', context=context) # создаем словарь context с параметрами menu,posts,title, а в rendere указываем специальный параметр context, куда сохраням словарь (context=context)

# функция index отвечает за отображение главной страницы

# def categories(request, catid):
#     print (request.GET) # вставляем вначале, так как если после return, то request не будет найден
#     return HttpResponse (f"<h1>Статьи по категориям</h1><p>{catid}</p>") #http://127.0.0.1:8000/cats/1/

# # def archive (request, year):
# #     if int(year) > 2022:
# #         #raise Http404 # почему нельзя просто вставить функцию pageNotFound? А Http404 автоматом дает переход на эту функцию?
# #         return redirect('home') # идет перенаправление на главную страницу
# #     return HttpResponse(f'<h1>Архим по годам </h1><p>{year}</p>') # http://127.0.0.1:8000/archive/2019/  



class AddPage(LoginRequiredMixin, DataMixin, CreateView): # LoginRequiredMixin - встроенный класс, который позволяет скрывать какие-либо функции неавторизованным пользователям
    form_class = AddPostForm # 
    template_name = 'women/addpage.html'
    login_url = reverse_lazy('login') # куда идет перенаправление
    # для указания url, куда надо перейти после отправки формы по умолчанию стоит функция get_absolute_url, но если нужно отправить на другой маршрут, используем атрибут success_url
    # success_url = reverse_lazy('home')
    # reverse_lazy - выполняет построение маршрута только в момент, когда он понадобится
    # reverse - пытается сразу построить маршрут в момент создания экземпляра класса, но в нашем случае это невозможно, так как маршрут на данный не построен
    # почему именно на кнопку "Добавить статью" требуется аутентификация? Потому что именно в этом классе AddPage мыдобавили этот класс LoginRequiredMixin.



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить статью") # передаем значение title, так как остальные menu, cats, cat_selected уже существуют
        # return context # возвращаем переменную
        return dict(list(context.items()) + list(c_def.items())) # формируем общий словарь на основе двух словарей: context верхний на основе ListView, c_def - на основе DataMixin
# def addpage(request):
#     if request.method == 'POST': # если форма передается первый раз, POST = Nan, переход идет по else, где идет вызывается пустая форма. Когда данные заполнены, POST присваивается некоторое значение, так как данные передаются по POST.запросу, тогда срабатывает это условие
#         form = AddPostForm(request.POST, request.FILES) # форма сформирована на основе объекта словаря POST, где хранятся заполненные данные, которые передал пользователь на сервер. Если она не проходит проверку - назад возвращается уже с заполенными пользователем данными ему обратно
#         if form.is_valid(): # условие - если данные заполнены правильно - отобразить словарь данных - условие ниже
#             # print(form.cleaned_data) # если проверка сработала и ничего не показала - новая форма будет пустая
#                 form.save() # сохраняем именно в БД, так как форма связано с БД women
#                 return redirect('home')                
#     else:
#         form = AddPostForm() # при вызове функции создается экземпляр класса, затем передается параметр шаблону addpage.html
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': "Добавление статьи"}) # в фигурных скобках menu - задана списком словарей выше, title - задаем сами, который идет в шаблоне
# #
# ----------------------------------------------Формы-----------------------------------------------------------------
# 
# 
# 
# Формы предназначены для задания параметров авторизации (блок кнопок, полей для ввода, чек-бокса). В django есть специальный класс class{{произвольное название}} (forms.Form) и теги <form></form>
# Можно создавать формы в связки с моделью из БД, а также самостоятельно. С БД делают формы, связанные с даными и БД(регистрация пользователей)
# Если простой поиск на сайте, отправка письма, иными словами нет работы с данными, то достаточно сделать обычную формуЮ не свящанную с моделью и БД
# создаем файл forms.py в приложении women 
# Логика работы такая: когда страница отображается первый раз - форма пустая. Пользователь ввел данные, они отправляются на сервер и проходят проверку.
# Если все хорошо - идет перенаправление на другую страницу, если нет - пользователю возвращается зта же форма, только с уже заполненными ранее полями, чтобы не пришлось вводить ничего заново с нуля.
#----------------------------------------------------------------------------------------------------------------------
#
#
#
#
#
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm # прописываем в forms.py
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs): # название get_context_data - строгое
        context = super().get_context_data(**kwargs) # наследуется с базового класса вся коллекция в переменную context
        c_def = self.get_user_context(title="Обратная связь") # title формируется на основе context, который формируется на основе метода get_context_data базового класса DetailView, где в title передаем значение ключа из post для отображения нужного имени
        return dict(list(context.items()) + list(c_def.items())) # формируем общий словарь на основе двух словарей: context верхний на основе ListView, c_def - на основе DataMixin

    def form_valid(self, form): 
        print(form.cleaned_data) # выводим отправленные по данной форме чистые данные в терминале
        return redirect('home') 

# ------------------------------------------ Капча------------------------------------------
# Нужна для защиты от ботов ( графическая картинка, которую в любом случае вводит человек)
# Для ее установки прописываем в терминале команду: pip install django-simple-captcha
# Прописываем ее в списке установленных приложениях 'captcha
# в urls.py (глобальном) прописываем маршрут path('captcha/', include('captcha.urls')),
# в forms.py импортируем CaptchaField(from captcha.fields import CaptchaField)
# прописываем captcha = CaptchaField()
# --------------------------------------------------------------------------------------------------------------------------------------
# 
# 


# def contact(request):
#     return HttpResponse("Обратная связь")

# def login(request):
#     return HttpResponse("Авторизация")

#def deaf(request):
 #   return HttpResponse ('Ссылка приложения cat2')

# GET и POST запросы - которые передают в request.GET request.POST имя 'Gagarina' и ключ (cat) значение (тип) 'music'
# http://127.0.0.1:8000/?name=Gagarina&cat=music
# при создании функции в views.py с передачей аргумента request передаются эти параметры (обращение к словарю request.Get) 
#
# POST запрос - передает логин пароль, или изображения на сервис. Работает с формами
# работает через форму print(request.POST) 
#  
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'О сайте'})



class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug' # в urls.py переменую post_slug прописываем  
    # если используется pk, то pk_url_kwarg
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs): # название get_context_data - строгое
        context = super().get_context_data(**kwargs) # наследуется с базового класса вся коллекция в переменную context
        # print (context)
        c_def = self.get_user_context(title=context['post']) # title формируется на основе context, который формируется на основе метода get_context_data базового класса DetailView, где в title передаем значение ключа из post для отображения нужного имени
        # return context # возвращаем переменную
        return dict(list(context.items()) + list(c_def.items())) # формируем общий словарь на основе двух словарей: context верхний на основе ListView, c_def - на основе DataMixin

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug) # импортируем из django.shortcuts 
# # get_object_or_404 - специальная функция, которая вызывается при необходимости отобразить какой-то единичный объект(запись) из БД

#     context = {
#         'post': post, 
#         'menu': menu,
#         'content': post.content,
#         'title': post.title,
#         'cats': cats,
#         'cat_selected': post.slug, # post - ссылка на объект класса Women. Когда создается экземпляр, автоматически появляется свойство cat_id
#         }
#     return render (request, 'women/post.html', context=context) 

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False # если False, то возникает страница 404

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat') # выбираем те записи категорий, которые указаны по slug. Через параметр kwargs  можем получить все параметры нашего маршрута - в том числе cat_slug. 2 подчеркивания cat_slug для объекта cat, который ссылается к модели, связанной с текущей записью

    def get_context_data(self, *, object_list=None, **kwargs): # название get_context_data - строгое
        context = super().get_context_data(**kwargs) # наследуется с базового класса вся коллекция в переменную context
        # print (context)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat) # объект(.cat), который возвращает название категории. Превращаем его в строку
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title = 'Категория - ' + str(c.name), cat_selected=c.pk) # передаем значение title, так как остальные menu, cats, cat_selected уже существуют
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_id): # предыдущий вариант
#     posts = Women.objects.filter(cat_id = cat_id) # сохраняем в переменные все данные из БД. Фильтр включен, чтобы отображать статьи по отдельным рубрикам (cat_id = cat_id). Внешний cat_id совпадает с тем, который передали в виде запроса (присвоили через update)
#     # cats = Category.objects.all() # в шаблоне они идут в виде списка

#     context = {
#         'posts': posts, 
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#          'cats': cats,
#         'cat_selected': cat_id, # post - ссылка на объект класса Women. Когда создается экземпляр, автоматически появляется свойство cat_id
#         }
#     return render (request, 'women/index.html', context=context)
    
# создаем словарь context с параметрами menu,posts,title, а в rendere указываем специальный параметр context, куда сохраням словарь (context=context)
# шаблоны - html страница. В этих файлах можно прописывать конструкции для отображения информации из базы данных
# для этого в определении функции прописываем параметры после указания откуда брать шаблон, прописываем в виде словаря ключ - title и его значение 'О сайте'
# можно передавать список на сайте. Для этого прописываем в качестве параметра еще один ключ со значением - 'menu': menu, где menu - список
# подключение данных из БД идет через сохранение в переменную posts, где данные сохраняются в виде объектов. Сохраняем в функцию эту переменную, прописываем ключ и сохраням в шаблоне html - каркас.


# -----------------------------------------Подкючение статических файлов--------------------------------------------------
# подключение статических файлов осуще# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug) # импортируем из django.shortcuts 
# # get_object_or_404 - специальная функция, которая вызывается при необходимости отобразить какой-то единичный объект(запись) из БД

#     context = {
#         'post': post, 
#         'menu': menu,
#         'content': post.content,
#         'title': post.title,
#       #  'cats': cats,
#         'cat_selected': post.slug, # post - ссылка на объект класса Women. Когда создается экземпляр, автоматически появляется свойство cat_id
#         }
#     return render (request, 'women/post.html', context=context) ствляется для оформления: СSS, JavaScript. Приложение может работать в 2 режимах:
# - режим отладки. Статические файлы ищутся во всех подкаталогах static приложений
# - режим эксплуатации. Все статические файлы реальный сервер будет брать файлы static из каталога проекта.
# Для появления этой папке есть команда. Выполняется при подготовке к эксплуатации
# python manage.py collectstatic 
# Для корректной работы необходимо корректно определить три константы в settings.py:
# STATIC_URL, STATIC_ROOT,STATICFILES_DIR(нестандартные пути помимо основного)
#
#------------------------------------------Работа в шаблонизаторе:-------------------------------------
# {% имя_тега %} - спецификатор шаблона 
# {{ имя_переменная }} - выражение для вставки конструкций в шаблон
# {{value|имя_фильтра}}
# {# #} - блок комментариев
# # ## - строковый комментарий
# 
#-----------------------------------------Пользовательские теги--------------------------------------------------

# Пользовательские теги нужны для того, чтобы не было повторения частей кода в разных функциях. Есть 2 типа тегов: simple tags(простые), inclusion tags(включающие)
# Все теги располагаются в специальном подкаталоге приложения
# создаем папку templatestags c файлом __init__.py (чтобы был пакет), затем women_tags.py
#
#
#   {# прикрепляем простой тег, который возвращает QuerySet из таблицы категорий #}
#
# {% getcats as caregories %}
#
#    {# как перебрать список, который ниже с помощью этого тега. Перебрать напрямую из тега нельзя. Надо содержимое тега перенести в переменную с помощью ключеового слова as ...
# она ссылается на переменную, где перенесены данные из тега. Переменная ссылается на тег, откуда возвращаются данные. #}
#

#--------------------------------------- Классы представлений ( CBV) -------------------------------------

# Вместо функций прдеставлений, которые используются для реализации простой логики обработки запросов, однако можно для этой функции использовать классы представлений (CBV - Class-Based-Views)
# с помощью них код становится более читабельным
# C помозью базовых классов-представлений можно делать свои собственные классы представлений (CBV)
#
# -------------------------------------Mixin-------------------------------------

# Mixins нужны для того, чтобы убирать дублирование кода. В Python благодаря наличию множественного наследования примеси можно добавлять отдельного базового класса. 
# Классы представлений WomenHome, AddPage, ShowPost наследованы от WomenHome(ListView),AddPage(CreateView), ShowPost(DetailView) соответсвенно. Поэтому можно прописать еще один базовый класс наследования 
# class WomenHome(DataMixin, ListView) - пишем DataMixin первым, так как обрабатываться он будет первым, тогда общие атрибуты из  DataMixin будут обрабатываться в первую очередь
# Класс DataMixin обычно прописывают в отдельном файле utils.py приложения women
# ------------------------------------- Регистрация --------------------------------------
# Прописываем класс RegisterUser, в шаблоне Base.html добавляем кнопку маршрутизации, прописываем в urls.py маршрут с классом представления

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm # ссылается на стандартную фому для регистрации пользователей
    template_name = 'women/register.html'
    success_url = reverse_lazy('login') # перенаправление на страницу при успешной регистрации


    def get_context_data(self, *, object_list=None, **kwargs): # название get_context_data - строгое
        context = super().get_context_data(**kwargs) # наследуется с базового класса вся коллекция в переменную context
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form): # при успешной форме регистрации вызываем этот метод
        user = form.save() # сохранение формы в БД
        login(self.request, user) # функция login, которая авторизовывает пользователя после регистрации
        return redirect('home') # перенаправление на главную страницу 

# --------------------------------------------Авторизация-----------------------------------------------

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'
    # success_url = reverse_lazy('about')

    def get_context_data(self, *, object_list=None, **kwargs): # название get_context_data - строгое
        context = super().get_context_data(**kwargs) # наследуется с базового класса вся коллекция в переменную context
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self): #название строгое
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')
    
   

# def login_user(request):
#     user = authenticate() # в скобках можно передавать логин и пароль, тогда это будет автоматом аутентификация и вход
#     login(request, user)
#     return redirect('home')


# ---------------------------------------------Оптимизация------------------------------------------------
# Делается с помощью Django Debug Tool Bar. Загружает сбоку панельку с отображением разных данных, таких как SQL запросы, время загрузки сайта и так далее. 
# Одна из причин, по которой сайт может грузиться долго - большое количество лишних запросов в БД.
# Есть 2 типа запросов: ленивые и сжатые. Ленивые - отложенные запросы - те, которые нужны в момент получения запроса (Вывод рубрики,например).
# Сжатые запросы - 
# В Django есть 2 метода оптимизации: 
# select_related(key) - "жадная" загрузка связанных данных по внешнему ключу key, который имеет тип ForeignKey
# prefetch_related(key) - "жадная" загрузка связанных по внешнему ключу key, который имеет тип ManyToManyField 
# 
# 
# 
# --------------------------------------Кеширование в urls.py------------------------------------
# 
# path('', cache_page(60)(WomenHome.as_view()), name='home'), # http://127.0.0.1:8000/
# Добавляем функцию cache_page, предварительно импортировав ее, затем оборачиваем класс представления в нее после path
# Также если используются функции представления, то оборачиваем в декоратор @cache_page(60*15), где указываем интервал кеширования (в данном случае 15 секунд)
# Также можно кешировать весь сайт, но это делается очень редко
# Как правило кешиуются отдельные страницы, а также элементы
# 
# 
# Отдельные элементы кешируются через шаблон в шаблонизаторе:
# {% load cache %} - загружаем специальный тег в наш шаблон
# {% cache 500 sidebar %} - кеширование на 500 секунд
# ... sidebar ... - будет закеширован фрагмент, между тегами
# {% endcache %}
# 
# Кеширование с испозьвоанием API низкого уровня:
# делается в функциях представления путем задания команд и условий:
# cache.set() - сохранение произвольных данных в кеш по ключу
# cache.get() - выбор произвольных данных из кеша по ключу
# cache.add() - заносит новое значение в кеш, если его там еще нет (иначе данная операция игнорируется)
# cache.get_or_set() - извлекает данные из кеша, если их нет, то автоматически заносится значение по умолчанию
# cache.delete() - удаление данных из кеша по ключу
# cache.clear() - полная очистка кеша

# cats = cache.get('cats') - первоначально данные берутся из коллекции
#         if not cats:  - если данные не в коллекции
#             cats = Category.objects.annotate(Count('women')) - берем из БД
#             cache.set('cats', cats, 60) - из какой коллекции (cats), на 60 секунд, заносим их в кеш