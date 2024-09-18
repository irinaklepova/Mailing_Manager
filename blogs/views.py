from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from blogs.models import Blog


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, CreateView):
    model = Blog
    fields = ('title', 'body', 'preview')
    permission_required = 'blogs.add_blogs'
    template_name = 'blogs/blogs_form.html'
    success_url = reverse_lazy('blogs:blogs_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.title)
            new_art.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.groups.filter(name='manager')


class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Статьи блога',
    }
    template_name = 'blogs/blogs_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blogs_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'body', 'preview')
    template_name = 'blogs/blogs_form.html'
    permission_required = 'blogs.change_blogs'

    def form_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.title)
            new_art.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogs:blogs_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = 'blogs.delete_blogs'
    template_name = 'blogs/blogs_confirm_delete.html'
    success_url = reverse_lazy('blogs:blogs_list')


def toggle_published(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True
    blog_item.save()
    return redirect(reverse('blogs:blogs_list'))
