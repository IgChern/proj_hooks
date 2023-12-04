from rest_framework.routers import DefaultRouter
from .views import FilterViewSet, EventViewSet

router = DefaultRouter()
router.register('filter', FilterViewSet, basename='filters')
router.register('event', EventViewSet, basename='events')

urlpatterns = router.urls
