from django.contrib import admin # представляет собой связь приложения с админ-панелью сайта (админ панель поставляется совместно Джанго)

from .models import * # для отображения приложения в админ-панели  нужно импортировать все модели


class WomenAdmin(admin.ModelAdmin): # таблица с постами женщин, ниже помещаются атрибуты, которые взаимодействуют с параметрами таблицы или отображения
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published') # список полей, которые будут отображаться на админ-панели
    list_display_links = ('id', 'title') # поля, на которые можно перейти
    search_fields = ('title', 'content') # по каким полям можно делать поиск
    list_editable = ('is_published',) # какие поля можно редактировать
    list_filter = ('is_published', 'time_create',) # фильрация по полям
    prepopulated_fields = {"slug": ("title",)} # автоматическое заполнение поля slug при заполнении поля title
    save_on_top = True # по умолчанию, если стоит значение True, то внизу при редактировании поста будет показываться панелька с кнопками удлания, редактиования, сохранения.
    
    
class CategoryAdmin(admin.ModelAdmin): # таблица "Категории"
    list_display = ('id', 'name') # список полей, которые будут отображаться на админ-панели
    list_display_links = ('id', 'name') # поля, на которые можно перейти
    search_fields = ('name',) # по каким полям можно делать поиск. Не забывать, что это кортеж!!! Запятая в конце
    prepopulated_fields = {"slug": ("name",)} # автоматическое заполнение поля slug при заполнении поля name

admin.site.register(Women, WomenAdmin) # спецаильная команда по регистрации модели приложения в админ-панели(Women), вспомогательный класс (WomenAdmin)

admin.site.register(Category, CategoryAdmin) # регистрация второй модели приложения в админ-панели (Category), вспомогательный класс(CategoryAdmin)


# Register your models here.
