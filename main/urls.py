from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import (HomeView, ClientDetailView, ClientListView, ClientCreateView, ClientUpdateView,
                        ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView,
                        MessageDeleteView, MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView,
                        MailingDeleteView, LogListView, toggle_activity_mailing)

app_name = MainConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('client_list/', cache_page(60)(ClientListView.as_view()), name='client_list'),
    path('client_details/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('message_list/', cache_page(60)(MessageListView.as_view()), name='message_list'),
    path('message_details/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('mailing_list/', cache_page(60)(MailingListView.as_view()), name='mailing_list'),
    path('mailing_details/<int:pk>/', cache_page(60)(MailingDetailView.as_view()), name='mailing_detail'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('log_list/', cache_page(60)(LogListView.as_view()), name='log_list'),
    path('mailing_activity/<int:pk>/', toggle_activity_mailing, name='mailing_activity'),
]
