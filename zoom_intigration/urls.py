from django.contrib import admin
from django.urls import path, include
from django.views.static import serve 
from zoom_intigration import settings
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('zoom_app.urls')),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    url(r'^zoom/(?P<path>.*)$', serve,{'document_root': settings.ZOOM_APP_TEMPLATE})
]
