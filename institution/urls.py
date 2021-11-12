from django.urls import path, include
from .views import *
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
company = router.register(r'company',
                        CompanyDocumentView,
                        basename='companyDocument')

urlpatterns = [
    url(r'^', include(router.urls)),
]
