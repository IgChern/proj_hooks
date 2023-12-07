from celery import shared_task
from .parsers import CallbackParser
from .storage import FileStorage
from .webhook import Service


@shared_task
def process_jira_callback_task(data):
    webhook_service = Service()
    result = webhook_service.process_jira_callback(data)
    return result
