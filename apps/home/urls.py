from rest_framework.routers import DefaultRouter
from apps.home.views import (
    SectionView, RulesView,
    PointView, ContactView,
)


router = DefaultRouter()
router.register('sections/', SectionView, basename='sections')
router.register('rules/', RulesView, basename='rules')
router.register('point/', PointView, basename='point')
router.register('contact/', ContactView, basename='contact')


urlpatterns = router.urls
