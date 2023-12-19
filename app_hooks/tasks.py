from celery import shared_task
from .webhook import Service
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_jira_callback_task(data: dict) -> dict:
    """
    Process Jira callback task

    param data: The data (dictionary) received from Jira callback.
    return: A dictionary with the result, or None if an error.
    """
    try:
        webhook_service = Service()
        result = webhook_service.process_jira_callback(data)
        return result
    except Exception as e:
        logger.error(f"An error: {e}")
        return None
