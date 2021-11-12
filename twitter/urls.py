from django.urls import path, include
from .views import *
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
status = router.register(r'status',
                        StatusDocumentView,
                        basename='statusdocument')

urlpatterns = [
    path('latest-status/', LatestStatus.as_view()),
    url(r'^', include(router.urls)),
]
