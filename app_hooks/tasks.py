from celery import shared_task
from .models import Event
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_jira_callback_task(event_id):
    try:
        event = Event.objects.get(id=event_id)
        filters = event.filters.all()

        for filter_obj in filters:
            logger.info(
                f"Event: {event.name}, Filter: {filter_obj.name}")
    except Event.DoesNotExist:
        logger.error(f"Event ID {event_id} is not found")
    except Exception as e:
        logger.error(f"Error {event_id}: {e}")
