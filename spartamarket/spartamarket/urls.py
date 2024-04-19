from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from items import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='items/index/')),
    path('items/', include('items.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
