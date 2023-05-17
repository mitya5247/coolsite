from django.db import models
from django.urls import reverse
# все типы полей можно посмотреть в документации DJango
# Create your models here.
class Women(models.Model): # ID прописано в классе models.Model
    title = models.CharField(max_length=255, verbose_name="Заголовок") # class Charfield определяет текстовое поле
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL") # unique - поле должно быть уникальным, db_index - поле индексируемое(чтобы поиск был побыстрее)
    content = models.TextField(blank=True, verbose_name="Текст статьи") # текстовое поле, blank = True - поле может быть пустым
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания") # если True, новая запись принимает текущее значение времени и меняться больше не будет
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения") # поле будет меняться, когда каждый раз что-то будет изменяться в текущей записи
    is_published = models.BooleanField(default=True, verbose_name="Публикация") # когда будем добавлять запись, поле по умолчанию True
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория") # добавили новый параметр, null = True означает, что можно заполнять нулями

# verbose_name в модели Women в местах таблицы, в скобках - это альтернативное имя, которое отображается в админ-панели
# данная таблица - лишь пример как можно описывать модель таблиц в БД. Последовательность полей будет такая же, какая представлена здесь в модели
# Миграции БД - модули языка Python, где написаны наборы команд на уровне ORM интерфейса для создания таблиц определенных структур.
# при выполнении файла Миграции в БД автоматически создаются новые или меняются прежние таблицы, а также связи между ними
# каждый новый файл Миграции помещается в папку migrations, затем они выполняются
# на основе этих файлов миграции создается структура таблиц в БД
# каждый новый файл миграции описывает лишь изменения, которые произошли в структурах таблиц с прошлого раза.
# их можно воспринимать как контроллеры версии и всегда можно откатиться благодаря этому к предыдущей версии, к предыдущей структуре
# для создания файла миграции после создания модели создаем файл миграции с помощью команды в терминале python manage.py makemigrations, там в папке с миграциями появился файл 

    def __str__(self): # метод перегрузки, который возвращает заголовки записей в БД
      return self.title

# def get_absolute_url(self):
#    return f"/post/{self.pk}"

# функция reverse подставляет значения в ссылку, указанную в файле urls.py

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    class Meta: # специальный класс, который используется admin - панелью для настройки отобрадения модели Women
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"
        ordering = ['time_create', 'title']
    
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

# Нормализация - разделение данных на несколько таблиц и установление связей между ними.
# Для этого есть определенные классы для организации связей
# ForeignKey - для связей Many to One (поля отношений)
# ManyToManyField - для связей Many to Many (многие ко многим)
# OneToOneField - для связей One to One (один к одному)
# ForeignKey(<ссылка на первичную модель(category)>, on_delete=<ограничение при удалении записи из первичной модели>) 
# Внесение изменений в структуру БД крайне нежелательны(изменения ячеек)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug}) # 'category' дает отсылку на url, который прописан в urls.py

    def __str__(self):
        return self.name

    
    class Meta: # специальный класс, который используется admin - панелью для настройки отобрадения модели Women
        verbose_name = "Категория"
        verbose_name_plural = "Категория"
        ordering = ['id']

