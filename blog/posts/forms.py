from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Message

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'image']

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'image': 'Аватарка',
            'email': 'Ваша почта'
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 100, 'rows': 5, 'placeholder': 'Сообщение'}),
            'image': forms.ClearableFileInput()
        }
        labels = {
            'text': 'Оставить сообщение',
            'image': 'Изображение',
        }

    def clean_text(self):
        cd = self.cleaned_data
        if cd['text'] == '' or cd['text'] == ' ':
            raise forms.ValidationError('Комментарий не должен быть пустым.')
        return cd['text']

class UpdateForm(forms.Form):
    first_name = forms.CharField(label='Имя ')
    last_name = forms.CharField(label='Фамилия ')
    date_birth = forms.DateField(label='Дата вашего рождения ', widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.CharField(label='Статус ')
    about = forms.CharField(label='О себе ', widget=forms.Textarea(attrs={
                            'cols': 65, 'rows': 10, 'placeholder': 'Введите текст'}))
    image = forms.ImageField(label='Аватарка ', required=False)