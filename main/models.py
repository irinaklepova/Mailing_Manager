from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Модель Клиент"""
    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=200, **NULLABLE, verbose_name='Отчество')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Контактный email')
    image = models.ImageField(**NULLABLE, verbose_name='Аватар')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """Модель Сообщение для рассылки"""
    title = models.CharField(max_length=250, verbose_name='Тема письма')
    text = models.TextField(**NULLABLE, verbose_name='Текст письма')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    """Модель Рассылка (настройки)"""
    DAILY = 'Ежедневно'
    WEEKLY = 'Еженедельно'
    MONTHLY = 'Ежемесячно'
    PERIODICITY_CHOICES = (
        (DAILY, 'Ежедневно'),
        (WEEKLY, 'Еженедельно'),
        (MONTHLY, 'Ежемесячно'),
    )

    CREATED = 'Создана'
    STARTED = 'Запущена'
    COMPLETED = 'Завершена'
    STATUS_CHOICES = (
        (COMPLETED, 'Завершена'),
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
    )

    start_time = models.DateTimeField(**NULLABLE, verbose_name='Дата и время начала рассылки')
    next_time = models.DateTimeField(**NULLABLE, verbose_name='Дата и время следующей рассылки')
    end_time = models.DateTimeField(**NULLABLE, verbose_name='Дата и время окончания рассылки')
    periodicity = models.CharField(max_length=50, default='once', choices=PERIODICITY_CHOICES,
                                   verbose_name='Периодичность')
    status = models.CharField(max_length=50, default=CREATED, choices=STATUS_CHOICES, verbose_name='Статус')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    letter = models.ForeignKey(Message, **NULLABLE, on_delete=models.SET_NULL, verbose_name='Письмо')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'time: {self.start_time}, periodicity: {self.periodicity}, status: {self.status}'

    class Meta:
        verbose_name = 'Настройка рассылки'
        verbose_name_plural = 'Настройки рассылки'

        permissions = [('set_inactive', 'Can block mailing')]


class Log(models.Model):
    """Модель Попытка"""
    SENT = 'Успешно'
    FAIL = 'Безуспешно'
    LOG_CHOICES = (
        (SENT, 'Успешно'),
        (FAIL, 'Безуспешно'),
    )

    last_attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Последняя отправка')
    attempt_status = models.CharField(max_length=15, choices=LOG_CHOICES, verbose_name='Статус попытки')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, **NULLABLE, verbose_name='Рассылка')

    def __str__(self):
        return f'{self.last_attempt_time} - {self.attempt_status}'

    class Meta:
        verbose_name = 'Попытка отправки'
        verbose_name_plural = 'Попытки отправки'
