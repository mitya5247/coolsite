from django.apps import AppConfig # настройка текущего приложения


class WomenConfig(AppConfig): # класс WomenConfig используется для кофигурации всего приложения.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'women'
    verbose_name = "Женщины мира" # Прописываем альтернативное имя, которое используется в панелях


