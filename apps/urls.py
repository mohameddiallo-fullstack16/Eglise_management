from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from membres import views as membres_views  # ✅ importer la vue dashboard
from membres.views import dashboard_home
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='home'),   
    path('membres/', include('membres.urls')), 
    path('finance/', include('finance.urls')), 
    path('accounts/', include('accounts.urls')),
    path('dashboard/', dashboard_home, name='dashboard'),  
    path('events/', include('events.urls')),
    path('settings/', include('settings.urls')),
   

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
