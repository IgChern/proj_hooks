from rest_framework.routers import DefaultRouter
from .views import FilterViewSet, EventViewSet

router = DefaultRouter()
router.register(r'filter', FilterViewSet, basename='filters')
router.register(r'event', EventViewSet, basename='events')

urlpatterns = router.urls
