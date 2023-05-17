
from django import forms # откуда будем брать всю необходимую информацию для создания класса формы
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import *

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): # конструктор, когжа нужно какое-то поле изменить
        super().__init__(*args, **kwargs) # конструктор базового класса - наследование с суперкласса
        self.fields['cat'].empty_label = "Категория не выбрана" # меняем свойство empty_label поля cat на указанное

    def clean_title(self):
        title = self.cleaned_data['title'] # self.cleaned_data - колеекция, которая доступна в экземпляре класса AddPostForm
        if len(title)> 200:
            raise ValidationError('Длина превышает 200 символов')
        return title



    class Meta:
        model = Women # связываем форму и модель БД с классом оболочки
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat'] # '__all__' # показывать все поля, кроме тех, что заполняются автоматически
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

# создаем атрибуты - те поля, которые будут отображаться в форме, создаем те, которые необходимы конечному пользователю. Отображаем не все, которые есть в БД. Некоторые создадуться автоматически (time_create, time_update)
# лучше прописывать названия атрибутов в точности с теми, которые совпадают с атрибутами из модели Women. Это облегчит написание кода в будущем
# required - поле необязательно для заполения
# initial = True - автоматом стоит галка

# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label="Заголовок") 
#     slug = forms.SlugField(max_length=255, label="URL")
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
#     is_published = forms.BooleanField(label="Публикация", required=False, initial=True) # чек-бокс, который показывает опубликована или нет запись
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Категория не выбрана") # показывает список категорий


class RegisterUserForm(UserCreationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'})) # дублируем стили полей здесь, так как почему-то в классе Meta в данном фреймворке Django они не срабатываают
    email = forms.CharField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }

class LoginUserForm(AuthenticationForm):

    
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    contact = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()