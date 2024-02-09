from abc import ABCMeta, abstractmethod
from ..models import Filter, EndpointInterface


class EndpointInterfaceABC(metaclass=ABCMeta):

    def __init__(self, data_filter: dict, jira_data: dict):
        self.data_filter: dict = data_filter
        self.jira_data: dict = jira_data
        self.endpoint = self.get_endpoint()
        self.middleware = self.get_middleware(self.endpoint)

    def process_middleware(self):
        for middleware in self.endpoint.middleware.all():
            self.jira_data[middleware.type] = middleware.process_middleware(
                self.jira_data)

    def get_endpoint(self):
        return EndpointInterface.objects.get(
            id=self.data_filter['endpoint_id'])

    def get_middleware(self, endpoint):
        if endpoint.middleware.exists():
            self.process_middleware()

    @abstractmethod
    async def send_message(self, data_filter: Filter, jira_data: dict) -> bool:
        return False
