
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, re_path
from twitter import urls as search_index_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('twitter.urls')),
    re_path(r'^search/', include(search_index_urls)),
] 