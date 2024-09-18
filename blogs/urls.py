from django.urls import path
from django.views.decorators.cache import cache_page

from blogs.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, toggle_published
from blogs.apps import BlogsConfig

app_name = BlogsConfig.name

urlpatterns = [
    path('', cache_page(60)(BlogListView.as_view()), name='blogs_list'),
    path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='blogs_detail'),
    path('create/', BlogCreateView.as_view(), name='blogs_create'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blogs_update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blogs_delete'),
    path('published/<int:pk>/', toggle_published, name='toggle_published'),
]
