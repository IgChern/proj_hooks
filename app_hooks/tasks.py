from celery import shared_task
from .parsers import CallbackParser
from .storage import FileStorage


@shared_task
def process_jira_callback_task(data):
    parser = CallbackParser(data_storage=FileStorage())
    result = parser.parse_callback(data)
    return result
