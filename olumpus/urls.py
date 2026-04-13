from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from store import views   # IMPORT YOUR VIEWS

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('store.urls')),

    # Authentication (CUSTOM VIEWS)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
