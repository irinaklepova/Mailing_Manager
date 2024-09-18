import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from main.services import my_job

logger = logging.getLogger(__name__)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = 'Запускэ APScheduler'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(minute='*/1'),
            id='Запуск рассылки',
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлено задание 'Запуск рассылки'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week='mon', hour='00', minute='00'
            ),
            id='Удалить исполненные задачи',
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Добавлено еженедельное задание: 'Удалить исполненные задачи'."
        )

        try:
            logger.info('Запуск планировщика...')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info('Остановка планировщика...')
            scheduler.shutdown()
            logger.info('Планировщик успешно завершает работу!')