from abc import ABCMeta, abstractmethod

from ..models import Filter


class EndpointInterface(metaclass=ABCMeta):

    @abstractmethod
    async def send_message(self, data_filter: Filter, jira_data: dict) -> bool:
        return False
