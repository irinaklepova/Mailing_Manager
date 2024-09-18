from datetime import datetime, timedelta
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.core.cache import cache

from main.models import Mailing, Log, Client


def change_status(mailing, time):
    if mailing.status == 'Создана':
        mailing.status = 'Запущена'
        print('Запущена')
    elif mailing.status == 'Запущена' and mailing.end_time <= time:
        mailing.status = 'Завершена'
        print('Завершена')
    mailing.save()


def change_start_datetime_mailing(mailing, time):
    if mailing.start_time < time:
        if mailing.periodicity == 'Ежедневно':
            mailing.start_time += timedelta(days=1)
        elif mailing.periodicity == 'Еженедельно':
            mailing.start_time += timedelta(days=7)
        elif mailing.periodicity == 'Ежемесячно':
            mailing.start_time += timedelta(days=30)
        mailing.save()


def my_job():
    print('my_job запущен')
    now = datetime.now()
    timenow = timezone.make_aware(now, timezone.get_current_timezone())
    mailings = Mailing.objects.filter(is_active=True)
    if mailings:
        for mailing in mailings:
            change_status(mailing, timenow)
            if mailing.start_time <= timenow <= mailing.end_time:
                for client in mailing.clients.all():
                    try:
                        response = send_mail(
                            subject=mailing.letter.title,
                            message=mailing.letter.text,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[client.email],
                            fail_silently=False
                        )
                        mailing_log = Log.objects.create(
                            last_attempt_time=mailing.start_time,
                            attempt_status='Успешно',
                            server_response=response,
                            mailing=mailing
                        )
                        mailing_log.save()
                        change_start_datetime_mailing(mailing, timenow)
                        print('лог сохранен')
                    except SMTPException as error:
                        mailing_log = Log.objects.create(
                            last_attempt_time=mailing.start_time,
                            attempt_status='Безуспешно',
                            server_response=error,
                            mailing=mailing
                        )
                        mailing_log.save()
                        print('Ошибка')
    else:
        print('нет активных рассылок')


def get_cache_mailing_count():
    """Функция для кеширования данных о количестве рассылок"""
    if settings.CACHE_ENABLED:
        key = 'mailings_count'
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mailing.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mailing.objects.all().count()
    return mailings_count


def get_cache_mailing_active():
    """Функция для кеширования данных о количестве активных рассылок"""
    if settings.CACHE_ENABLED:
        key = 'active_mailings_count'
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = Mailing.objects.filter(is_active=True).count()
            cache.set(key, active_mailings_count)
    else:
        active_mailings_count = Mailing.objects.filter(is_active=True).count()
    return active_mailings_count


def get_cache_clients_count():
    """Функция для кеширования данных о количестве уникальных клиентов"""
    if settings.CACHE_ENABLED:
        key = 'unique_clients_count'
        clients_count = cache.get(key)
        if clients_count is None:
            clients_count = Client.objects.distinct().count()
            cache.set(key, clients_count)
    else:
        clients_count = Client.objects.distinct().count()
    return clients_count
