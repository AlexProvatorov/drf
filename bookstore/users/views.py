from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from carts.models import Cart
from users.forms import *
from users.models import User


class RegisterUser(CreateView):
    """
    Представление для регистрации юзера.
    """
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        old_context = {
            'title': 'Регистрация',
            'content': 'Регистрация «BOOK STORE»',
        }
        return dict(list(context.items()) + list(old_context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    """
    Представление для авторизации юзера.
    """
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        old_context = {
            'title': 'Авторизация',
            'content': 'Авторизация «BOOK STORE»',
        }
        return dict(list(context.items()) + list(old_context.items()))

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    """
    Представление для выхода из учетной записи.
    """
    logout(request)
    return redirect('login')


class UserForgotPassword(SuccessMessageMixin, PasswordResetView):
    """
    Представление для сброса пароля через почту.
    """
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('index')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'email/password_subject_reset_mail.txt'
    email_template_name = 'email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirm(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление для установки нового пароля.
    """
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('index')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


class UserDetail(DetailView):
    """
    Представление для просмотра профиля.
    """
    model = User
    template_name = 'users/profile_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.username}'
        context['slug'] = self.object.slug
        return context


class UserUpdate(UpdateView):
    """
    Представление для редактирования профиля.
    """
    model = User
    template_name = 'users/profile_update.html'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = (f'Редактирование профиля пользователя: '
                            f'{self.request.user.username}'
                            )
        if self.request.POST:
            context['user_form'] = UserUpdateForm(
                self.request.POST,
                instance=self.request.user,
            )
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


def history_user(request):
    """
    Представление для отображения покупок пользователя.
    """
    personal_positions = Cart.cart_objects.filter(
        customer=request.user.id, status="COMPLETED",
    ).order_by("created_at").annotate(total=F("item__cost") * F("count"))

    context = {
        'title': 'История покупок',
        'content': 'История покупок',
        'personal_positions': personal_positions,
    }

    return render(request, 'users/history_user.html', context)
