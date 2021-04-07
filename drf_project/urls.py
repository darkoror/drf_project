from django.contrib import admin
from django.urls import path, include
from drf_project.yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('blog/', include('blog.urls')),
    path('profile/', include('user_profile.urls'))
]

urlpatterns += doc_urls
