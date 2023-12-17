from celery import shared_task
from .webhook import Service
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_jira_callback_task():
    try:
        webhook_service = Service()
        result = webhook_service.process_jira_callback()
        return result
    except Exception as e:
        logger.error(f"An error: {e}")
        return None
