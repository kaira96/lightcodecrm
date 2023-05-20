from django.contrib import admin
from django.conf.urls import handler404, handler500
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('srm/', include('srm.urls')),
    path('account/', include('account.urls')),
    path('classroom/', include('classroom.urls')),
    path('forum/', include('forum.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', include('landing.urls')),
    path('classroom/', include('classroom.urls')),
    path('forum/', include('forum.urls')),
)

handler404 = 'landing.views.error_404'
handler500 = 'landing.views.error_500'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
