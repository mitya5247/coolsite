from women.models import *

from django.db.models import Count
from django.core.cache import cache

menu = [{'title': "О сайте", 'url_name': 'about'}, # список из словарей
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}]


class DataMixin:
    paginate_by = 20
    def get_user_context(self, **kwargs): # для передачи динамических данных создают специальную функцию, куда передают все имеющиеся данные путем наследования от суперкласса. Они формируют динамический и статический контекст, которые передаются затем в шаблон index.html
        context = kwargs # получаем контекст, который уже сформирован для шаблона (posts, menu). Обращение к базовому классу, распаковываем словарь **kwargs и передаем все именованные параметры
        cats = Category.objects.annotate(Count('women'))
        context['menu'] = menu # новому сформированному ключу меню присваиваем список menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        # print(context)
        return context