from abc import ABCMeta, abstractmethod

from ..models import Filter, EndpointInterface


class EndpointInterfaceABC(metaclass=ABCMeta):

    def __init__(self, data_filter: dict, jira_data: dict):
        self.data_filter: dict = data_filter
        self.jira_data: dict = jira_data
        self.endpoint = self.get_endpoint()
        self.process_middleware()

    def process_middleware(self):
        for middleware in self.endpoint.middlewares.all():
            self.jira_data[middleware.type] = middleware.process_middleware(
                self.jira_data)

    def get_endpoint(self):
        return EndpointInterface.objects.get(
            id=self.data_filter['endpoint_id'])

    @abstractmethod
    async def send_message(self, data_filter: Filter, jira_data: dict) -> bool:
        return False
