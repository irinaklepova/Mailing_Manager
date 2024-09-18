from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView

from blogs.models import Blog
from main.forms import ClientForm, MessageForm, MailingForm
from main.models import Client, Message, Mailing, Log
from main.services import get_cache_mailing_count, get_cache_mailing_active, get_cache_clients_count


class HomeView(TemplateView):
    """Контроллер для просмотра главной страницы"""
    template_name = 'main/home_view.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_count'] = get_cache_mailing_count()
        context_data['active_mailing_count'] = get_cache_mailing_active()
        context_data['unique_clients_count'] = get_cache_clients_count()
        context_data['random_blogs'] = Blog.objects.order_by("?")[:3]  # три случайные статьи из блога
        return context_data


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для просмотра сведений о клиенте"""
    model = Client
    extra_context = {
        'title': 'Информация о клиенте',
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or self.object.owner == user:
            return self.object
        raise PermissionDenied


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка клиентов"""
    model = Client
    extra_context = {
        'title': 'Информация о клиентах',
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Контроллер для создания клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.groups.filter(name='manager')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования клиента"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('main:client_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or self.object.owner == user:
            return self.object
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления клиента"""
    model = Client
    success_url = reverse_lazy('main:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or self.object.owner == user:
            return self.object
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    """Контроллер для списка писем"""
    model = Message
    extra_context = {
        'title': 'Список писем',
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.is_superuser or self.request.user.groups.filter(name='manager'):
            queryset = queryset
        else:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для просмотра письма"""
    model = Message
    extra_context = {
        'title': 'Информация о письмах',
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or self.object.owner == user:
            return self.object
        raise PermissionDenied


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Контроллер для создания письма"""
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.groups.filter(name='manager')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования письма"""
    model = Message
    form_class = MessageForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or self.object.owner == user:
            return self.object
        raise PermissionDenied

    def get_success_url(self):
        return reverse('main:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления письма"""
    model = Message
    success_url = reverse_lazy('main:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or self.object.owner == user:
            return self.object
        raise PermissionDenied


class MailingListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка рассылок"""
    model = Mailing
    extra_context = {
        'title': 'Список рассылок',
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.groups.filter(name='manager') or user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Контроллер для просмотра рассылки"""
    model = Mailing
    extra_context = {
        'title': 'Информация о рассылках',
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or self.object.owner == user or user.groups.filter(name='manager'):
            return self.object
        raise PermissionDenied

    def get_success_url(self):
        return reverse('main:mailing_list', args=[self.kwargs.get('pk')])


class MailingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Контроллер для создания рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.groups.filter(name='manager')


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для редактирования рассылки"""
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def test_func(self):
        custom_perms = ('mailing.set_inactive',)
        if self.request.user.groups.filter(name='manager') and self.request.user.has_perms(custom_perms):
            return True
        return self.handle_no_permission()

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or self.object.owner == user:
            return self.object
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер для удаления рассылки"""
    model = Mailing
    success_url = reverse_lazy('main:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if user.is_superuser or self.object.owner == user:
            return self.object
        raise PermissionDenied


class LogListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра списка логов"""
    model = Log
    extra_context = {
        'title': 'Статистика рассылок',
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        user = self.request.user
        if user.groups.filter(name='manager') or user.is_superuser:
            queryset = queryset
        else:
            queryset = queryset.filter(mailing=self.kwargs.get('pk'))
        return queryset


def toggle_activity_mailing(request, pk):
    """Контроллер для изменения статуса рассылки"""
    mailing_status = get_object_or_404(Mailing, pk=pk)
    if mailing_status.is_active:
        mailing_status.is_active = False
    else:
        mailing_status.is_active = True
    mailing_status.save()
    return redirect(reverse('main:mailing_list'))
