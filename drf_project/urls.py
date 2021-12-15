from django.contrib import admin
from django.urls import path, include
from drf_project.schema import urlpatterns as doc_urls


api_urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('blog/', include('blog.urls')),
    path('profile/', include('user_profile.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]

urlpatterns += doc_urls
