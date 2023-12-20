from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .forms import *
from .models import *

def index(request):
    p = Paginator(Message.objects.order_by('-date'), 50)
    if request.GET:
        page_object = p.get_page(request.GET.get('page_number'))
        number_of_page = request.GET.get('page_number')
    else:
        page_object = p.get_page(1)
        number_of_page = 1

    context = {
        'title': 'Главная страница',
        'page_object': page_object,
        'number_of_page': number_of_page
    }

    return render(request, 'index.html', context=context )

class AllUsers(ListView):
    def get_queryset(self):
        return get_user_model().objects.filter(is_superuser=False)
    template_name = 'all_user.html'
    context_object_name = 'users_list'

class Registration(CreateView):
    form_class = RegistrationForm
    template_name = 'user/registration.html'
    extra_context = {
        'title': 'Создание пользователя'
    }
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        profile = Profile.objects.create()
        user.page = profile
        user.save()
        return response

class LoginViewMy(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Авторизация'}
    success_url = reverse_lazy('index')

@login_required
def page_with_message(request, pk):
    user_object = get_user_model().objects.get(pk=pk)
    page_object = user_object.page

    if request.method == 'POST':
        form = CommentsForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.username = request.user
            f.page = page_object
            f.destination = user_object.username
            f.save()
    else:
        form = CommentsForm()

    message_q = page_object.message_set.all()
    context = {
        'user_object': user_object,
        'page_object': page_object,
        'message_q': message_q,
        'form': form,
        'title': user_object.username
    }
    return render(request, 'user/profile.html', context=context)

@login_required
def update_page(request, pk):
    if pk == request.user.pk:
        if request.method == 'POST':
            form = UpdateForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                user = get_user_model().objects.get(pk=pk)
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                if cd['image']:
                    user.image = cd['image']

                user.save()

                profile = Profile.objects.get(pk=pk)
                profile.status = cd['status']
                profile.date_birth = cd['date_birth']
                profile.about = cd['about']

                profile.save()

                return redirect(reverse_lazy('user/profile', kwargs={'pk': pk}))
        else:
            stub = get_user_model().objects.get(pk=pk).first_name
            stub2 = get_user_model().objects.get(pk=pk).last_name
            stub3 = get_user_model().objects.get(pk=pk).image
            stub4 = Profile.objects.get(pk=pk).status
            stub5 = Profile.objects.get(pk=pk).date_birth
            stub6 = Profile.objects.get(pk=pk).about

            dict1 = {
                'first_name': stub,
                'last_name': stub2,
                'image': stub3,
                'status': stub4,
                'date_birth': stub5,
                'about': stub6
            }

            form = UpdateForm(initial=dict1)
        context = {
            'form': form,
            'title': 'Редактирование данных'
        }
        return render(request, 'update.html', context=context)
    else:
        return redirect('/')

def wanna_delete(request, pk):
    return render(request, 'confirm_del_user.html', context={'title': 'Удаление пользователя', 'pk': pk})

def delete_u_and_p(pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    page = user.page
    page.delete()
    user.delete()
    return redirect('/')

class EditComment(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = CommentsForm
    template_name = 'edit.html'

    def dispatch(self, request, *args, **kwargs):
        self.return_key = request.GET.get('return_key')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.return_key:
            form.save()
            return redirect(reverse_lazy('user/profile', kwargs={'pk': self.return_key}))
        else:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_key'] = self.return_key
        return context


class DelComment(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'del_confirm.html'
    extra_context = {
        'title': 'Подтвердите удаление комментария'
    }

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.return_key})

    def dispatch(self, request, *args, **kwargs):
        self.return_key = request.GET.get('return_key')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_key'] = self.return_key
        return context