from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.site_header = "Панель управления ТСЖ"
admin.site.site_title = "ТСЖ Админ"
admin.site.index_title = "Добро пожаловать в админ-панель"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.pages.urls')),
    path('api/', include('api.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
